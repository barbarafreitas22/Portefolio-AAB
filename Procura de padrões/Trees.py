class Trie:
    """
    Implementação de uma Trie para armazenamento e pesquisa de palavras.

    A estrutura Trie permite inserir palavras e realizar pesquisas de forma eficiente, 
    tanto para verificar a existência completa de palavras como para encontrar todas as palavras que partilham um prefixo comum.
    """

    def __init__(self):
        """
        Inicializa a Trie como um dicionário vazio, onde cada chave representa um caractere e cada valor representa a continuação da palavra.
        """
        self.trie = {}

    def insert(self, word):
        """
        Insere uma palavra na Trie, adicionando um marcador especial ('$') no final para indicar o término da palavra.

        Parâmetros:
            word (str): A palavra a ser inserida na Trie.
        """
        current = self.trie
        for char in word + "$":  # Percorre cada caractere da palavra acrescido do marcador de fim.
            if char not in current:
                current[char] = {}  # Cria um novo ramo na Trie caso o caractere ainda não exista.
            current = current[char]

    def search(self, word):
        """
        Verifica se uma palavra completa está armazenada na Trie.

        A pesquisa percorre a estrutura da Trie caractere a caractere e verifica no final se existe o marcador especial de fim ('$').

        Parâmetros:
            word (str): A palavra a procurar na Trie.

        Retorna:
            bool: True se a palavra existir na Trie, False caso contrário.
        """
        current = self.trie
        for char in word:
            if char not in current:
                return False  # Se um dos caracteres não existir, a palavra não está presente.
            current = current[char]
        return "$" in current  # Verifica se a palavra termina corretamente com o marcador.

    def starts_with(self, prefix):
        """
        Encontra todas as palavras na Trie que começam com o prefixo fornecido.

        Após localizar o prefixo na Trie, percorre recursivamente todos os caminhos possíveis para recolher as palavras completas.

        Parâmetros:
            prefix (str): Prefixo a procurar na Trie.

        Retorna:
            list: Lista de palavras que começam com o prefixo fornecido.
        """
        current = self.trie
        for char in prefix:
            if char not in current:
                return []  # Prefixo não encontrado na Trie.
            current = current[char]
        return self._collect_words(prefix, current)

    def _collect_words(self, prefix, node):
        """
        Função auxiliar que recolhe todas as palavras completas a partir de um determinado nó da Trie.

        Esta função é chamada recursivamente até encontrar todos os caminhos terminados com o marcador especial de fim ('$').

        Parâmetros:
            prefix (str): Prefixo acumulado até ao nó atual.
            node (dict): Subárvore da Trie correspondente ao prefixo.

        Retorna:
            list: Lista de palavras completas derivadas do prefixo fornecido.
        """
        words = []
        for char, child in node.items():
            if char == "$":
                words.append(prefix)  # Palavra completa encontrada.
            else:
                words.extend(self._collect_words(prefix + char, child))  # Continua a explorar os ramos.
        return words


class SuffixTree:
    """
    Implementação de uma Árvore de Sufixos para armazenamento e pesquisa de substrings.

    Esta estrutura permite inserir todos os sufixos de uma string para facilitar a pesquisa eficiente de substrings, 
    devolvendo as posições onde essas substrings ocorrem no texto original.
    """

    def __init__(self):
        """
        Inicializa a Árvore de Sufixos como um dicionário vazio, onde cada caminho representa um sufixo do texto.
        """
        self.tree = {}

    def insert(self, text):
        """
        Insere todos os sufixos da string fornecida na Árvore de Sufixos.

        Para cada sufixo, cria-se um caminho separado na árvore, marcando o fim com o símbolo especial ('$') e registando a posição inicial do sufixo.

        Parâmetros:
            text (str): Texto base de onde serão gerados e inseridos os sufixos.
        """
        if text == "":
            current = self.tree
            if "$" not in current:
                current["$"] = {}
            if "index" not in current["$"]:
                current["$"]["index"] = []
            current["$"]["index"].append(0)
            return

        for i in range(len(text)):
            self._insert_suffix(text[i:], i)

    def _insert_suffix(self, suffix, index):
        """
        Função auxiliar que insere um sufixo específico na Árvore de Sufixos.

        Cada caractere do sufixo é adicionado sequencialmente, e ao final regista-se a posição inicial do sufixo.

        Parâmetros:
            suffix (str): Sufixo a ser inserido.
            index (int): Posição inicial do sufixo na string original.
        """
        current = self.tree
        for char in suffix + "$":
            if char not in current:
                current[char] = {}
            current = current[char]
            if char == "$":
                if "index" not in current:
                    current["index"] = []
                if index not in current["index"]:
                    current["index"].append(index)

    def search(self, substring):
        """
        Procura todas as posições onde uma determinada substring ocorre na Árvore de Sufixos.

        A pesquisa percorre a árvore seguindo os caracteres da substring e, caso encontrada, recolhe todas as posições associadas.

        Parâmetros:
            substring (str): Substring a procurar na Árvore de Sufixos.

        Retorna:
            list: Lista das posições iniciais onde a substring ocorre no texto original.
        """
        if substring == "":
            return []

        current = self.tree
        for char in substring:
            if char not in current:
                return []  # Substring não encontrada.
            current = current[char]
        return self._collect_positions(current)

    def _collect_positions(self, node):
        """
        Função auxiliar que recolhe todas as posições associadas a partir de um determinado nó da árvore.

        Esta função é chamada recursivamente para recolher todos os índices armazenados nas folhas.

        Parâmetros:
            node (dict): Nó atual da Árvore de Sufixos.

        Retorna:
            list: Lista ordenada de posições onde a substring ocorre.
        """
        positions = []
        for key, child in node.items():
            if key == "index":
                positions.extend(child)
            elif isinstance(child, dict):
                positions.extend(self._collect_positions(child))
        return sorted(positions)

# Exemplo
if __name__ == "__main__":
    # Exemplo de Trie
    print("=== Trie Example ===")
    trie = Trie()
    words = ["apple", "app", "banana", "band", "bandana"]
    for word in words:
        trie.insert(word)

    print("Search 'app':", trie.search("app"))  # Verdadeiro
    print("Search 'apple':", trie.search("apple"))  # Verdadeiro
    print("Search 'apples':", trie.search("apples"))  # Falso
    print("Words starting with 'ban':", trie.starts_with("ban"))  # ['banana', 'band', 'bandana']

    # Exemplo Suffix Tree
    print("\n=== Suffix Tree Example ===")
    suffix_tree = SuffixTree()
    text = "banana"
    suffix_tree.insert(text)

    print("Search 'ana':", suffix_tree.search("ana"))  # [1, 3]
    print("Search 'ban':", suffix_tree.search("ban"))  # [0]
    print("Search 'xyz':", suffix_tree.search("xyz"))  # []
