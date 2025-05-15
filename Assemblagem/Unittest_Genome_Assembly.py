
from Genome_Assembly import *
import unittest

class TestGenomeAssembly(unittest.TestCase):
    def test_generate_kmers_basic(self):
        self.assertEqual(
            generate_kmers("ATGC", 3),
            ["ATG", "TGC"]
        )

    def test_generate_kmers_with_repeats(self):
        self.assertEqual(
            generate_kmers("ATGATG", 3),
            ["ATG", "TGA", "GAT", "ATG"]
        )

    def test_debruijn_graph_nodes_and_edges(self):
        kmers = ["GAT", "ATT", "TTA", "TAG"]
        dbg = DeBruijnGraph(kmers)
        expected_nodes = {"GA", "AT", "TT", "TA"}
        self.assertTrue(expected_nodes.issubset(set(dbg.graph.keys())))
        self.assertIn(("AT", 1), dbg.graph["GA"])
        self.assertIn(("TA", 1), dbg.graph["TT"])

    def test_debruijn_eulerian_path_and_assembly(self):
        kmers = ["CTTA", "ACCA", "TACC", "GGCT", "GCTT", "TTAC"]
        dbg = DeBruijnGraph(kmers)
        path = dbg.find_eulerian_path()
        if path is not None:
            seq = dbg.assemble_sequence(path)
            for kmer in kmers:
                self.assertIn(kmer, seq)
        else:
            self.assertIsNone(path)

    def test_debruijn_no_eulerian_path(self):
        kmers = ["AAA", "CCC", "GGG"]
        dbg = DeBruijnGraph(kmers)
        path = dbg.find_eulerian_path()
        self.assertIsNone(path)

    def test_debruijn_assemble_sequence_none(self):
        dbg = DeBruijnGraph([])
        self.assertIsNone(dbg.assemble_sequence(None))

    def test_overlap_graph_hamiltonian_and_assembly(self):
        frags = ["ATTA", "TTAC", "TACC", "ACCG"]
        og = OverlapGraph(frags)
        path = og.find_hamiltonian_path()
        if path is not None:
            seq = og.assemble_sequence(path)
            for frag in frags:
                self.assertIn(frag, seq)
        else:
            self.assertIsNone(path)

    def test_overlap_graph_no_hamiltonian(self):
        frags = ["AAA", "CCC", "GGG"]
        og = OverlapGraph(frags)
        self.assertIsNone(og.find_hamiltonian_path())

    def test_overlap_assemble_sequence_none(self):
        og = OverlapGraph([])
        self.assertIsNone(og.assemble_sequence(None))

if __name__ == '__main__':
    unittest.main()