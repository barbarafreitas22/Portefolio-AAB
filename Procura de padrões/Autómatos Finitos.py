class Automato_finito:
    """
    Implementação de um autómato finito para busca de padrões.

    Este autómato é configurado através de um alfabeto e um padrão a serem procurados em sequências. 
    A tabela de transições é construída com base no padrão, o que permite identificar os estados percorridos e as ocorrências do padrão.
    """

    def __init__(self, alfabeto, padrao):
        """
        Inicializa o autómato finito com o alfabeto e o padrão a serem procurados.

        Parâmetros:
            alphabet (str): O alfabeto utilizado tanto no padrão quanto nas sequências.
            pattern (str): O padrão que se deseja encontrar nas sequências.
        """
        self.alfabeto = alfabeto
        self.padrao = padrao
        self.num_estados = len(padrao) + 1
        self.tabela_transicao = {}
        self._constr_tabela_transicao()

    def _constr_tabela_transicao(self):
        """
        Constrói a tabela de transições do autómato com base no padrão definido.

        Para cada estado possível e para cada caractere do alfabeto, este método calcula
        a sobreposição entre o prefixo formado pelo estado atual acrescido do caractere e o padrão, ao registar o resultado correspondente na tabela de transições.
        """
        for estado in range(self.num_estados):
            for char in self.alfabeto:
                prefixo = self.padrao[:estado] + char
                self.tabela_transicao[(estado, char)] = self._sobreposicao(prefixo)

    def _sobreposicao(self, s):
        """
        Calcula o tamanho da sobreposição entre o final da string 's' e o início do padrão.

        Este método determina quantos caracteres finais de 's' coincidem com os caracteres
        iniciais do padrão, retornando o comprimento desta sobreposição.

        Parâmetros:
            s (str): A string na qual se quer identificar a sobreposição com o padrão.

        Retorna:
            int: O tamanho da sobreposição encontrado.
        """
        max_sobreposicao = min(len(s), len(self.padrao))
        for i in range(max_sobreposicao, 0, -1):
            if s[-i:] == self.padrao[:i]:
                return i
        return 0

    def aplicar_sequencia(self, sequencia):
        """
        Aplica o autómato a uma sequência e retorna a lista dos estados percorridos.

        O autómato processa cada caractere da sequência através da tabela de transições, registrando a evolução dos estados.

        Parâmetros:
            sequence (str): A sequência na qual o autómato será aplicado.

        Retorna:
            list[int]: Uma lista com os estados visitados durante o processamento da sequência.
        """
        estado = 0
        estados = [estado]
        for char in sequencia:
            estado = self.tabela_transicao.get((estado, char), 0)
            estados.append(estado)
        return estados

    def encontrar_ocorrencias_padrao(self, sequencia):
        """
        Identifica todas as ocorrências do padrão na sequência fornecida.

        Ao aplicar o autómato na sequência, este método verifica em quais posições
        o autómato alcança o estado final, indicando assim a ocorrência do padrão.

        Parâmetros:
            sequence (str): A sequência na qual se irá procurar o padrão.

        Retorna:
            list[int]: Uma lista com as posições iniciais onde o padrão ocorre na sequência.
        """
        estado = 0
        ocorrencias = []
        for i, char in enumerate(sequencia):
            estado = self.tabela_transicao.get((estado, char), 0)
            if estado == self.num_estados - 1:
                ocorrencias.append(i - len(self.padrao) + 1)
        return ocorrencias


if __name__ == "__main__":

    alfabeto = "AC"
    padrao = "ACA"

    automato = Automato_finito(alfabeto, padrao)

    print("Tabela de Transições:")
    for key, value in automato.tabela_transicao.items():
        print(f"Estado {key[0]}, Caractere '{key[1]}' -> Estado {value}")

    sequencia = "CACAACAA"
    estados = automato.aplicar_sequencia(sequencia)
    print("\nEstados percorridos:", estados)

    ocorrencias = automato.encontrar_ocorrencias_padrao(sequencia)
    print("\nOcorrências do padrão:", ocorrencias)
