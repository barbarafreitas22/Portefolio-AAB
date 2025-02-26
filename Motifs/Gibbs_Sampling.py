def gibbs_sampling_motif_search(sequences, motif_length, num_iterations=1000):
    """Finds motifs using a Gibbs Sampling algorithm."""
    num_sequences = len(sequences)
    sequence_length = len(sequences[0])

    # Initialize starting positions randomly
    motif_positions = [random.randint(0, sequence_length - motif_length) for _ in range(num_sequences)]
    best_motif_positions = list(motif_positions)  # Start with the initial positions
    best_score = 0

    # Calculate probabilities for the excluded sequence
    probabilities = [calculate_probability(sequences[excluded_index], motif_length, start_pos, other_motifs)
        for start_pos in range(sequence_length - motif_length + 1)]

    # Normalize probabilities
    total_probability = sum(probabilities)
    probabilities = [p / total_probability if total_probability > 0 else 1 / len(probabilities) for p in probabilities]

    # Sample a new starting position for the excluded sequence
    motif_positions[excluded_index] = random.choices(range(sequence_length - motif_length + 1), weights=probabilities)[0]

    # Calculate new score
    new_score = calculate_score([sequences[i][motif_positions[i]:motif_positions[i] + motif_length] for i in range(num_sequences)])

    if new_score > best_score:
        best_score = new_score
        best_motif_positions = list(motif_positions)

    return best_motif_positions, best_score
