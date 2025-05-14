import unittest
from Procura_Exaustiva import *

class TestMotifFinding(unittest.TestCase):

    def test_score_motif_identicas(self):
        """Testa o cálculo do score quando as sequências são idênticas"""
        sequencias = ["ACGT", "ACGT"]
        indices = [0, 0]
        L = 2
        self.assertEqual(score_motif(sequencias, indices, L), 4)

    def test_score_motif_variadas(self):
        """Testa o cálculo do score para sequências com motifs diferentes"""
        sequencias = ["ATCG", "AGCG"]
        indices = [0, 1]
        L = 3
        self.assertEqual(score_motif(sequencias, indices, L), 3)

    def test_prox_combinacao(self):
        """Testa a geração da próxima combinação de índices"""
        comprimentos = [8, 8]
        L = 3
        self.assertEqual(prox_combinacao([0, 0], comprimentos, L), [0, 1])
        self.assertEqual(prox_combinacao([0, 5], comprimentos, L), [1, 0])
        self.assertIsNone(prox_combinacao([5, 5], comprimentos, L))

    def test_procura_exaustiva(self):
        """Testa a procura exaustiva com sequências simples"""
        sequencias = ["ACGT", "ACGT"]
        L = 2
        melhores_indices, melhor_score = procura_exaustiva(sequencias, L)
        self.assertEqual(melhor_score, 4)
        for indice, seq in zip(melhores_indices, sequencias):
            self.assertTrue(0 <= indice <= len(seq) - L)


    def test_motif_tamanho_maximo(self):
        """Testa motifs com comprimento igual ao tamanho total da sequência"""
        sequencias = ["ACGT", "ACGT"]
        L = 4  
        indices_esperados = [0, 0]
        self.assertEqual(score_motif(sequencias, indices_esperados, L), 8)  
    
        melhores_indices, melhor_score = procura_exaustiva(sequencias, L)
        self.assertEqual(melhor_score, 8)
        self.assertEqual(melhores_indices, indices_esperados)

    def test_comprimentos_variaveis(self):
        """Testa combinações com sequências de comprimentos diferentes"""
        comprimentos = [5, 3]  
        L = 2
        casos = [([0,0], [0,1]), ([0,1], [1,0]), ([3,0], [3,1]), ([3,1], None)]
    
        for entrada, saida_esperada in casos:
            resultado = prox_combinacao(entrada.copy(), comprimentos, L)
            self.assertEqual(resultado, saida_esperada)

if __name__ == '__main__':
    unittest.main()
