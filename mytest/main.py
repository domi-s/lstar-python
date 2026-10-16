"""
Unit tests.
"""

from collections import deque

from mytest.framework import *

from utils.definitions import Alphabet, str_to_word
from utils.constants import EPSILON
from utils.dfa import DFA

from lstar import lstar

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

dfa_ends_with_0101 = DFA(
    alphabet=alphabet_0_1,
    states=set(range(1000)),
    initial_state=0,
    accepting_states={i for i in range(1000) if i % 5 == 4},
    transitions={
        i: {
            "0": 5 * ((i * 3 + 7) % 200) + (3 if (i % 5) in (2, 4) else 1),
            "1": 5 * ((i * 5 + 11) % 200) + (2 if (i % 5) == 1 else (4 if (i % 5) == 3 else 0)),
        }
        for i in range(1000)
    },
)
"""DFA that accepts words that end with 0101."""

dfa_ends_with_500_ones = DFA(
    alphabet=alphabet_0_1,
    states=set(range(501)),
    initial_state=0,
    accepting_states={500},
    transitions={
        i: {
            "0": 0,
            "1": min(i + 1, 500),
        }
        for i in range(501)
    },
)
"""DFA that accepts words that end with exactly 500 1s."""

def equivalence_query(reference, hypothesis):
    """Return a distinguishing word, or None if two DFAs are equivalent.
    
    Works by BFS on the product of the two DFAs, looking for a state where one is accepting and the other is not.
    """
    pending = deque([(reference.initial_state, hypothesis.initial_state, "")])
    visited = set()

    while pending:
        reference_state, hypothesis_state, word = pending.popleft()
        state_pair = (reference_state, hypothesis_state)

        if state_pair in visited:
            continue
        visited.add(state_pair)

        if (reference_state in reference.accepting_states) != (hypothesis_state in hypothesis.accepting_states):
            return word

        for symbol in reference.alphabet:
            pending.append((
                reference.step(reference_state, symbol),
                hypothesis.step(hypothesis_state, symbol),
                word + symbol,
            ))

    return None

dfa_lstar_even_ones = lstar(
    alphabet=alphabet_0_1,
    membership_query=lambda word: word.count("1") % 2 == 0,
    equivalence_query=lambda hypothesis: equivalence_query(dfa_even_ones, hypothesis),
)
"""DFA learned by L* algorithm for words with an even number of 1s."""

dfa_lstar_ends_with_01 = lstar(
    alphabet=alphabet_0_1,
    membership_query=lambda word: word.endswith("01"),
    equivalence_query=lambda hypothesis: equivalence_query(dfa_ends_with_01, hypothesis),
)
"""DFA learned by L* algorithm for words that end with 01."""

dfa_lstar_ends_with_0101 = lstar(
    alphabet=alphabet_0_1,
    membership_query=lambda word: word.endswith("0101"),
    equivalence_query=lambda hypothesis: equivalence_query(dfa_ends_with_0101, hypothesis),
)
"""DFA learned by L* algorithm for words that end with 0101."""

dfa_lstar_ends_with_500_ones = lstar(
    alphabet=alphabet_0_1,
    membership_query=lambda word: word.count("1") == 500,
    equivalence_query=lambda hypothesis: equivalence_query(dfa_ends_with_500_ones, hypothesis),
)
"""DFA learned by L* algorithm for words that end with exactly 500 1s."""

def test_dfa_even_ones():
    print_test_group_subheader("dfa_even_ones")

    print_test_result("dfa_even_ones accepts empty string", dfa_even_ones.accepts(str_to_word("")))
    print_test_result("dfa_even_ones accepts 000", dfa_even_ones.accepts(str_to_word("000")))
    print_test_result("dfa_even_ones does not accept 01", not dfa_even_ones.accepts(str_to_word("01")))
    print_test_result("dfa_even_ones does not accept 1", not dfa_even_ones.accepts(str_to_word("1")))
    print_test_result("dfa_even_ones does not accept 10", not dfa_even_ones.accepts(str_to_word("10")))
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

