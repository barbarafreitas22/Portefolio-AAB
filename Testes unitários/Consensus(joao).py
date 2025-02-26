import unittest

class TestMotifFinding(unittest.TestCase):
    
    def test_score_motifs_identical(self):
        """Testa score_motifs com sequências idênticas e posições 0."""
        seqs = ["ACGT", "ACGT"]
        positions = [0, 0]
        motif_length = 2
        # Motivos: "AC" e "AC" → colunas: ('A','A') e ('C','C') → score = 2 + 2 = 4
        expected_score = 4
        self.assertEqual(score_motifs(seqs, positions, motif_length), expected_score)
    
    def test_score_motifs_different(self):
        """Testa score_motifs com sequências diferentes."""
        seqs = ["ATCG", "AGCG"]
        positions = [0, 1]
        motif_length = 3
        # Motivos: "ATC" e "GCG"
        # Coluna 1: ('A','G') → max = 1; Coluna 2: ('T','C') → max = 1; Coluna 3: ('C','G') → max = 1
        # Score total = 3
        expected_score = 3
        self.assertEqual(score_motifs(seqs, positions, motif_length), expected_score)
    
    def test_heuristic_consensus_valid(self):
        """Testa se heuristic_consensus retorna posições válidas e o score correspondente."""
        seqs = ["ATGGTCGC", "TTGTCTGA", "CCGTAGTA"]
        motif_length = 3
        positions, final_score = heuristic_consensus(seqs, motif_length)
        # Verifica se cada posição está dentro do intervalo válido para a respectiva sequência
        for pos, seq in zip(positions, seqs):
            self.assertGreaterEqual(pos, 0)
            self.assertLessEqual(pos, len(seq) - motif_length)
        # Verifica se o score final bate com o score calculado a partir das posições retornadas
        self.assertEqual(final_score, score_motifs(seqs, positions, motif_length))
    
    def test_heuristic_consensus_error(self):
        """Testa se heuristic_consensus lança erro quando há menos de duas sequências."""
        seqs = ["ATGGTCGC"]
        motif_length = 3
        with self.assertRaises(ValueError):
            heuristic_consensus(seqs, motif_length)

if __name__ == '__main__':
    unittest.main()
