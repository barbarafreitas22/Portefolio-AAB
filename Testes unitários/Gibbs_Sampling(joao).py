import unittest
import random
from wd import score, calculate_probability, gibbs_sampling_motif_search
# Caso o código esteja no mesmo arquivo, remova a linha acima e certifique-se de que as funções estejam disponíveis.

class TestMotifSearch(unittest.TestCase):

    def test_score_basic(self):
        """
        Testa a função score para o caso simples em que ambas as sequências possuem o mesmo motivo.
        Exemplo:
            Sequências: ["ACGT", "ACGT"]
            Posições: [0, 0]
            L = 2  --> motivos: "AC" e "AC"
            Para cada coluna, a base mais frequente ocorre 2 vezes.
            Score esperado: 2 + 2 = 4
        """
        sequences = ["ACGT", "ACGT"]
        positions = [0, 0]
        L = 2
        expected = 4
        self.assertEqual(score(positions, sequences, L), expected)

    def test_score_different_positions(self):
        """
        Testa a função score com posições diferentes.
        Exemplo:
            Sequências: ["ATCG", "AGCG"]
            Posições: [0, 1]
            Motivos: "ATC" (da primeira sequência) e "GCG" (da segunda)
            Colunas:
                (A, G) -> máximo = 1
                (T, C) -> máximo = 1
                (C, G) -> máximo = 1
            Score esperado: 1 + 1 + 1 = 3
        """
        sequences = ["ATCG", "AGCG"]
        positions = [0, 1]
        L = 3
        expected = 3
        self.assertEqual(score(positions, sequences, L), expected)

    def test_calculate_probability(self):
        """
        Testa calculate_probability usando um exemplo conhecido.
        Exemplo:
            seq = "ACGT", motif_len = 2, start = 0, other_motifs = ["AC", "AA"]
            Para o primeiro caractere (i=0):
                - Contagens iniciais: {"A":1, "C":1, "G":1, "T":1}
                - Outras seqs: para ambas, o caractere na posição 0 é "A":
                  -> counts["A"] = 1 + 2 = 3
                - Total = len(other_motifs) + 4 = 2 + 4 = 6
                - Probabilidade = 3/6 = 0.5
            Para o segundo caractere (i=1), letra "C":
                - Contagens iniciais: {"A":1, "C":1, "G":1, "T":1}
                - Outras seqs: primeira tem "C" (counts["C"] passa a 2) e a segunda tem "A" (não afeta "C")
                - Probabilidade = 2/6 ≈ 0.33333
            Probabilidade total = 0.5 * (2/6) ≈ 0.16667
        """
        seq = "ACGT"
        motif_len = 2
        start = 0
        other_motifs = ["AC", "AA"]
        expected = 0.5 * (2/6)
        result = calculate_probability(seq, motif_len, start, other_motifs)
        self.assertAlmostEqual(result, expected, places=5)

    def test_gibbs_sampling_valid_output(self):
        """
        Testa que a função gibbs_sampling_motif_search retorne posições válidas.
        São verificadas:
          - A quantidade de posições é igual ao número de sequências.
          - Cada posição está dentro do intervalo válido para a respectiva sequência.
          - O score retornado é do tipo inteiro.
        """
        random.seed(42)  # Garante reprodutibilidade
        sequences = ["ATGGTCGC", "TTGTCTGA", "CCGTAGTA"]
        motif_length = 3
        positions, best_score_val = gibbs_sampling_motif_search(sequences, motif_length, num_iterations=100)
        
        # Verifica se a quantidade de posições é igual ao número de sequências
        self.assertEqual(len(positions), len(sequences))
        # Verifica se cada posição está dentro do intervalo permitido
        for pos, seq in zip(positions, sequences):
            self.assertGreaterEqual(pos, 0)
            self.assertLessEqual(pos, len(seq) - motif_length)
        # Verifica se o score é um número inteiro
        self.assertIsInstance(best_score_val, int)

if __name__ == '__main__':
    unittest.main() 
