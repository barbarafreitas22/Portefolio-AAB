{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "9317be4a-8bf9-43e2-9d0d-4fe60ef0d37f",
   "metadata": {},
   "outputs": [],
   "source": [
    "class TestGibbsSampling(unittest.TestCase):\n",
    "\n",
    "    def setUp(self):\n",
    "        self.sequences = [\n",
    "            \"ACGTACGTGACG\",\n",
    "            \"ACGTGACGTGAC\",\n",
    "            \"GACGTACGTGAC\"\n",
    "        ]\n",
    "        self.motif_length = 3\n",
    "\n",
    "    def test_score(self):\n",
    "        positions = [0, 0, 0]  # Posições iniciais\n",
    "        result = score(positions, self.sequences, self.motif_length)\n",
    "        self.assertIsInstance(result, int)  # A pontuação deve ser um inteiro\n",
    "\n",
    "    def test_calculate_probability(self):\n",
    "        seq = \"ACGTGACGT\"\n",
    "        motif_len = 3\n",
    "        start = 0\n",
    "        other_motifs = [\"ACG\", \"GAC\", \"TAC\"]\n",
    "        result = calculate_probability(seq, motif_len, start, other_motifs)\n",
    "        self.assertGreaterEqual(result, 0)  # A probabilidade deve ser não negativa\n",
    "\n",
    "    def test_gibbs_sampling_motif_search(self):\n",
    "        positions, best_score = gibbs_sampling_motif_search(self.sequences, self.motif_length, num_iterations=100)\n",
    "        self.assertIsInstance(positions, list)  # Deve retornar uma lista de posições\n",
    "        self.assertEqual(len(positions), len(self.sequences))  # O número de posições deve ser igual ao número de sequências\n",
    "        self.assertIsInstance(best_score, (int, float))  # A pontuação deve ser um número\n",
    "\n",
    "if __name__ == '__main__':\n",
    "    unittest.main()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
