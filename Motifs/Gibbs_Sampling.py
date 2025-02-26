def calculate_probability(seq, motif_len, start, other_motifs):
    motif = seq[start:start + motif_len]
    score = 1.0
    total = len(other_motifs) + 4  # Laplace smoothing

    for i, base in enumerate(motif):
        counts = {n: 1 for n in "ACGT"}  # Inicializa com 1 para Laplace
        for m in other_motifs:
            counts[m[i].upper()] = counts.get(m[i].upper(), 1) + 1
        score *= counts[base.upper()] / total

    return score

def gibbs_sampling_motif_search(sequences, motif_length, num_iterations=1000):
    # Inicializa as posições dos motivos aleatoriamente
    motif_positions = [random.randint(0, len(seq) - motif_length) for seq in sequences]
    best_score = score(motif_positions, sequences, motif_length)

    for _ in range(num_iterations):
        for i in range(len(sequences)):
            # Exclui a sequência atual
            excluded_sequence = sequences[i]
            other_motifs = [sequences[j][motif_positions[j]:motif_positions[j] + motif_length] for j in range(len(sequences)) if j != i]

            # Calcula as probabilidades para a sequência excluída
            probabilities = [calculate_probability(excluded_sequence, motif_length, pos, other_motifs) for pos in range(len(excluded_sequence) - motif_length + 1)]

            # Normaliza as probabilidades
            total_prob = sum(probabilities)
            probabilities = [p / total_prob for p in probabilities]

            # Amostra uma nova posição para a sequência excluída
            motif_positions[i] = random.choices(range(len(probabilities)), weights=probabilities)[0]

        # Avalia a nova solução
        current_score = score(motif_positions, sequences, motif_length)
        if current_score > best_score:
            best_score = current_score  # Atualiza a melhor pontuação

    return motif_positions, best_score
