import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import rc

rc('font',**{'family':'serif', 'serif':['Palatino']})
rc('text', usetex=True)
dataset_display = {'email': 'EuEmail', 'citation': 'Cora', 'friendship': 'Pokec', 'polblogs': 'PolBlogs'}
sns.set_palette("Set2")


def load_results(ds):
    df = pd.read_csv('results/hols/%s_grid_search.csv' % ds, index_col=False, header=None,
                     names=['alpha%d'% i for i in range(2, 6)] + ['acc%d'% i for i in range(5)])
    for i in range(2, 6):
        df['alpha%d' % i] = df['alpha%d' % i].apply(lambda d: round(d * 10))
    df['acc'] = df.apply(lambda r: np.sum([r['acc%d' % i] for i in range(5)]) / 5, axis=1)
    results = {}
    for i in range(len(df)):
        r = df.loc[i, :]
        results[tuple(int(r['alpha%d' % i]) for i in range(2, 6))] = r['acc']
    baseline = df.loc[0, 'acc']
    return results, baseline


def plot_accuracy_vs_clique_size(ds, results, baseline):
    df = pd.DataFrame(columns=['dataset', 'k', 'absolute', 'relative'])
    for k in range(2, 6):
        best_key, best_val = 0, 0
        for key, val in results.items():
            if np.sum(list(key)[k-1:]) > 0:
                continue
            if val > best_val:
                best_key = key
                best_val = val
        df = df.append({'dataset':ds, 'k': k, 'absolute': results[best_key],
                        'relative': 100 * (results[best_key] - baseline) / baseline}, ignore_index=True)

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(3.5, 3)
    sns.lineplot(x='k', y='relative', hue='dataset', data=df, marker='o', markersize=10, linewidth=2)
    ax.set_ylabel(r'Accuracy increase $\%$', fontsize=14)
    ax.set_xlabel('Maximum clique size: $k$', fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.set_xticks(range(2, 6))
    ax.yaxis.grid(color='gray', alpha=0.5)
    ax.xaxis.grid(color='gray', alpha=0.5)
    ax.set_axisbelow(True)
    fname = 'results/hols/fig3a_%s.pdf' % ds
    fig.savefig(fname, bbox_inches='tight', pad_inches=0)


def plot_accuracy_vs_triangle_weight(ds, results, baseline):
    wts = np.linspace(0, 0.9, 10)
    df = pd.DataFrame(columns=['dataset', 'w', 'absolute', 'relative'])
    for i, w in enumerate(wts):
        df = df.append({'dataset': ds, 'w': w,
                        'absolute': results[round((1 - w) * 10), round(10 * w), 0, 0],
                        'relative': 100 * (
                        results[round((1 - w) * 10), round(10 * w), 0, 0] - baseline) / baseline}, ignore_index=True)
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(3.5, 3)
    sns.lineplot(x='w', y='relative', hue='dataset', data=df, marker='o', markersize=10, linewidth=2)
    ax.set_ylabel(r'Accuracy increase $\%$', fontsize=14)
    ax.set_xlabel(r'Weight for triangles: $\alpha_{K_3}$', fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.yaxis.grid(color='gray', alpha=0.5)
    ax.xaxis.grid(color='gray', alpha=0.5)
    ax.set_axisbelow(True)
    fname = 'results/hols/fig3b_%s.pdf' % ds
    fig.savefig(fname, bbox_inches='tight', pad_inches=0)

if __name__ == '__main__':
    datasets = sys.argv[1:]

    for d in datasets:
        _results, _baseline = load_results(d)
        plot_accuracy_vs_clique_size(d, _results, _baseline)
        plot_accuracy_vs_triangle_weight(d, _results, _baseline)
