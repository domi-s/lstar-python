# L* in Python

A small Python implementation of Angluin's L* algorithm for learning DFAs.

The learner discovers a DFA by asking whether individual words are accepted and submitting candidate machines for equivalence checking; these two queries are called `membership` and `equivalence` queries, respectively.

## Running the tests

```bash
git clone https://github.com/domi-s/lstar-python.git
cd lstar-python
python main.py
```

The normal suite checks 14 cases: parity, suffixes, substrings, forbidden
patterns, binary divisibility, combined counters, and unary inputs. It includes
a 1,000-state reference whose language needs only five states.

Each case runs its accepted/rejected examples against both the reference DFA
and its L* learned version. Tests also check transition structure, exact
equivalence, and the learned state count without depending on state numbering.
Learning runs inside tests, not during imports. No third-party packages are needed.

```bash
python -m unittest discover -s tests -v
python main.py --large
```

The opt-in large suite adds 1,001-state trailing-ones and 257-state length-counter
machines, plus a 10,002-state reference reducible to two states. All states in
these large references are reachable. The same example and learning checks run
for every large case; these runs can take longer.

### Adding tests

- `tests/cases/basic.py`: the original cases.
- `tests/cases/counting.py` and `patterns.py`: more language families.
- `tests/cases/large.py`: opt-in stress cases.
- `tests/harness.py`: a small `DFACase` record and shared assertions.
- `tests/test_dfas.py`: reference and learned DFA tests.
- `tests/oracles.py`: exact equivalence checking for known DFAs.
- `tests/test_oracles.py`: checks for the equivalence helper.

Add a `DFACase(name, dfa, accepted, rejected, minimal_states)` to a case list.
New case modules can be included in `DFATests.cases()`. Keep large cases in
the separate large suite so normal runs stay quick.

`check_examples(test, case, accepts)` takes any callable that maps a word to a
boolean. Future teacher experiments can reuse those examples in a separate
test module, with their own membership and counterexample-search functions.
LLM/Ollama integrations are not implemented. The exact DFA oracle requires
two known machines and cannot establish equivalence with an LLM.

## Usage

```python
from lstar import lstar

dfa = lstar(
    alphabet=("0", "1"),
    membership_query=membership_query,
    equivalence_query=equivalence_query,
)

print(dfa.accepts("101"))
```

You provide two functions:

```python
def membership_query(word):
    # Return True if the target accepts word; otherwise False.
    ...


def equivalence_query(hypothesis):
    # Return a word on which hypothesis and target disagree.
    # Return None if they are equivalent.
    ...
```

## How it works

Please read [my blog post](https://domis.at/blog/lstar) for a detailed explanation of the algorithm and its implementation.

## References

- Dana Angluin, [Learning Regular Sets from Queries and Counterexamples](https://people.eecs.berkeley.edu/~dawnsong/teaching/s10/papers/angluin87.pdf), 1987 — the original L* algorithm.
- James Worrell, [Exactly Learning Regular Languages Using Membership and Equivalence Queries](https://www.cs.ox.ac.uk/people/james.worrell/DFA-learning.pdf) — lecture notes explaining DFA learning, including a binary-search approach to processing counterexamples.
- Zhengxiang (Jack) Wang, [Lstar_Python](https://github.com/jaaack-wang/Lstar_Python/) — a readable Python implementation used as a reference. Its counterexample search uses bounded exhaustive testing; this implementation accepts a separate equivalence oracle.
