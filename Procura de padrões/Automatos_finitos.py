class FiniteAutomaton:
    """
    A finite automaton implementation for pattern matching.
    """

    def __init__(self, alphabet, pattern):
        """
        Initialize the automaton with the given alphabet and pattern.

        Parameters
        ----------
        alphabet : str
            The alphabet used in the pattern and sequences.
        pattern : str
            The pattern to search for in sequences.
        """
        self.alphabet = alphabet
        self.pattern = pattern
        self.num_states = len(pattern) + 1
        self.transition_table = {}
        self._build_transition_table()

    def _build_transition_table(self):
        """
        Build the transition table for the automaton based on the pattern.
        """
        for state in range(self.num_states):
            for char in self.alphabet:
                prefix = self.pattern[:state] + char
                self.transition_table[(state, char)] = self._overlap(prefix)

    def _overlap(self, s):
        """
        Calculate the overlap between the end of string `s` and the pattern.

        Parameters
        ----------
        s : str
            The string to calculate overlap for.

        Returns
        -------
        int
            The length of the overlap.
        """
        max_overlap = min(len(s), len(self.pattern))
        for i in range(max_overlap, 0, -1):
            if s[-i:] == self.pattern[:i]:
                return i
        return 0

    def apply_sequence(self, sequence):
        """
        Apply the automaton to a sequence and return the states visited.

        Parameters
        ----------
        sequence : str
            The sequence to process.

        Returns
        -------
        list[int]
            A list of states visited during the processing of the sequence.
        """
        state = 0
        states = [state]
        for char in sequence:
            state = self.transition_table.get((state, char), 0)
            states.append(state)
        return states

    def find_pattern_occurrences(self, sequence):
        """
        Find all occurrences of the pattern in the sequence.

        Parameters
        ----------
        sequence : str
            The sequence to search for the pattern.

        Returns
        -------
        list[int]
            A list of starting positions where the pattern occurs in the sequence.
        """
        state = 0
        occurrences = []
        for i, char in enumerate(sequence):
            state = self.transition_table.get((state, char), 0)
            if state == self.num_states - 1:
                occurrences.append(i - len(self.pattern) + 1)
        return occurrences


# Example Usage
if __name__ == "__main__":
    # Define the alphabet and pattern
    alphabet = "AC"
    pattern = "ACA"

    # Create the automaton
    automaton = FiniteAutomaton(alphabet, pattern)

    # Print the transition table
    print("Transition Table:")
    for key, value in automaton.transition_table.items():
        print(f"State {key[0]}, Character '{key[1]}' -> State {value}")

    # Apply the automaton to a sequence
    sequence = "CACAACAA"
    states = automaton.apply_sequence(sequence)
    print("\nStates visited:", states)

    # Find pattern occurrences
    occurrences = automaton.find_pattern_occurrences(sequence)
    print("\nPattern occurrences:", occurrences)
