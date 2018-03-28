
from node import Node
import pickle


class Graph:
    def __init__(self):
        self._nodes = {}

    def _ensure_nodes(self, node_names):
        for node_name in node_names:
            if node_name not in self._nodes:
                self._nodes[node_name] = Node(node_name)

    def process_connection(self, dp, source, target):
        self._ensure_nodes([source, target])
        self._nodes[source].process_connection(target, dp, 's')
        self._nodes[target].process_connection(source, dp, 't')

    def get_nodes(self):
        return self._nodes

    def get_node(self, nodename):
        if nodename in self._nodes:
            return self._nodes[nodename]
        else:
            raise ValueError(nodename + ' not in graph')

    def save(self, name):
        with open(name, mode='wb') as f:
            pickle.dump(self, f)
