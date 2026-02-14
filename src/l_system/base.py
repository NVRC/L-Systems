"""Base classes to define an L-System.

A DOL-System is composed of:
    - alphabet (A): a set of symbols.
    - productions (P): a set of (predecessor (n) -> successor (w)) pairs. Where,
        - n is a character from the alphabet;
        - w is any string composed of the alphabet and/or turtle operation symbols.
    - axiom (L): Initial value of iter0. Must be a _predecessor_ in the set of productions.

Simple parameteric models:
    - Pseudo-random alphabet
    - Geometric
    - Cyclindrical (wrapped planar geometry)
    - Polygons
    - Timed DOL (tDOL) where each projection may related to a monotonic time.

See https://en.wikipedia.org/wiki/L-system#Generalized_Inference_Algorithms for generalized approaches.
"""

from abc import ABC, abstractmethod
from typing import Dict, Iterable

import tqdm


class Lsystem(ABC):
    """L-Systems need to inherit this ABC."""

    _state: str

    def __init__(self):
        self._state = self.axiom

    @property
    def state(self) -> str:
        """
        Returns:
            The current state of the L-System as a string.
        """
        return self._state

    @property
    def alphabet(self) -> str:
        """
        An L-system consists of an alphabet of symbols that can be used to make strings.

        Returns:
            The alphabet of the L-System, which are the keys of the `productions` (rules) dictionary.
        """

        return "".join(self.productions.keys())

    @property
    def constants(self) -> str:
        """
        Returns:
            The symbols of the L-System that are part of the alphabet but cannot be replaced by the production rules.
        """
        alphabet_set = set(self.alphabet)
        production_rules_set = set("".join(self.productions.values()))
        return "".join(production_rules_set.symmetric_difference(alphabet_set))

    @property
    def recursions(self) -> int:
        """How many times to recursively apply the productions rules."""
        return 1

    def apply(self, n: int | None = None, reset_state: bool = True) -> str:
        """
        Apply the production rules iteratively `n` times.

        Args:
            n: How many times to apply the `productions` (rules) on the L-System's state (string of symbols)?
                If set to `None` then the `productions` (rules) will be applied as many times as defined by the
                `recursions` property.
            reset_state: If set to `True` it will reset the state of the string of symbols to its `axiom` prior to
                applying any `productions` (rules).

        Returns:
            Returns the updated state of the string symbols after applying the `productions` (rules) `n` times on the
                string onf symbols.
        """
        n_recursions = self.recursions if n is None else n
        if reset_state:
            self.reset_state()

        for _ in tqdm.tqdm(range(n_recursions), desc="Applying the L-System production rules."):
            next_state = []
            for s in self._state:
                next_v = self.productions.get(s)
                next_state += next_v if next_v is not None else s
            self._state = "".join(next_state)
        return self._state

    def reset_state(self) -> None:
        """Resets the state of the L-System to it's `axiom`."""
        self._state = self.axiom

    def __len__(self) -> int:
        """Returns the length of the L-System's state (the length of the string of symbols)."""
        return len(self._state)

    def __repr__(self) -> str:
        return f"{self.name()}()"

    def __iter__(self) -> Iterable[str]:
        """Iterate over the L-System's state (symbols)."""
        yield from self._state

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    @property
    @abstractmethod
    def axiom(self) -> str:
        """
        Returns:
            The axiom is an initial state (string) of the L-System on which productions are applied iteratively.
        """

    @property
    @abstractmethod
    def productions(self) -> Dict[str, str]:
        """
        Productions (rules) that expand each symbol into some larger string of symbols.

        Returns:
            A dictionary of the production rules where keys are the symbols to be changed and their values are the
                values that will be replaced with.
        """
