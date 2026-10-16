from dataclasses import dataclass

from utils.dfa import DFA


@dataclass
class DFACase:
    name: str
    dfa: DFA
    accepted: list[str]
    rejected: list[str]
    minimal_states: int


def check_examples(test, case, accepts):
    for expected, words in ((True, case.accepted), (False, case.rejected)):
        for word in words:
            with test.subTest(word=word):
                test.assertEqual(accepts(word), expected)


def check_structure(test, dfa):
    test.assertIn(dfa.initial_state, dfa.states)
    test.assertLessEqual(dfa.accepting_states, dfa.states)
    test.assertEqual(set(dfa.transitions), dfa.states)
    for state in dfa.states:
        test.assertEqual(set(dfa.transitions[state]), set(dfa.alphabet))
        test.assertLessEqual(set(dfa.transitions[state].values()), dfa.states)
