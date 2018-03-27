
class Node:
    def __init__(self):
        self.connections = set()
        self.dps = {'s': set(), 't': set()}

    def recognize_connection(self, relative, dp, connection_type):
        self.dps[connection_type].add(dp)
        self.connections.add(relative)