def test_dfa_ends_with_0101():
    print_test_group_subheader("dfa_ends_with_0101")

    print_test_result("dfa_ends_with_0101 does not accept empty string", not dfa_ends_with_0101.accepts(str_to_word("")))
    print_test_result("dfa_ends_with_0101 does not accept 0", not dfa_ends_with_0101.accepts(str_to_word("0")))
    print_test_result("dfa_ends_with_0101 does not accept 1", not dfa_ends_with_0101.accepts(str_to_word("1")))
    print_test_result("dfa_ends_with_0101 does not accept 01", not dfa_ends_with_0101.accepts(str_to_word("01")))
    print_test_result("dfa_ends_with_0101 does not accept 10", not dfa_ends_with_0101.accepts(str_to_word("10")))
    print_test_result("dfa_ends_with_0101 does not accept 101", not dfa_ends_with_0101.accepts(str_to_word("101")))
    print_test_result("dfa_ends_with_0101 accepts 0101", dfa_ends_with_0101.accepts(str_to_word("0101")))
    print_test_result("dfa_ends_with_0101 accepts 110101", dfa_ends_with_0101.accepts(str_to_word("110101")))
    print_test_result("dfa_ends_with_0101 does not accept 110100", not dfa_ends_with_0101.accepts(str_to_word("110100")))

def test_dfa_ends_with_500_ones():
    print_test_group_subheader("dfa_ends_with_500_ones")

    print_test_result("dfa_ends_with_500_ones does not accept empty string", not dfa_ends_with_500_ones.accepts(str_to_word("")))
    print_test_result("dfa_ends_with_500_ones does not accept 0", not dfa_ends_with_500_ones.accepts(str_to_word("0")))
    print_test_result("dfa_ends_with_500_ones does not accept 1", not dfa_ends_with_500_ones.accepts(str_to_word("1")))
    print_test_result("dfa_ends_with_500_ones does not accept 111", not dfa_ends_with_500_ones.accepts(str_to_word("111")))
    print_test_result("dfa_ends_with_500_ones accepts 111...1 (500 times)", dfa_ends_with_500_ones.accepts(str_to_word("1" * 500)))
    print_test_result("dfa_ends_with_500_ones does not accept 111...1 (499 times)", not dfa_ends_with_500_ones.accepts(str_to_word("1" * 499)))
    print_test_result("dfa_ends_with_500_ones accepts 111...1 (501 times)", dfa_ends_with_500_ones.accepts(str_to_word("1" * 501)))

def test_dfa_lstar_even_ones():
    print_test_group_subheader("dfa_lstar_even_ones")

    print_test_result("dfa_lstar_even_ones.states == {0, 1}", dfa_lstar_even_ones.states == {0, 1})
    print_test_result("dfa_lstar_even_ones.transitions == {0: {'0': 0, '1': 1}, 1: {'0': 1, '1': 0}}", dfa_lstar_even_ones.transitions == {0: {"0": 0, "1": 1}, 1: {"0": 1, "1": 0}})
    print_test_result("dfa_lstar_even_ones accepts empty string", dfa_lstar_even_ones.accepts(str_to_word("")))
    print_test_result("dfa_lstar_even_ones accepts 000", dfa_lstar_even_ones.accepts(str_to_word("000")))
    print_test_result("dfa_lstar_even_ones does not accept 1", not dfa_lstar_even_ones.accepts(str_to_word("1")))
    print_test_result("dfa_lstar_even_ones accepts 11", dfa_lstar_even_ones.accepts(str_to_word("11")))
    print_test_result("dfa_lstar_even_ones accepts 101", dfa_lstar_even_ones.accepts(str_to_word("101")))
    print_test_result("dfa_lstar_even_ones accepts 0101", dfa_lstar_even_ones.accepts(str_to_word("0101")))

def test_dfa_lstar_ends_with_01():
    print_test_group_subheader("dfa_lstar_ends_with_01")

    print_test_result("dfa_lstar_ends_with_01.states == {0, 1, 2}", dfa_lstar_ends_with_01.states == {0, 1, 2})
    print_test_result("dfa_lstar_ends_with_01.transitions == {0: {'0': 1, '1': 0}, 1: {'0': 1, '1': 2}, 2: {'0': 1, '1': 0}}", dfa_lstar_ends_with_01.transitions == {0: {"0": 1, "1": 0}, 1: {"0": 1, "1": 2}, 2: {"0": 1, "1": 0}})
    print_test_result("dfa_lstar_ends_with_01 does not accept empty string", not dfa_lstar_ends_with_01.accepts(str_to_word("")))
    print_test_result("dfa_lstar_ends_with_01 does not accept 0", not dfa_lstar_ends_with_01.accepts(str_to_word("0")))
    print_test_result("dfa_lstar_ends_with_01 does not accept 1", not dfa_lstar_ends_with_01.accepts(str_to_word("1")))
    print_test_result("dfa_lstar_ends_with_01 accepts 01", dfa_lstar_ends_with_01.accepts(str_to_word("01")))
    print_test_result("dfa_lstar_ends_with_01 does not accept 10", not dfa_lstar_ends_with_01.accepts(str_to_word("10")))
    print_test_result("dfa_lstar_ends_with_01 accepts 101", dfa_lstar_ends_with_01.accepts(str_to_word("101")))

