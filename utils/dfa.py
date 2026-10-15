from utils.definitions import Symbol, Alphabet, State

class DFA:
    alphabet: Alphabet
    states: set[State]
    initial_state: State
    accepting_states: set[State]
    transitions: dict[State, dict[Symbol, State]]

    def __init__(self, alphabet, states, initial_state,
                 accepting_states, transitions):
        self.alphabet = alphabet
        self.states = states
        self.initial_state = initial_state
        self.accepting_states = accepting_states
        self.transitions = transitions

    def step(self, state, symbol):
        """Return the next state after reading one symbol."""
        return self.transitions[state][symbol]

    def run(self, word):
        """Read the word and return the state we finish in."""
        state = self.initial_state

        for symbol in word:
            state = self.step(state, symbol)

        return state

    def accepts(self, word):
        """Return True if the word is accepted."""
        return self.run(word) in self.accepting_states
