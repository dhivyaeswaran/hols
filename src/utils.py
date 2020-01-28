import sys, os
import matplotlib.pyplot as plt
import seaborn as sns
from src.loader import load_labels
import pandas as pd
import scipy
import scipy.stats
import numpy as np
from sympy.utilities.iterables import multiset_permutations
from tqdm import tqdm
from collections import defaultdict
from matplotlib import rc
import _pickle as pickle
import sklearn.metrics


rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)


label_configs = {1: ['1'], 2: ['2', '1-1'], 3: ['3', '2-1', '1-1-1'],
                 4: ['4', '3-1', '2-2', '2-1-1', '1-1-1-1'],
                 5: ['5', '4-1', '3-2', '3-1-1', '2-2-1', '2-1-1-1', '1-1-1-1-1'],
                 6: ['6', '5-1', '4-2', '3-3', '4-1-1', '3-2-1', '2-2-2', '3-1-1-1', '2-2-1-1',
                     '2-1-1-1-1', '1-1-1-1-1-1']}

dataset_display = {'email': 'EuEmail', 'citation': 'Cora', 'friendship': 'Pokec', 'polblogs': 'PolBlogs'}
sns.set_palette("Set2")

class GlobalInfo:
    def __init__(self, df, trueH, nullH):
        self.df = df
        self.trueH = trueH
        self.nullH = nullH

label_names = {
    'polblogs': ['right', 'left'],
    'email': [i for i in range(42)],
    'citation': ['AI', 'DSA', 'DB', 'EC', 'HWA', 'HCI', 'IR', 'NW', 'OS', 'PG'],
    'friendship': ['bans', 'brat', 'cesk', 'kosi', 'nitr', 'pres', 'trna', 'tren', 'zahr', 'zili']
}