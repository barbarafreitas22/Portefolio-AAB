
import unittest
from BWT import BWT

class TestBWT(unittest.TestCase):
    """
    Testes unitários para a classe BWT.

    Esta classe contém métodos de teste para validar as funções implementadas na classe BWT,
    tais como a construção da BWT, inversão da BWT, correspondência backward search e
    definição manual da BWT.
    """

    def setUp(self):
        """
        Configuração inicial para os testes.

        Define uma sequência de teste ("banana$") e cria uma instância da classe BWT com o array de sufixos.
        """
        self.texto = "banana$"
        self.instancia_bwt = BWT(self.texto, constroi_array_sufixos=True)

    def test_constroi_bwt(self):
        """
        Testa a construção da BWT.

        Verifica se a BWT construída para o texto "banana$" corresponde ao resultado esperado.
        """
        resultado_esperado = "annb$aa"  
        self.assertEqual(
            self.instancia_bwt.bwt,
            resultado_esperado,
            msg="A BWT calculada não corresponde ao esperado."
        )

    def test_inversa_bwt(self):
        """
        Testa a inversão da BWT.

        Verifica se a operação de inversão da BWT recupera corretamente o texto original.
        """
        texto_invertido = self.instancia_bwt.inversa_bwt()
        self.assertEqual(
            texto_invertido,
            self.texto,
            msg="A inversão da BWT não retornou o texto original."
        )

    def test_array_sufixos(self):
        """
        Testa a construção do array de sufixos.

        Compara o array de sufixos gerado com o array esperado para o texto "banana$".
        """
        sa_esperado = [6, 5, 3, 1, 0, 4, 2]
        self.assertEqual(
            self.instancia_bwt.sa,
            sa_esperado,
            msg="O array de sufixos calculado não está correto."
        )

    def test_correspondencia_bw(self):
        """
        Testa a função de correspondência backward search (correspondencia_bw).

        Verifica se os índices retornados para o padrão "ana" correspondem aos índices esperados.
        """
        indices_esperados = [2, 3]
        self.assertEqual(
            self.instancia_bwt.correspondencia_bw("ana"),
            indices_esperados,
            msg="correspondencia_bw não retornou os índices esperados para o padrão 'ana'."
        )

    def test_correspondencia_bw_prefixo(self):
        """
        Testa a função de correspondência backward search com conversão para posições originais.

        Verifica se os índices convertidos para as posições no texto original (através do array de sufixos)
        correspondem às posições esperadas para o padrão "ana".
        """
        posicoes_esperadas = [1, 3]
        self.assertEqual(
            self.instancia_bwt.correspondencia_bw_prefixo("ana"),
            posicoes_esperadas,
            msg="correspondencia_bw_prefixo não retornou as posições corretas no texto."
        )

    def test_correspondencia_bw_sem_correspondencia(self):
        """
        Testa a correspondência backward search para um padrão inexistente.

        Verifica se a função retorna uma lista vazia quando o padrão "xyz" não é encontrado.
        """
        self.assertEqual(
            self.instancia_bwt.correspondencia_bw("xyz"),
            [],
            msg="correspondencia_bw deveria retornar uma lista vazia para padrões não encontrados."
        )

    def test_define_bwt(self):
        """
        Testa o método define_bwt.

        Verifica se o método define_bwt atualiza corretamente o atributo BWT da instância.
        """
        novo_bwt = "test$bw"
        self.instancia_bwt.define_bwt(novo_bwt)
        self.assertEqual(
            self.instancia_bwt.bwt,
            novo_bwt,
            msg="O método define_bwt não atualizou a BWT corretamente."
        )

if __name__ == "__main__":
    unittest.main()
