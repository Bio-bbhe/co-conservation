import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.algorithms.components.connected import connected_components
import matplotlib.patheffects as path_effects
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from mpl_toolkits.mplot3d import Axes3D


def tsv2network(tsv_file, mini_node, out_dir):
    G = nx.Graph()
    with open(tsv_file) as f:
        connect = []
        for line in f:
            connect.append(line)
            s = ''.join(connect).replace('\n\t', '\t').split('\n')
            # print(s)
    cluster = []
    for sub_cluster in s:
        if len(sub_cluster) != 0:
            cluster.append(tuple(sub_cluster.split('\t')))
    G.add_edges_from(cluster, weight=0.3)

    # to_be_removed = []
    for connected_nodes in list(connected_components(G)):  # connected_nodes is a set that contains connected nodes
        if len(connected_nodes) < mini_node:
            for node in connected_nodes:
                G.remove_node(node)
    d = nx.degree(G)
    pos = nx.spring_layout(G)

    nx.draw_spring(G, width=0.1, node_size=2, node_color='#A0CBE2', edge_color='#BB0000', edge_cmap=plt.cm.Blues,
                   with_labels=False)
    plt.savefig(out_dir, dpi=600)
    return G


def shared_nodes(g_enzyme, g_pre, mini_node, coverage):
    shared_node = []
    rep_enzyme = []  # select representative enzyme node for labeling in the network
    rep_pre = []
    cluster_1 = list(connected_components(g_enzyme))
    cluster_2 = list(connected_components(g_pre))
    num_of_qualified_enzymes = 0
    for c1 in cluster_1:
        for c2 in cluster_2:
            c1_and_c2 = set.intersection(c1, c2)
            count = len(c1_and_c2) / len(c2)
            if min(len(c1), len(c2)) >= mini_node and count >= coverage:
                shared_node.extend(list(c1_and_c2))
                rep_pre.append(list(sorted(c2))[0])
        if len(c1) >= 5:  # mini node number in p450 cluster
            rep_enzyme.append(list(sorted(c1))[0])
    return set(shared_node), rep_enzyme, rep_pre,num_of_qualified_enzymes


