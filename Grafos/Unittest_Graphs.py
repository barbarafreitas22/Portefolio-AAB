
import unittest
from Grafos import MyGraph

class TestMyGraph(unittest.TestCase):
    def setUp(self):
        self.g = MyGraph({
            1: [(2, 3), (3, 1)],
            2: [(3, 7), (4, 5)],
            3: [(4, 2)],
            4: []
        })

    def test_nodes_and_edges(self):
        self.assertEqual(set(self.g.get_nodes()), {1, 2, 3, 4})
        self.assertIn((1, 2, 3), self.g.get_edges())
        self.assertEqual(self.g.size(), (4, 5))

    def test_add_vertex_and_edge(self):
        self.g.add_vertex(5)
        self.assertIn(5, self.g.get_nodes())
        self.g.add_edge(5, 1, 10)
        self.assertIn((5, 1, 10), self.g.get_edges())

    def test_successors_predecessors(self):
        self.assertEqual(set(self.g.get_successors(1)), {2, 3})
        self.assertEqual(set(self.g.get_predecessors(3)), {1, 2})
        self.assertEqual(set(self.g.get_adjacents(3)), {1, 2, 4})

    def test_degrees(self):
        self.assertEqual(self.g.out_degree(2), 2)
        self.assertEqual(self.g.in_degree(3), 2)
        self.assertEqual(self.g.degree(3), 3)

    def test_shortest_path_and_distance(self):
        self.assertEqual(self.g.shortest_path(1, 4), [1, 3, 4])
        self.assertEqual(self.g.distance(1, 4), 3)
        self.assertEqual(self.g.shortest_path(1, 1), [1])
        self.assertIsNone(self.g.shortest_path(4, 1))

    def test_reachability(self):
        self.assertEqual(set(self.g.reachable_bfs(1)), {2, 3, 4})
        self.assertEqual(set(self.g.reachable_dfs(1)), {2, 3, 4})
        dists = dict(self.g.reachable_with_dist(1))
        self.assertEqual(dists[4], 2)

    def test_cycles(self):
        self.assertFalse(self.g.has_cycle())
        self.g.add_edge(4, 1, 1)  # Cria ciclo
        self.assertTrue(self.g.has_cycle())

    def test_empty_graph(self):
        g = MyGraph({})
        self.assertEqual(g.get_nodes(), [])
        self.assertEqual(g.get_edges(), [])
        self.assertEqual(g.size(), (0, 0))
        self.assertFalse(g.has_cycle())

    def test_self_loop(self):
        g = MyGraph({1: [(1, 1)]})
        self.assertTrue(g.has_cycle())
        self.assertEqual(g.get_successors(1), [1])
        self.assertEqual(g.get_predecessors(1), [1])
        self.assertEqual(g.get_adjacents(1), [1])
        self.assertEqual(g.degree(1), 2)

    def test_disconnected_graph(self):
        g = MyGraph({1: [], 2: [], 3: []})
        self.assertEqual(g.get_edges(), [])
        self.assertFalse(g.has_cycle())
        for node in g.get_nodes():
            self.assertEqual(g.out_degree(node), 0)
            self.assertEqual(g.in_degree(node), 0)
            self.assertEqual(g.degree(node), 0)


if __name__ == "__main__":
    unittest.main()
