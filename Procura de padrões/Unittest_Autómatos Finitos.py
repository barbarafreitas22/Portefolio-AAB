import unittest
from Autómatos Finitos import Automato_finito

class TestAutomatoFinito(unittest.TestCase):
    def setUp(self):
        """
        Configura um autómato finito para os testes.
        """
        self.alfabeto = "AC"  
        self.padrao = "ACA"  
        self.automato = Automato_finito(self.alfabeto, self.padrao)  

    def test_tabela_transicao(self):
        """
        Testa se a tabela de transições é construída corretamente.
        """
        transicoes_esperadas = {
            (0, 'A'): 1, (0, 'C'): 0,
            (1, 'A'): 1, (1, 'C'): 2,
            (2, 'A'): 3, (2, 'C'): 0,
            (3, 'A'): 1, (3, 'C'): 2
        }
        self.assertEqual(self.automato.tabela_transicao, transicoes_esperadas)

    def test_funcao_sobreposicao(self):
        """
        Testa a função _sobreposicao para vários casos.
        """
        self.assertEqual(self.automato._sobreposicao("A"), 1)
        self.assertEqual(self.automato._sobreposicao("AC"), 2)
        self.assertEqual(self.automato._sobreposicao("ACA"), 3)
        self.assertEqual(self.automato._sobreposicao("C"), 0)
        self.assertEqual(self.automato._sobreposicao("G"), 0)

    def test_aplicar_sequencia(self):
        """
        Testa a aplicação do autómato a uma sequência.
        """
        sequencia = "CACAACAA"
        estados_esperados = [0, 0, 1, 2, 3, 1, 2, 3, 1]
        self.assertEqual(self.automato.aplicar_sequencia(sequencia), estados_esperados)

    def test_encontrar_ocorrencias_padrao(self):
        """
        Testa a identificação de ocorrências do padrão numa sequência.
        """
        sequencia = "CACAACAA"
        ocorrencias_esperadas = [1, 4]
        self.assertEqual(self.automato.encontrar_ocorrencias_padrao(sequencia), ocorrencias_esperadas)

    def test_sem_ocorrencias(self):
        """
        Testa quando o padrão não ocorre na sequência.
        """
        sequencia = "CCCCCCCC"
        self.assertEqual(self.automato.encontrar_ocorrencias_padrao(sequencia), [])

    def test_sequencia_vazia(self):
        """
        Testa com uma sequência vazia.
        """
        sequencia = ""
        self.assertEqual(self.automato.aplicar_sequencia(sequencia), [0])
        self.assertEqual(self.automato.encontrar_ocorrencias_padrao(sequencia), [])

    def test_padrao_vazio(self):
        """
        Testa com um padrão vazio.
        """
        automato = Automato_finito(self.alfabeto, "")
        sequencia = "CACAACAA"
        self.assertEqual(automato.encontrar_ocorrencias_padrao(sequencia), list(range(len(sequencia) + 1)))

    def test_caracteres_fora_do_alfabeto(self):
        """
        Testa com caracteres fora do alfabeto definido.
        """
        sequencia = "CACAACAA123"
        estados_esperados = [0, 0, 1, 2, 3, 1, 2, 3, 1, 0, 0, 0]
        self.assertEqual(self.automato.aplicar_sequencia(sequencia), estados_esperados)
        self.assertEqual(self.automato.encontrar_ocorrencias_padrao(sequencia), [1, 4])

    def test_sensibilidade_a_maiusculas_minusculas(self):
        """
        Testa a sensibilidade a maiúsculas e minúsculas do autómato.
        """
        sequencia = "cacaacaa"
        self.assertEqual(self.automato.encontrar_ocorrencias_padrao(sequencia), [])


if __name__ == "__main__":
    unittest.main()
