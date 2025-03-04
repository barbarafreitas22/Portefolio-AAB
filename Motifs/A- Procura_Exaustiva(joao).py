def score_motif(seqs, indices, L):
    """
    Calcula o score de uma configuração de motifs

    Parâmetros:
        seqs (list[str]): Lista de sequências de onde os motifs são extraídos
        indices (list[int]): Lista com as posições de início dos motifs em cada sequência
        L (int): Comprimento do motif

    Return:
        int: O score
    """
    motifs = [seq[i:i+L] for seq, i in zip(seqs, indices)]
    total_score = 0
    for col in zip(*motifs):
        total_score += max(col.count(base) for base in set(col))
    return total_score

def prox_combinacao(indices, seq_comp, L):
    """
    Gera a próxima combinação de índices para os motifs

    Parâmetros:
        indices (list[int]): Combinação atual de índices 
        seq_comp (list[int]): Lista com os comprimentos de cada sequência
        L (int): Comprimento do motif

    Return:
        list[int] ou None: A próxima combinação de índices se existir; caso contrário, None se não houver mais combinações
    """
    novos_indices = indices.copy()
    pos = len(novos_indices) - 1
    while pos >= 0 and novos_indices[pos] >= seq_comp[pos] - L:
        pos -= 1
    if pos < 0:
        return None
    novos_indices[pos] += 1
    for i in range(pos+1, len(novos_indices)):
        novos_indices[i] = 0
    return novos_indices

def procura_exaustiva(seqs, L):
    """
    Executa uma procura exaustiva nas sequências para encontrar a configuração de posições que maximiza o score

    Parâmetros:
        seqs (list[str]): Lista de sequências de onde se pretende extrair os motifs
        L (int): Comprimento do motif

    Return:
        Um tuplo com:
            - list[int]: A configuração de índices que maximiza o score
            - int: O score máximo obtido
    """
    seq_lengths = [len(seq) for seq in seqs]
    indices = [0] * len(seqs)
    melhor_score = -1
    melhores_indices = None
    while indices is not None:
        s = score_motif(seqs, indices, L)
        if s > melhor_score:
            melhor_score = s
            melhores_indices = indices.copy()
        indices = prox_combinacao(indices, seq_lengths, L)
    return melhores_indices, melhor_score

if __name__ == '__main__':
    sequencias = ["ATGGTCGC", "TTGTCTGA", "CCGTAGTA"]
    L = 3
    melhores_indices, melhor_score = procura_exaustiva(sequencias, L)
    print("Melhores posições:", melhores_indices)
    print("Score:", melhor_score)
