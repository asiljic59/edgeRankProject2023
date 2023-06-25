import math
import pickle

import networkx as nx
from tqdm import tqdm
import time

#HIGLIGHT
RED = '\033[91m'
RESET = '\033[0m'

string = "Obama Barack my nigga"
word = "Obama"
colored_word = colored_word = f"{RED}{word}{RESET}"
print (string.replace(word,colored_word))