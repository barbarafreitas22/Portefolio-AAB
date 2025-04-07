class TestFiniteAutomaton(unittest.TestCase):
    def setUp(self):
        """
        Set up a finite automaton for testing.
        """
        self.alphabet = "AC"
        self.pattern = "ACA"
        self.automaton = FiniteAutomaton(self.alphabet, self.pattern)

    def test_transition_table(self):
        """
        Test if the transition table is built correctly.
        """
        expected_transitions = {
            (0, 'A'): 1, (0, 'C'): 0,
            (1, 'A'): 1, (1, 'C'): 2,
            (2, 'A'): 3, (2, 'C'): 0,
            (3, 'A'): 1, (3, 'C'): 2
        }
        self.assertEqual(self.automaton.transition_table, expected_transitions)

    def test_overlap_function(self):
        """
        Test the _overlap function for various cases.
        """
        self.assertEqual(self.automaton._overlap("A"), 1)
        self.assertEqual(self.automaton._overlap("AC"), 2)
        self.assertEqual(self.automaton._overlap("ACA"), 3)
        self.assertEqual(self.automaton._overlap("C"), 0)
        self.assertEqual(self.automaton._overlap("G"), 0)

    def test_apply_sequence(self):
        """
        Test the application of the automaton to a sequence.
        """
        sequence = "CACAACAA"
        expected_states = [0, 0, 1, 2, 3, 1, 2, 3, 1]
        self.assertEqual(self.automaton.apply_sequence(sequence), expected_states)

    def test_find_pattern_occurrences(self):
        """
        Test finding pattern occurrences in a sequence.
        """
        sequence = "CACAACAA"
        expected_occurrences = [1, 4]
        self.assertEqual(self.automaton.find_pattern_occurrences(sequence), expected_occurrences)

    def test_no_occurrences(self):
        """
        Test when the pattern does not occur in the sequence.
        """
        sequence = "CCCCCCCC"
        self.assertEqual(self.automaton.find_pattern_occurrences(sequence), [])

    def test_empty_sequence(self):
        """
        Test with an empty sequence.
        """
        sequence = ""
        self.assertEqual(self.automaton.apply_sequence(sequence), [0])
        self.assertEqual(self.automaton.find_pattern_occurrences(sequence), [])

    def test_empty_pattern(self):
        """
        Test with an empty pattern.
        """
        automaton = FiniteAutomaton(self.alphabet, "")
        sequence = "CACAACAA"
        self.assertEqual(automaton.find_pattern_occurrences(sequence), list(range(len(sequence) + 1)))

    def test_non_alphabet_characters(self):
        """
        Test with characters outside the defined alphabet.
        """
        sequence = "CACAACAA123"
        expected_states = [0, 0, 1, 2, 3, 1, 2, 3, 1, 0, 0, 0]
        self.assertEqual(self.automaton.apply_sequence(sequence), expected_states)
        self.assertEqual(self.automaton.find_pattern_occurrences(sequence), [1, 4])

    def test_case_sensitivity(self):
        """
        Test case sensitivity of the automaton.
        """
        sequence = "cacaacaa"
        self.assertEqual(self.automaton.find_pattern_occurrences(sequence), [])


if __name__ == "__main__":
    unittest.main()
