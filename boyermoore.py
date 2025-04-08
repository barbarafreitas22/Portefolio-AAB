class BoyerMoore:
    """
    Implementação do algoritmo Boyer-Moore para procura de padrões.
    O algoritmo utiliza duas regras principais de otimização: a regra do bad character e a regra do good suffix.
    """

    def __init__(self, alphabet, pattern):
        """
        Inicializa a classe com o alfabeto e o padrão a ser buscado.
        """
        self.alphabet = alphabet
        self.pattern = pattern
        self.preprocess()  # Sempre que damos alphabet e pattern, corre esta função

    def preprocess(self):
        """
        Realiza o pré-processamento utilizando as duas regras de Boyer-Moore:
        1. Bad Character Rule (BCR)
        2. Good Suffix Rule (GSR)
        """
        self.process_bcr()
        self.process_gsr()

    def process_bcr(self):
        """
        Implementação do pré-processamento da regra do bad character (BCR).
        A função calcula a última ocorrência de cada caractere do alfabeto no padrão
        e armazena essas informações em um dicionário (self.occ).
        """
        self.occ = {}  # Dicionário que mapeia caracteres para suas últimas ocorrências no padrão
        for s in self.alphabet:
            self.occ[s] = -1  # Inicializa todas as ocorrências com -1 (não encontrado)
        for i in range(len(self.pattern)):
            self.occ[self.pattern[i]] = i  # A última ocorrência de cada caractere no padrão
        print(self.occ)

    def process_gsr(self):
        """
        Implementação do pré-processamento da regra do good suffix (GSR).
        A função calcula o deslocamento máximo para avançar no padrão sem comprometer a busca.
        São criadas duas listas:
        Define o maior sufixo possível para um prefixo do padrão.
        Define o número de posições que podem ser avançadas no texto.
        """
        self.f = [0] * (len(self.pattern) + 1)  # Lista de índices para a regra do good suffix
        self.s = [0] * (len(self.pattern) + 1)  # Lista de deslocamentos para a regra do good suffix
        i = len(self.pattern)             # Começa do final do padrão
        j = len(self.pattern) + 1        # J é sempre maior que o tamanho do padrão
        self.f[i] = j  # A última posição da lista f recebe o valor de j
        print(self.f)
        
        while i > 0:  # Percorre o padrão da direita para a esquerda
            while j <= len(self.pattern) and self.pattern[i - 1] != self.pattern[j - 1]:  # Busca onde ocorre a falha
                if self.s[j] == 0:  # Se a posição j não foi definida ainda
                    self.s[j] = j - i  # Calcula a distância do bom sufixo
                j = self.f[j]  # Atualiza o valor de j baseado na lista f
            i = i - 1
            j = j - 1
            self.f[i] = j  # Atualiza a lista f para o valor de j
        j = self.f[0]  # j recebe o valor do primeiro elemento da lista f
        for i in range(0, len(self.pattern)):  # Finaliza o cálculo dos deslocamentos
            if self.s[i] == 0:
                self.s[i] = j
            if i == j:
                j = self.f[j]
        print(self.f)
        print(self.s)

    def search_pattern(self, text):
        """
        Realiza a busca do padrão no texto utilizando o algoritmo Boyer-Moore.
        """
        res = [] 
        i = 0
        while i <= (len(text) - len(self.pattern)):  # Enquanto for possível realizar uma comparação
            j = (len(self.pattern) - 1)  # Inicia a comparação no final do padrão
            while j >= 0 and self.pattern[j] == text[j + i]:  
                j -= 1
            if j < 0:
                res.append(i)  # Padrão encontrado, armazena a posição i
                i = i + self.s[0]  # Avança de acordo com a regra do good suffix
            else:
                c = text[i + j]
                i += max(self.s[j + 1], j - self.occ[c])  # Avança conforme a regra do bad character
        return res


def test():
    """
    Função de teste para verificar a implementação do algoritmo Boyer-Moore.
    """
    bm = BoyerMoore("ACTG", "ACCA")
    print(bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC"))


if __name__ == "__main__":
    test()

