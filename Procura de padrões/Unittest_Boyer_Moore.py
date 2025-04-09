import unittest
from BoyerMoore import BoyerMoore  # Certifique-se de que a classe BoyerMoore está no mesmo diretório ou no PYTHONPATH

class TesteBoyerMoore(unittest.TestCase):

    def test_uma_ocorrencia(self):
        bm = BoyerMoore("ACTG", "ACCA")
        resultado = bm.procurar_padrao("ATAGAACCAATG")
        self.assertEqual(resultado, [6])  # "ACCA" começa na posição 6

    def test_varias_ocorrencias(self):
        bm = BoyerMoore("ACTG", "ACCA")
        resultado = bm.procurar_padrao("ACCAACCAACCA")
        self.assertEqual(resultado, [0, 4, 8]) 

    def test_nenhuma_ocorrencia(self):
        bm = BoyerMoore("ACTG", "ACCA")
        resultado = bm.procurar_padrao("ATAGATGTGTAGTG")
        self.assertEqual(resultado, []) 
    def test_padrao_maior_que_texto(self):
        bm = BoyerMoore("ACTG", "ACCA")
        resultado = bm.procurar_padrao("AC")
        self.assertEqual(resultado, [])  # O padrão é maior que o texto

    def test_texto_vazio(self):
        bm = BoyerMoore("ACTG", "ACCA")
        resultado = bm.procurar_padrao("")
        self.assertEqual(resultado, [])  # Texto vazio não contém padrão

    def test_padrao_vazio(self):
        bm = BoyerMoore("ACTG", "")
        resultado = bm.procurar_padrao("ACCA")
        self.assertEqual(resultado, [])  # Padrão vazio retorna lista vazia

if __name__ == '__main__':
    unittest.main()

