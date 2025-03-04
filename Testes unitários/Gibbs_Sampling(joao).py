import random
import unittest

def score(posicoes, sequencias, L):
    """
    Calcula a pontuação de conservação para um conjunto de motivos
    
    Parâmetros:
        posicoes (list): Lista de posições iniciais em cada sequência
        sequencias (list): Lista de sequências biológicas
        L (int): Comprimento do motif
        
    Return:
        int: Pontuação total das colunas conservadas
    """
    motifs = [seq[p:p+L] for seq, p in zip(sequencias, posicoes)]
    return sum(max(col.count(b) for b in set(col)) for col in zip(*motifs))

def calcula_probabilidade(seq, L, pi, outros_motifs):
    """
    Calcula a probabilidade do motif a partir da posição inicial na sequência

    Parâmetros:
        seq (str): A sequência onde se procura o motif
        L (int): Comprimento do motif
        pi (int): Posição de início do motif na sequência.
        outros_motifs (list[str]): Lista dos motifs das outras sequências, para a contagem das bases.

    Return:
        float: A probabilidade do motif na posição inicial
    """
    motif = seq[pi:pi + L]
    prob = 1.0
    total = len(outros_motifs) + 4  

    for i, base in enumerate(motif):
        counts = {n: 1 for n in "ACGT"}
        for m in outros_motifs:
            counts[m[i].upper()] = counts.get(m[i].upper(), 1) + 1
        prob *= counts[base.upper()] / total

    return prob


def gibbs_sampling(sequences, L, num_it=1000):
    """
    Realiza a procura de motifs nas sequências através do algoritmo de Gibbs Sampling

    Parâmetros:
        sequences (list[str]): Lista de sequências onde se pretende encontrar os motifs
        L (int): Comprimento do motif
        num_it (int, opcional): Número de iterações para executar o algoritmo

    Return:
        Um tuplo com:
            - list[int]: Lista com as posições de início dos motifs em cada sequência.
            - int: O score final 
    """
    motif_pos = [random.randint(0, len(seq) - L) for seq in sequences]
    m_score_val = score(motif_pos, sequences, L)
    m_positions = motif_pos.copy()

    for _ in range(num_it):
        for i in range(len(sequences)):
            exc_seq = sequences[i]
            outros_motifs = [
                sequences[j][motif_pos[j]:motif_pos[j] + L] 
                for j in range(len(sequences)) if j != i
            ]

            probabilidades = [
                calcula_probabilidade(exc_seq, L, pos, outros_motifs)
                for pos in range(len(exc_seq) - L + 1)
            ]
            total_prob = sum(probabilidades)
            if total_prob == 0:
                probabilidades = [1 / len(probabilidades)] * len(probabilidades)
            else:
                probabilidades = [p / total_prob for p in probabilidades]

            motif_pos[i] = random.choices(range(len(probabilidades)), weights=probabilidades)[0]

        score_atual = score(motif_pos, sequences, L)
        if score_atual > m_score_val:
            m_score_val = score_atual
            m_positions = motif_pos.copy()

    return m_positions, m_score_val


if __name__ == "__main__":
    sequences = "ATGGTCGC TTGTCTGA CCGTAGTA".split()
    L = 3

    gibbs_pos, gibbs_m_score = gibbs_sampling(sequences, L, num_it=1000)
    print("Posições:", gibbs_pos, "Score:", gibbs_m_score)


class TestMotifSearch(unittest.TestCase):

    def test_score_identico(self):
        """Testa a função score para o caso com sequências idênticas"""
        sequencias = ["ACGT", "ACGT"]
        posicoes = [0, 0]
        L = 2
        score_esperado = 4
        self.assertEqual(score(posicoes, sequencias, L), score_esperado)

    def test_score_posicoes_diferentes(self):
        """Testa a função score com posições iniciais diferentes"""
        sequencias = ["ATCG", "AGCG"]
        posicoes = [0, 1]
        L = 3
        score_esperado = 3
        self.assertEqual(score(posicoes, sequencias, L), score_esperado)

    def test_calcula_probabilidade(self):
        """Testa a função calcula_probabilidade com um exemplo"""
        seq = "ACGT"
        L = 2
        pi = 0
        outros_motifs = ["AC", "AA"]
        score_esperado = 0.5 * (2/6)
        resultado = calcula_probabilidade(seq, L, pi, outros_motifs)
        self.assertAlmostEqual(resultado, score_esperado, places=5)

    def test_gibbs_sampling_output_valido(self):
        """Testa se o Gibbs Sampling retorna posições e score válidos"""
        random.seed(42)
        sequencias = ["ATGGTCGC", "TTGTCTGA", "CCGTAGTA"]
        L = 3
        posicoes, score_final = gibbs_sampling(sequencias, L, num_it=100)
        
        self.assertEqual(len(posicoes), len(sequencias))
        for pos, seq in zip(posicoes, sequencias):
            self.assertTrue(0 <= pos <= len(seq) - L)
        self.assertIsInstance(score_final, int)
    
    def test_sequencia_vazia(self):
      """Testa o comportamento com uma sequência vazia"""
      sequencias = ["ATGC", "", "TGCA"]
      L = 2
      with self.assertRaises(ValueError):
          gibbs_sampling(sequencias, L)

if __name__ == '__main__':
    unittest.main()
