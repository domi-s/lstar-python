from utils.dfa import DFA

from tests.harness import DFACase


def length_modulo(modulus):
    return DFA(
        ("0", "1"), set(range(modulus)), 0, {0},
        {i: {"0": (i + 1) % modulus, "1": (i + 1) % modulus}
         for i in range(modulus)},
    )


def trailing_ones(count):
    return DFA(
        ("0", "1"), set(range(count + 1)), 0, {count},
        {i: {"0": 0, "1": min(i + 1, count)}
         for i in range(count + 1)},
    )


def cases():
    alphabet = ("0", "1")
    return [
        DFACase(
            "length_multiple_of_17", length_modulo(17),
            ["", "0" * 17, "01" * 17],
            ["0", "1" * 16, "0" * 18],
            17,
        ),
        DFACase(
            "binary_divisible_by_7",
            DFA(alphabet, set(range(7)), 0, {0}, {
                i: {"0": (2 * i) % 7, "1": (2 * i + 1) % 7}
                for i in range(7)
            }),
            ["", "0", "000", "111", "1110", "10101"],
            ["1", "10", "110", "1000", "10100"],
            7,
        ),
        DFACase(
            "exactly_three_ones",
            DFA(alphabet, set(range(5)), 0, {3}, {
                i: {"0": i, "1": min(i + 1, 4)}
                for i in range(5)
            }),
            ["111", "10101", "011100"],
            ["", "11", "1111", "1010101"],
            5,
        ),
        DFACase(
            "even_zeros_and_ones_multiple_of_three",
            DFA(alphabet, set(range(6)), 0, {0}, {
                i: {"0": (1 - i // 3) * 3 + i % 3,
                    "1": (i // 3) * 3 + (i % 3 + 1) % 3}
                for i in range(6)
            }),
            ["", "00", "111", "00111", "01011"],
            ["0", "1", "01", "0011", "0111"],
            6,
        ),
        DFACase(
            "unary_length_multiple_of_11",
            DFA(("a",), set(range(11)), 0, {0}, {
                i: {"a": (i + 1) % 11} for i in range(11)
            }),
            ["", "a" * 11, "a" * 22],
            ["a", "a" * 10, "a" * 12],
            11,
        ),
    ]
