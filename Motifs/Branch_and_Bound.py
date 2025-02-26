def procura_exaustiva_motifs(seqs, L):
    """
    Searches for the best motifs of length L in the given sequences by exhaustively trying all possible positions, 
    selecting the combination with the highest conservation score.

    Args:
        seqs (list): List of biological sequences (strings).
        L (int): Length of the motif to find.

    Returns:
        A tuple containing:
            - best_s (list): List of start positions for the best motifs in each sequence.
            - best_score (int): The score of the best motif set.
    """
    best_score, best_s = 0, None
    tam_seq = len(seqs[0])
    limite = tam_seq - L + 1 

    def score(s):
        motifs = [seq[p:p+L] for seq, p in zip(seqs, s)]
        return sum(max(col.count(b) for b in set(col)) for col in zip(*motifs))
 
    def busca(i, s):
        nonlocal best_score, best_s
        if i == len(seqs):
            sc = score(s)
            if sc > best_score:
                best_score, best_s = sc, s
            return
        for p in range(limite):
            busca(i + 1, s + [p]) 
    busca(0, [])
    return best_s, best_score


seqs = "ATGGTCGC TTGTCTGA CCGTAGTA".split()
L = 3                                      
melhor, score_final = procura_exaustiva_motifs(seqs, L)
print("Melhores posições:", melhor, "score:", score_final)
