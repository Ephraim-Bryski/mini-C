from pyvis.network import Network
import networkx as nx

G = nx.DiGraph()
G.add_edges_from([("main", "foo"), ("foo", "bar"), ("bar", "baz"), ("main", "helper")])

net = Network(directed=True, notebook=False)
net.from_nx(G)
net.show("call_graph.html")
