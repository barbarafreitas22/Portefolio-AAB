import random

def score(posicoes, sequencias, L):
    """
    Calcula a pontuação para um conjunto de motifs.

    Parâmetros:
        posicoes (list): Lista de posições iniciais em cada sequência.
        sequencias (list): Lista de sequências de DNA.
        L (int): Comprimento do motif.
        
    Retorna:
        int: Pontuação total dos motifs encontrados.
    """
    motifs = [seq[p:p+L] for seq, p in zip(sequencias, posicoes)]  # Extrai os motifs das sequências com base nas posições fornecidas.
    return sum(max(col.count(b) for b in set(col)) for col in zip(*motifs))  # Soma a contagem da base mais frequente em cada coluna.

def calcula_probabilidade(seq, L, pi, outros_motifs):
    """
    Calcula a probabilidade do motif a partir da posição inicial na sequência,
    usando um modelo baseado nas contagens de bases das restantes sequências.

    Parâmetros:
        seq (str): A sequência onde se procura o motif.
        L (int): Comprimento do motif.
        pi (int): Posição de início do motif na sequência.
        outros_motifs (list[str]): Lista dos motifs das outras sequências, usada para calcular as frequências das bases.

    Retorna:
        float: A probabilidade do motif começar na posição especificada.
    """
    motif = seq[pi:pi + L]  # Extrai o motif da sequência a partir da posição fornecida.
    prob = 1.0
    total = len(outros_motifs) + 4  # Adiciona 4 para garantir pseudocontagens (evitar zeros nas probabilidades).

    for i, base in enumerate(motif):  # Percorre cada posição do motif.
        counts = {n: 1 for n in "ACGT"}  # Inicializa a contagem das bases com pseudocontagens.
        for m in outros_motifs:  # Percorre os outros motifs para calcular as frequências das bases.
            counts[m[i].upper()] = counts.get(m[i].upper(), 1) + 1
        prob *= counts[base.upper()] / total  # Calcula a probabilidade com base nas contagens.

    return prob

def gibbs_sampling(sequences, L, num_it=1000):
    """
    Realiza a procura de motifs nas sequências utilizando o algoritmo de Gibbs Sampling.

    Parâmetros:
        sequences (list[str]): Lista de sequências onde se pretende encontrar os motifs.
        L (int): Comprimento do motif.
        num_it (int, opcional): Número de iterações do algoritmo.

    Retorna:
        Um tuplo com:
            - list[int]: Lista das melhores posições de início dos motifs em cada sequência.
            - int: A pontuação final dos motifs encontrados.
    """
    # Inicializa aleatoriamente as posições dos motifs dentro de cada sequência.
    motif_pos = [random.randint(0, len(seq) - L) for seq in sequences]
    m_score_val = score(motif_pos, sequences, L)  # Calcula o score inicial.
    m_positions = motif_pos.copy()  # Guarda a melhor configuração encontrada.

    for _ in range(num_it):  # Executa o algoritmo durante o número de iterações especificado.
        for i in range(len(sequences)):  # Percorre cada sequência, retirando-a temporariamente do conjunto.
            exc_seq = sequences[i]  # Seleciona a sequência a ser removida.
            outros_motifs = [
                sequences[j][motif_pos[j]:motif_pos[j] + L] 
                for j in range(len(sequences)) if j != i  # Mantém os motifs das restantes sequências.
            ]

            # Calcula a probabilidade de cada posição ser a melhor para o motif na sequência removida.
            probabilidades = [
                calcula_probabilidade(exc_seq, L, pos, outros_motifs)
                for pos in range(len(exc_seq) - L + 1)
            ]
            total_prob = sum(probabilidades)  # Soma total das probabilidades calculadas.

            # Normaliza as probabilidades para evitar valores inválidos (exemplo: divisão por zero).
            if total_prob == 0:
                probabilidades = [1 / len(probabilidades)] * len(probabilidades)
            else:
                probabilidades = [p / total_prob for p in probabilidades]

            # Escolhe aleatoriamente a nova posição para o motif da sequência removida, ponderando pelas probabilidades.
            motif_pos[i] = random.choices(range(len(probabilidades)), weights=probabilidades)[0]

        # Calcula o score com as novas posições encontradas.
        score_atual = score(motif_pos, sequences, L)
        if score_atual > m_score_val:  # Se for melhor que o anterior, atualiza os melhores valores.
            m_score_val = score_atual
            m_positions = motif_pos.copy()

    return m_positions, m_score_val  # Retorna as melhores posições encontradas e a pontuação final.

if __name__ == "__main__":
    sequences = "ATGGTCGC TTGTCTGA CCGTAGTA".split()
    L = 3
    gibbs_pos, gibbs_m_score = gibbs_sampling(sequences, L, num_it=1000)
    print("Posições:", gibbs_pos, "Score:", gibbs_m_score)
