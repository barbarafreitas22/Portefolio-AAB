class BoyerMoore:
    
    def __init__(self, alphabet, pattern):
        self.alphabet = alphabet
        self.pattern = pattern
        self.preprocess()                #sempre que damos alphabet e pattern corre esta função

    def preprocess(self):
        self.process_bcr()
        self.process_gsr()
        
    def process_bcr(self):
        """Implementação do pre-processamento do bad caracter rule"""
        self.occ = {}#abre o {}
        for s in self.alphabet:#add ao {} todos os caracteres do alfabeto e atribui o valor de -1
            self.occ[s] = -1#atribuição do -1
        for i in range(len(self.pattern)):#altera o que esta no {}, vai definir como valores do dicionario as pocioes mais à direita onde os simbolos ocorrem
            self.occ[self.pattern[i]] = i#altera no {} o valor da letras do alphabet para i que é a
            #ou
            # c = self.pattern
            #self.occ[c] = i
        print(self.occ)

    def process_gsr(self):
        """Implementação do pre-processamento do good suffix rule"""
        self.f = [0] * (len(self.pattern) + 1) #abre uma lista com 0 com o tamanho do padrão MISMATCH
        self.s = [0] * (len(self.pattern) + 1) #MATCH
        i = len(self.pattern) #tamanho do padrão
        j = len(self.pattern) + 1#define o i e j pelo comprimento do padrão
        self.f[i] = j#aletra o valor do ultimo elemento da lista self.f para j, vai seo o ultimo elemento do padrão
        print(self.f)
        while i > 0:#enquanto que a posição no padrão > 0, da direita para a esquerda
            while j <= len(self.pattern) and self.pattern[i - 1] != self.pattern[j - 1]: #enquanto que o j for menor que o i
                #define a lista s que é o nº de casas que pode avançar na seq caso o padrão não encaixe
                if self.s[j] == 0:# se a a posição j == 0, é a última pos
                    self.s[j] = j - i #a posição j vao tomar o valor de j - i
                j = self.f[j] #j = à posição self.f[j]
            i = i - 1
            j = j - 1
            self.f[i] = j#a lista f na posição i vao tomar o valor de j
        j = self.f[0] # j = ao caracter na psoiçao 0 da lista f
        for i in range(0, len(self.pattern)):#quando i está como 0, vai alterar para o valor de j mais recente, que significa passar o nº possível de posições à frente ca cadeia sem comprometer a procura no padrao
            if self.s[i] == 0:
                self.s[i] = j
            if i == j:
                j = self.f[j]
        print(self.f)
        print(self.s)

    def search_pattern(self, text):
        res = []
        i = 0 #posição i na sequencia, POSIÇAO NO TEXTO
        while i <= (len(text) - len(self.pattern)):#para começar a correr a seq
            j = (len(self.pattern) - 1) #posicao no padrao vai ser = ao tamanho do padrão -1
            while j >= 0 and self.pattern[j] == text[j + i]: #continuar a correr enquanto esta a dar match
                j -= 1
            if j < 0:
                res.append(i) #ocorreu um padrão inteiro
                i = i +self.s[0] #avança para i "casas" para a frente uma vez que o padrao já foi encontrado uma vez
            else:
                c = text[i + j]
                i += max(self.s[j + 1], j - self.occ[c]) #o +1 no j+1 é por causa da casa vazia no inicio do bcr
                #avança dependendo
        return res



def test():
    bm = BoyerMoore("ACTG", "ACCA")
    print(bm.search_pattern("ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC"))


if __name__ == "__main__":
    test()


#result: [5, 13, 23, 37]
