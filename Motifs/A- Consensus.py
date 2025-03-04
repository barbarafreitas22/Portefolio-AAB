def score_motifs(seqs, pos, L):
    """
    Calcula o score dos motifs extraídos de seqs através das posições em pos
    O score é a soma, para cada coluna do alinhamento dos motifs, da frequência da letra mais comum

    Parâmetros:
        seqs (list of str): Lista de sequências de DNA
        pos (list of int): Lista de posições iniciais para extrair os motifs
        L (int): Tamanho do motif

    Return:
        int: O score dos motifs
    """
    motifs = [seq[p:p+L] for seq, p in zip(seqs, pos)]
    score = 0
    for col in zip(*motifs):
        score += max(col.count(let) for let in set(col))
    return score

def consensus_heu(seqs, L):
    """
    Algoritmo heurístico que encontra, de forma greedy, as melhores posições iniciais dos motifs:
      - Para as duas primeiras sequências, testa todas as combinações possíveis.
      - Para cada sequência subsequente, escolhe a posição que maximiza o score dos motifs já formados.

    Parâmetros:
        seqs (list of str): Lista de sequências de DNA
        L (int): Tamanho do motif

    Return:
        Um tuplo com:
            - list of int: Lista das melhores posições iniciais para os motifs
            - int: O score final dos motifs
    """
    if len(seqs) < 2:
        raise ValueError("É necessário ter pelo menos duas sequências.")

    melhor_pos = None
    melhor_score = -1
    for s1 in range(len(seqs[0]) - L + 1):
        for s2 in range(len(seqs[1]) - L + 1):
            posicoes = [s1, s2]
            score_atual = score_motifs(seqs[:2], posicoes, L)
            if score_atual > melhor_score:
                melhor_score = score_atual
                melhor_pos = posicoes.copy()
    
    for i in range(2, len(seqs)):
        m_posicoes = None
        melhor_score_i = -1
        for pos in range(len(seqs[i]) - L + 1):
            posicoes = melhor_pos + [pos]
            score_atual = score_motifs(seqs[:i+1], posicoes, L)
            if score_atual > melhor_score_i:
                melhor_score_i = score_atual
                m_posicoes = pos
        melhor_pos.append(m_posicoes)
        melhor_score = melhor_score_i  

    score_f = score_motifs(seqs, melhor_pos, L)
    return melhor_pos, score_f

if __name__ == '__main__':
    seqs = ["ATGGTCGC", "TTGTCTGA", "CCGTAGTA"]
    L = 3

    pos_f, score_f = consensus_heu(seqs, L)
    print("Posições:", pos_f)
    print("Score:", score_f)
