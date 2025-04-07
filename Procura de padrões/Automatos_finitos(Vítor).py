
class Automata:
    
    def __init__(self, alphabet, pattern):
        self.numstates = len(pattern) + 1
        self.alphabet = alphabet
        self.transitionTable = {}
        self.buildTransitionTable(pattern)        
    
    def buildTransitionTable(self, pattern): 
        for q in range(self.numstates):
            for a in self.alphabet:
                prefixo = pattern[:q] + a 
                self.transitionTable[(q,a)] = overlap(prefixo, pattern) 
       
    def printAutomata(self):
        print("States:", self.numstates)
        print("Alphabet:", self.alphabet)
        print("Transition table:")
        for k in self.transitionTable.keys():
            print(k[0], ",", k[1], " -> ", self.transitionTable[k])
         
    def nextState(self, current, symbol):
        return self.transitionTable[(current, symbol)]

    def applySeq(self, seq):
        q = 0 
        res = [q]
        for c in seq:
            q = self.nextState(q, c) 
            res.append(q)
        return res
        
    def occurencesPattern(self, text):
        q = 0 
        res = []
        for aa in range(len(text)):
            q = self.nextState(q, text[aa])
            if q == self.numstates - 1:
                res.append(aa - self.numstates + 2)
        return res

def overlap(s1, s2):
    maxov = min(len(s1), len(s2))
    for i in range(maxov, 0, -1):
        if s1[-i:] == s2[:i]:
            return i
    return 0

if __name__ == "__main__":
    alphabet = ['A', 'C', 'G', 'T']
    pattern = "ACGT"
    text = "GACGTACACGTACGT"

    automato = Automata(alphabet, pattern)
    automato.printAutomata()

    print("\nTransições para a sequência:", text)
    print(automato.applySeq(text))

    print("\nOcorrências do padrão:")
    print(automato.occurencesPattern(text))
