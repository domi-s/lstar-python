from collections.abc import Callable, Hashable
from typing import TYPE_CHECKING

if TYPE_CHECKING: # Avoiding circular import, there's probably a better way to do this
    from utils.dfa import DFA

Symbol = str
Alphabet = tuple[Symbol, ...]
Word = tuple[Symbol, ...]
State = Hashable

MembershipQuery = Callable[[Word], bool]
EquivalenceQuery = Callable[["DFA"], Word | None]

def str_to_word(s: str) -> Word:
    return tuple(s)
