
import unittest
from BWT import BWT

class TestBWT(unittest.TestCase):
    def setUp(self):
        self.texto = "banana$"
        self.bwt_instance = BWT(self.texto, buildsufarray=True)

    def test_build_bwt(self):
        resultado_esperado = "annb$aa"  
        self.assertEqual(self.bwt_instance.bwt, resultado_esperado, msg="A BWT calculada não corresponde ao esperado.")

    def test_inverse_bwt(self):
        texto_invertido = self.bwt_instance.inverse_bwt()
        self.assertEqual(texto_invertido, self.texto, msg="A inversão da BWT não retornou o texto original.")

    def test_suffix_array(self):
        sa_esperado = [6, 5, 3, 1, 0, 4, 2]
        self.assertEqual(self.bwt_instance.sa, sa_esperado, msg="O suffix array calculado não está correto.")

    def test_bw_matching(self):
        indices_esperados = [2, 3]
        self.assertEqual(self.bwt_instance.bw_matching("ana"), indices_esperados, msg="bw_matching não retornou os índices esperados para o padrão 'ana'.")

    def test_bw_matching_prefix(self):
        posicoes_esperadas = [1, 3]
        self.assertEqual(self.bwt_instance.bw_matching_prefix("ana"), posicoes_esperadas, msg="bw_matching_prefix não retornou as posições corretas no texto.")

    def test_bw_matching_no_match(self):
        self.assertEqual(self.bwt_instance.bw_matching("xyz"), [], msg="bw_matching deveria retornar uma lista vazia para padrões não encontrados.")

    def test_set_bwt(self):
        novo_bwt = "test$bw"
        self.bwt_instance.set_bwt(novo_bwt)
        self.assertEqual(self.bwt_instance.bwt, novo_bwt, msg="O método set_bwt não atualizou a BWT corretamente.")

if __name__ == "__main__":
    unittest.main()
