import time

import parse_files_dict
import networkx as nx
import graph
import pickle
from tqdm import tqdm
import time



comments = parse_files_dict.load_comments('./dataset/original_comments.csv')
graph_ = nx.DiGraph()
# File path to write the Digraph
file_path = "graph.pickle"
all_users = parse_files_dict.load_friends('./dataset/friends.csv')
statuses = parse_files_dict.load_statuses('./dataset/original_statuses.csv')
reactions = parse_files_dict.load_reactions('./dataset/original_reactions.csv')
shares = parse_files_dict.load_shares('./dataset/original_shares.csv')

start_time = time.perf_counter()
counter = tqdm(len(all_users))
for user in all_users.keys():
        for other in all_users.keys():
            if other==user:
                continue
            other_user = all_users[other]
            affinity = int(graph.define_affinity(user,other,all_users,comments,shares,reactions,statuses))
            end_time = time.perf_counter()
            if affinity!=0:
                graph_.add_edge(user,other,weight = affinity)
        counter.update(1)
# Dump the Digraph to the file
with open(file_path, "wb") as file:
    pickle.dump(graph_, file)