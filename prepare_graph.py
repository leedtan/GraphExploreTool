
import json
import pandas as pd
from utils import build_forward_backward_hash
from graph import Graph

with open('data') as handle:
    dictdump = json.loads(handle.read())

graph = Graph()
df = pd.DataFrame(dictdump)

source_usrs = set(df['source'].unique())
target_usrs = set(df['target'].unique())
all_uni_usrs = source_usrs.union(target_usrs)

usr2idx, idx2usr = build_forward_backward_hash(all_uni_usrs)


for idx in range(df.shape[0]):
    if idx % 10000 == 0:
        print('%d of %d, progress: %.3f percent ' %
              (idx, df.shape[0], idx / df.shape[0]))
    graph.process_connection(*df.loc[idx, :])

graph.save('graph.pkl')