class BoyerMoore:
    """
    Implementação do algoritmo Boyer-Moore para procura de padrões.
    O algoritmo utiliza duas regras principais de otimização: a regra do mau caráter e a regra do bom sufixo.
    """

    def __init__(self, alfabeto, padrao):
        """
        Inicializa a classe com o alfabeto e o padrão a ser buscado.
        
        Parâmetros:
        alfabeto (str): O alfabeto utilizado no texto.
        padrao (str): O padrão a ser procurado no texto.
        """
        self.alfabeto = alfabeto
        self.padrao = padrao
        self.preprocessar()  # Executa o pré-processamento com base no alfabeto e no padrão

    def preprocessar(self):
        """
        Realiza o pré-processamento utilizando as duas regras de Boyer-Moore:
        
        1. Regra do mau caráter (BCR)
        2. Regra do bom sufixo (GSR)
        """
        self.processar_bcr()
        self.processar_gsr()

    def processar_bcr(self):
        """
        Pré-processamento da regra do mau caráter.
        Calcula a última ocorrência de cada caráter do alfabeto no padrão e armazena essas informações em um dicionário (self.ocorrencias).
        """
        self.ocorrencias = {}  # Dicionário que mapeia caracteres para suas últimas ocorrências no padrão
        for simbolo in self.alfabeto:
            self.ocorrencias[simbolo] = -1  # Inicializa todas as ocorrências com -1 (não encontrado)
        for indice in range(len(self.padrao)):
            self.ocorrencias[self.padrao[indice]] = indice  # Atualiza com a última ocorrência de cada caractere no padrão
        print(self.ocorrencias)

    def processar_gsr(self):
        """
        Pré-processamento da regra do bom sufixo.
        Calcula o deslocamento máximo que permite avançar no padrão sem comprometer a busca.
        São criadas duas listas:
          - self.f: que armazena, para cada posição, o maior sufixo que é também um prefixo do padrão.
          - self.s: que armazena o número de posições a avançar quando ocorre uma falha.
        """
        self.f = [0] * (len(self.padrao) + 1)  # Lista de índices para a regra do bom sufixo
        self.s = [0] * (len(self.padrao) + 1)  # Lista de deslocamentos para a regra do bom sufixo
        i = len(self.padrao)             # Começa do final do padrão
        j = len(self.padrao) + 1         # j é sempre maior que o tamanho do padrão
        self.f[i] = j                  # Define o último elemento de f
        print(self.f)
        
        while i > 0:  # Percorre o padrão da direita para a esquerda
            while j <= len(self.padrao) and self.padrao[i - 1] != self.padrao[j - 1]:
                if self.s[j] == 0:
                    self.s[j] = j - i  # Calcula a distância do bom sufixo
                j = self.f[j]  # Atualiza j baseado em f
            i -= 1
            j -= 1
            self.f[i] = j  # Atualiza f para o valor de j
        j = self.f[0]
        for i in range(len(self.padrao)):
            if self.s[i] == 0:
                self.s[i] = j
            if i == j:
                j = self.f[j]
        print(self.f)
        print(self.s)

    def procurar_padrao(self, texto):
        """
        Realiza a busca do padrão no texto utilizando o algoritmo Boyer-Moore.
        
        Parâmetros:
        texto (str): O texto onde o padrão será procurado.
        
        Retorna:
        list: Uma lista com os índices onde o padrão ocorre no texto.
        """
        res = []
        i = 0
        while i <= (len(texto) - len(self.padrao)):
            j = len(self.padrao) - 1  # Inicia a comparação do final do padrão
            while j >= 0 and self.padrao[j] == texto[j + i]:
                j -= 1
            if j < 0:
                res.append(i)  # Padrão encontrado; armazena a posição
                i += self.s[0]  # Avança de acordo com a regra do bom sufixo
            else:
                c = texto[i + j]
                i += max(self.s[j + 1], j - self.ocorrencias[c])  # Avança conforme a regra do mau caráter
        return res


def testar():
    """
    Função de teste para verificar a implementação do algoritmo Boyer-Moore.
    """
    bm = BoyerMoore("ACTG", "ACCA")
    print(bm.procurar_padrao("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC"))


if __name__ == "__main__":
    testar()

