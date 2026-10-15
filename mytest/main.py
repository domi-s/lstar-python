"""
Unit tests.
"""

from mytest.framework import *

from utils.definitions import Alphabet, str_to_word
from utils.constants import EPSILON
from utils.dfa import DFA


alphabet_0_1 = Alphabet(("0", "1"))
"""Alphabet of 0s and 1s."""

dfa_even_ones = DFA(
    alphabet=alphabet_0_1,
    states={0, 1},
    initial_state=0,
    accepting_states={0},
    transitions={ 0: {"0": 0, "1": 1}, 1: {"0": 1, "1": 0}, },
)
"""DFA that accepts words with an even number of 1s."""

dfa_ends_with_01 = DFA(
    alphabet=alphabet_0_1,
    states={0, 1, 2},
    initial_state=0,
    accepting_states={2},
    transitions={ 0: {"0": 1, "1": 0}, 1: {"0": 1, "1": 2}, 2: {"0": 1, "1": 0}, },
)
"""DFA that accepts words that end with 01."""

def test_dfa_even_ones():
    print_test_group_subheader("dfa_even_ones")

    print_test_result("dfa_even_ones accepts empty string", dfa_even_ones.accepts(str_to_word("")))
    print_test_result("dfa_even_ones accepts 000", dfa_even_ones.accepts(str_to_word("000")))
    print_test_result("dfa_even_ones does not accept 1", not dfa_even_ones.accepts(str_to_word("1")))
    print_test_result("dfa_even_ones accepts 11", dfa_even_ones.accepts(str_to_word("11")))
    print_test_result("dfa_even_ones accepts 101", dfa_even_ones.accepts(str_to_word("101")))
    print_test_result("dfa_even_ones accepts 0101", dfa_even_ones.accepts(str_to_word("0101")))

def test_dfa_ends_with_01():
    print_test_group_subheader("dfa_ends_with_01")

    print_test_result("dfa_ends_with_01 does not accept empty string", not dfa_ends_with_01.accepts(str_to_word("")))
    print_test_result("dfa_ends_with_01 does not accept 0", not dfa_ends_with_01.accepts(str_to_word("0")))
    print_test_result("dfa_ends_with_01 does not accept 1", not dfa_ends_with_01.accepts(str_to_word("1")))
    print_test_result("dfa_ends_with_01 accepts 01", dfa_ends_with_01.accepts(str_to_word("01")))
    print_test_result("dfa_ends_with_01 does not accept 10", not dfa_ends_with_01.accepts(str_to_word("10")))
    print_test_result("dfa_ends_with_01 accepts 101", dfa_ends_with_01.accepts(str_to_word("101")))

def main():
    print_header()

    print_test_group_header("DFA Tests")

    test_dfa_even_ones()
    test_dfa_ends_with_01()

    print_footer()

if __name__ == "__main__":
    main()
