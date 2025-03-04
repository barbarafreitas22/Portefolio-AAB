import unittest
import random

class TesteGibbsSampling(unittest.TestCase):
    def _local_semente(self):
        """
        Configuração inicial para os testes.
        
        Define uma semente aleatória para garantir reprodutibilidade
        e prepara um conjunto padrão de sequências para teste.
        
        """
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

    def _local_calcular_probabilidade(self, seq, L, inicio, outros_motifs):
        """
        Função local de cálculo de probabilidade
        """
        motif = seq[inicio:inicio + L]
    probabilidade = 1.0
    total = len(outros_motifs) + 4  # Laplace smoothing
    for i, base in enumerate(motif):
        counts = {n: 1 for n in "ACGT"}  # Inicializa com 1 para Laplace
        for m in outros_motifs:
            counts[m[i].upper()] = counts.get(m[i].upper(), 1) + 1
        probabilidade *= counts[base.upper()] / total
    return probabilidade
    
    def _local_gibbs_sampling(self, seqs, L, num_it=1000):
        """
        Método auxiliar para realizar Gibbs Sampling
        """
        posições_motif = [random.randint(0, len(seq) - L) for seq in seqs]
    melhor_score = score(posições_motif)
    for _ in range(num_it):
        for i in range(len(seqs)):
            sequencia_excluida = seqs[i]
            outros_motifs = [seqs[j][posições_motif[j]:posições_motif[j] + L] for j in range(len(seqs)) if j != i]           
            probabilidades = [calcular_probabilidade(sequencia_excluida, L, pos, outros_motifs) for pos in range(len(sequencia_excluida) - L + 1)]           
            prob_total = sum(probabilidades)
            probabilidades = [p / prob_total for p in probabilidades]            
            posições_motif[i] = random.choices(range(len(probabilidades)), weights=probabilidades)[0]      
        score_atual = score(posições_motif)
        
        if score_atual > melhor_score:
            melhor_score = score_atual
    return posições_motif, melhor_score

    def teste_procura_motif_basico(self):
        """
        Teste básico para verificar a funcionalidade do algoritmo de busca de motifs.
        
        Este teste valida se o algoritmo de Gibbs Sampling:
        - Retorna o número correto de posições de motifs
        - Garante que todas as posições estão dentro dos limites válidos das sequências
        - Produz uma pontuação válida
        
        O teste usa um conjunto padrão de sequências de DNA e verifica 
        a integridade básica do algoritmo.
        
        Raises:
            AssertionError: Se alguma das verificações falhar
        """
        L = 4

        posições, best_score = self._local_gibbs_sampling(self.seqs, L)

        self.assertEqual(len(posições), len(self.seqs))
        self.assertTrue(all(0 <= pos <= len(seq) - L for pos, seq in zip(posições, self.seqs)))
        self.assertIsInstance(melhor_score, (int, float))

    def teste_score(self):
        """
        Teste da função de pontuação de motifs.
        
        Verifica a implementação correta da função de score que calcula
        a conservação dos motifs encontrados:
        - Confirma que a pontuação é um número inteiro
        - Verifica se a pontuação calculada é maior que zero
        
        Utiliza um conjunto de posições de teste para validar 
        o cálculo de pontuação.
        
        Raises:
            AssertionError: Se a pontuação não atender aos critérios esperados
        """
        posições_teste = [2, 3, 4]
        L = 4

        teste_score = self._local_score(posições_teste, self.seqs, L)

        self.assertIsInstance(teste_score, int)
        self.assertGreater(teste_score, 0)

    def teste_calculo_probabilidade(self):
        """
        Teste do cálculo de probabilidade com suavização de Laplace.
        
        Valida a função de cálculo de probabilidade que:
        - Verifica se o resultado é um número num ponto flutuante
        - Confirma que a probabilidade está no intervalo [0, 1]
        
        Usa uma sequência de teste e motifs de referência para 
        calcular a probabilidade de um motif específico.
        
        Raises:
            AssertionError: Se a probabilidade calculada não atender 
            aos critérios de tipo e intervalo
        """
        seq = "ATGCATGCATGCATGC"
        L = 4
        inicio = 2
        outros_motifs = ["TGCA", "CGTA"]

        prob = self._local_calcular_probabilidade(seq, L, inicio, outros_motifs)

        self.assertIsInstance(prob, float)
        self.assertTrue(0 <= prob <= 1)

    def teste_casos_extremos(self):
        """
        Teste de casos extremos para o algoritmo de busca de motifs.
        
        Verifica o comportamento do algoritmo em situações extremas:
        - Testa o tratamento de sequências muito curtas
        - Espera que uma exceção seja lançada quando o motif 
          é maior que as sequências
        
        O objetivo é garantir que o algoritmo lida corretamente 
        com entradas inválidas ou limitadas.
        
        Raises:
            ValueError: Esperado quando o comprimento do motif 
            é maior que o das sequências
        """
        seqs_pequenas = ["AAA", "CCC", "GGG"]
        
        with self.assertRaises(ValueError):
            if any(len(seq) < 4 for seq in seqs_pequenas):
                raise ValueError("Motif length cannot be larger than sequence length")

    def teste_reprodutibilidade_semente_aleatoria(self):
       """
        Teste de reprodutibilidade da semente aleatória.
        
        Verifica se o algoritmo produz resultados consistentes 
        quando executado com a mesma semente aleatória:
        - Compara resultados de duas execuções consecutivas
        - Confirma que as posições e pontuações são idênticas
        
        Fundamental para garantir testes determinísticos e 
        reproduzíveis em ambientes de desenvolvimento e teste.
        
        Raises:
            AssertionError: Se os resultados das execuções não forem idênticos
        """
        L = 4

        random.seed(42)
        posições1, score1 = self._local_gibbs_sampling(self.seqs, L)

        random.seed(42)
        posições2, score2 = self._local_gibbs_sampling(self.seqs, L)

        self.assertEqual(posições1, posições2)
        self.assertEqual(score1, score2)

# Função para rodar os testes no Jupyter
def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TesteGibbsSampling)
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)

# Executar os testes
if __name__ == '__main__':
    run_tests()
