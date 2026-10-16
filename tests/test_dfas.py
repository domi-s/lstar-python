import unittest

from lstar import lstar
from tests.cases.basic import cases
from tests.harness import check_examples, check_structure
from tests.oracles import equivalence_query


class DFATests(unittest.TestCase):
    def test_reference_dfas(self):
        for case in cases():
            with self.subTest(case=case.name):
                check_structure(self, case.dfa)
                check_examples(self, case, case.dfa.accepts)

    def test_learned_dfas(self):
        for case in cases():
            with self.subTest(case=case.name):
                learned = lstar(
                    alphabet=case.dfa.alphabet,
                    membership_query=case.dfa.accepts,
                    equivalence_query=lambda hypothesis: equivalence_query(
                        case.dfa, hypothesis
                    ),
                )
                check_structure(self, learned)
                check_examples(self, case, learned.accepts)
                self.assertIsNone(equivalence_query(case.dfa, learned))
                self.assertEqual(len(learned.states), case.minimal_states)
