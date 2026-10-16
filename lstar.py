import time

from utils.definitions import Word, Alphabet, MembershipQuery, EquivalenceQuery
from utils.constants import EPSILON
from utils.dfa import DFA

class LStarTelemetry:
    """Telemetry for the L* algorithm."""

    membership_queries: int
    equivalence_queries: int

    start_time: float
    end_time: float
    last_notified_time: float

    def __init__(self):
        self.membership_queries = 0
        self.equivalence_queries = 0
        self.start_time = 0.0
        self.end_time = 0.0
        self.last_notified_time = 0.0

    def record_membership_query(self):
        self.membership_queries += 1

    def record_equivalence_query(self):
        self.equivalence_queries += 1

    def start_timer(self):
        self.start_time = time.time()
        self.last_notified_time = self.start_time

    def stop_timer(self):
        self.end_time = time.time()

    def elapsed_time(self):
        if self.end_time == 0.0:
            return time.time() - self.start_time
        
        return self.end_time - self.start_time

    def should_notify(self, interval: float = 15.0):
        """Check if enough time has passed since the last notification."""
        current_time = time.time()
        if current_time - self.last_notified_time >= interval:
            self.last_notified_time = current_time
            return True
        return False

    def __str__(self):
        return f"Membership queries: {self.membership_queries}, Equivalence queries: {self.equivalence_queries}, Elapsed time: {self.elapsed_time():.4f} seconds"

class ObservationTable:
    alphabet: Alphabet
    membership_query: MembershipQuery

    S: list[Word]
    """The set of prefixes that represent the states of the hypothesis DFA. Each prefix is a word over the alphabet."""

    E: list[Word]
    """The set of suffixes that distinguish the states of the hypothesis DFA. Each suffix is a word over the alphabet."""

    cache: dict[Word, bool]
    """The cache of previously asked membership queries. Keys are words, values are True/False."""

    def __init__(self, alphabet, membership_query):
        self.alphabet = alphabet
        self.membership_query = membership_query

        self.S = [""]
        self.E = [""]

        self.cache = {}
        self.row_cache = {}

    def query(self, word):
        """Ask the membership oracle, reusing previously recorded answers."""
        if word not in self.cache:
            self.cache[word] = self.membership_query(word)

        return self.cache[word]

    def row(self, prefix):
        """Answers obtained by appending every suffix in E."""
        row = self.row_cache.get(prefix, ())

        if len(row) < len(self.E):
            row += tuple(
                self.query(prefix + suffix)
                for suffix in self.E[len(row):]
            )
            self.row_cache[prefix] = row

        return row

    def resolve_closed(self):
        """Add a prefix if its row represents a new state."""
        known_rows = {self.row(prefix) for prefix in self.S}

        for prefix in self.S:
            for symbol in self.alphabet:
                extension = prefix + symbol

                if self.row(extension) not in known_rows:
                    self.S.append(extension)
                    return True

        return False

    def resolve_consistent(self):
        """Distinguish equal rows whose next steps differ."""
        prefixes_by_row = {}
        for prefix in self.S:
            prefixes_by_row.setdefault(self.row(prefix), []).append(prefix)

        for prefixes in prefixes_by_row.values():
            for i, first in enumerate(prefixes):
                for second in prefixes[i + 1:]:

                    for symbol in self.alphabet:
                        for suffix in self.E:
                            experiment = symbol + suffix

                            first_answer = self.query(first + experiment)
                            second_answer = self.query(second + experiment)

                            if first_answer != second_answer:
                                self.E.append(experiment)
                                return True

        return False

    def to_dfa(self):
        """Build a DFA once the table is closed and consistent."""
        row_to_state = {}
        representatives = {}

        # Give each distinct row a state number.
        for prefix in self.S:
            answers = self.row(prefix)

            if answers not in row_to_state:
                state = len(row_to_state)
                row_to_state[answers] = state
                representatives[state] = prefix

        transitions = {}
        accepting_states = set()

        for state, prefix in representatives.items():
            transitions[state] = {}

            if self.query(prefix):
                accepting_states.add(state)

            for symbol in self.alphabet:
                next_row = self.row(prefix + symbol)
                transitions[state][symbol] = row_to_state[next_row]

        return DFA(
            alphabet=self.alphabet,
            states=set(representatives),
            initial_state=row_to_state[self.row("")],
            accepting_states=accepting_states,
            transitions=transitions,
        )

    def resolve_counterexample(self, word, hypothesis):
        """Add a distinguishing prefix and suffix found by binary search."""
        representatives = {}
        for prefix in self.S:
            representatives.setdefault(hypothesis.run(prefix), prefix)

        target_answer = self.query(word)
        low = 0
        high = len(word)

        while high - low > 1:
            midpoint = (low + high) // 2
            state = hypothesis.run(word[:midpoint])
            representative = representatives[state]
            suffix = word[midpoint:]

            if self.query(representative + suffix) == target_answer:
                low = midpoint
            else:
                high = midpoint

        prefix = word[:high]
        suffix = word[high:]

        if prefix not in self.S:
            self.S.append(prefix)
        if suffix not in self.E:
            self.E.append(suffix)

def lstar(alphabet: Alphabet, membership_query: MembershipQuery, equivalence_query: EquivalenceQuery) -> DFA:
    """Learn a DFA using membership and equivalence queries.

    The membership query receives a word and returns True or False.
    The equivalence query receives the current hypothesis DFA and returns
    a counterexample word, or None when the hypothesis is correct.
    """

    telemetry = LStarTelemetry()

    membership_query_with_telemetry = lambda word: (telemetry.record_membership_query(), membership_query(word))[1]
    equivalence_query_with_telemetry = lambda dfa: (telemetry.record_equivalence_query(), equivalence_query(dfa))[1]

    print(f"Starting L* algorithm...")

    telemetry.start_timer()

    table = ObservationTable(alphabet, membership_query_with_telemetry)

    while True:
        while True:
            if telemetry.should_notify():
                print(f"Still learning... {telemetry}")

            if table.resolve_closed():
                continue

            if table.resolve_consistent():
                continue

            break

        dfa = table.to_dfa()
        counterexample = equivalence_query_with_telemetry(dfa)

        if counterexample is None:
            telemetry.stop_timer()
            print(f"Learning complete. {telemetry}")
            return dfa

        table.resolve_counterexample(counterexample, dfa)
