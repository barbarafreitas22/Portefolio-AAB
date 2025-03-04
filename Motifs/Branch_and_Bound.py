def procura_exaustiva_motifs(seqs, L):
    """
    Procura os melhores motifs de um determinado comprimento nas sequências fornecidas,
    ao testar exaustivamente todas as posições possíveis e selecionar a combinação
    com a maior pontuação.

    Parâmetros:
        seqs (list): Lista das sequências biológicas (strings)
        L (int): Comprimento do motif a procurar

    Retorna:
        Um tuplo com:
            - melhor_p (list): Posições iniciais dos melhores motifs em cada sequência
            - melhor_score (int): Pontuação do melhor conjunto de motifs
    """
    melhor_score, melhor_p = 0, None  # Inicializa a melhor pontuação e as melhores posições
    tam_seq = len(seqs[0])  # Obtém o tamanho das sequências (assume-se que têm o mesmo tamanho)
    limite = tam_seq - L + 1  # Calcula o número de posições possíveis para um motif de comprimento L

    def score(pos):
        """
        Calcula a pontuação de conservação para um conjunto de motivos nas posições especificadas
        
        Parâmetros:
           pos (list): Lista de posições iniciais em cada sequência
            
        Retorna:
           int: Pontuação total de conservação das colunas dos motifs
        """
        motifs = [seq[p:p+L] for seq, p in zip(seqs, pos)]  # Extrai os motifs das sequências com base nas posições iniciais
        return sum(max(col.count(b) for b in set(col)) for col in zip(*motifs))  # Calcula a pontuação somando os nucleótidos mais frequentes em cada coluna

    def procura(i, pos_at):
        """
        Função recursiva que realiza a procura por todas as combinações possíveis
        de posições iniciais nas sequências

        Parâmetros:
            i (int): Índice da sequência atual que está a ser processada
            pos_at (list): Lista de posições iniciais já escolhidas para as sequências anteriores
            
        Retorna:
            A função não retorna valores, atualiza as variáveis melhor_score e melhor_p
        """
        nonlocal melhor_score, melhor_p  # Permite modificar as variáveis globais dentro da função
        if i == len(seqs):  # Se já processámos todas as sequências
            sc = score(pos_at)  # Calcula a pontuação para as posições escolhidas
            if sc > melhor_score:  # Se a pontuação for a melhor encontrada até agora
                melhor_score, melhor_p = sc, pos_at  # Atualiza a melhor pontuação e as melhores posições
            return
        for p in range(limite):  # Percorre todas as posições possíveis para a sequência atual
            procura(i + 1, pos_at + [p])  # Chama recursivamente para a próxima sequência com a posição atual adicionada
    
    procura(0, [])  # Inicia a procura recursiva
    return melhor_p, melhor_score  # Retorna as melhores posições e a pontuação correspondente


seqs = "ATGGTCGC TTGTCTGA CCGTAGTA".split()  
L = 3                                         
melhor, score_final = procura_exaustiva_motifs(seqs, L)
print("Posições:", melhor, "Score:", score_final)  
