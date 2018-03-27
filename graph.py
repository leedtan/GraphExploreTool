
from node import Node
import pickle


class Graph:
    def __init__(self):
        self.nodes = {}

    def ensure_nodes(self, nodes):
        for node_name in nodes:
            if node_name not in self.nodes:
                self.nodes[node_name] = Node()

    def process_connection(self, dp, source, target):
        self.ensure_nodes([source, target])
        self.nodes[source].recognize_connection(target, dp, 's')
        self.nodes[target].recognize_connection(source, dp, 't')

    def save(self, name):
        with open(name, mode='wb') as f:
            pickle.dump(self, f)
