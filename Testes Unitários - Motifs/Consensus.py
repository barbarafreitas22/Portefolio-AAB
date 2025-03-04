import unittest
import random

class TestMotifFinding(unittest.TestCase):
    
    def test_score_motifs_identico(self):
        """Testa score_motifs com sequências idênticas e posições 0"""
        seqs = ["ACGT", "ACGT"]
        posicoes = [0, 0]
        L = 2
        score_esperado = 4
        self.assertEqual(score_motifs(seqs, posicoes, L), score_esperado)
    
    def test_score_motifs_diferente(self):
        """Testa score_motifs com sequências diferentes"""
        seqs = ["ATCG", "AGCG"]
        posicoes = [0, 1]
        L = 3
        score_esperado = 3
        self.assertEqual(score_motifs(seqs, posicoes, L), score_esperado)
    
    def test_consensus_heu_valido(self):
        """Testa se consensus_heu retorna posições válidas e o score correspondente"""
        seqs = ["ATGGTCGC", "TTGTCTGA", "CCGTAGTA"]
        L = 3
        posicoes, score_f = consensus_heu(seqs, L)
        
        for pos, seq in zip(posicoes, seqs):
            self.assertGreaterEqual(pos, 0)
            self.assertLessEqual(pos, len(seq) - L)
    
        self.assertEqual(score_f, score_motifs(seqs, posicoes, L))
    
    def test_consensus_heu_erro(self):
        """Testa se consensus_heu dá erro quando há menos de duas sequências"""
        seqs = ["ATGGTCGC"]
        L = 3
        with self.assertRaises(ValueError):
            consensus_heu(seqs, L)
    
    def test_nao_primeira_posicao(self):
        """Testa se seleciona posições não ótimas iniciais quando há empate no score"""
        seqs = ["AAAAA", "AAAAA", "AAACAAAA"]
        L = 3
        posicoes, score = consensus_heu(seqs, L)
        self.assertEqual(posicoes[2], 0)
        self.assertEqual(score, 9)

    def test_dif_comp_seq(self):
        """Testa sequências com comprimentos diferentes"""
        seqs = ["AAAA", "TTTTTT", "CCCC"]
        L = 2
        posicoes, score = consensus_heu(seqs, L)
        self.assertTrue(0 <= posicoes[0] <= 2)
        self.assertTrue(0 <= posicoes[1] <= 4)
        self.assertTrue(0 <= posicoes[2] <= 2)

    def test_maximo_motif(self):
        """Testa motifs com tamanho igual ao máximo possível"""
        seqs = ["ABCDE", "FGHIJ"]  
        L = 5
        posicoes, score = consensus_heu(seqs, L)
        self.assertEqual(posicoes, [0, 0])
        self.assertEqual(score, 5)

if __name__ == '__main__':
    unittest.main()
