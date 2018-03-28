
import sys
import os
import pickle
import re
import prepare_graph
from explore_graph import explore_graph
from handle_text_utils import process_stiring, node_meets_rule, report_dissidents


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
        explored_nodes = explore_graph.explore_graph(
            root_node, distance, graph)
        dissident_nodes = set()
        for node in explored_nodes:
            if node_meets_rule(node, relation_str, operator_type, boundary):
                dissident_nodes.add(node)
        report_dissidents(dissident_nodes - set([root_node]))
