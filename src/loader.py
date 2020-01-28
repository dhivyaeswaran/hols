import numpy as np


def load_data(ds):
    """
    :param ds: dataset name
    :return: (np.array, np.array) list of edges (deduplicated, undirected, excluding self-loops)
            and a list of labels for each vertex; vertices and labels are zero-indexed.
    """
    edges = np.loadtxt('data/%s/edges.txt' % ds, dtype=int)
    labels = np.loadtxt('data/%s/labels.txt' % ds, dtype=int)
    return edges, labels


def load_labels(ds):
    return np.loadtxt('data/%s/labels.txt' % ds, dtype=int)
