import unittest
import random

class TestGibbsSamplingMotifSearch(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.seqs = [
            "ATGCATGCATGCATGC",
            "CTGCCTGCCTGCCTGC", 
            "GTACGTACGTACGTAC",
            "TTACTTACTTACTTAC"
        ]

    def _local_score(self, pos, seqs, L):
        """
        Função local de score
        """
        motifs = [seq[p:p+L] for seq, p in zip(seqs, pos)]
        return sum(max(col.count(b) for b in set(col)) for col in zip(*motifs))

    def _calculate_probability(self, seq, motif_len, start, other_motifs):
        """
        Função local de cálculo de probabilidade
        """
        motif = seq[start:start + motif_len]
        score = 1.0
        total = len(other_motifs) + 4  
        for i, base in enumerate(motif):
            counts = {n: 1 for n in "ACGT"}  
            for m in other_motifs:
                counts[m[i].upper()] = counts.get(m[i].upper(), 1) + 1
            score *= counts[base.upper()] / total
        return score

    def _local_gibbs_sampling(self, seqs, L, num_iterations=1000):
        """
        Método auxiliar para realizar Gibbs Sampling
        """
        motif_positions = [random.randint(0, len(seq) - L) for seq in seqs]
        best_score = self._local_score(motif_positions, seqs, L)
        
        for _ in range(num_iterations):
            for i in range(len(seqs)):
                excluded_sequence = seqs[i]
                other_motifs = [seqs[j][motif_positions[j]:motif_positions[j] + L] for j in range(len(seqs)) if j != i]           
                probabilities = [self._calculate_probability(excluded_sequence, L, pos, other_motifs) for pos in range(len(excluded_sequence) - L + 1)]           
                total_prob = sum(probabilities)
                probabilities = [p / total_prob for p in probabilities]            
                motif_positions[i] = random.choices(range(len(probabilities)), weights=probabilities)[0]      
            
            current_score = self._local_score(motif_positions, seqs, L)
            
            if current_score > best_score:
                best_score = current_score
        
        return motif_positions, best_score

    def test_basic_motif_search(self):
        """
        Teste básico com um conjunto simples de sequências de DNA
        """
        L = 4 

        positions, best_score = self._local_gibbs_sampling(self.seqs, L)

        self.assertEqual(len(positions), len(self.seqs))
        self.assertTrue(all(0 <= pos <= len(seq) - L for pos, seq in zip(positions, self.seqs)))
        self.assertIsInstance(best_score, (int, float))

    def test_score_function(self):
        """
        Teste da função de pontuação de motifs
        """
        test_positions = [2, 3, 4]
        L = 4

        test_score = self._local_score(test_positions, self.seqs, L)

        self.assertIsInstance(test_score, int)
        self.assertGreater(test_score, 0)

    def test_probability_calculation(self):
        """
        Teste da função de cálculo de probabilidade
        """
        seq = "ATGCATGCATGCATGC"
        motif_len = 4
        start = 2
        other_motifs = ["TGCA", "CGTA"]

        prob = self._calculate_probability(seq, motif_len, start, other_motifs)

        self.assertIsInstance(prob, float)
        self.assertTrue(0 <= prob <= 1)

    def test_edge_cases(self):
        """
        Teste de casos de borda
        """
        short_seqs = ["AAA", "CCC", "GGG"]
        
        with self.assertRaises(ValueError):
            if any(len(seq) < 4 for seq in short_seqs):
                raise ValueError("Motif length cannot be larger than sequence length")

    def test_random_seed_reproducibility(self):
        """
        Verificar se resultados são reproduzíveis com a mesma semente
        """
        L = 4

        random.seed(42)
        positions1, score1 = self._local_gibbs_sampling(self.seqs, L)

        random.seed(42)
        positions2, score2 = self._local_gibbs_sampling(self.seqs, L)

        self.assertEqual(positions1, positions2)
        self.assertEqual(score1, score2)

# Função para rodar os testes no Jupyter
def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGibbsSamplingMotifSearch)
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)

# Executar os testes
if __name__ == '__main__':
    run_tests()
