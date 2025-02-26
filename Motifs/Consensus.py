def score_motifs(seqs, positions, motif_length):
    """
    Calculates the score for a given set of motif positions across all sequences. 
    The score is based on the frequency of characters in each column of the aligned motifs.
    """
    motifs = [seq[p:p + motif_length] for seq, p in zip(seqs, positions)]
    score = 0
    for col in zip(*motifs):
        col_counts = [col.count(b) for b in set(col)]
        score += max(col_counts)
    return score

def heuristic_consensus(seqs, motif_length):
    """
    This algorithm iteratively finds the best starting positions for motifs in the sequences by:
    - Finding the best positions for the first two sequences.
    - For each subsequent sequence chooses the best starting position that maximizes the score, 
    considering the fixed positions from previous sequences.
    """
    num_seqs = len(seqs)
    best_score = 0
    best_positions = [0, 0]
   
    for s1 in range(len(seqs[0]) - motif_length + 1):
        for s2 in range(len(seqs[1]) - motif_length + 1):
            score = score_motifs(seqs, [s1, s2], motif_length)
            if score > best_score:
                best_score = score
                best_positions = [s1, s2]
    for i in range(2, num_seqs):
        best_pos_for_i = 0
        best_score_for_i = -1
        for pos in range(len(seqs[i]) - motif_length + 1):
  
            current_positions = best_positions + [pos]
            score = score_motifs(seqs, current_positions, motif_length)
            if score > best_score_for_i:
                best_score_for_i = score
                best_pos_for_i = pos
        
        best_positions.append(best_pos_for_i)
    
    return best_positions, best_score

seqs = ["ATGGTCGC", "TTGTCTGA", "CCGTAGTA"]
motif_length = 3

best_positions, best_score = heuristic_consensus(seqs, motif_length)
print("Best positions:", best_positions)
print("Best score:", best_score)

