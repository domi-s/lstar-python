import unittest

from tests.cases import basic, patterns
from tests.oracles import equivalence_query
from utils.dfa import DFA


class EquivalenceTests(unittest.TestCase):
    def test_equivalent_machines_with_different_state_counts(self):
        expanded = basic.cases()[2].dfa
        compact = patterns.cases()[-1].dfa
        self.assertIsNone(equivalence_query(expanded, compact))

    def test_empty_counterexample(self):
        accept_all, reject_all = patterns.cases()[:2]
        self.assertEqual(equivalence_query(accept_all.dfa, reject_all.dfa), "")

    def test_shortest_counterexample(self):
        even_ones = basic.cases()[0].dfa
        accept_all = patterns.cases()[0].dfa
        self.assertEqual(equivalence_query(even_ones, accept_all), "1")

    def test_relabelled_states(self):
        reference = basic.cases()[0].dfa
        hypothesis = DFA(("0", "1"), {7, 9}, 7, {7}, {
            7: {"0": 7, "1": 9},
            9: {"0": 9, "1": 7},
        })
        self.assertIsNone(equivalence_query(reference, hypothesis))
