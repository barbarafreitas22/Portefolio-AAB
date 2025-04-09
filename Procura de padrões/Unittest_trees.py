import unittest

class TestTrie(unittest.TestCase):
    """
    Testes unitários para a estrutura Trie.

    Estes testes verificam a correcta adição de palavras, a pesquisa de palavras completas,
    a pesquisa por prefixos e o comportamento da Trie em casos de adições duplicadas ou Trie vazia.
    """

    def setUp(self):
        """
        Configura o ambiente de testes ao iniciar uma Trie
        e insere uma lista de palavras para os testes.
        """
        self.trie = Trie()
        self.words = ["apple", "app", "banana", "band", "bandana"]
        for word in self.words:
            self.trie.insert(word)

    def test_insert_and_search(self):
        """
        Testa a inserção e pesquisa de palavras na Trie.

        Verifica se palavras inseridas podem ser corretamente encontradas
        e se palavras não inseridas não são encontradas.
        """
        self.assertTrue(self.trie.search("apple"))
        self.assertTrue(self.trie.search("app"))
        self.assertTrue(self.trie.search("band"))
        self.assertFalse(self.trie.search("apples"))
        self.assertFalse(self.trie.search("bandanas"))

    def test_starts_with(self):
        """
        Testa a pesquisa de palavras com um dado prefixo.

        Verifica se a Trie retorna corretamente todas as palavras
        que começam por um prefixo específico.
        """
        self.assertEqual(sorted(self.trie.starts_with("ban")), ["banana", "band", "bandana"])
        self.assertEqual(sorted(self.trie.starts_with("app")), ["app", "apple"])
        self.assertEqual(self.trie.starts_with("xyz"), [])

    def test_empty_trie(self):
        """
        Testa o comportamento da Trie vazia.

        Verifica se a pesquisa numa Trie vazia retorna resultados apropriados.
        """
        empty_trie = Trie()
        self.assertFalse(empty_trie.search("anything"))
        self.assertEqual(empty_trie.starts_with("any"), [])

    def test_insert_duplicate(self):
        """
        Testa a inserção de palavras duplicadas na Trie.

        Verifica se a inserção repetida de uma palavra não causa erros
        e se a pesquisa continua a funcionar corretamente.
        """
        self.trie.insert("apple")
        self.assertTrue(self.trie.search("apple"))
        self.assertEqual(sorted(self.trie.starts_with("app")), ["app", "apple"])


class TestSuffixTree(unittest.TestCase):
    """
    Testes unitários para a estrutura Árvore de Sufixos (Suffix Tree).

    Estes testes verificam a correcta adição dos sufixos de uma string,
    a pesquisa de substrings, e o comportamento em casos especiais como
    strings vazias ou caracteres especiais.
    """

    def setUp(self):
        """
        Configura o ambiente de testes ao iniciar uma Árvore de Sufixos
        com o texto "banana" para utilização nos testes.
        """
        self.suffix_tree = SuffixTree()
        self.text = "banana"
        self.suffix_tree.insert(self.text)

    def test_insert_and_search(self):
        """
        Testa a adição e pesquisa de substrings na Árvore de Sufixos.

        Verifica se substrings corretas são encontradas nas posições apropriadas.
        """
        self.assertEqual(sorted(self.suffix_tree.search("ana")), [1, 3])
        self.assertEqual(self.suffix_tree.search("ban"), [0])
        self.assertEqual(self.suffix_tree.search("xyz"), [])

    def test_search_full_string(self):
        """
        Testa a pesquisa da string completa na Árvore de Sufixos.

        Verifica se a string original é encontrada na posição zero.
        """
        self.assertEqual(self.suffix_tree.search("banana"), [0])

    def test_search_empty_string(self):
        """
        Testa a pesquisa de uma string vazia.

        Garante que a pesquisa de uma string vazia retorna uma lista vazia.
        """
        self.assertEqual(self.suffix_tree.search(""), [])

    def test_insert_empty_string(self):
        """
        Testa a inserção de uma string vazia.

        Garante que a adição de uma string vazia é tratada corretamente
        e não gera erro na pesquisa.
        """
        empty_suffix_tree = SuffixTree()
        empty_suffix_tree.insert("")
        self.assertEqual(empty_suffix_tree.search(""), [])

    def test_insert_and_search_single_character(self):
        """
        Testa a adição e pesquisa de uma única letra.

        Verifica se uma letra inserida isoladamente pode ser corretamente encontrada.
        """
        single_char_tree = SuffixTree()
        single_char_tree.insert("a")
        self.assertEqual(single_char_tree.search("a"), [0])
        self.assertEqual(single_char_tree.search("b"), [])

    def test_collect_positions(self):
        """
        Testa a função auxiliar _collect_positions.

        Verifica se os índices recolhidos a partir de um nó específico
        correspondem às posições esperadas da substring "ana" no texto "banana".
        """
        node = self.suffix_tree.tree
        for char in "ana":
            node = node[char]
        positions = self.suffix_tree._collect_positions(node)
        self.assertEqual(sorted(positions), [1, 3])

    def test_insert_and_search_with_special_characters(self):
        """
        Testa a inserção e pesquisa de strings com caracteres especiais.

        Verifica se a Árvore de Sufixos lida corretamente com símbolos como '!', '@' e '#'.
        """
        special_tree = SuffixTree()
        special_tree.insert("a!b@c#")
        self.assertEqual(special_tree.search("!b"), [1])
        self.assertEqual(special_tree.search("xyz"), [])

    def test_insert_and_search_unicode(self):
        """
        Testa a inserção e pesquisa de caracteres Unicode.

        Verifica se palavras que contêm caracteres acentuados são corretamente armazenadas e pesquisadas.
        """
        unicode_tree = SuffixTree()
        unicode_tree.insert("café")
        self.assertEqual(unicode_tree.search("afé"), [1])
        self.assertEqual(unicode_tree.search("é"), [3])
        self.assertEqual(unicode_tree.search("xyz"), [])


if __name__ == "__main__":
    unittest.main()
