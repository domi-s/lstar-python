from tests import test_dfas
from tests.cases import large


class LargeDFATests(test_dfas.DFATests):
    def cases(self):
        return large.cases()

    def test_all_reference_states_are_reachable(self):
        for case in self.cases():
            with self.subTest(case=case.name):
                reached = {case.dfa.initial_state}
                pending = [case.dfa.initial_state]

                while pending:
                    state = pending.pop()
                    for symbol in case.dfa.alphabet:
                        target = case.dfa.step(state, symbol)
                        if target not in reached:
                            reached.add(target)
                            pending.append(target)

                self.assertEqual(reached, case.dfa.states)
