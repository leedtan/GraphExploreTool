
def _explore_deeper(nodes_to_explore, dist_remaining, previously_explored, graph):

    next_nodes_to_explore = set()

    for active in nodes_to_explore:
        if active not in previously_explored:
            connections = active.get_connections()
            for connection in connections:
                next_nodes_to_explore.add(graph.get_node(connection))
            previously_explored.add(active)

    if dist_remaining > 0:
        return _explore_deeper(
            next_nodes_to_explore, dist_remaining - 1, previously_explored, graph)
    else:
        return previously_explored


def explore_graph(node, distance, graph):

    return _explore_deeper([node], distance, set(), graph)
