def score_motifs(seqs, pos, L):
    """
    Calcula o score dos motifs extraídos de seqs através das posições em pos.
    O score é a soma, para cada coluna do alinhamento dos motifs, da frequência da letra mais comum.

    Parâmetros:
        seqs (list of str): Lista de sequências de DNA.
        pos (list of int): Lista de posições iniciais para extrair os motifs.
        L (int): Tamanho do motif.

    Retorna:
        int: O score dos motifs.
    """
    motifs = [seq[p:p+L] for seq, p in zip(seqs, pos)]  # Extrai os motifs das sequências com base nas posições fornecidas.
    score = 0
    for col in zip(*motifs):  # Percorre cada coluna do alinhamento dos motifs.
        score += max(col.count(let) for let in set(col))  # Soma a frequência da letra mais comum em cada coluna.
    return score

def consensus_heu(seqs, L):
    """
    Algoritmo heurístico que encontra, de forma greedy, as melhores posições iniciais dos motifs:
      - Para as duas primeiras sequências, testa todas as combinações possíveis.
      - Para cada sequência subsequente, escolhe a posição que maximiza o score dos motifs já formados.

    Parâmetros:
        seqs (list of str): Lista de sequências de DNA.
        L (int): Tamanho do motif.

    Retorna:
        Um tuplo com:
            - list of int: Lista das melhores posições iniciais para os motifs.
            - int: O score final dos motifs.
    """
    if len(seqs) < 2:
        raise ValueError("É necessário ter pelo menos duas sequências.")  # Garante que há pelo menos duas sequências.

    melhor_pos = None  # Inicializa a variável para armazenar as melhores posições.
    melhor_score = -1  # Inicializa a melhor pontuação com um valor baixo.
    
    # Testa todas as combinações possíveis para as duas primeiras sequências.
    for s1 in range(len(seqs[0]) - L + 1):  # Percorre todas as posições possíveis na primeira sequência.
        for s2 in range(len(seqs[1]) - L + 1):  # Percorre todas as posições possíveis na segunda sequência.
            posicoes = [s1, s2]  # Conjunto de posições a testar.
            score_atual = score_motifs(seqs[:2], posicoes, L)  # Calcula o score das duas primeiras sequências.
            if score_atual > melhor_score:  # Se o score atual for melhor, guarda-o.
                melhor_score = score_atual
                melhor_pos = posicoes.copy()
    
    # Para cada sequência subsequente, escolhe a melhor posição para maximizar o score.
    for i in range(2, len(seqs)):  # Começa na terceira sequência (índice 2).
        m_posicoes = None  # Armazena a melhor posição para esta sequência.
        melhor_score_i = -1  # Inicializa o melhor score para esta sequência.
        
        for pos in range(len(seqs[i]) - L + 1):  # Testa todas as posições possíveis na sequência atual.
            posicoes = melhor_pos + [pos]  # Conjunto de posições incluindo a atual.
            score_atual = score_motifs(seqs[:i+1], posicoes, L)  # Calcula o score considerando as sequências até agora.
            if score_atual > melhor_score_i:  # Se o score for melhor, atualiza a melhor posição.
                melhor_score_i = score_atual
                m_posicoes = pos
        
        melhor_pos.append(m_posicoes)  # Adiciona a melhor posição encontrada.
        melhor_score = melhor_score_i  # Atualiza o melhor score global.

    score_f = score_motifs(seqs, melhor_pos, L)  # Calcula o score final dos motifs encontrados.
    return melhor_pos, score_f  # Retorna as melhores posições e a pontuação final.

if __name__ == '__main__':
    seqs = ["ATGGTCGC", "TTGTCTGA", "CCGTAGTA"] 
    L = 3  
    pos_f, score_f = consensus_heu(seqs, L)
    print("Posições:", pos_f)  
    print("Score:", score_f)  
