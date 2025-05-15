from Graphs import MyGraph

def get_prefix(seq):
    """Return the prefix (all but last character) of a sequence."""
    return seq[:-1]

def get_suffix(seq):
    """Return the suffix (all but first character) of a sequence."""
    return seq[1:]

class DeBruijnGraph(Graph):
    """
    De Bruijn graph for genome assembly from k-mers.
    Nodes: (k-1)-mers; Edges: k-mers as transitions.
    """

    def __init__(self, kmers):
        super().__init__()
        for kmer in kmers:
            self.add_edge(get_prefix(kmer), get_suffix(kmer))

    def find_eulerian_path(self):
        """Find an Eulerian path if the graph is nearly balanced."""
        start, end = self._find_path_ends()
        if not start or not end:
            return None

        self.add_edge(end, start)  # Temporary edge to make Eulerian cycle

        # Use stack-based Hierholzer's algorithm
        path, stack = [], [start]
        local_edges = {u: list(vs) for u, vs in self.graph.items()}
        while stack:
            u = stack[-1]
            if local_edges.get(u):
                stack.append(local_edges[u].pop())
            else:
                path.append(stack.pop())
        path.reverse()

        # Remove the temporary edge from the path
        for i in range(len(path) - 1):
            if path[i] == end and path[i + 1] == start:
                return path[i + 1:] + path[1:i + 1]
        return None

    def _find_path_ends(self):
        """Return (start, end) nodes for Eulerian path if nearly balanced."""
        start = end = None
        for node in self.graph:
            indeg = self.in_degree(node)
            outdeg = self.out_degree(node)
            if outdeg - indeg == 1:
                if start is None:
                    start = node
                else:
                    return None, None
            elif indeg - outdeg == 1:
                if end is None:
                    end = node
                else:
                    return None, None
            elif indeg != outdeg:
                return None, None
        return start, end

    def assemble_sequence(self, path):
        """Reconstruct sequence from Eulerian path."""
        if not path:
            return None
        return path[0] + ''.join(node[-1] for node in path[1:])

class OverlapGraph(Graph):
    """
    Overlap graph for genome assembly from k-mers.
    Nodes: uniquely labeled k-mers; Edges: overlap of k-1 between suffix and prefix.
    """

    def __init__(self, kmers):
        super().__init__()
        # Uniquely label each k-mer to handle duplicates
        self.labeled = [f"{kmer}#{i}" for i, kmer in enumerate(kmers)]
        for label in self.labeled:
            self.add_vertex(label)
        # Add edges for overlaps
        for src in self.labeled:
            src_seq = src.split('#')[0]
            for dst in self.labeled:
                if src != dst and get_suffix(src_seq) == get_prefix(dst.split('#')[0]):
                    self.add_edge(src, dst)

    def find_hamiltonian_path(self):
        """Find a Hamiltonian path using DFS with pruning."""
        def dfs(path, visited):
            if len(path) == len(self.graph):
                return path
            for neighbor in self.graph[path[-1]]:
                if neighbor not in visited:
                    res = dfs(path + [neighbor], visited | {neighbor})
                    if res:
                        return res
            return None

        for start in self.graph:
            res = dfs([start], {start})
            if res:
                return res
        return None

    def _extract_seq(self, label):
        return label.split('#')[0]

    def assemble_sequence(self, path):
        """Reconstruct sequence from Hamiltonian path."""
        if not path:
            return None
        return self._extract_seq(path[0]) + ''.join(self._extract_seq(n)[-1] for n in path[1:])

def generate_kmers(sequence, k):
    """Generate all k-mers from a sequence."""
    return [sequence[i:i+k] for i in range(len(sequence) - k + 1)]

def genome_assembly_demo(sequence, k):
    print("Original sequence:", sequence)
    kmers = generate_kmers(sequence, k)
    print("k-mers:", kmers)

    # De Bruijn Graph Assembly
    print("\n--- De Bruijn Graph Assembly ---")
    dbg = DeBruijnGraph(kmers)
    dbg.print_graph()
    path = dbg.find_eulerian_path()
    if path:
        print("Eulerian path:", path)
        print("Assembled sequence:", dbg.assemble_sequence(path))
    else:
        print("No Eulerian path found.")

    # Overlap Graph Assembly
    print("\n--- Overlap Graph Assembly ---")
    og = OverlapGraph(kmers)
    og.print_graph()
    path = og.find_hamiltonian_path()
    if path:
        print("Hamiltonian path:", path)
        print("Assembled sequence:", og.assemble_sequence(path))
    else:
        print("No Hamiltonian path found.")

# Example usage with a longer sequence:
genome_assembly_demo('GATTACAGATTACAGGATCAGATTACA', 4)

def generate_kmers(seq, k):
    """Generate all k-mers from a sequence (no sorting, preserves order)."""
    return [seq[i:i+k] for i in range(len(seq) - k + 1)]

def genome_assembly_all(seq, k):
    print("Original sequence:", seq)
    kmers = generate_kmers(seq, k)
    print("k-mers:", kmers)

    # De Bruijn Graph Assembly
    print("\n--- De Bruijn Graph Assembly ---")
    dbg = DeBruijnGraph(kmers)
    dbg.print_graph()
    path = dbg.find_eulerian_path()
    if path:
        print("Eulerian path found:", path)
        print("Assembled sequence:", dbg.assemble_sequence(path))
    else:
        print("Eulerian path not found.")

    # Overlap Graph Assembly
    print("\n--- Overlap Graph Assembly ---")
    og = OverlapGraph(kmers)
    og.print_graph()
    path = og.find_hamiltonian_path()
    if path:
        print("Hamiltonian path found:", path)
        print("Assembled sequence:", og.assemble_sequence(path))
    else:
        print("Hamiltonian path not found.")

# Example usage with a longer sequence:
genome_assembly_all('GATTACAGATTACAGGATCAGATTACA', 4)
