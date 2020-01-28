from src.utils import *


def global_null_prob(typ, label_dist):
    """Probability of seeing this label configuration in the graph."""
    nonzero_counts = [int(v) for v in typ.split('-')]
    if len(nonzero_counts) > len(label_dist):
        return 0
    counts = np.zeros(len(label_dist))
    counts[:len(nonzero_counts)] = np.array(nonzero_counts)
    k = np.sum(counts)
    prob = 0
    for config in multiset_permutations(counts):
        prob += scipy.stats.multinomial.pmf(config, n=k, p=label_dist)
    return prob


def compute_distribution(ds, k, label_arr, label_dist):
    global_type_counts = defaultdict(int)
    global_total = 0

    with open('data/%s/%dcliques.txt' % (ds, k)) as f:
        for line in tqdm(f):
            vertices = [int(v) for v in line.strip().split(' ')]
            l_arr = np.array([label_arr[v] for v in vertices])
            typ = '-'.join(str(d) for d in np.sort([np.sum(l_arr == i) for i in np.unique(l_arr)])[::-1])
            global_type_counts[typ] += 1
            global_total += 1

    df = pd.DataFrame(columns=['type', 'entropy', 'trueProb', 'nullProb'])
    df['type'] = label_configs[k]
    df['trueProb'] = df.type.apply(lambda typ: global_type_counts[typ] / global_total)
    df['nullProb'] = df.type.apply(lambda typ: global_null_prob(typ, label_dist))
    return GlobalInfo(df, np.sum(df.entropy * df.trueProb), np.sum(df.entropy * df.nullProb))


def plot_prevalence(ds, k_vals, global_info):
    for k in k_vals:
        fig, ax = plt.subplots(1, 1)
        # global_info[k].df['type'] = global_info[k].df['type'].apply(lambda s: s + '\n(%1.3f)' % config_to_entropy[s])
        n = len(global_info[k].df)
        fig.set_size_inches(0.87 * n, 1.7)

        df = global_info[k].df.rename(columns={'nullProb': 'Random', 'trueProb': 'Observed'})[
            ['type', 'Random', 'Observed']].melt(id_vars='type')
        sns.barplot(x='type', y='value', hue='variable', data=df, ax=ax)
        sns.despine(fig)
        ax.set_ylim(0, 1)
        ax.set_ylabel('Fraction', fontsize=14, labelpad=0)
        ax.get_legend().remove()
        ax.set_title(r'%s: $K_%d$' % (dataset_display[ds], k), fontsize=16, fontweight='bold')
        ax.set_xlabel('Label configuration', fontsize=14)
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.yaxis.grid(color='gray', alpha=0.5)
        ax.set_axisbelow(True)
        if k == 5:
            ax.legend(fancybox=True, shadow=True, prop={'size': 14}, ncol=2,
                      bbox_to_anchor=(0.5, 0.9), loc='center')
        fname = 'results/holh/fig2_%s_k%d.pdf' % (ds, k)
        fig.savefig(fname, bbox_inches='tight', pad_inches=0.1)
        os.system('pdfcrop %s %s' % (fname, fname))
        plt.close(fig)


if __name__ == '__main__':
    datasets = sys.argv[1:]
    k_vals = range(2, 6)

    for ds in datasets:
        labels = load_labels(ds)
        C = labels.max() + 1
        label_dist = np.array([np.sum(labels == i) for i in range(C)]) / len(labels)
        global_info = {}
        for k in k_vals:
            print(ds, 'k=%d' % k)
            global_info[k] = compute_distribution(ds, k, labels, label_dist)

        print('Plotting')
        plot_prevalence(ds, k_vals, global_info)
