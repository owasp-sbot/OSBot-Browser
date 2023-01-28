import networkx
from networkx import isolates

# todo figure out a way to use the name methods as NX_Graph
class NX_DiGraph(networkx.DiGraph):

    def remove_nodes(self, nodes_ids):
        self.remove_nodes_from(nodes_ids)
        return self

    def remove_nodes_with_no_edges(self):
        nodes_with_no_edges = list(isolates(self))
        self.remove_nodes_from(nodes_with_no_edges)
        return nodes_with_no_edges