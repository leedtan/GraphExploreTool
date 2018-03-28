
import sys
import os
import pickle
import re
import prepare_graph


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


def process_rule(rule):

    if not re.match(
            '(SENT_OR_RECEIVED|SENT|RECEIVED)\((<>|>|<)[\.0-9]*\)',
            rule):
        return False

    relation_str, operator_str, _ = re.split('\(|\)', rule)

    if operator_str == '<>':
        operator_type = '<>'
        boundary = float(operator_str[2:])
    else:
        operator_type = operator_str[0]
        boundary = float(operator_str[1:])

    return (relation_str, operator_type, boundary)


def process_string(
        nodename, rule, distance, graph):

    if distance.isdigit():
        distance = int(distance)
    else:
        return False, False, False, False

    if nodename in graph.get_nodes().keys():
        node = graph.get_node(nodename)
    else:
        return False, False, False, False

    rule_processed = process_rule(rule)
    if rule_processed:
        return True, node, rule_processed, distance
    else:
        return False, False, False, False


def node_passes(node, relation_str, operator_type, boundary):

    if relation_str == 'SENT_OR_RECEIVED':
        active_dps = node.get_all_dps()
    if relation_str == 'SENT':
        active_dps = node.get_dps_sent()
    if relation_str == 'RECEIVED':
        active_dps = node.get_dps_received()

    if operator_type == '<>':
        return boundary in active_dps

    if operator_type == '>':
        return max(active_dps) > boundary

    if operator_type == '<':
        return min(active_dps) < boundary


def report_dissidents(dissident_nodes):

    if len(dissident_nodes) == 0:
        print('No dissidents found!')
    else:
        print('Dissidents found!')
        print(dissident_nodes)


if __name__ == '__main__':

    if not os.path.exists('graph.pkl'):
        print('Graph doesnt exist. Performing one-time build.')
        print('A dissident hacker must have deleted it. They must be destroyed')
        prepare_graph.pre_process_graph()
    else:
        print('Pre build graph found')

    print('Prepared to surface undesirables.')

    with open('graph.pkl', 'rb') as f:
        graph = pickle.load(f)
    nodes = graph.get_nodes()

    while True:
        print('\nReminder good citizen: the format for execution is')
        print('C1 => R({> | < | <>}DP) => L')
        user_input = input(
            'Which Thought-Dissidents should we surface? :exit if they have all been silenced')

        user_input = "".join(user_input.split())
        if user_input == ':exit':
            print('Good job cleansing the population. Have a nice day :)')
            sys.exit(0)

        if user_input.count('=>') != 2:
            print("need two '=>' characters")
            continue

        user_input_split = user_input.split('=>')
        if len(user_input_split) != 3:
            print("=>s in the wrong locations")
            continue

        nodename, rule, distance = user_input_split
        rule = rule.upper()
        consistent, root_node, rule_processed, distance = process_string(
            nodename, rule, distance, graph)

        if not consistent:
            print("incorrect format")
            continue
        relation_str, operator_type, boundary = rule_processed
        explored_nodes = explore_graph(root_node, distance, graph)
        dissident_nodes = set()
        for node in explored_nodes:
            if node_passes(node, relation_str, operator_type, boundary):
                dissident_nodes.add(node)
        report_dissidents(dissident_nodes - set([root_node]))