def test_dfa_lstar_ends_with_0101():
    print_test_group_subheader("dfa_lstar_ends_with_0101")

    print_test_result("dfa_lstar_ends_with_0101.states == {0, 1, 2, 3, 4}", dfa_lstar_ends_with_0101.states == {0, 1, 2, 3, 4})
    print_test_result("dfa_lstar_ends_with_0101.transitions == {0: {'0': 1, '1': 0}, 1: {'0': 1, '1': 2}, 2: {'0': 3, '1': 0}, 3: {'0': 1, '1': 4}, 4: {'0': 3, '1': 0}}", dfa_lstar_ends_with_0101.transitions == {0: {"0": 1, "1": 0}, 1: {"0": 1, "1": 2}, 2: {"0": 3, "1": 0}, 3: {"0": 1, "1": 4}, 4: {"0": 3, "1": 0}})
    print_test_result("dfa_lstar_ends_with_0101 does not accept empty string", not dfa_lstar_ends_with_0101.accepts(str_to_word("")))
    print_test_result("dfa_lstar_ends_with_0101 does not accept 0", not dfa_lstar_ends_with_0101.accepts(str_to_word("0")))
    print_test_result("dfa_lstar_ends_with_0101 does not accept 1", not dfa_lstar_ends_with_0101.accepts(str_to_word("1")))
    print_test_result("dfa_lstar_ends_with_0101 does not accept 01", not dfa_lstar_ends_with_0101.accepts(str_to_word("01")))
    print_test_result("dfa_lstar_ends_with_0101 does not accept 10", not dfa_lstar_ends_with_0101.accepts(str_to_word("10")))
    print_test_result("dfa_lstar_ends_with_0101 does not accept 101", not dfa_lstar_ends_with_0101.accepts(str_to_word("101")))
    print_test_result("dfa_lstar_ends_with_0101 accepts 0101", dfa_lstar_ends_with_0101.accepts(str_to_word("0101")))
    print_test_result("dfa_lstar_ends_with_0101 accepts 110101", dfa_lstar_ends_with_0101.accepts(str_to_word("110101")))
    print_test_result("dfa_lstar_ends_with_0101 does not accept 110100", not dfa_lstar_ends_with_0101.accepts(str_to_word("110100")))

def test_dfa_lstar_ends_with_500_ones():
    print_test_group_subheader("dfa_lstar_ends_with_500_ones")

    print_test_result("dfa_lstar_ends_with_500_ones.states == {0, 1, 2, ..., 500}", dfa_lstar_ends_with_500_ones.states == set(range(501)))
    print_test_result("dfa_lstar_ends_with_500_ones.transitions == {i: {'0': 0, '1': min(i + 1, 500)} for i in range(501)}", dfa_lstar_ends_with_500_ones.transitions == {i: {"0": 0, "1": min(i + 1, 500)} for i in range(501)})
    print_test_result("dfa_lstar_ends_with_500_ones does not accept empty string", not dfa_lstar_ends_with_500_ones.accepts(str_to_word("")))
    print_test_result("dfa_lstar_ends_with_500_ones does not accept 0", not dfa_lstar_ends_with_500_ones.accepts(str_to_word("0")))
    print_test_result("dfa_lstar_ends_with_500_ones does not accept 1", not dfa_lstar_ends_with_500_ones.accepts(str_to_word("1")))
    print_test_result("dfa_lstar_ends_with_500_ones does not accept 111", not dfa_lstar_ends_with_500_ones.accepts(str_to_word("111")))
    print_test_result("dfa_lstar_ends_with_500_ones accepts 111...1 (500 times)", dfa_lstar_ends_with_500_ones.accepts(str_to_word("1" * 500)))
    print_test_result("dfa_lstar_ends_with_500_ones does not accept 111...1 (499 times)", not dfa_lstar_ends_with_500_ones.accepts(str_to_word("1" * 499)))
    print_test_result("dfa_lstar_ends_with_500_ones accepts 111...1 (501 times)", dfa_lstar_ends_with_500_ones.accepts(str_to_word("1" * 501)))

def main():
    print_header()

    print_test_group_header("DFA Tests")

    test_dfa_even_ones()
    test_dfa_ends_with_01()
    test_dfa_ends_with_0101()
    test_dfa_ends_with_500_ones()

    print_test_group_header("L* Algorithm Tests")

    test_dfa_lstar_even_ones()
    test_dfa_lstar_ends_with_01()
    test_dfa_lstar_ends_with_0101()
    test_dfa_lstar_ends_with_500_ones()

    print_footer()

if __name__ == "__main__":
    main()
