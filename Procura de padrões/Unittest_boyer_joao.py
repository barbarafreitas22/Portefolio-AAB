import unittest
class TestBoyerMoore(unittest.TestCase):
    def setUp(self):
        """
        Set up the Boyer-Moore algorithm for testing.
        """
        self.alphabet = "ACTG"
        self.pattern = "ACCA"
        self.bm = BoyerMoore(self.alphabet, self.pattern)

    def test_good_suffix_rule(self):
        """
        Test the good suffix rule preprocessing for a simple pattern.
        """
        self.assertEqual(len(self.bm.s), len(self.pattern) + 1)
        self.assertEqual(len(self.bm.f), len(self.pattern) + 1)

    def test_pattern_found(self):
        """
        Test when the pattern is found in the text.
        """
        text = "ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC"
        expected = [5, 13, 23, 37]
        self.assertEqual(self.bm.search(text), expected)

    def test_pattern_not_found(self):
        """
        Test when the pattern is not found in the text.
        """
        text = "ATAGATGATGATGATG"
        expected = []
        self.assertEqual(self.bm.search(text), expected)

    def test_empty_pattern(self):
        """
        Test when the pattern is empty.
        """
        bm = BoyerMoore(self.alphabet, "")
        text = "ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC"
        expected = []
        self.assertEqual(bm.search(text), expected)

    def test_empty_text(self):
        """
        Test when the text is empty.
        """
        text = ""
        expected = []
        self.assertEqual(self.bm.search(text), expected)

    def test_pattern_equals_text(self):
        """
        Test when the pattern is equal to the text.
        """
        text = "ACCA"
        expected = [0]
        self.assertEqual(self.bm.search(text), expected)

    def test_pattern_larger_than_text(self):
        """
        Test when the pattern is larger than the text.
        """
        text = "AC"
        expected = []
        self.assertEqual(self.bm.search(text), expected)

    def test_multiple_occurrences(self):
        """
        Test when the pattern occurs multiple times in the text.
        """
        text = "ACCAACACCAACCA"
        expected = [0, 6, 10]
        self.assertEqual(self.bm.search(text), expected)




if __name__ == "__main__":
    unittest.main()
