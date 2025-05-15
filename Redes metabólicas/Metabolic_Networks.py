from Graphs import MyGraph
import re
import heapq
from collections import deque


class MN_Graph(MyGraph):
    """
    Specialized graph class for metabolite networks, extending Graph with methods 
    for analyzing node degrees, centrality, and clustering.
    """
    def __init__(self, g = {}):
        super().__init__(g)

    def all_degrees(self, deg_type="inout"):
        """
        Return node degrees based on direction: 'in', 'out', or both.
        """
        degs = {}
        for v in self.graph:
            if deg_type in ("out", "inout"):
                degs[v] = len(self.graph[v])
            else:
                degs[v] = 0
        if deg_type in ("in", "inout"):
            for v in self.graph:
                for d in self.graph[v]:
                    if deg_type == "in" or v not in self.graph.get(d, []):
                        degs[d] = degs.get(d, 0) + 1
        return degs

    def highest_degrees(self, all_deg=None, deg_type="inout", top=10):
        """
        Return top nodes by degree.
        Parameters:
            all_deg (dict): Degree dict.
            deg_type (str): Degree type.
            top (int): Number of top nodes to return.
        """
        if all_deg is None:
            all_deg = self.all_degrees(deg_type)
        return sorted(all_deg, key=all_deg.get, reverse=True)[:top]

    def mean_degree(self, deg_type="inout"):
        """
        Calculate average degree of all nodes.
        """
        degs = self.all_degrees(deg_type)
        return sum(degs.values()) / len(degs)

    def prob_degree(self, deg_type="inout"):
        """
        Return the node degrees distribution as a probability.
        Parameters:
            deg_type (str): Degree type.

        Returns:
            dict: Degree value to probability.
        """
        degs = self.all_degrees(deg_type)
        hist = {}
        for d in degs.values():
            hist[d] = hist.get(d, 0) + 1
        return {k: v / len(degs) for k, v in hist.items()}

    def mean_distances(self):
        """
        Compute the average of shortest path length and the density of the graph.
        """
        total_dist = 0
        count = 0
        for node in self.get_nodes():
            for _, dist in self.reachable_with_dist(node):
                total_dist += dist
            count += len(self.reachable_with_dist(node))
        mean_dist = total_dist / count if count else 0
        n = len(self.get_nodes())
        density = count / (n * (n - 1)) if n > 1 else 0
        return mean_dist, density

    def closeness_centrality(self, node):
        """
        Returns closeness centrality for a given node.
        """
        dists = self.reachable_with_dist(node)
        if not dists:
            return 0.0
        return len(dists) / sum(dist for _, dist in dists)

    def highest_closeness(self, top=10):
        """
        Returns nodes with highest closeness centrality.
        """
        centrality = {n: self.closeness_centrality(n) for n in self.get_nodes()}
        return sorted(centrality, key=centrality.get, reverse=True)[:top]

    def betweenness_centrality(self, node):
        """
        Approximate betweenness centrality for a node.
        """
        total = 0
        through = 0
        for s in self.get_nodes():
            for t in self.get_nodes():
                if s != t and s != node and t != node:
                    path = self.shortest_path(s, t)
                    if path:
                        total += 1
                        if node in path:
                            through += 1
        return through / total if total > 0 else 0

    def clustering_coef(self, v):
        """
        Computes local clustering coefficient for a node.
        """
        neighbors = self.get_adjacents(v)
        if len(neighbors) <= 1:
            return 0.0
        links = 0
        for i in neighbors:
            for j in neighbors:
                if i != j and (j in self.get_successors(i) or i in self.get_successors(j)):
                    links += 1
        return links / (len(neighbors) * (len(neighbors) - 1))

    def all_clustering_coefs(self):
        """
        Returns clustering coefficients for all nodes.
        """
        return {v: self.clustering_coef(v) for v in self.get_nodes()}

    def mean_clustering_coef(self):
        """
        Average clustering coefficient across all nodes.
        """
        cc = self.all_clustering_coefs()
        return sum(cc.values()) / len(cc) if cc else 0.0

    def mean_clustering_perdegree(self, deg_type="inout"):
        """
        Average clustering coefficient grouped by degree.
        """
        degs = self.all_degrees(deg_type)
        ccs = self.all_clustering_coefs()
        grouped = {}
        for node, deg in degs.items():
            grouped.setdefault(deg, []).append(ccs[node])
        return {k: sum(v) / len(v) for k, v in grouped.items()}


