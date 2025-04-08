class FiniteAutomaton:
    """
    Implementação de um autómato finito para busca de padrões.

    Este autómato é configurado através de um alfabeto e um padrão a serem procurados em sequências. 
    A tabela de transições é construída com base no padrão, o que permite identificar os estados percorridos e as ocorrências do padrão.
    """

    def __init__(self, alphabet, pattern):
        """
        Inicializa o autómato finito com o alfabeto e o padrão a serem procurados.

        Parâmetros:
            alphabet (str): O alfabeto utilizado tanto no padrão quanto nas sequências.
            pattern (str): O padrão que se deseja encontrar nas sequências.
        """
        self.alphabet = alphabet
        self.pattern = pattern
        self.num_states = len(pattern) + 1
        self.transition_table = {}
        self._build_transition_table()

    def _build_transition_table(self):
        """
        Constrói a tabela de transições do autómato com base no padrão definido.

        Para cada estado possível e para cada caractere do alfabeto, este método calcula
        a sobreposição entre o prefixo formado pelo estado atual acrescido do caractere e o padrão, ao registar o resultado correspondente na tabela de transições.
        """
        for state in range(self.num_states):
            for char in self.alphabet:
                prefix = self.pattern[:state] + char
                self.transition_table[(state, char)] = self._overlap(prefix)

    def _overlap(self, s):
        """
        Calcula o tamanho da sobreposição entre o final da string 's' e o início do padrão.

        Este método determina quantos caracteres finais de 's' coincidem com os caracteres
        iniciais do padrão, retornando o comprimento desta sobreposição.

        Parâmetros:
            s (str): A string na qual se quer identificar a sobreposição com o padrão.

        Retorna:
            int: O tamanho da sobreposição encontrado.
        """
        max_overlap = min(len(s), len(self.pattern))
        for i in range(max_overlap, 0, -1):
            if s[-i:] == self.pattern[:i]:
                return i
        return 0

    def apply_sequence(self, sequence):
        """
        Aplica o autómato a uma sequência e retorna a lista dos estados percorridos.

        O autómato processa cada caractere da sequência através da tabela de transições, registrando a evolução dos estados.

        Parâmetros:
            sequence (str): A sequência na qual o autómato será aplicado.

        Retorna:
            list[int]: Uma lista com os estados visitados durante o processamento da sequência.
        """
        state = 0
        states = [state]
        for char in sequence:
            state = self.transition_table.get((state, char), 0)
            states.append(state)
        return states

    def find_pattern_occurrences(self, sequence):
        """
        Identifica todas as ocorrências do padrão na sequência fornecida.

        Ao aplicar o autómato na sequência, este método verifica em quais posições
        o autómato alcança o estado final, indicando assim a ocorrência do padrão.

        Parâmetros:
            sequence (str): A sequência na qual se irá procurar o padrão.

        Retorna:
            list[int]: Uma lista com as posições iniciais onde o padrão ocorre na sequência.
        """
        state = 0
        occurrences = []
        for i, char in enumerate(sequence):
            state = self.transition_table.get((state, char), 0)
            if state == self.num_states - 1:
                occurrences.append(i - len(self.pattern) + 1)
        return occurrences


if __name__ == "__main__":
    alphabet = "AC"
    pattern = "ACA"

    automaton = FiniteAutomaton(alphabet, pattern)

    print("Tabela de Transições:")
    for key, value in automaton.transition_table.items():
        print(f"Estado {key[0]}, Caractere '{key[1]}' -> Estado {value}")

    sequence = "CACAACAA"
    states = automaton.apply_sequence(sequence)
    print("\nEstados percorridos:", states)

    occurrences = automaton.find_pattern_occurrences(sequence)
    print("\nOcorrências do padrão:", occurrences)
