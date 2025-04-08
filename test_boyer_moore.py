import unittest

class TestBoyerMoore(unittest.TestCase):
    
    def test_single_match(self):
        bm = BoyerMoore("ACTG", "ACCA")
        result = bm.search_pattern("ATAGAACCAATG")
        self.assertEqual(result, [6]) 

    def test_multiple_matches(self):
        bm = BoyerMoore("ACTG", "ACCA")
        result = bm.search_pattern("ACCAACCAACCA")
        self.assertEqual(result, [0, 4, 8])  # Ocorrências em 0, 4 e 8

    def test_no_match(self):
        bm = BoyerMoore("ACTG", "ACCA")
        result = bm.search_pattern("ATAGATGTGTAGTG")
        self.assertEqual(result, [])  # Nenhuma ocorrência

    def test_pattern_longer_than_text(self):
        bm = BoyerMoore("ACTG", "ACCA")
        result = bm.search_pattern("AC")
        self.assertEqual(result, [])  # Padrão maior do que o texto

    def test_empty_text(self):
        bm = BoyerMoore("ACTG", "ACCA")
        result = bm.search_pattern("")
        self.assertEqual(result, [])  # Texto vazio

    def test_empty_pattern(self):
        bm = BoyerMoore("ACTG", "")
        result = bm.search_pattern("ACCA")
        self.assertEqual(result, [])  # Padrão vazio, nenhum resultado

if __name__ == '__main__':
    unittest.main()