if __name__ == '__main__':
    import argparse
    import os
    parser = argparse.ArgumentParser(
        description='Sequence pairs co-conservation analysis. The input files are clustered .tsv files of both '
                    'sequence_1 and sequence_2. The output will be monolayer SSNs of sequence_1 and _2 and a '
                    'multilayer SSN that connects sequence pairs')
    parser.add_argument('-seq1', '--seq1_path', type=str,  required=True,
                        help='<-seq1 /home/seq1.tsv> The first .tsv file generated by mmseq2')
    parser.add_argument('-seq2', '--seq2_path', type=str, required=True,
                        help='<-seq2 /home/seq2.tsv> The second .tsv file generated by mmseq2')
    parser.add_argument('-seq1_node_num', '--seq1_node_num', type=int, required=False, default=0,
                        help='<--seq1_node_num 3> The minimal node number in a cluster for seq1, default=0')
    parser.add_argument('-seq2_node_num', '--seq2_node_num',type=int,  required=False, default=0,
                        help='<--seq2_node_num 3> The minimal node number in a cluster for seq2, default=0')
    parser.add_argument('-c', '--coverage', type=float, required=True,
                        help='<--coverage 0.3> coverage = (seq1∩seq2)/seq2')
    parser.add_argument('-o', '--outdir', type=str, required=True,
                        help='<-o /test/output> A path to save output files. e.g., ./output')

    args = parser.parse_args()

    if not os.path.exists(args.outdir):  # abs path
        os.makedirs(args.outdir)

    tsv_pre = args.seq1_path
    tsv_P450 = args.seq2_path
    seq1_name = args.seq1_path.split('/')[-1].split('.tsv')[0]
    seq2_name = args.seq2_path.split('/')[-1].split('.tsv')[0]
    G_pre = tsv2network(tsv_pre, args.seq1_node_num, args.outdir + '/' + seq1_name + '_SSN.png')
    G_P450 = tsv2network(tsv_P450, args.seq2_node_num, args.outdir + '/' + seq2_name + '_SSN.png')

    shared_node = shared_nodes(G_P450, G_pre, 1, args.coverage)[0]
    rep_enzyme = shared_nodes(G_P450, G_pre, 1, args.coverage)[1]
    rep_pre = shared_nodes(G_P450, G_pre, 1, args.coverage)[2]
    num_of_qualified_enzymes = len(shared_node)
    print(f'number of qualified {seq2_name} is {num_of_qualified_enzymes}')
    # let's start with the important stuff. pick your colors.
    cols = ['steelblue', 'darksalmon', 'mediumseagreen']
    # Imagine you have three node-aligned snapshots of a network
    pos_p450 = nx.spring_layout(G_P450)  # assuming common node location
    pos_pre = nx.spring_layout(G_pre)
    # graphs = [G1,G2, G3]
    graphs = [G_pre, G_P450]

    w = 20
    h = 16

    '''
    inspried by https://github.com/jkbren/matplotlib-multilayer-network"
    '''

    fig, ax = plt.subplots(1, 1, figsize=(w, h), dpi=600, subplot_kw={'projection': '3d'})

    # draw P450 layer
    xs_p450 = list(list(zip(*list(pos_p450.values())))[0])
    ys_p450 = list(list(zip(*list(pos_p450.values())))[1])
    zs_p450 = [1 / 1.5] * len(xs_p450)  # set a common z-position 0 of the nodes in P450 layer
    cs = [cols[1]] * len(xs_p450)
    # add edge within P450 layer
    lines3d = [(list(pos_p450[i]) + [1 / 1.5], list(pos_p450[j]) + [1 / 1.5]) for i, j in G_P450.edges()]
    line_collection = Line3DCollection(lines3d, zorder=4, color=[0.3, 0.7, 0.5, 1], alpha=0.5)
    line_collection.set_linewidth(0.2)
    ax.add_collection3d(line_collection)
    ax.scatter(xs_p450, ys_p450, zs_p450, c='#3266a4', s=5, edgecolors='.2', marker='o', linewidth=0.2, alpha=1, zorder=4)

    # add a plane to designate the layer
    xdiff = max(xs_p450) - min(xs_p450)
    ydiff = max(ys_p450) - min(ys_p450)
    ymin = min(ys_p450) - ydiff * 0.01
    ymax = max(ys_p450) + ydiff * 0.01
    xmin = min(xs_p450) - xdiff * 0.01 * (w / h)
    xmax = max(xs_p450) + xdiff * 0.01 * (w / h)
    xx, yy = np.meshgrid([xmin, xmax], [ymin, ymax])
    zz = np.zeros(xx.shape) + 1
    ax.plot_surface(xx, yy, zz / 1.5, color=cols[1], alpha=0.1, zorder=3)

    ax.set_ylim(min(ys_p450) - ydiff * 0.1, max(ys_p450) + ydiff * 0.1)
    ax.set_xlim(min(xs_p450) - xdiff * 0.1, max(xs_p450) + xdiff * 0.1)
    ax.set_zlim(-0.1, len(graphs) - 1 + 0.1)

    # change shared node position in pre layer
    for pre, p in pos_pre.items():
        if pre in shared_node:
            pos_pre[pre] = pos_p450[pre]

    # draw pre layer
    xs_pre = list(list(zip(*list(pos_pre.values())))[0])
    ys_pre = list(list(zip(*list(pos_pre.values())))[1])
    zs_pre = [0 / 1.5] * len(xs_pre)  # set a common z-position 0 of the nodes in P450 layer
    cs = [cols[0]] * len(xs_pre)

    # add edge within pre layer
    lines3d = [(list(pos_pre[i]) + [0 / 1.5], list(pos_pre[j]) + [0 / 1.5]) for i, j in G_pre.edges()]
    line_collection = Line3DCollection(lines3d, zorder=1, color=[0.3, 0.7, 0.5, 1], alpha=0.5)
    line_collection.set_linewidth(0.2)
    ax.add_collection3d(line_collection)

    ax.scatter(xs_pre, ys_pre, zs_pre, c='#ffff00', s=5, edgecolors='.2', marker='o', linewidth=0.2, alpha=1, zorder=1)

    # add a plane to designate the layer
    xdiff = max(xs_pre) - min(xs_pre)
    ydiff = max(ys_pre) - min(ys_pre)
    ymin = min(ys_pre) - ydiff * 0.01
    ymax = max(ys_pre) + ydiff * 0.01
    xmin = min(xs_pre) - xdiff * 0.01 * (w / h)
    xmax = max(xs_pre) + xdiff * 0.01 * (w / h)
    xx, yy = np.meshgrid([xmin, xmax], [ymin, ymax])
    zz = np.zeros(xx.shape) + 0
    ax.plot_surface(xx, yy, zz / 1.5, color=cols[0], alpha=0.1, zorder=0)

    # color = cols[0]
    ax.set_ylim(min(ys_pre) - ydiff * 0.1, max(ys_pre) + ydiff * 0.1)
    ax.set_xlim(min(xs_pre) - xdiff * 0.1, max(xs_pre) + xdiff * 0.1)
    ax.set_zlim(-0.1, len(graphs) - 1 + 0.1)

    # add between-layer connections
    lines3d_between = [(list(pos_pre[i]) + [0 / 1.5], list(pos_p450[i]) + [1 / 1.5]) for i in shared_node]
    # print(lines3d_between)
    between_lines = Line3DCollection(lines3d_between, zorder=2, color=[1, 0.6, 0.3, 0.5],
                                     alpha=0.5, linestyle=(5, (1, 0)), linewidth=0.1)
    # linestyle = (5, (1, 5))
    ax.add_collection3d(between_lines)

    # add one representative label for each P450 cluster
    target = {'pre_3046', 'pre_2020', 'pre_2992'}  # 11, 7 ,15
    # pre_10: try, pre_2021: bgc7,pre_2020: bgc7, pre_2191: YSYY， pre_1673： YIYY, pre_1683: WFIW
    for node in rep_enzyme:
        x_node = float(pos_p450[node][0])
        y_node = float(pos_p450[node][1])
        z_node = 1 / 1.5
        ax.text(x_node, y_node, z_node, node.replace('pre','P450'), color='blue', size=6, zorder=5)

    angle = 60
    height_angle = 20
    ax.view_init(height_angle, angle)

    # zoom into the fig
    ax.dist = 9
    ax.set_axis_off()
    # plt.savefig('multilayer_network_wlabels.png',dpi=425,bbox_inches='tight')
    plt.show()
    plt.savefig(args.outdir + '/'  + 'seq_pairs_SSN.svg')
