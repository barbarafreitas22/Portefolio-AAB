def procura_exaustiva_motifs(seqs, L):
    """
    Procura os melhores motifs de um determinado comprimento nas sequências fornecidas,
    ao testar exaustivamente todas as posições possíveis e selecionar a combinação
    com a maior pontuação.

    Parâmetros:
        seqs (list): Lista das sequências biológicas (strings)
        L (int): Comprimento do motif a procurar

    Return:
        Um tuplo com:
            - melhor_p (list): Posições iniciais dos melhores motifs em cada sequência
            - melhor_score (int): Pontuação do melhor conjunto de motifs
    """
    melhor_score, melhor_p = 0, None
    tam_seq = len(seqs[0])
    limite = tam_seq - L + 1 

    def score(pos):
        """
        Calcula a pontuação de conservação para um conjunto de motivos nas posições especificadas
        
        Parâmetros:
           pos (list): Lista de posições iniciais em cada sequência
            
        Return:
           int: Pontuação total de conservação das colunas dos motifs
        """
        motifs = [seq[p:p+L] for seq, p in zip(seqs, pos)]
        return sum(max(col.count(b) for b in set(col)) for col in zip(*motifs))
 
    def procura(i, pos_at):
        """
        Função recursiva que realiza a procura por todas as combinações possíveis
        de posições iniciais nas sequências

        Parâmetros:
            i (int): Índice da sequência atual que está a ser processada
            pos_at (list): Lista de posições iniciais já escolhidas para as sequências anteriores
            
        Return:
            A função não retorna valores, atualiza as variáveis melhor_score e melhor_p
        """
        nonlocal melhor_score, melhor_p
        if i == len(seqs):
            sc = score(pos_at)
            if sc > melhor_score:
                melhor_score, melhor_p = sc, pos_at
            return
        for p in range(limite):
            procura(i + 1, pos_at + [p]) 
    procura(0, [])
    return melhor_p, melhor_score

seqs = "ATGGTCGC TTGTCTGA CCGTAGTA".split()
L = 3                                      
melhor, score_final = procura_exaustiva_motifs(seqs, L)
print("Posições:", melhor, "Score:", score_final)
