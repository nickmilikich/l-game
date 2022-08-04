import pickle
from utils import *

# Get full graph of game moves
G = build_graph()

with open('../data/graph.pkl', 'wb') as file:
    pickle.dump(G, file)
