import random
from Branch_and_Bound import score #se fizermos isto tira se a def score
def score(positions, sequences, L):
    """
    Calcula o score de uma configuração de motivos, dado que cada posição em 'positions'
    indica o início do motivo de comprimento L em cada sequência.
    O score é a soma, para cada coluna do alinhamento dos motivos, da frequência da base mais comum.
    """
    motifs = [seq[p:p+L] for seq, p in zip(sequences, positions)]
    # Para cada coluna, pega a contagem máxima de uma base
    return sum(max(col.count(b) for b in set(col)) for col in zip(*motifs))

def calculate_probability(seq, motif_len, start, other_motifs):
    """
    Calcula a probabilidade do motivo começando na posição 'start' na sequência 'seq',
    usando Laplace smoothing (inicializando as contagens com 1) e considerando os outros motivos.
    """
    motif = seq[start:start + motif_len]
    prob = 1.0
    total = len(other_motifs) + 4  # Laplace smoothing: 1 para cada base (A, C, G, T)

    for i, base in enumerate(motif):
        # Inicializa a contagem com 1 para cada base
        counts = {n: 1 for n in "ACGT"}
        for m in other_motifs:
            counts[m[i].upper()] = counts.get(m[i].upper(), 1) + 1
        prob *= counts[base.upper()] / total

    return prob

def gibbs_sampling_motif_search(sequences, motif_length, num_iterations=1000):
    """
    Realiza a busca de motivos em 'sequences' usando o algoritmo de Gibbs Sampling.
    Inicializa posições aleatórias para os motivos e, em cada iteração, remove uma sequência,
    recalcula as probabilidades para todas as possíveis posições de motivo e reamostra.
    Retorna a configuração de posições com o melhor score encontrado.
    """
    # Inicializa as posições dos motivos aleatoriamente
    motif_positions = [random.randint(0, len(seq) - motif_length) for seq in sequences]
    best_score_val = score(motif_positions, sequences, motif_length)
    best_positions = motif_positions.copy()

    for _ in range(num_iterations):
        for i in range(len(sequences)):
            # Exclui a sequência i
            excluded_sequence = sequences[i]
            other_motifs = [sequences[j][motif_positions[j]:motif_positions[j] + motif_length] 
                            for j in range(len(sequences)) if j != i]

            # Calcula as probabilidades para cada posição possível na sequência excluída
            probabilities = [
                calculate_probability(excluded_sequence, motif_length, pos, other_motifs)
                for pos in range(len(excluded_sequence) - motif_length + 1)
            ]
            total_prob = sum(probabilities)
            # Evita divisão por zero
            if total_prob == 0:
                probabilities = [1 / len(probabilities)] * len(probabilities)
            else:
                probabilities = [p / total_prob for p in probabilities]

            # Amostra uma nova posição para a sequência excluída
            motif_positions[i] = random.choices(range(len(probabilities)), weights=probabilities)[0]

        current_score = score(motif_positions, sequences, motif_length)
        if current_score > best_score_val:
            best_score_val = current_score
            best_positions = motif_positions.copy()

    return best_positions, best_score_val


if __name__ == "__main__":
    # Exemplo de sequências e comprimento do motivo
    sequences = "ATGGTCGC TTGTCTGA CCGTAGTA".split()
    motif_length = 3

    # Executa a busca por Gibbs Sampling
    gibbs_positions, gibbs_best_score = gibbs_sampling_motif_search(sequences, motif_length, num_iterations=1000)
    print("Gibbs Sampling Motif Search:")
    print("Posições:", gibbs_positions, "Score:", gibbs_best_score)
