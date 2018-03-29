import re


def _process_rule(rule):

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

    rule_processed = _process_rule(rule)
    if rule_processed:
        return True, node, rule_processed, distance
    else:
        return False, False, False, False


def _get_active_dps(node, relation_str, operator_type):
    if relation_str == 'SENT_OR_RECEIVED':
        active_dps = node.get_all_dps()
    elif relation_str == 'SENT':
        active_dps = node.get_dps_sent()
    elif relation_str == 'RECEIVED':
        active_dps = node.get_dps_received()
    else:
        raise ValueError(
            'relation str not understood but passed regex')
    return active_dps


def node_meets_rule(node, relation_str, operator_type, boundary):
    active_dps = _get_active_dps(node, relation_str, operator_type)

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
