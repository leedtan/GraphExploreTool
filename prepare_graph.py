
import json
import pandas as pd
from graph import Graph


def _read_data(filename):

    with open(filename) as handle:
        dictdump = json.loads(handle.read())

    df = pd.DataFrame(dictdump)
    return df


def _build_graph(df):

    graph = Graph()
    num_rows = df.shape[0]
    for idx in range(num_rows):
        if idx % 50000 == 0:
            print('%d of %d, %.3f percent ' % (idx, num_rows, idx / num_rows))
        graph.process_connection(*df.loc[idx, :])

    graph.save('graph.pkl')


def pre_process_graph():
    df = _read_data('oceania_citizen_relationships_2m.json')
    _build_graph(df)
