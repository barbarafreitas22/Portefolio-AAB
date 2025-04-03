import unittest
import random

def motif_score(seqs, posicoes, L):
     """
    Calcula o score dos motifs extraídos de seqs através das posições 

    Parâmetros:
        seqs (list of str): Lista de sequências de DNA
        posicoes (list of int): Lista de posições iniciais para extrair os motifs
        L (int): Tamanho do motif

    Return:
        int: O score
    """
     motifs = [seq[p:p+L] for seq, p in zip(seqs, posicoes)]
     return sum(max(col.count(base) for base in set(col)) for col in zip(*motifs))

def random_dna_seq(n):
    """
    Gera uma sequência aleatória de DNA com comprimento n

    Parâmetros:
        n (int): Comprimento da sequência a gerar

    Retorna:
        str: Uma sequência aleatória composta pelas letras A, C, G e T
    """
    return ''.join(random.choice("ACGT") for _ in range(n))

def procura_exaustiva_motifs(seqs, L):
    """
    Procura os melhores motifs de um determinado comprimento nas sequências fornecidas,
    ao testar exaustivamente todas as posições possíveis e selecionar a combinação
    com a maior pontuação.

    Parâmetros:
        seqs (list): Lista das sequências biológicas (strings)
        L (int): Comprimento do motif a procurar

    Return:
        Um tuplo com:
            - melhor_p (list): Posições iniciais dos melhores motifs em cada sequência
            - melhor_score (int): Pontuação do melhor conjunto de motifs
    """
    melhor_score, melhor_p = 0, None
    tam_seq = len(seqs[0])
    limite = tam_seq - L + 1 

    def score(pos):
        """
        Calcula a pontuação de conservação para um conjunto de motivos nas posições especificadas
        
        Parâmetros:
           pos (list): Lista de posições iniciais em cada sequência
            
        Return:
           int: Pontuação total de conservação das colunas dos motifs
        """
        motifs = [seq[p:p+L] for seq, p in zip(seqs, pos)]
        return sum(max(col.count(b) for b in set(col)) for col in zip(*motifs))
 
    def procura(i, pos_at):
        """
        Função recursiva que realiza a procura por todas as combinações possíveis
        de posições iniciais nas sequências

        Parâmetros:
            i (int): Índice da sequência atual que está a ser processada
            pos_at (list): Lista de posições iniciais já escolhidas para as sequências anteriores
            
        Return:
            A função não retorna valores, atualiza as variáveis melhor_score e melhor_p
        """
        nonlocal melhor_score, melhor_p
        if i == len(seqs):
            sc = score(pos_at)
            if sc > melhor_score:
                melhor_score, melhor_p = sc, pos_at
            return
        for p in range(limite):
            procura(i + 1, pos_at + [p]) 
    procura(0, [])
    return melhor_p, melhor_score

class TestProcuraExaustivaMotifs(unittest.TestCase):
    def test_exemplo_basico(self):
        """Testa o exemplo fornecido"""
        seqs = "ATGGTCGC TTGTCTGA CCGTAGTA".split()
        L = 3
        melhor_p, melhor_score = procura_exaustiva_motifs(seqs, L)
        self.assertEqual(melhor_score, 8)
        self.assertEqual(motif_score(seqs, melhor_p, L), 8)

    def test_sequencia_unica(self):
        """Testa o caso com uma única sequência."""
        seqs = ["ATGGTCGC"]
        L = 3
        melhor_p, melhor_score = procura_exaustiva_motifs(seqs, L)
        self.assertEqual(melhor_p, [0])
        self.assertEqual(melhor_score, L)

    def test_motif_tamanho_total(self):
        """Testa o caso em que o comprimento da sequência é igual ao comprimento do motif."""
        seqs = ["ATG", "ATG", "ATG"]
        L = 3
        melhor_p, melhor_score = procura_exaustiva_motifs(seqs, L)
        self.assertEqual(melhor_p, [0, 0, 0])
        self.assertEqual(melhor_score, 9)

    def test_random_sequences(self):
        """Testa com sequências geradas aleatoriamente."""
        t = 5
        n = 10
        L = 3
        random.seed(42)
        seqs = [random_dna_seq(n) for _ in range(t)]
        melhor_p, melhor_score = procura_exaustiva_motifs(seqs, L)
        self.assertEqual(melhor_score, motif_score(seqs, melhor_p, L))
        self.assertTrue(L <= melhor_score <= L * t)

if __name__ == '__main__':
    unittest.main()
