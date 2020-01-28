import sys
import os
from tqdm import tqdm


datasets = sys.argv[1:]

for ds in datasets:
    for k in tqdm([2, 3, 4, 5]):
        os.system('./kClist {k} data/{ds}/edges.txt > data/{ds}/{k}cliques.txt'.format(
            k=k, ds=ds
        ))
