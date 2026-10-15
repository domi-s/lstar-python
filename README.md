# L* in Python

A small Python implementation of Angluin's L* algorithm for learning DFAs.

The learner discovers a DFA by asking whether individual words are accepted and submitting candidate machines for equivalence checking; these two queries are called `membership` and `equivalence` queries, respectively.

## Running the tests

```bash
git clone https://github.com/domi-s/lstar-python.git
cd lstar-python
python main.py
```

The tests include learning languages containing an even number of `1`s and ending in `01`.

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