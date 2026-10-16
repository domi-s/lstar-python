from utils.dfa import DFA

from tests.cases.counting import length_modulo, trailing_ones
from tests.harness import DFACase


def cases():
    return [
        DFACase(
            "trailing_1000_ones", trailing_ones(1000),
            ["1" * 1000, "1" * 1001, "0" + "1" * 1000],
            ["", "1" * 999, "1" * 1000 + "0",
             "1" * 500 + "0" + "1" * 500],
            1001,
        ),
        DFACase(
            "length_multiple_of_257", length_modulo(257),
            ["", "0" * 257, "01" * 257],
            ["0", "1" * 256, "0" * 258],
            257,
        ),
        DFACase(
            "even_trailing_ones_expanded",
            DFA(("0", "1"), set(range(10002)), 0,
                set(range(0, 10002, 2)), {
                    i: {"0": 0, "1": (i + 1) % 10002}
                    for i in range(10002)
                }),
            ["", "0", "11", "1011", "1" * 10002],
            ["1", "111", "1101", "1" * 10001],
            2,
        ),
    ]
