import json
import networkx as nx
import matplotlib.pyplot as plt

from data import persons_statements, statements_persons

def color(id):
    if id.startswith('statement'):
        return 'blue'
    else:
        return 'red'

def generate_json():
    G = nx.Graph()
    G.add_nodes_from(persons_statements.keys())
    G.add_nodes_from(statements_persons.keys())

    edges = []

    for person, statements in persons_statements.items():
        edges.extend([(person, statement) for statement in statements])

    for statement, persons in statements_persons.items():
        edges.extend([(statement, person) for person in persons])

    G.add_edges_from(edges)
    layout = nx.bipartite_layout(G, persons_statements.keys())

    with open('static/data.json', 'w') as f:
        nodes = [ {'id': id, 'label': id, 'x': str(pos[0]), 'y': str(pos[1]), 'size': 3} for id, pos in layout.items() ]
        edges = [ {'id': id, 'source': edge[0], 'target': edge[1]} for id, edge in enumerate(edges) ]
        graph = {
                'nodes': nodes,
                'edges': edges
                }
        json.dump(graph, f)
