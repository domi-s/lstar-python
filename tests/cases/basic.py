from utils.dfa import DFA

from tests.harness import DFACase


def cases():
    alphabet = ("0", "1")
    return [
        DFACase(
            "even_ones",
            DFA(alphabet, {0, 1}, 0, {0}, {
                0: {"0": 0, "1": 1},
                1: {"0": 1, "1": 0},
            }),
            ["", "000", "11", "101", "0101"],
            ["1", "01", "10"],
            2,
        ),
        DFACase(
            "ends_with_01",
            DFA(alphabet, {0, 1, 2}, 0, {2}, {
                0: {"0": 1, "1": 0},
                1: {"0": 1, "1": 2},
                2: {"0": 1, "1": 0},
            }),
            ["01", "101", "0001"],
            ["", "0", "1", "10", "010"],
            3,
        ),
        DFACase(
            "ends_with_0101_expanded",
            DFA(alphabet, set(range(1000)), 0,
                {i for i in range(1000) if i % 5 == 4}, {
                    i: {
                        "0": 5 * ((i * 3 + 7) % 200)
                        + (3 if i % 5 in (2, 4) else 1),
                        "1": 5 * ((i * 5 + 11) % 200)
                        + (2 if i % 5 == 1 else (4 if i % 5 == 3 else 0)),
                    }
                    for i in range(1000)
                }),
            ["0101", "110101", "010101"],
            ["", "0", "1", "01", "10", "101", "110100"],
            5,
        ),
        DFACase(
            "trailing_100_ones",
            DFA(alphabet, set(range(101)), 0, {100}, {
                i: {"0": 0, "1": min(i + 1, 100)}
                for i in range(101)
            }),
            ["1" * 100, "1" * 101, "01" + "1" * 100],
            ["", "0", "1", "111", "1" * 99, "1" * 100 + "0",
             "1" * 50 + "0" + "1" * 50],
            101,
        ),
    ]
