import unittest
from Gibbs_Sampling import *

class TestMotifSearch(unittest.TestCase):

    def test_score_identico(self):
        """Testa a função score para o caso com sequências idênticas"""
        sequencias = ["ACGT", "ACGT"]
        posicoes = [0, 0]
        L = 2
        score_esperado = 4
        self.assertEqual(score(posicoes, sequencias, L), score_esperado)

    def test_score_posicoes_diferentes(self):
        """Testa a função score com posições iniciais diferentes"""
        sequencias = ["ATCG", "AGCG"]
        posicoes = [0, 1]
        L = 3
        score_esperado = 3
        self.assertEqual(score(posicoes, sequencias, L), score_esperado)

    def test_calcula_probabilidade(self):
        """Testa a função calcula_probabilidade com um exemplo"""
        seq = "ACGT"
        L = 2
        pi = 0
        outros_motifs = ["AC", "AA"]
        score_esperado = 0.5 * (2/6)
        resultado = calcula_probabilidade(seq, L, pi, outros_motifs)
        self.assertAlmostEqual(resultado, score_esperado, places=5)

    def test_gibbs_sampling_output_valido(self):
        """Testa se o Gibbs Sampling retorna posições e score válidos"""
        random.seed(42)
        sequencias = ["ATGGTCGC", "TTGTCTGA", "CCGTAGTA"]
        L = 3
        posicoes, score_final = gibbs_sampling(sequencias, L, num_it=100)
        
        self.assertEqual(len(posicoes), len(sequencias))
        for pos, seq in zip(posicoes, sequencias):
            self.assertTrue(0 <= pos <= len(seq) - L)
        self.assertIsInstance(score_final, int)
    
    def test_sequencia_vazia(self):
      """Testa o comportamento com uma sequência vazia"""
      sequencias = ["ATGC", "", "TGCA"]
      L = 2
      with self.assertRaises(ValueError):
          gibbs_sampling(sequencias, L)

if __name__ == '__main__':
    unittest.main()
