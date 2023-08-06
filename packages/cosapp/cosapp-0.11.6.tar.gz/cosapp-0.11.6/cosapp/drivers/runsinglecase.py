import numpy
from typing import Any, Callable, Dict, Optional, Union

from cosapp.core.eval_str import AssignString
from cosapp.core.numerics.basics import MathematicalProblem
from cosapp.core.numerics.boundary import Boundary
from cosapp.drivers.iterativecase import IterativeCase
from cosapp.ports.enum import PortType
from cosapp.systems import System
from cosapp.utils.helpers import check_arg

import logging
logger = logging.getLogger(__name__)


class RunSingleCase(IterativeCase):
    """Set new boundary conditions and equations on the system.

    By default, it has a :py:class:`~cosapp.drivers.runonce.RunOnce` driver as child to run the system.

    Attributes
    ----------
    case_values : List[AssignString]
        List of requested variable assignments to set up the case
    initial_values : Dict[str, Tuple[Any, Optional[numpy.ndarray]]]
        List of variables to set with the values to set and associated indices selection

    Parameters
    ----------
    name : str
        Name of the driver
    owner : System, optional
        :py:class:`~cosapp.systems.system.System` to which this driver belong; default None
    **kwargs : Any
        Keyword arguments will be used to set driver options
    """

    __slots__ = ('__case_values', 'offdesign', 'problem')

    def __init__(self,
        name: str,
        owner: Optional[System] = None,
        **kwargs
        ) -> None:
        """Initialize a driver

        Parameters
        ----------
        name: str, optional
            Name of the `Module`
        owner : System, optional
            :py:class:`~cosapp.systems.system.System` to which this driver belong; default None
        **kwargs : Dict[str, Any]
            Optional keywords arguments
        """
        super().__init__(name, owner, **kwargs)
        self.__case_values = []  # type: List[AssignString]
            # desc="List of assignments 'lhs <- rhs' to perform in the present case.")
        self.owner = owner
        self.offdesign = MathematicalProblem(f"{self.name} - offdesign", self.owner)  # type: MathematicalProblem
            # desc="Additional mathematical problem to solve for on this case only.")
        self.problem = None  # type: Optional[MathematicalProblem]
            # desc='Full mathematical problem to be solved on this case.'

    def setup_run(self):
        """Method called once before starting any simulation."""
        super().setup_run()
        
        local_name = lambda name: f"{self.name}[{name}]"

        self.problem = problem = MathematicalProblem(self.name, self.owner)
        unknown_list = []

        def add_problem(other: MathematicalProblem, rename_unknowns=True, copy=False) -> None:
            nonlocal problem, unknown_list
            rename = local_name if rename_unknowns else lambda name: name

            # Add unknowns
            for name, unknown in other.unknowns.items():
                unknown = self.get_free_unknown(unknown, name)
                if unknown is None:
                    continue
                aliased = (unknown is not other.unknowns[name])
                uname = unknown.name if aliased else name
                if uname in unknown_list:
                    raise ValueError(
                        f"{name!r} is defined as design and offdesign unknown in driver {self.name!r}"
                    )
                name = rename(name)
                problem.unknowns[name] = unknown.copy() if copy else unknown
                unknown_list.append(rename(uname))
            
            # Add residues
            for name, residue in other.residues.items():
                fullname = local_name(name)
                if fullname in problem.residues:
                    raise ValueError(
                        f"{name!r} is defined as design and offdesign equation in driver {self.name!r}"
                    )
                problem.residues[fullname] = residue.copy() if copy else residue

            for name, residue in other.get_target_residues().items():
                problem.residues[local_name(name)] = residue.copy() if copy else residue

        # Add design unknowns & equations
        # Warning:
        #   Even if unknowns are modified, `unknowns` dict keys
        #   must be preserved for later comparison between
        #   self.problem and self.design; hence, no renaming.
        add_problem(self.design, rename_unknowns=False)

        # Add off-design unknowns & equations
        add_problem(self.offdesign)

        # Add owner system's off-design problem to be solved on each point
        # Unknowns & residues are duplicated to avoid side effects between points
        add_problem(self.owner.get_unsolved_problem(), copy=True)

    def _precompute(self) -> None:
        """Actions to carry out before the :py:meth:`~cosapp.drivers.runonce.RunOnce.compute` method call.

        It sets the boundary conditions and changes variable status.
        """
        super()._precompute()

        # Set the boundary conditions
        for assignment in self.case_values:
            value, changed = assignment.exec()
            if changed:
                self.owner.set_dirty(PortType.IN)

        # Set the offdesign variables
        for name, unknown in self.get_problem().unknowns.items():
            if name not in self.design.unknowns and not numpy.array_equal(unknown.value, unknown.default_value):
                unknown.set_to_default()

    def clean_run(self):
        """Method called once after any simulation."""
        self.problem = None

    @IterativeCase.owner.setter
    def owner(self, owner: Optional[System]) -> None:
        # Trick to call super setter (see: https://bugs.python.org/issue14965)
        if self.owner is not owner:
            if self.owner is not None:
                logger.warning(
                    f"System owner of Driver {self.name!r} has changed. Design and offdesign equations have been cleared."
                )
            self.offdesign = MathematicalProblem(self.offdesign.name, owner)
        cls = self.__class__
        super(cls, cls).owner.__set__(self, owner)

    def get_problem(self) -> MathematicalProblem:
        """Returns the full mathematical for the case.

        Returns
        -------
        MathematicalProblem
            The full mathematical problem to solve for the case
        """
        if self.problem is None:
            logger.warning("RunSingleCase.get_problem called with no prior call to RunSingleCase.setup_run.")
            return MathematicalProblem(self.name, self.owner)
        else:
            return self.problem

    def set_values(self, modifications: Dict[str, Any]) -> None:
        """Enter the set of variables defining the case, from a dictionary of the kind {'variable1': value1, ...}
        Note: will erase all previously defined values. Use 'add_values' to append new case values.

        The variable can be contextual `child1.port2.var`. The only rule is that it should belong to
        the owner `System` of this driver or any of its descendants.

        Parameters
        ----------
        modifications : Dict[str, Any]
            Dictionary of (variable name, value)

        Examples
        --------
        >>> driver.set_values({'myvar': 42, 'port.dummy': 'banana'})
        """
        self.clear_values()
        self.add_values(modifications)

    def add_values(self, modifications: Dict[str, Any]) -> None:
        """Add a set of variables to the list of case values, from a dictionary of the kind {'variable1': value1, ...}

        The variable can be contextual `child1.port2.var`. The only rule is that it should belong to
        the owner `System` of this driver or any of its descendants.

        Parameters
        ----------
        modifications : Dict[str, Any]
            Dictionary of (variable name, value)

        Examples
        --------
        >>> driver.add_values({'myvar': 42, 'port.dummy': 'banana'})
        """
        check_arg(modifications, 'modifications', dict)

        for variable, value in modifications.items():
            self.add_value(variable, value)

    def add_value(self, variable: str, value: Any) -> None:
        """Add a single variable to list of case values.

        The variable can be contextual `child1.port2.var`. The only rule is that it should belong to
        the owner `System` of this driver or any of its descendants.

        Parameters
        ----------
        variable : str
            Name of the variable
        value : Any
            Value to be used.

        Examples
        --------
        >>> driver.add_value('myvar', 42)
        """
        if self.owner is None:
            raise AttributeError(
                f"Driver {self.name!r} must be attached to a System to set case values."
            )
        else:
            Boundary.parse(self.owner, variable)  # checks that variable is valid
            self.__case_values.append(AssignString(variable, value, self.owner))

    def clear_values(self):
        self.__case_values.clear()

    @property
    def case_values(self):
        return self.__case_values