class CentralityAnalyzer:
    """
    Centrality calculator using various metrics.
    """

    def __init__(self, graph):
        self.graph = graph

    def degree_centrality(self):
        """
        Return degree centrality of each node.
        """
        return {n: len(self.graph.get_successors(n)) for n in self.graph.get_nodes()}

    def closeness_centrality(self):
        """
        Return closeness centrality for all nodes.
        """
        result = {}
        for node in self.graph.get_nodes():
            dist, count = self._bfs_total_distance_and_reach_count(node)
            result[node] = (count / dist) if dist > 0 else 0.0
        return result

    def _bfs_total_distance_and_reach_count(self, start):
        """
        Breadth-first traversal for closeness computation.
        """
        visited = set()
        queue = deque([(start, 0)])
        total, count = 0, 0
        while queue:
            node, dist = queue.popleft()
            if node not in visited:
                visited.add(node)
                if node != start:
                    total += dist
                    count += 1
                queue.extend((n, dist + 1) for n in self.graph.get_successors(node) if n not in visited)
        return total, count

    def betweenness_centrality(self):
        """
        Compute node betweenness using Brandes' algorithm.
        """
        centrality = dict.fromkeys(self.graph.get_nodes(), 0.0)
        for s in self.graph.get_nodes():
            stack = []
            pred = {w: [] for w in self.graph.get_nodes()}
            sigma = dict.fromkeys(self.graph.get_nodes(), 0)
            dist = dict.fromkeys(self.graph.get_nodes(), -1)
            sigma[s], dist[s] = 1, 0
            queue = deque([s])
            while queue:
                v = queue.popleft()
                stack.append(v)
                for w in self.graph.get_successors(v):
                    if dist[w] < 0:
                        dist[w] = dist[v] + 1
                        queue.append(w)
                    if dist[w] == dist[v] + 1:
                        sigma[w] += sigma[v]
                        pred[w].append(v)
            delta = dict.fromkeys(self.graph.get_nodes(), 0)
            while stack:
                w = stack.pop()
                for v in pred[w]:
                    delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
                if w != s:
                    centrality[w] += delta[w]
        return centrality

    def top_nodes(self, centrality_dict, top_n=5):
        """
        Return highest ranked nodes by centrality score.
        """
        return heapq.nlargest(top_n, centrality_dict.items(), key=lambda x: x[1])


def parse_reactions(file_path):
    """
    Parse reaction data into structured reaction dictionaries.
    """
    reactions = []
    with open(file_path) as f:
        for line in f:
            if ':' not in line:
                continue
            parts = re.split(r':\s*', line.strip(), maxsplit=1)
            if len(parts) != 2:
                continue
            reaction_id, formula = parts
            match = re.match(r"(.*?)\s*(<=>|=>)\s*(.*)", formula)
            if not match:
                continue
            substrates = [s.strip() for s in match.group(1).split('+')]
            products = [p.strip() for p in match.group(3).split('+')]
            reactions.append({'id': reaction_id, 'substrates': substrates, 'products': products})
    return reactions


def build_metabolite_graph(reactions):
    """
    Build a metabolite interaction graph from reaction data.
    """
    g = MN_Graph()
    for r in reactions:
        compounds = r['substrates'] + r['products']
        for i in range(len(compounds)):
            for j in range(i + 1, len(compounds)):
                g.add_edge(compounds[i], compounds[j], 1)
                g.add_edge(compounds[j], compounds[i], 1)
    return g


def get_active_reactions(metabolites_set, reactions):
    """
    Return reactions that can occur with the available substrates.
    """
    return [r for r in reactions if all(m in metabolites_set for m in r['substrates'])]

def get_produced_metabolites(active_reactions):
    """
    Extract products from active reactions.
    """
    return set(p for r in active_reactions for p in r['products'])

def compute_final_metabolites(initial_metabolites, reactions):
    """
    Iteratively expand metabolite set by applying reactions.
    """
    known = set(initial_metabolites)
    while True:
        active = get_active_reactions(known, reactions)
        new = get_produced_metabolites(active)
        if new.issubset(known):
            break
        known.update(new)
    return known

reactions_file = "ecoli.txt"

parsed_reactions = parse_reactions(reactions_file)
print(f"Number of reactions parsed: {len(parsed_reactions)}")

metabolite_graph = build_metabolite_graph(parsed_reactions)

centrality_analyzer = CentralityAnalyzer(metabolite_graph)

print("\nDegree Centrality:")
for metabolite, degree_val in centrality_analyzer.top_nodes(centrality_analyzer.degree_centrality()):
    print(f"{metabolite}: {degree_val}")

print("\nCloseness Centrality:")
for metabolite, closeness_val in centrality_analyzer.top_nodes(centrality_analyzer.closeness_centrality()):
    print(f"{metabolite}: {closeness_val:.4f}")

print("\nBetweenness Centrality:")
for metabolite, betweenness_val in centrality_analyzer.top_nodes(centrality_analyzer.betweenness_centrality()):
    print(f"{metabolite}: {betweenness_val:.4f}")

initial_metabolites = ["M_glc_DASH_D_c", "M_h2o_c", "M_nad_c", "M_atp_c"]

reachable_metabolites = compute_final_metabolites(initial_metabolites, parsed_reactions)

print("\nInitial Metabolites:")
print(initial_metabolites)

print("\nReachable Metabolites After Propagation:")
print(sorted(reachable_metabolites))