def score_motifs(seqs, positions, L):
    """
    Calcula o score dos motivos extraídos de 'seqs' usando as posições em 'positions'.
    O score é a soma, para cada coluna do alinhamento dos motivos, da frequência da letra mais comum.
    """
    # Extrai os motivos (substrings) de cada sequência
    motifs = [seq[p:p+L] for seq, p in zip(seqs, positions)]
    score = 0
    # Para cada coluna dos motivos, soma a contagem máxima de uma letra
    for col in zip(*motifs):
        score += max(col.count(letter) for letter in set(col))
    return score

def heuristic_consensus(seqs, L):
    """
    Algoritmo heurístico que encontra, de forma gulosa, as melhores posições de início dos motivos:
      1. Para as duas primeiras sequências, testa todas as combinações possíveis.
      2. Para cada sequência subsequente, escolhe a posição que maximiza o score dos motivos formados.
    
    Retorna uma tupla (melhores_posições, score_final).
    """
    if len(seqs) < 2:
        raise ValueError("É necessário ter pelo menos duas sequências.")

    # Encontra as melhores posições para as duas primeiras sequências
    best_positions = None
    best_score = -1
    for s1 in range(len(seqs[0]) - L + 1):
        for s2 in range(len(seqs[1]) - L + 1):
            positions = [s1, s2]
            current_score = score_motifs(seqs[:2], positions, L)
            if current_score > best_score:
                best_score = current_score
                best_positions = positions.copy()
    
    # Para cada sequência adicional, escolhe a posição que maximiza o score
    for i in range(2, len(seqs)):
        best_pos = None
        best_score_i = -1
        for pos in range(len(seqs[i]) - L + 1):
            positions = best_positions + [pos]
            # Calcula o score usando as primeiras (i+1) sequências
            current_score = score_motifs(seqs[:i+1], positions, L)
            if current_score > best_score_i:
                best_score_i = current_score
                best_pos = pos
        best_positions.append(best_pos)
        best_score = best_score_i  # atualiza o score geral

    # Calcula o score final usando todas as sequências
    final_score = score_motifs(seqs, best_positions, L)
    return best_positions, final_score

# Exemplo de uso e teste:
if __name__ == '__main__':
    sequences = ["ATGGTCGC", "TTGTCTGA", "CCGTAGTA"]
    motif_length = 3

    positions, final_score = heuristic_consensus(sequences, motif_length)
    print("Melhores posições:", positions)
    print("Score final:", final_score)
