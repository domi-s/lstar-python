from collections.abc import Callable, Hashable
from typing import TYPE_CHECKING

if TYPE_CHECKING: # Avoiding circular import, there's probably a better way to do this
    from utils.dfa import DFA

Symbol = str # Assume symbols are single-character strings
Alphabet = tuple[Symbol, ...]
Word = str
State = int

MembershipQuery = Callable[[Word], bool]
EquivalenceQuery = Callable[["DFA"], Word | None]

def str_to_word(s: str) -> Word:
    return tuple(s)
