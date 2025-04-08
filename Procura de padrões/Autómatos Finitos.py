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
        self.alfabeto = alfabeto  # Define o alfabeto.
        self.padrao = padrao  # Define o padrão.
        self.num_estados = len(padrao) + 1  # Número de estados é o comprimento do padrão + 1.
        self.tabela_transicao = {}  # Inicializa a tabela de transições como um dicionário vazio.
        self._constr_tabela_transicao()  # Constrói a tabela de transições.

    def _constr_tabela_transicao(self):
        """
        Constrói a tabela de transições do autómato com base no padrão definido.

        Para cada estado possível e para cada caractere do alfabeto, este método calcula
        a sobreposição entre o prefixo formado pelo estado atual acrescido do caractere e o padrão, ao registar o resultado correspondente na tabela de transições.
        """
        for estado in range(self.num_estados):  # Itera por todos os estados possíveis.
            for char in self.alfabeto:  # Itera por cada caractere do alfabeto.
                prefixo = self.padrao[:estado] + char  # Constrói o prefixo atual.
                self.tabela_transicao[(estado, char)] = self._sobreposicao(prefixo)  # Calcula e armazena o próximo estado.

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
        max_sobreposicao = min(len(s), len(self.padrao))  # Define o tamanho máximo da sobreposição.
        for i in range(max_sobreposicao, 0, -1):  # Itera do tamanho máximo até 1.
            if s[-i:] == self.padrao[:i]:  # Verifica se o final de 's' coincide com o início do padrão.
                return i  # Retorna o tamanho da sobreposição.
        return 0  # Retorna 0 se não houver sobreposição.

    def aplicar_sequencia(self, sequencia):
        """
        Aplica o autómato a uma sequência e retorna a lista dos estados percorridos.

        O autómato processa cada caractere da sequência através da tabela de transições, registrando a evolução dos estados.

        Parâmetros:
            sequence (str): A sequência na qual o autómato será aplicado.

        Retorna:
            list[int]: Uma lista com os estados visitados durante o processamento da sequência.
        """
        estado = 0  # Começa no estado inicial (0).
        estados = [estado]  # Lista para armazenar os estados percorridos.
        for char in sequencia:  # Itera por cada caractere da sequência.
            estado = self.tabela_transicao.get((estado, char), 0)  # Obtém o próximo estado ou retorna 0 se não houver transição.
            estados.append(estado)  # Adiciona o estado atual à lista.
        return estados  # Retorna a lista de estados percorridos.

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
        estado = 0  # Começa no estado inicial (0).
        ocorrencias = []  # Lista para armazenar as posições das ocorrências do padrão.
        for i, char in enumerate(sequencia):  # Itera por cada caractere da sequência com seu índice.
            estado = self.tabela_transicao.get((estado, char), 0)  # Obtém o próximo estado ou retorna 0 se não houver transição.
            if estado == self.num_estados - 1:  # Verifica se o estado final foi alcançado.
                ocorrencias.append(i - len(self.padrao) + 1)  # Calcula e armazena a posição inicial do padrão.
        return ocorrencias  # Retorna a lista de ocorrências.

if __name__ == "__main__":

    alfabeto = "AC"  
    padrao = "ACA"  

    automato = Automato_finito(alfabeto, padrao)  # Cria uma instância do autómato com o alfabeto e o padrão.

    print("Tabela de Transições:")  # Exibe a tabela de transições.
    for key, value in automato.tabela_transicao.items():  # Itera por cada entrada da tabela de transições.
        print(f"Estado {key[0]}, Caractere '{key[1]}' -> Estado {value}")  # Exibe o estado atual, caractere e próximo estado.

    sequencia = "CACAACAA"  # Define a sequência onde o padrão será procurado.
    estados = automato.aplicar_sequencia(sequencia)  # Aplica o autómato à sequência.
    print("\nEstados percorridos:", estados)  # Exibe os estados percorridos.

    ocorrencias = automato.encontrar_ocorrencias_padrao(sequencia)  # Encontra as ocorrências do padrão na sequência.
    print("\nOcorrências do padrão:", ocorrencias)  # Exibe as posições das ocorrências do padrão.
