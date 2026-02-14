import random
from typing import Dict, Iterable

from l_system.base import Lsystem
from l_system.rendering.turtle import OperatorSymbols, TurtleConfiguration


class PseudoRandomAlphabet(Lsystem):
    """Concrete DOL L-System from a pseudo-random axiom and set of projections
    based on an alphabet set. See more at https://gpfault.net/posts/generating-trees.txt.html.
    """

    def __init__(self, alphabet: Iterable[str]):
        # Select a random axiom from alphabet
        self._rand_axiom = random.choice(alphabet)

        # Derive a set of productions from the alphabet
        # First production must be the axiom
        alphabet_with_ops = alphabet + [e.value for e in OperatorSymbols]
        self._rand_productions = {self._rand_axiom: random.choice(alphabet_with_ops)}
        super().__init__()

    @property
    def axiom(self) -> str:
        return self._rand_axiom

    @property
    def productions(self) -> Dict[str, str]:
        return self._rand_productions


DEFAULT_TURTLE_CONFIG = TurtleConfiguration(angle=35)
