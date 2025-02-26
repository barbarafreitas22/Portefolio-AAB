import unittest
import random

def motif_score(seqs, positions, L):
    motifs = [seq[p:p+L] for seq, p in zip(seqs, positions)]
    return sum(max(col.count(base) for base in set(col)) for col in zip(*motifs))

def random_dna_seq(n):
    return ''.join(random.choice("ACGT") for _ in range(n))

# Importe ou copie aqui a função procura_exaustiva_motifs
# from seu_modulo import procura_exaustiva_motifs
def procura_exaustiva_motifs(seqs, L):
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


class TestProcuraExaustivaMotifs(unittest.TestCase):
    def test_exemplo_basico(self):
        """Testa o exemplo fornecido no enunciado."""
        seqs = "ATGGTCGC TTGTCTGA CCGTAGTA".split()
        L = 3
        best_s, best_score = procura_exaustiva_motifs(seqs, L)
        
        # O algoritmo encontra score = 8, não 7
        self.assertEqual(best_score, 8)
        self.assertEqual(motif_score(seqs, best_s, L), 8)

    def test_sequencia_unica(self):
        seqs = ["ATGGTCGC"]
        L = 3
        best_s, best_score = procura_exaustiva_motifs(seqs, L)
        self.assertEqual(best_s, [0])
        self.assertEqual(best_score, L)

    def test_motif_tamanho_total(self):
        seqs = ["ATG", "ATG", "ATG"]
        L = 3
        best_s, best_score = procura_exaustiva_motifs(seqs, L)
        self.assertEqual(best_s, [0, 0, 0])
        self.assertEqual(best_score, 9)

    def test_random_sequences(self):
        t = 5
        n = 10
        L = 3
        random.seed(42)
        seqs = [random_dna_seq(n) for _ in range(t)]
        best_s, best_score = procura_exaustiva_motifs(seqs, L)
        self.assertEqual(best_score, motif_score(seqs, best_s, L))
        self.assertTrue(L <= best_score <= L * t)

if __name__ == '__main__':
    unittest.main()
