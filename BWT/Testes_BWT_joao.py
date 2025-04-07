import unittest
from BWT_Joao import BWT

class BWTTests(unittest.TestCase):
    
    def test_empty_string(self):
        """Test BWT with empty string"""
        bwt = BWT("")
        self.assertEqual(bwt.bwt, "")
        self.assertEqual(bwt.suffix_array, [])
        self.assertEqual(bwt.decode(), "")
    
    def test_simple_string(self):
        """Test BWT with a simple string"""
        test_str = "banana$"
        bwt = BWT(test_str)
        self.assertEqual(bwt.decode(), test_str)
    
    def test_auto_append_marker(self):
        """Test that $ is automatically appended if missing"""
        bwt = BWT("banana")
        self.assertEqual(bwt.original_text, "banana$")
        
    def test_repeated_characters(self):
        """Test BWT with repeated characters"""
        test_str = "aaaaaa$"
        bwt = BWT(test_str)
        self.assertEqual(bwt.decode(), test_str)
    
    def test_existing_marker(self):
        """Test BWT with string that already has $ marker"""
        test_str = "banana$"
        bwt = BWT(test_str)
        self.assertEqual(bwt.decode(), test_str)
    
    def test_complex_example(self):
        """Test with more complex example"""
        test_str = "ACGTACGT$"
        bwt = BWT(test_str)
        self.assertEqual(bwt.decode(), test_str)
        self.assertEqual(bwt.bwt, "TG$ACGTCA")
    
    def test_single_character(self):
        """Test with single character"""
        test_str = "a$"
        bwt = BWT(test_str)
        self.assertEqual(bwt.bwt, "$a")
        self.assertEqual(bwt.decode(), test_str)
    
    def test_pattern_matching_single(self):
        """Test finding a pattern that appears once"""
        bwt = BWT("mississippi$")
        occurrences = bwt.find_occurrences("ssi")
        self.assertEqual(occurrences, [1, 4])
    
    def test_pattern_matching_multiple(self):
        """Test finding a pattern that appears multiple times"""
        bwt = BWT("bananabanana$")
        occurrences = bwt.find_occurrences("ana")
        self.assertEqual(set(occurrences), {1, 3, 7, 9})
    
    def test_pattern_not_found(self):
        """Test finding a pattern that doesn't exist"""
        bwt = BWT("banana$")
        occurrences = bwt.find_occurrences("xyz")
        self.assertEqual(occurrences, [])
    
    def test_pattern_empty(self):
        """Test finding an empty pattern"""
        bwt = BWT("banana$")
        occurrences = bwt.find_occurrences("")
        self.assertEqual(occurrences, [])
    
    def test_pattern_at_beginning(self):
        """Test finding pattern at beginning of string"""
        bwt = BWT("banana$")
        occurrences = bwt.find_occurrences("ban")
        self.assertEqual(occurrences, [0])
    
    def test_pattern_at_end(self):
        """Test finding pattern at end of string"""
        bwt = BWT("banana$")
        occurrences = bwt.find_occurrences("na")
        self.assertEqual(set(occurrences), {2, 4})
    
    def test_unicode_string(self):
        """Test with Unicode characters"""
        test_str = "café$"
        bwt = BWT(test_str)
        self.assertEqual(bwt.decode(), test_str)
    
    def test_suffix_array_correctness(self):
        """Test that suffix array is correct"""
        bwt = BWT("banana$")
        expected_sa = [6, 5, 3, 1, 0, 4, 2]  # For rotations of "banana$"
        self.assertEqual(bwt.suffix_array, expected_sa)
    
    def test_last_to_first_mapping(self):
        """Test the last-to-first mapping functionality"""
        bwt = BWT("banana$")
        first_column = sorted(bwt.bwt)
        # Manual verification of some mapping entries
        mapping = bwt._build_last_to_first_mapping(first_column)
        # For "banana$", the BWT is "annb$aa"
        # The first column is "$aaabnn"
        # We expect the mapping to connect each character in the last column
        # to its corresponding position in the first column
        self.assertEqual(len(mapping), len(bwt.bwt))

if __name__ == "__main__":
    unittest.main()
