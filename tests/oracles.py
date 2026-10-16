from collections import deque


def equivalence_query(reference, hypothesis):
    pending = deque([(reference.initial_state, hypothesis.initial_state, "")])
    visited = set()

    while pending:
        reference_state, hypothesis_state, word = pending.popleft()
        pair = (reference_state, hypothesis_state)

        if pair in visited:
            continue
        visited.add(pair)

        if ((reference_state in reference.accepting_states)
                != (hypothesis_state in hypothesis.accepting_states)):
            return word

        for symbol in reference.alphabet:
            pending.append((
                reference.step(reference_state, symbol),
                hypothesis.step(hypothesis_state, symbol),
                word + symbol,
            ))

    return None
