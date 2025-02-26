from MySeq import MySeq
from MyMotifs import MyMotifs
import random

class MotifFinding:
    """
    Class for finding conserved motifs in a set of biological sequences.
    Implements multiple algorithms: exhaustive search, branch and bound, consensus, 
    greedy search, and stochastic approaches (Gibbs sampling).
    """
    
    def __init__(self, size=8, seqs=None):
        """Initialize the MotifFinding object with motif size and optional sequences."""
        self.motifSize = size
        if seqs is not None:
            self.seqs = seqs
            self.alphabet = seqs[0].alfabeto()
        else:
            self.seqs = []
            self.alphabet = None
    
    def __len__(self):
        """Return the number of sequences."""
        return len(self.seqs)
    
    def __getitem__(self, n):
        """Allow indexing to access sequences."""
        return self.seqs[n]
    
    def seqSize(self, i):
        """Return the size of the i-th sequence."""
        return len(self.seqs[i])
    
    def readFile(self, fic, t):
        """Read sequences from a file.
        
        Args:
            fic (str): Path to the file containing sequences.
            t (str): Type of sequences ('dna', 'rna', 'protein').
        """
        self.seqs = []
        with open(fic, "r") as file:
            for s in file:
                seq_str = s.strip().upper()
                if seq_str:  # Skip empty lines
                    self.seqs.append(MySeq(seq_str, t))
        
        if self.seqs:
            self.alphabet = self.seqs[0].alfabeto()
        else:
            raise ValueError("No valid sequences found in the file.")
    
    def createMotifFromIndexes(self, indexes):
        """Create a MyMotifs object from a list of starting positions.
        
        Args:
            indexes (list): List of starting positions for each sequence.
            
        Returns:
            MyMotifs: Object containing aligned subsequences.
        """
        if len(indexes) != len(self.seqs):
            raise ValueError("Number of indexes must match number of sequences")
            
        pseqs = []
        for i, ind in enumerate(indexes):
            if ind < 0 or ind + self.motifSize > self.seqSize(i):
                raise ValueError(f"Invalid index {ind} for sequence {i}")
                
            motif_seq = self.seqs[i][ind:(ind+self.motifSize)]
            pseqs.append(MySeq(motif_seq, self.seqs[i].tipo))
        
        return MyMotifs(pseqs)
    
    # SCORING METHODS
    
    def score(self, indexes):
        """Calculate score based on conservation (sum of maximum counts).
        
        Args:
            indexes (list): List of starting positions.
            
        Returns:
            int: Score value.
        """
        motif = self.createMotifFromIndexes(indexes)
        motif.doCounts()
        mat = motif.counts
        
        score = 0
        for j in range(len(mat[0])):
            maxcol = max(mat[i][j] for i in range(len(mat)))
            score += maxcol
            
        return score
    
    def scoreMult(self, indexes):
        """Calculate score based on probability (product of maximum probabilities).
        
        Args:
            indexes (list): List of starting positions.
            
        Returns:
            float: Score value.
        """
        motif = self.createMotifFromIndexes(indexes)
        motif.createPWM()
        mat = motif.pwm
        
        score = 1.0
        for j in range(len(mat[0])):
            maxcol = max(mat[i][j] for i in range(len(mat)))
            score *= maxcol
            
        return score
    
    def scoreEntropy(self, indexes):
        """Calculate score based on information content (entropy).
        
        Args:
            indexes (list): List of starting positions.
            
        Returns:
            float: Information content value.
        """
        motif = self.createMotifFromIndexes(indexes)
        return motif.informativity()
    
    # EXHAUSTIVE SEARCH
    
    def nextSol(self, indexes):
        """Generate the next combination of indexes for exhaustive search.
        
        Args:
            indexes (list): Current combination of indexes.
            
        Returns:
            list: Next combination or None if no more combinations.
        """
        next_indexes = indexes.copy()
        pos = len(indexes) - 1
        
        while pos >= 0 and indexes[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
            
        if pos < 0:
            return None
        
        next_indexes[pos] = indexes[pos] + 1
        for i in range(pos+1, len(indexes)):
            next_indexes[i] = 0
            
        return next_indexes
    
    def exhaustiveSearch(self, score_func=None):
        """Find the best motif by exhaustive search.
        
        Args:
            score_func: Scoring function to use (defaults to self.score)
            
        Returns:
            list: Best positions for the motif.
        """
        if score_func is None:
            score_func = self.score
            
        best_score = -1
        best_indexes = []
        indexes = [0] * len(self.seqs)
        
        iterations = 0
        while indexes is not None:
            iterations += 1
            if iterations % 10000 == 0:
                print(f"Tested {iterations} combinations")
                
            curr_score = score_func(indexes)
            if curr_score > best_score:
                best_score = curr_score
                best_indexes = indexes.copy()
                
            indexes = self.nextSol(indexes)
        
        return best_indexes, best_score
