
import unittest
import random
from Branch_and_Bound import *

class TestProcuraExaustivaMotifs(unittest.TestCase):
    def test_exemplo_basico(self):
        """Testa o exemplo fornecido"""
        seqs = "ATGGTCGC TTGTCTGA CCGTAGTA".split()
        L = 3
        melhor_p, melhor_score = procura_exaustiva_motifs(seqs, L)
        self.assertEqual(melhor_score, 8)
        self.assertEqual(motif_score(seqs, melhor_p, L), 8)

    def test_sequencia_unica(self):
        """Testa o caso com uma única sequência."""
        seqs = ["ATGGTCGC"]
        L = 3
        melhor_p, melhor_score = procura_exaustiva_motifs(seqs, L)
        self.assertEqual(melhor_p, [0])
        self.assertEqual(melhor_score, L)

    def test_motif_tamanho_total(self):
        """Testa o caso em que o comprimento da sequência é igual ao comprimento do motif."""
        seqs = ["ATG", "ATG", "ATG"]
        L = 3
        melhor_p, melhor_score = procura_exaustiva_motifs(seqs, L)
        self.assertEqual(melhor_p, [0, 0, 0])
        self.assertEqual(melhor_score, 9)

    def test_random_sequences(self):
        """Testa com sequências geradas aleatoriamente."""
        t = 5
        n = 10
        L = 3
        random.seed(42)
        seqs = [random_dna_seq(n) for _ in range(t)]
        melhor_p, melhor_score = procura_exaustiva_motifs(seqs, L)
        self.assertEqual(melhor_score, motif_score(seqs, melhor_p, L))
        self.assertTrue(L <= melhor_score <= L * t)

if __name__ == '__main__':
    unittest.main()
