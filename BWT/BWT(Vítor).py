
class BWT:
    def __init__(self, seq="", buildsufarray=True):
        self.bwt = self.build_bwt(seq, buildsufarray)

    def set_bwt(self, bw):
        self.bwt = bw

    def build_bwt(self, text, buildsufarray=False):
        ls = []
        for i in range(len(text)):
            ls.append(text[i:] + text[:i])
        ls.sort()
        res = ""
        for j in range(len(text)):
            res += ls[j][-1] 

        if buildsufarray:
            self.sa = []
            for i in range(len(ls)):
                stpos = ls[i].index("$")
                self.sa.append(len(text) - stpos - 1)
        return res

    def inverse_bwt(self):
        n = len(self.bwt)
        table = [""] * n
        for _ in range(n):
            table = sorted([self.bwt[i] + table[i] for i in range(n)])
        for row in table:
            if row.endswith("$"):
                return row
        return ""

    def get_first_col(self):
        firstcol = sorted(self.bwt)
        return firstcol

    def last_to_first(self):
        res = []
        firstcol = self.get_first_col()
        for i in range(len(firstcol)):
            c = self.bwt[i]
            ocs = self.bwt[:i].count(c) + 1
            res.append(self.find_ith_occ(firstcol, c, ocs))
        return res

    def bw_matching(self, patt):
        lf = self.last_to_first()
        res = []
        top = 0
        bottom = len(self.bwt) - 1
        flag = True
        while flag and top <= bottom:
            if patt != "":
                symbol = patt[-1]
                patt = patt[:-1]
                lmat = self.bwt[top:(bottom + 1)]
                if symbol in lmat:
                    topIndex = lmat.index(symbol) + top
                    bottomIndex = bottom - lmat[::-1].index(symbol)
                    top = lf[topIndex]
                    bottom = lf[bottomIndex]
                else:
                    flag = False
            else:
                for i in range(top, bottom + 1):
                    res.append(i)
                flag = False
        return res

    def bw_matching_prefix(self, patt):
        res = []
        match = self.bw_matching(patt)
        for m in match:
            res.append(self.sa[m])
        res.sort()
        return res

    def find_ith_occ(self, l, elem, index):
        j, k = 0, 0
        while k < index and j < len(l):
            if l[j] == elem:
                k += 1
                if k == index:
                    return j
            j += 1
        return -1
    
if __name__ == "__main__":
    dna_seq = "ACGTACGT$"
    bwt_dna = BWT(dna_seq)
    print(f"\nSequência original: {dna_seq}")
    print(f"BWT: {bwt_dna.bwt}")
    
    original = bwt_dna.inverse_bwt()
    print(f"BWT inversa: {original}")
    print(f"Coincide com o original: {original == dna_seq}")
