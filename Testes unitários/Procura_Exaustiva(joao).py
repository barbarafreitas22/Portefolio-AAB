import unittest

class TestMotifFindingSimplified(unittest.TestCase):

    def test_motif_score_identical(self):
        """
        Testa o cálculo do score quando as sequências são idênticas.
        Exemplo: seqs = ["ACGT", "ACGT"], indexes = [0, 0] e L = 2
        Motivos: "AC" e "AC" → Score: 2 (coluna 1) + 2 (coluna 2) = 4.
        """
        sequences = ["ACGT", "ACGT"]
        indexes = [0, 0]
        L = 2
        self.assertEqual(motif_score(sequences, indexes, L), 4)

    def test_motif_score_varied(self):
        """
        Testa o cálculo do score para sequências com motivos diferentes.
        Exemplo: seqs = ["ATCG", "AGCG"], indexes = [0, 1] e L = 3
        Motivos: "ATC" e "GCG"
         - Coluna 1: (A, G) → máximo = 1
         - Coluna 2: (T, C) → máximo = 1
         - Coluna 3: (C, G) → máximo = 1
         Score total: 3.
        """
        sequences = ["ATCG", "AGCG"]
        indexes = [0, 1]
        L = 3
        self.assertEqual(motif_score(sequences, indexes, L), 3)

    def test_next_combination(self):
        """
        Testa se a função next_combination gera a próxima combinação corretamente.
        Para seq_lengths = [8, 8] e L = 3:
         - De [0, 0] deve retornar [0, 1].
         - De [0, 5] (valor máximo para a segunda sequência é 5, pois 8-3=5)
           deve retornar [1, 0].
         - De [5, 5] não há combinação seguinte (retorna None).
        """
        seq_lengths = [8, 8]
        L = 3

        self.assertEqual(next_combination([0, 0], seq_lengths, L), [0, 1])
        self.assertEqual(next_combination([0, 5], seq_lengths, L), [1, 0])
        self.assertIsNone(next_combination([5, 5], seq_lengths, L))

    def test_exhaustive_search(self):
        """
        Testa a busca exaustiva com sequências simples.
        Para seqs = ["ACGT", "ACGT"] e L = 2, o melhor score deve ser 4.
        """
        sequences = ["ACGT", "ACGT"]
        L = 2
        best_indexes, best_score = exhaustive_search(sequences, L)
        self.assertEqual(best_score, 4)
        # Verifica se os índices retornados estão dentro do intervalo válido.
        for idx, seq in zip(best_indexes, sequences):
            self.assertTrue(0 <= idx <= len(seq) - L)

if __name__ == '__main__':
    unittest.main()
