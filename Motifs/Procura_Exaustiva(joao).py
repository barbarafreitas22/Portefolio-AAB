def motif_score(seqs, indexes, L):
    """
    Calcula o score de uma configuração de motivos.
    Para cada coluna dos motivos (substrings extraídas das sequências em 'indexes'),
    soma a frequência da letra mais comum.
    """
    motifs = [seq[i:i+L] for seq, i in zip(seqs, indexes)]
    total_score = 0
    for col in zip(*motifs):
        total_score += max(col.count(base) for base in set(col))
    return total_score

def next_combination(indexes, seq_lengths, L):
    """
    Gera a próxima combinação de índices para os motivos.
    Se não houver mais combinações, retorna None.
    """
    new_indexes = indexes.copy()
    pos = len(new_indexes) - 1
    while pos >= 0 and new_indexes[pos] >= seq_lengths[pos] - L:
        pos -= 1
    if pos < 0:
        return None
    new_indexes[pos] += 1
    for i in range(pos+1, len(new_indexes)):
        new_indexes[i] = 0
    return new_indexes

def exhaustive_search(seqs, L):
    """
    Executa uma busca exaustiva em 'seqs' para encontrar a configuração de posições
    (início do motivo em cada sequência) que maximiza o score.
    Retorna (melhor_indexes, melhor_score).
    """
    seq_lengths = [len(seq) for seq in seqs]
    indexes = [0] * len(seqs)
    best_score = -1
    best_indexes = None
    while indexes is not None:
        s = motif_score(seqs, indexes, L)
        if s > best_score:
            best_score = s
            best_indexes = indexes.copy()
        indexes = next_combination(indexes, seq_lengths, L)
    return best_indexes, best_score

# Exemplo de uso:
if __name__ == '__main__':
    sequences = ["ATGGTCGC", "TTGTCTGA", "CCGTAGTA"]
    motif_length = 3
    best_indexes, best_score = exhaustive_search(sequences, motif_length)
    print("Melhores posições:", best_indexes)
    print("Score:", best_score)
