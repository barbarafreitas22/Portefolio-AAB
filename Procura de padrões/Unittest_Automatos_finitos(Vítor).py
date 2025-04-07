
from Automatos_finitos import Automata, overlap
import unittest

class TestAutomata(unittest.TestCase):

    def setUp(self):
        self.alphabet = ['A', 'C', 'G', 'T']
        self.pattern = "ACGT"
        self.text = "GACGTACACGTACGT"
        self.automata = Automata(self.alphabet, self.pattern)

    def test_overlap_basic(self):
        self.assertEqual(overlap("A", "AC"), 1)
        self.assertEqual(overlap("CG", "CGT"), 2)
        self.assertEqual(overlap("ACGT", "ACGT"), 4)
        self.assertEqual(overlap("GTAC", "ACGT"), 2)
        self.assertEqual(overlap("TTTT", "ACGT"), 0)
        self.assertEqual(overlap("", "ACGT"), 0)
        self.assertEqual(overlap("ACGT", ""), 0)

    def test_transition_table_size(self):
        expected_size = (len(self.pattern) + 1) * len(self.alphabet)
        self.assertEqual(len(self.automata.transitionTable), expected_size)

    def test_transition_table_content(self):
        for q in range(len(self.pattern) + 1):
            for a in self.alphabet:
                self.assertIn((q, a), self.automata.transitionTable)

    def test_next_state_valid(self):
        current = 0
        symbol = 'A'
        next_state = self.automata.nextState(current, symbol)
        self.assertIsInstance(next_state, int)
        self.assertGreaterEqual(next_state, 0)
        self.assertLessEqual(next_state, len(self.pattern))

    def test_apply_sequence(self):
        seq = "ACGTAC"
        result = self.automata.applySeq(seq)
        self.assertEqual(len(result), len(seq) + 1)
        self.assertTrue(all(isinstance(q, int) for q in result))

    def test_pattern_occurrences(self):
        occurrences = self.automata.occurencesPattern(self.text)
        expected = [1, 7, 11] 
        self.assertEqual(occurrences, expected)

    def test_empty_pattern(self):
        a = Automata(self.alphabet, "")
        self.assertEqual(a.numstates, 1)
        self.assertTrue(all(v == 0 for v in a.transitionTable.values()))

    def test_empty_text_occurrence(self):
        result = self.automata.occurencesPattern("")
        self.assertEqual(result, [])

    def test_pattern_longer_than_text(self):
        short_text = "AC"
        result = self.automata.occurencesPattern(short_text)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()
