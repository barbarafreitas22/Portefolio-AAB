
class MyGraph:

    def __init__(self, g = {}):
        self.graph = g

    def print_graph(self):
        for v in self.graph:
            print(v, "->", self.graph[v])

    def get_nodes(self):
        return list(self.graph.keys())

    def get_edges(self):
        edges = []
        for v in self.graph:
            for d, w in self.graph[v]:
                edges.append((v, d, w))
        return edges

    def size(self):
        return len(self.get_nodes()), len(self.get_edges())

    def add_vertex(self, v):
        if v not in self.graph:
            self.graph[v] = []

    def add_edge(self, o, d, w):
        if o not in self.graph:
            self.add_vertex(o)
        if d not in self.graph:
            self.add_vertex(d)
        self.graph[o].append((d, w))

    def get_successors(self, v):
        return [dest for dest, _ in self.graph[v]]

    def get_predecessors(self, v):
        preds = []
        for node in self.graph:
            for dest, _ in self.graph[node]:
                if dest == v:
                    preds.append(node)
        return preds

    def get_adjacents(self, v):
        return list(set(self.get_successors(v) + self.get_predecessors(v)))

    def out_degree(self, v):
        return len(self.graph[v])

    def in_degree(self, v):
        return len(self.get_predecessors(v))

    def degree(self, v):
        return self.in_degree(v) + self.out_degree(v)

    def distance(self, s, d):
        if s == d: return 0
        dist, _ = self._dijkstra(s)
        return dist.get(d, None)

    def shortest_path(self, s, d):
        if s == d: return [s]
        dist, prev = self._dijkstra(s)
        if d not in dist:
            return None
        path = []
        current = d
        while current != s:
            path.append(current)
            current = prev.get(current)
            if current is None:
                return None
        path.append(s)
        path.reverse()
        return path

    def _dijkstra(self, source):
        unvisited = {node: float('inf') for node in self.graph}
        unvisited[source] = 0
        prev = {}
        visited = {}

        while unvisited:
            u = min(unvisited, key=unvisited.get)
            current_dist = unvisited[u]
            visited[u] = current_dist
            del unvisited[u]

            for v, weight in self.graph[u]:
                if v in visited:
                    continue
                new_dist = current_dist + weight
                if new_dist < unvisited.get(v, float('inf')):
                    unvisited[v] = new_dist
                    prev[v] = u

        return visited, prev

    def reachable_bfs(self, v):
        l = [v]
        res = []
        while l:
            node = l.pop(0)
            if node != v: res.append(node)
            for elem, _ in self.graph[node]:
                if elem not in res and elem not in l and elem != node:
                    l.append(elem)
        return res

    def reachable_dfs(self, v):
        l = [v]
        res = []
        while l:
            node = l.pop(0)
            if node != v: res.append(node)
            s = 0
            for elem, _ in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)
                    s += 1
        return res

    def reachable_with_dist(self, s):
        res = []
        l = [(s, 0)]
        while l:
            node, dist = l.pop(0)
            if node != s:
                res.append((node, dist))
            for elem, _ in self.graph[node]:
                if not is_in_tuple_list(l, elem) and not is_in_tuple_list(res, elem):
                    l.append((elem, dist + 1))
        return res

    def node_has_cycle(self, v):
        l = [v]
        visited = [v]
        while l:
            node = l.pop(0)
            for elem, _ in self.graph[node]:
                if elem == v:
                    return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return False

    def has_cycle(self):
        for v in self.graph:
            if self.node_has_cycle(v):
                return True
        return False

def is_in_tuple_list(tl, val):
    for x, _ in tl:
        if val == x:
            return True
    return False

def test_graph():
    g = {
        1: [(2, 3), (3, 1)],
        2: [(3, 7), (4, 5)],
        3: [(4, 2)],
        4: []
    }
    wg = MyGraph(g)
    wg.print_graph()
    print("Nodes:", wg.get_nodes())
    print("Edges:", wg.get_edges())
    print("Shortest path 1->4:", wg.shortest_path(1, 4))
    print("Distance 1->4:", wg.distance(1, 4))
    print("Shortest path 2->4:", wg.shortest_path(2, 4))
    print("Distance 2->4:", wg.distance(2, 4))

if __name__ == "__main__":
    test_graph()