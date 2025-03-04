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

def calculate_probability(seq, motif_len, start, other_motifs):
    """
    Calcula a probabilidade de um motif específico usando suavização de Laplace.
    
    A função calcula a probabilidade de um motif candidato ao considerar as bases 
    já encontradas nas outras sequências e vai aplicar uma suavização de Laplace para 
    lidar com probabilidades de bases raras.
    
    Parâmetros:
        seq (str): Sequência na qual será calculada a probabilidade do motif.
        motif_len (int): Comprimento do motif.
        start (int): Posição inicial do motif candidato na sequência.
        other_motifs (list): Lista de motifs já encontrados nas outras sequências.
    
    Return:
        float: Probabilidade calculada do motif
    """
    motif = seq[start:start + motif_len]
    score = 1.0
    total = len(other_motifs) + 4  # Laplace smoothing
    for i, base in enumerate(motif):
        counts = {n: 1 for n in "ACGT"}  # Inicializa com 1 para Laplace
        for m in other_motifs:
            counts[m[i].upper()] = counts.get(m[i].upper(), 1) + 1
        score *= counts[base.upper()] / total
    return score

def gibbs_sampling_motif_search(seqs, L, num_iterations=1000):
    """
    Realiza busca de motifs usando o algoritmo de Gibbs Sampling.

    O algoritmo é uma meta-heurística probabilística para encontrar motifs conservados num conjunto de sequências. 
    Funciona iterativamente:
    1. Inicializa posições de motifs aleatoriamente
    2. Para cada sequência, remove-se temporariamente o seu motif
    3. Calculam-se as probabilidades de novos motifs candidatos
    4. Escolhe uma nova posição após uma amostragem aleatória
    5. Atualiza a melhor pontuação encontrada
    
    Parâmetros:
        seqs (list): Sequências de DNA para encontrar motifs
        L (int): Comprimento dos motifs
        num_iterations (int, opcional): Número de iterações. Padrão é 1000
    
    Return:
        tuple: Tupla contendo posições dos motifs e melhor pontuação
    """
    motif_positions = [random.randint(0, len(seq) - L) for seq in seqs]
    best_score = score(motif_positions)
    for _ in range(num_iterations):
        for i in range(len(seqs)):
            excluded_sequence = seqs[i]
            other_motifs = [seqs[j][motif_positions[j]:motif_positions[j] + L] for j in range(len(seqs)) if j != i]           
            probabilities = [calculate_probability(excluded_sequence, L, pos, other_motifs) for pos in range(len(excluded_sequence) - L + 1)]           
            total_prob = sum(probabilities)
            probabilities = [p / total_prob for p in probabilities]            
            motif_positions[i] = random.choices(range(len(probabilities)), weights=probabilities)[0]      
        current_score = score(motif_positions)
        
        if current_score > best_score:
            best_score = current_score
    return motif_positions, best_score
