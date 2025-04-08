
class BWT:
    def __init__(self, seq="", constroi_array_sufixos=True):
        """
        Inicializa uma instância da classe BWT.

        Cria a transformação de Burrows-Wheeler (BWT) a partir da sequência fornecida e,
        opcionalmente, constroi o array de sufixos.

        Args:
            seq (str, optional): Sequência de caracteres a processar. Por defeito, é uma string vazia.
            constroi_array_sufixos (bool, optional): Se True, também constrói o array de sufixos. Por defeito é True.
        """
        self.bwt = self.constroi_bwt(seq, constroi_array_sufixos)            # Constroi a BWT e armazena no atributo self.bwt.

    def define_bwt(self, bw):
        """
        Define manualmente a BWT.

        Args:
            bw (str): String que representa a BWT a definir.
        """
        self.bwt = bw                                                        # Atualiza o atributo self.bwt com a nova string informada.

    def constroi_bwt(self, texto, constroi_array_sufixos=False):
        """
        Constrói a BWT a partir do texto fornecido.

        Gera todas as rotações do texto, ordena-as e constrói a BWT a partir do último
        caractere de cada linha ordenada. Se solicitado, constrói também o array de sufixos.

        Args:
            texto (str): Texto de entrada.
            constroi_array_sufixos (bool, optional): Se True, o array de sufixos é também construído. Por defeito é False.

        Returns:
            str: A BWT correspondente à sequência de entrada.
        """
        lista = []                                           # Lista para armazenar todas as rotações do texto.
        for i in range(len(texto)):
            lista.append(texto[i:] + texto[:i])              # Para cada posição, cria uma rotação começando do caractere i.
        lista.sort()                                         # Ordena lexicograficamente todas as rotações.
        resultado = ""
        for j in range(len(texto)):                          # Constrói a BWT recolhendo o último caractere de cada rotação ordenada.
            resultado += lista[j][-1]

        if constroi_array_sufixos:
            self.sa = []                                     # Array de sufixos a ser construído.
            for i in range(len(lista)):
                pos_inicial = lista[i].index("$")            # Localiza a posição do caractere especial '$' na rotação.
                self.sa.append(len(texto) - pos_inicial - 1) # Calcula a posição real do sufixo no texto original.
        return resultado

    def inversa_bwt(self):
        """
        Inverte a BWT para recuperar o texto original.

        Reconstrói o texto original a partir da BWT, usando o método da tabela iterativa.

        Returns:
            str: O texto original se a inversão for bem-sucedida; caso contrário, retorna uma string vazia.
        """
        n = len(self.bwt)                                                     # Número de linhas na tabela.
        tabela = [""] * n                                                     # Inicializa a tabela com strings vazias.
        for _ in range(n):
            tabela = sorted([self.bwt[i] + tabela[i] for i in range(n)])      # Em cada iteração, concatena o caractere da BWT à esquerda de cada linha da tabela.
        for linha in tabela:                                                  # Cada iteração aproxima a tabela da reconstrução completa do texto original.
            if linha.endswith("$"):                                           # Procura a linha que termina com o caractere especial '$'.
                return linha
        return ""                                                             # Retorna vazio se não encontrar o texto original.

    def obtem_primeira_coluna(self):
        """
        Obtém a primeira coluna da matriz da BWT.

        A primeira coluna é a versão ordenada da BWT.

        Returns:
            list: Lista que representa a primeira coluna da matriz BWT.
        """
        primeira_coluna = sorted(self.bwt)                                    # Ordena os caracteres da BWT para obter a primeira coluna.
        return primeira_coluna

    def ultimo_para_primeiro(self):
        """
        Cria o mapeamento da última para a primeira coluna da BWT.

        Este método gera uma lista de índices correspondentes na primeira coluna (ordenada)
        para cada posição na BWT.

        Returns:
            list: Lista com os índices correspondentes na primeira coluna para cada caractere da BWT.
        """
        resultado = []                                                                                 # Lista para armazenar os índices de mapeamento.
        primeira_coluna = self.obtem_primeira_coluna()                                                 # Obtém a primeira coluna.
        for i in range(len(primeira_coluna)):
            c = self.bwt[i]                                                                            # Para cada índice na BWT, determina o caractere correspondente.
            ocorrencias = self.bwt[:i].count(c) + 1                                                    # Conta quantas vezes o caractere aparece até à posição i.

            resultado.append(self.encontra_iesima_ocorrencia(primeira_coluna, c, ocorrencias))         # Encontra a posição da ocorrência correspondente na primeira coluna.
        return resultado

    def correspondencia_bw(self, padrao):
        """
        Realiza a procura backward search para encontrar o padrão na BWT.

        Utiliza o mapeamento 'último para o primeiro' para efetuar a procura do padrão 
        de forma eficiente na BWT.

        Args:
            padrao (str): O padrão a ser procurado.

        Returns:
            list: Lista de índices da BWT onde o padrão é encontrado.
        """
        lf = self.ultimo_para_primeiro()                                            # Obtém o mapeamento de última para a primeira coluna.
        resultado = []                                                              # Lista para armazenar os índices onde o padrão é encontrado.
        topo = 0                                                                    # Limite superior da procura.
        fundo = len(self.bwt) - 1                                                   # Limite inferior da procura.
        continuar = True                                                            # Flag de controlo do ciclo.
        while continuar and topo <= fundo:
            if padrao != "":
                simbolo = padrao[-1]                                                # Seleciona o último caractere do padrão.
                padrao = padrao[:-1]                                                # Remove o último caractere do padrão.
                sublista = self.bwt[topo:(fundo + 1)]                               # Extrai a sublista da BWT entre os índices topo e fundo.
                if simbolo in sublista:
                    indice_topo = sublista.index(simbolo) + topo                    # Determina a nova posição superior para a procura.
                    indice_fundo = fundo - sublista[::-1].index(simbolo)            # Determina a nova posição inferior para a procura.
                    topo = lf[indice_topo]
                    fundo = lf[indice_fundo]
                else:
                    continuar = False                                               # Se o símbolo não estiver na sublista, o padrão não existe.
            else:
                for i in range(topo, fundo + 1):                                    # Se o padrão estiver vazio, adiciona todos os índices do intervalo atual.
                    resultado.append(i)
                continuar = False
        return resultado

    def correspondencia_bw_prefixo(self, padrao):
        """
        Realiza a correspondência backward search e retorna as posições relativas no texto original.

        O método utiliza o array de sufixos (sa) para converter os índices da BWT nas posições
        correspondentes do texto original.

        Args:
            padrao (str): O padrão a ser procurado.

        Returns:
            list: Lista ordenada com as posições correspondentes no texto original.
        """
        resultado = []                                                 # Lista para armazenar as posições no texto original.
        correspondencias = self.correspondencia_bw(padrao)             # Índices da BWT que correspondem ao padrão.
        for m in correspondencias:
            resultado.append(self.sa[m])                               # Converte cada índice da BWT para a posição correspondente no array de sufixos.
        resultado.sort()                                               # Ordena as posições.
        return resultado

    def encontra_iesima_ocorrencia(self, lista, elemento, indice):
        """
        Encontra a i-ésima ocorrência de um elemento numa lista.

        Percorre a lista procurando pelo elemento e retorna a posição da ocorrência
        especificada.

        Args:
            lista (list): Lista onde o elemento será procurado.
            elemento: Elemento a procurar.
            indice (int): Número da ocorrência desejada (1ª, 2ª, etc.).

        Returns:
            int: O índice na lista da i-ésima ocorrência ou -1 se não for encontrada.
        """
        j, contagem = 0, 0                                         # Inicializa variáveis de controlo.
        while contagem < indice and j < len(lista):
            if lista[j] == elemento:
                contagem += 1                                      # Incrementa a contagem quando encontra o elemento.
                if contagem == indice:
                    return j                                       # Retorna o índice quando atinge a ocorrência desejada.
            j += 1                                                 # Avança para o próximo elemento na lista.
        return -1                                                  # Retorna -1 caso a ocorrência desejada não seja encontrada.

if __name__ == "__main__":
    seq_dna = "ACGTACGT$"
    bwt_dna = BWT(seq_dna)
    print(f"\nSequência original: {seq_dna}")
    print(f"BWT: {bwt_dna.bwt}")
    
    original = bwt_dna.inversa_bwt()
    print(f"BWT inversa: {original}")
    print(f"Coincide com o original: {original == seq_dna}")
