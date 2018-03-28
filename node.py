
class Node:
    def __init__(self, name):
        self._connections = set()
        self._dps = {'s': set(), 't': set()}
        self._name = name

    def recognize_connection(self, relative, dp, connection_type):
        self._dps[connection_type].add(dp)
        self._connections.add(relative)

    def get_connections(self):
        return self._connections

    def get_all_dps(self):
        return self.get_dps_sent().union(self.get_dps_received())

    def get_dps_sent(self):
        return self._dps['s']

    def get_dps_received(self):
        return self._dps['t']

    def __str__(self):
        return 'node %s' % self._name

    def __repr__(self):
        return 'node %s' % self._name
