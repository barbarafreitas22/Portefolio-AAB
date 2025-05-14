
import unittest
from unittest.mock import mock_open, patch
from Redes_Metabolicas import *

class TestMetabolicNetwork(unittest.TestCase):

    def test_add_vertex_type(self):
        net = MetabolicNetwork()
        net.add_vertex_type("A", "metabolite")
        self.assertIn("A", net.node_types["metabolite"])

    def test_get_nodes_type(self):
        net = MetabolicNetwork()
        net.add_vertex_type("A", "reaction")
        self.assertEqual(net.get_nodes_type("reaction"), ["A"])
        self.assertIsNone(net.get_nodes_type("unknown"))

    def test_active_reactions(self):
        net = MetabolicNetwork()
        net.add_vertex_type("R1", "reaction")
        net.add_vertex_type("M1", "metabolite")
        net.add_edge("M1", "R1", 1)
        self.assertEqual(net.active_reactions(["M1"]), ["R1"])
        self.assertEqual(net.active_reactions(["X"]), [])

    def test_produced_metabolites(self):
        net = MetabolicNetwork()
        net.add_vertex_type("R1", "reaction")
        net.add_vertex_type("P1", "metabolite")
        net.add_edge("R1", "P1", 1)
        self.assertEqual(net.produced_metabolites(["R1"]), ["P1"])

    def test_reachable_metabolites(self):
        net = MetabolicNetwork()
        net.add_vertex_type("R1", "reaction")
        net.add_vertex_type("M1", "metabolite")
        net.add_vertex_type("M2", "metabolite")
        net.add_edge("M1", "R1", 1)
        net.add_edge("R1", "M2", 1)
        result = net.reachable_metabolites(["M1"])
        self.assertCountEqual(result, ["M1", "M2"])

    @patch("Redes_Metabolicas.open", new_callable=mock_open, read_data="""
R1: M1 + M2 => P1 + P2
R2: P2 <=> M3
""")
    def test_load_from_file_split_rev_false(self, mock_file):
        net = MetabolicNetwork(split_rev=False)
        net.load_from_file("dummy.txt")
        self.assertIn("R1", net.node_types["reaction"])
        self.assertIn("R2", net.node_types["reaction"])
        self.assertIn("P2", net.node_types["metabolite"])

    @patch("Redes_Metabolicas.open", new_callable=mock_open, read_data="""
R1: M1 + M2 => P1 + P2
R2: P2 <=> M3
""")
    def test_load_from_file_split_rev_true(self, mock_file):
        net = MetabolicNetwork(split_rev=True)
        net.load_from_file("dummy.txt")
        self.assertIn("R2_f", net.node_types["reaction"])
        self.assertIn("R2_b", net.node_types["reaction"])
        self.assertIn("M3", net.node_types["metabolite"])
        self.assertIn("P2", net.node_types["metabolite"])


if __name__ == "__main__":
    unittest.main()