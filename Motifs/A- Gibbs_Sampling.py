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

def calcular_probabilidade(seq, L, inicio, outros_motifs):
    """
    Calcula a probabilidade de um motif específico usando suavização de Laplace.
    
    A função calcula a probabilidade de um motif candidato ao considerar as bases 
    já encontradas nas outras sequências e vai aplicar uma suavização de Laplace para 
    lidar com probabilidades de bases raras.
    
    Parâmetros:
        seq (str): Sequência na qual será calculada a probabilidade do motif.
        L (int): Comprimento do motif.
        inicio (int): Posição inicial do motif candidato na sequência.
        outros_motifs (list): Lista de motifs já encontrados nas outras sequências.
    
    Return:
        float: Probabilidade calculada do motif
    """
    motif = seq[inicio:inicio + L]
    probabilidade = 1.0
    total = len(outros_motifs) + 4  # Laplace smoothing
    for i, base in enumerate(motif):
        counts = {n: 1 for n in "ACGT"}  # Inicializa com 1 para Laplace
        for m in outros_motifs:
            counts[m[i].upper()] = counts.get(m[i].upper(), 1) + 1
        probabilidade *= counts[base.upper()] / total
    return probabilidade

def gibbs_sampling(seqs, L, num_it=1000):
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
        num_it (int, opcional): Número de iterações. Padrão é 1000
    
    Return:
        tuple: Tupla contendo posições dos motifs e melhor pontuação
    """
    posições_motif = [random.randint(0, len(seq) - L) for seq in seqs]
    melhor_score = score(posições_motif)
    for _ in range(num_it):
        for i in range(len(seqs)):
            sequencia_excluida = seqs[i]
            outros_motifs = [seqs[j][posições_motif[j]:posições_motif[j] + L] for j in range(len(seqs)) if j != i]           
            probabilidades = [calcular_probabilidade(sequencia_excluida, L, pos, outros_motifs) for pos in range(len(sequencia_excluida) - L + 1)]           
            prob_total = sum(probabilidades)
            probabilidades = [p / prob_total for p in probabilidades]            
            posições_motif[i] = random.choices(range(len(probabilidades)), weights=probabilidades)[0]      
        score_atual = score(posições_motif)
        
        if score_atual > melhor_score:
            melhor_score = score_atual
    return posições_motif, melhor_score
