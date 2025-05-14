
from Grafos import MyGraph

class MetabolicNetwork(MyGraph):
    def __init__(self, network_type="metabolite-reaction", split_rev=False):
        super().__init__({})
        self.net_type = network_type
        self.node_types = {"metabolite": [], "reaction": []} if network_type == "metabolite-reaction" else {}
        self.split_rev = split_rev

    def add_vertex_type(self, v, nodetype):
        self.add_vertex(v)
        if v not in self.node_types[nodetype]:
            self.node_types[nodetype].append(v)

    def get_nodes_type(self, node_type):
        return self.node_types.get(node_type, None)

    def active_reactions(self, metabolites):
        active = []
        for r in self.node_types["reaction"]:
            preds = self.get_predecessors(r)
            if all(p in metabolites for p in preds):
                active.append(r)
        return active

    def produced_metabolites(self, active_reactions):
        products = set()
        for r in active_reactions:
            sucs = self.get_successors(r)
            products.update(sucs)
        return list(products)

    def reachable_metabolites(self, initial_metabolites):
        current_metabolites = set(initial_metabolites)
        while True:
            active = self.active_reactions(current_metabolites)
            products = set(self.produced_metabolites(active))
            new_metabs = products - current_metabolites
            if not new_metabs:
                break
            current_metabolites.update(new_metabs)
        return list(current_metabolites)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                reaction_id, reaction = line.split(":")
                reaction_id = reaction_id.strip()
                reversible = "<=>" in reaction
                arrow = "<=>" if reversible else "=>"
                left, right = reaction.split(arrow)
                substrates = [x.strip() for x in left.strip().split('+')]
                products = [x.strip() for x in right.strip().split('+')]

                if reversible and self.split_rev:
                    rid_fwd = reaction_id + "_f"
                    rid_bwd = reaction_id + "_b"
                    self.add_vertex_type(rid_fwd, "reaction")
                    self.add_vertex_type(rid_bwd, "reaction")
                    for s in substrates:
                        self.add_vertex_type(s, "metabolite")
                        self.add_edge(s, rid_fwd, 1)
                    for p in products:
                        self.add_vertex_type(p, "metabolite")
                        self.add_edge(rid_fwd, p, 1)
                    for p in products:
                        self.add_edge(p, rid_bwd, 1)
                    for s in substrates:
                        self.add_edge(rid_bwd, s, 1)
                else:
                    self.add_vertex_type(reaction_id, "reaction")
                    for s in substrates:
                        self.add_vertex_type(s, "metabolite")
                        self.add_edge(s, reaction_id, 1)
                    for p in products:
                        self.add_vertex_type(p, "metabolite")
                        self.add_edge(reaction_id, p, 1)

if __name__ == "__main__":
    net = MetabolicNetwork("metabolite-reaction", split_rev=True)
    net.load_from_file("example-net.txt")
    net.print_graph()
    print("Reações", net.get_nodes_type("reaction"))
    print("Metabolitos:", net.get_nodes_type("metabolite"))

    result = net.reachable_metabolites(["M1", "M2"])
    print("Metabolitos alcançáveis a partir de M1, M2:", result)