class BoyerMoore:
    """
    Implementation of the Boyer-Moore string search algorithm.
    """

    def __init__(self, alphabet, pattern):
        """
        Initialize the Boyer-Moore algorithm with the given alphabet and pattern.

        Parameters
        ----------
        alphabet : str
            The alphabet used in the text and pattern.
        pattern : str
            The pattern to search for in the text.
        """
        self.alphabet = alphabet
        self.pattern = pattern
        self.occ = {}
        self.s = []
        self.f = []
        self._preprocess()

    def _preprocess(self):
        """
        Preprocess the pattern to compute the bad character rule and good suffix rule.
        """
        self._process_bad_character_rule()
        self._process_good_suffix_rule()

    def _process_bad_character_rule(self):
        """
        Preprocess the pattern for the bad character rule.
        """
        self.occ = {char: -1 for char in self.alphabet}
        for i, char in enumerate(self.pattern):
            self.occ[char] = i

    def _process_good_suffix_rule(self):
        """
        Preprocess the pattern for the good suffix rule.
        """
        m = len(self.pattern)
        self.f = [0] * (m + 1)
        self.s = [0] * (m + 1)

        i = m
        j = m + 1
        self.f[i] = j

        while i > 0:
            while j <= m and self.pattern[i - 1] != self.pattern[j - 1]:
                if self.s[j] == 0:
                    self.s[j] = j - i
                j = self.f[j]
            i -= 1
            j -= 1
            self.f[i] = j

        j = self.f[0]
        for i in range(m):
            if self.s[i] == 0:
                self.s[i] = j
            if i == j:
                j = self.f[j]

    def search(self, text):
        """
        Search for occurrences of the pattern in the given text.

        Parameters
        ----------
        text : str
            The text to search for the pattern.

        Returns
        -------
        list[int]
            A list of starting positions where the pattern occurs in the text.
        """
        m = len(self.pattern)
        n = len(text)
        res = []

        # Caso especial: padrão vazio
        if m == 0:
            return []

        # Caso especial: texto vazio
        if n == 0:
            return []

        # Caso especial: padrão maior que o texto
        if m > n:
            return []

        i = 0
        while i <= n - m:
            j = m - 1
            while j >= 0 and self.pattern[j] == text[i + j]:
                j -= 1
            if j < 0:
                res.append(i)
                i += self.s[0] if m > 1 else 1  # Para padrões de comprimento 1, avance uma posição
            else:
                char_shift = j - self.occ.get(text[i + j], -1)
                suffix_shift = self.s[j + 1]
                i += max(1, suffix_shift, char_shift)  # Garante que avançamos pelo menos 1

        return res


# Example Usage
if __name__ == "__main__":
    bm = BoyerMoore("ACTG", "ACCA")
    text = "ATAGAACCAATGAACCATGATGAACCATGGATACCCAACCACC"
    occurrences = bm.search(text)
    print("Pattern found at positions:", occurrences)
