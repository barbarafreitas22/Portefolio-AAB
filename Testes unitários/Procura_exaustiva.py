import random
import unittest

def random_dna_seq(n):
    """Gera uma sequência aleatória de DNA de tamanho n."""
    return ''.join(random.choice("ACGT") for _ in range(n))

class TestProcuraExaustivaMotifs(unittest.TestCase):
    def test_exemplo_basico(self):
        # Exemplo com 3 sequências e motif de tamanho 3
        seqs = "ATGGTCGC TTGTCTGA CCGTAGTA".split()
        L = 3
        best_s, best_score = ProcuraExaustivaMotifs(seqs, L)
        # Para este exemplo, espera-se que a melhor solução seja [1, 1, 1] com score 7.
        self.assertEqual(best_s, [1, 1, 1])
        self.assertEqual(best_score, 7)
    
    def test_sequencia_unica(self):
        # Se houver apenas uma sequência, há somente uma opção: [0]
        seqs = ["ATGGTCGC"]
        L = 3
        best_s, best_score = ProcuraExaustivaMotifs(seqs, L)
        self.assertEqual(best_s, [0])
        # O score será igual a L, pois cada coluna terá uma ocorrência.
        self.assertEqual(best_score, L)
    
    def test_motif_tamanho_total(self):
        # Se o motif ocupa toda a sequência, a única opção é [0,...,0]
        seqs = ["ATG", "ATG", "ATG"]
        L = 3
        best_s, best_score = ProcuraExaustivaMotifs(seqs, L)
        self.assertEqual(best_s, [0, 0, 0])
        # Cada coluna tem 3 ocorrências iguais: score = 3+3+3 = 9.
        self.assertEqual(best_score, 9)
    
    def test_random_sequences(self):
        # Gerador aleatório de sequências de DNA
        t = 5    # número de sequências
        n = 10   # tamanho de cada sequência
        seqs = [random_dna_seq(n) for _ in range(t)]
        L = 3
        best_s, best_score = ProcuraExaustivaMotifs(seqs, L)
        # Verifica se o score calculado pela função de procura bate com o da função motif_score
        self.assertEqual(best_score, motif_score(seqs, best_s, L))
        # O score deve estar entre L (mínimo: cada coluna tem 1 ocorrência) e L*t (máximo: todas iguais)
        self.assertTrue(L <= best_score <= L * t)

class TestMotifScore(unittest.TestCase):
    def test_score_conhecido(self):
        # Testa a função motif_score com um caso conhecido
        seqs = ["ATG", "ATG", "ATG"]
        s = [0, 0, 0]
        L = 3
        # Cada coluna terá 3 ocorrências iguais: score = 3+3+3 = 9.
        self.assertEqual(motif_score(seqs, s, L), 9)
    
    def test_score_variante(self):
        # Testa outro caso conhecido
        seqs = ["TGG", "TGT", "CGT"]
        s = [0, 0, 0]
        L = 3
        # Colunas:
        # Col0: T, T, C => max = 2; Col1: G, G, G => max = 3; Col2: G, T, T => max = 2; Total = 7.
        self.assertEqual(motif_score(seqs, s, L), 7)

if __name__ == '__main__':
    unittest.main()
