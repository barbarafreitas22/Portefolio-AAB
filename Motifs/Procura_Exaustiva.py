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
    # Extrai os motifs das sequências nas posições especificadas
    motifs = [seq[i:i+L] for seq, i in zip(seqs, indices)]
    total_score = 0  # Inicializa a pontuação total
    # Para cada coluna dos motifs, calcula a pontuação
    for col in zip(*motifs):
        # Adiciona o máximo da contagem de cada base na coluna à pontuação total
        total_score += max(col.count(base) for base in set(col))
    return total_score  # Retorna a pontuação total

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
    novos_indices = indices.copy()  # Faz uma cópia da combinação atual
    pos = len(novos_indices) - 1  # Começa a verificar a partir do último índice
    # Enquanto a posição atual estiver dentro do limite e não puder ser incrementada
    while pos >= 0 and novos_indices[pos] >= seq_comp[pos] - L:
        pos -= 1  # Move para a esquerda
    if pos < 0:  # Se não houver mais combinações possíveis
        return None  # Retorna None
    novos_indices[pos] += 1  # Incrementa o índice na posição atual
    # Reseta os índices à direita da posição atual para 0
    for i in range(pos + 1, len(novos_indices)):
        novos_indices[i] = 0
    return novos_indices  # Retorna a nova combinação de índices

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
    seq_lengths = [len(seq) for seq in seqs]  # Obtém os comprimentos de cada sequência
    indices = [0] * len(seqs)  # Inicializa os índices com 0
    melhor_score = -1  # Inicializa a melhor pontuação como -1
    melhores_indices = None  # Inicializa as melhores posições como None
    # Enquanto houver combinações de índices
    while indices is not None:
        s = score_motif(seqs, indices, L)  # Calcula o score para a combinação atual
        if s > melhor_score:  # Se o score atual é melhor que o melhor score encontrado
            melhor_score = s  # Atualiza o melhor score
            melhores_indices = indices.copy()  # Atualiza as melhores posições
        indices = prox_combinacao(indices, seq_lengths, L)  # Gera a próxima combinação
    return melhores_indices, melhor_score  # Retorna as melhores posições e o score máximo

if __name__ == '__main__':
    sequencias = ["ATGGTCGC", "TTGTCTGA", "CCGTAGTA"]  
    L = 3  
    melhores_indices, melhor_score = procura_exaustiva(sequencias, L)  
    print("Melhores posições:", melhores_indices)  
    print("Score:", melhor_score)  
