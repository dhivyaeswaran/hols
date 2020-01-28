import sys
import numpy as np
from collections import defaultdict
from tqdm import tqdm


datasets = sys.argv[1:]

for ds in datasets:
    for k in tqdm([2, 3, 4, 5]):
        cliques = np.loadtxt('data/%s/%dcliques.txt' % (ds, k), delimiter=' ')
        matrix_entries = defaultdict(int)
        for clique in cliques:
            for u in clique:
                for v in clique:
                    if u < v:
                        matrix_entries[u, v] += 1
        matrix_entries_list = np.array([[u, v, e] for (u, v), e in matrix_entries.items()] + \
                                       [[v, u, e] for (u, v), e in matrix_entries.items()], dtype=int)
        np.savetxt('data/%s/%dclique_matrix.txt' % (ds, k), matrix_entries_list, fmt='%d')
