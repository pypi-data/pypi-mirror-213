import argparse
import kssd
import quicktree
import os
import create_distance_matrix
import pandas as pd
import warnings
import math
import pkg_resources

warnings.filterwarnings('ignore')


def deal_kssd(kssd_distance_path):
    print('deal kssd...')
    df = pd.read_csv(kssd_distance_path, delimiter='\t')
    new_df = df[['Qry', 'Ref', 'MashD']]
    if '.fasta.gz' in new_df['Qry'][0] or '.fastq.gz' in new_df['Qry'][0] or '.fna.gz' in new_df['Qry'][0]:
        new_df['Ref'] = new_df['Ref'].apply(lambda x: x.split('/')[-1].split('.')[0])
        new_df['Qry'] = new_df['Qry'].apply(lambda x: x.split('/')[-1].split('.')[0])
    elif new_df['Qry'][0][-3:] == '.fa':
        new_df['Qry'] = new_df['Qry'].apply(lambda x: x.split('.')[-2].split('/')[-1].split('_')[0])
        new_df['Ref'] = new_df['Ref'].apply(lambda x: x.split('.')[-2].split('/')[-1].split('_')[0])
    elif new_df['Qry'][0][-6:] == '.fasta':
        new_df['Qry'] = new_df['Qry'].apply(lambda x: x.split('/')[1][:-6])
        new_df['Ref'] = new_df['Ref'].apply(lambda x: x.split('/')[1][:-6])
    else:
        pass
    current_path = os.getcwd()
    txt_path = current_path + '/kssd_distance.txt'
    new_df.to_csv(txt_path, index=False, sep='\t')
    data = {}
    with open(txt_path, 'r') as f:
        next(f)
        for line in f:
            seq1, seq2, distance = line.strip().split()
            if seq1 not in data:
                data[seq1] = {}
            if seq2 not in data:
                data[seq2] = {}
            data[seq1][seq2] = float(distance)
            data[seq2][seq1] = float(distance)
    if os.path.exists(txt_path):
        os.remove(txt_path)
        # print("File deleted successfully")
    else:
        print(f"The file {txt_path} does not exist")
    n_seqs = len(data)
    seq_names = sorted(data.keys())
    '''
    3
    Seq1         0.00000    0.10000    0.30000
    Seq2         0.10000    0.00000    0.20000
    Seq3         0.30000    0.20000    0.00000
    '''
    with open('kssd_dist_matrix.phy', 'w') as f:
        f.write(str(len(seq_names)) + '\n')
        for i in range(n_seqs):
            f.write(seq_names[i])
            for j in range(n_seqs):
                if i == j:
                    f.write('\t{:.5f}'.format(0.0))
                else:
                    f.write('\t{:.5f}'.format(data[seq_names[i]][seq_names[j]]))
            f.write('\n')


def deal_mash(mash_distance_path):
    print('deal mash...')
    df = pd.read_csv(mash_distance_path, delimiter='\t', header=None)
    df.columns = ['Ref', 'Qry', 'MashD', 'P-value', 'Matching-hashes']
    new_df = df[['Qry', 'Ref', 'MashD']]
    if '.fasta.gz' in new_df['Qry'][0] or '.fastq.gz' in new_df['Qry'][0] or '.fna.gz' in new_df['Qry'][0]:
        new_df['Ref'] = new_df['Ref'].apply(lambda x: x.split('/')[-1].split('.')[0])
        new_df['Qry'] = new_df['Qry'].apply(lambda x: x.split('/')[-1].split('.')[0])
    elif new_df['Qry'][0][-3:] == '.fa':
        new_df['Qry'] = new_df['Qry'].apply(lambda x: x.split('.')[-2].split('/')[-1].split('_')[0])
        new_df['Ref'] = new_df['Ref'].apply(lambda x: x.split('.')[-2].split('/')[-1].split('_')[0])
    elif new_df['Qry'][0][-6:] == '.fasta':
        new_df['Qry'] = new_df['Qry'].apply(lambda x: x.split('/')[1][:-6])
        new_df['Ref'] = new_df['Ref'].apply(lambda x: x.split('/')[1][:-6])
    else:
        pass
    current_path = os.getcwd()
    txt_path = current_path + '/mash_distance.txt'
    new_df.to_csv(txt_path, index=False, sep='\t')
    data = {}
    with open(txt_path, 'r') as f:
        next(f)
        for line in f:
            seq1, seq2, distance = line.strip().split()
            if seq1 not in data:
                data[seq1] = {}
            if seq2 not in data:
                data[seq2] = {}
            data[seq1][seq2] = float(distance)
            data[seq2][seq1] = float(distance)
    if os.path.exists(txt_path):
        os.remove(txt_path)
        # print("File deleted successfully")
    else:
        print(f"The file {txt_path} does not exist")
    n_seqs = len(data)
    seq_names = sorted(data.keys())
    with open('mash_dist_matrix.phy', 'w') as f:
        f.write(str(len(seq_names)) + '\n')
        for i in range(n_seqs):
            f.write(seq_names[i])
            for j in range(n_seqs):
                if i == j:
                    f.write('\t{:.5f}'.format(0.0))
                else:
                    f.write('\t{:.5f}'.format(data[seq_names[i]][seq_names[j]]))
            f.write('\n')


def deal_sourmash(k, sourmash_distance_path):
    print('deal sourmash...')
    with open(sourmash_distance_path) as f:
        first_line = f.readline().strip()
    temp_names = first_line.split(',')
    seq_names = []
    for x in temp_names:
        if '.fasta.gz' in x or '.fastq.gz' in x or '.fna.gz' in x:
            seq_names.append(x.split('/')[-1].split('.')[0])
        elif x[-3:] == '.fa':
            seq_names.append(x.split('.')[-2].split('/')[-1].split('_')[0])
        elif x[-6:] == '.fasta':
            seq_names.append(x.split('/')[1][:-6])
        else:
            pass
    data = pd.read_csv(sourmash_distance_path, header=None, skiprows=[0])
    with open('sourmash_dist_matrix.phy', 'w') as f:
        f.write(str(len(seq_names)) + '\n')
        for i in range(len(seq_names)):
            f.write(seq_names[i])
            for j in range(len(seq_names)):
                if i == j:
                    f.write('\t{:.5f}'.format(0.0))
                else:
                    jaccard = data[i][j]
                    if jaccard == 0:
                        mashD = 1
                    else:
                        mashD = -(1 / k) * math.log(2 * jaccard / (1 + jaccard))
                    f.write('\t{:.5f}'.format(mashD))
            f.write('\n')


def deal_bindash(k, bindash_distance_path):
    print('deal bindash...')
    df = pd.read_csv(bindash_distance_path, delimiter='\t', header=None)
    df.columns = ['Ref', 'Qry', 'MashD', 'P-value', 'Matching-hashes']
    new_df = df[['Qry', 'Ref', 'Matching-hashes']]
    new_df['Matching-hashes'] = new_df['Matching-hashes'].apply(lambda x: int(x.split('/')[0]) / int(x.split('/')[1]))
    if '.fasta.gz' in new_df['Qry'][0] or '.fastq.gz' in new_df['Qry'][0] or '.fna.gz' in new_df['Qry'][0]:
        new_df['Ref'] = new_df['Ref'].apply(lambda x: x.split('/')[-1].split('.')[0])
        new_df['Qry'] = new_df['Qry'].apply(lambda x: x.split('/')[-1].split('.')[0])
    elif new_df['Qry'][0][-3:] == '.fa':
        new_df['Qry'] = new_df['Qry'].apply(lambda x: x.split('.')[-2].split('/')[-1].split('_')[0])
        new_df['Ref'] = new_df['Ref'].apply(lambda x: x.split('.')[-2].split('/')[-1].split('_')[0])
    elif new_df['Qry'][0][-6:] == '.fasta':
        new_df['Qry'] = new_df['Qry'].apply(lambda x: x.split('/')[1][:-6])
        new_df['Ref'] = new_df['Ref'].apply(lambda x: x.split('/')[1][:-6])
    else:
        pass
    current_path = os.getcwd()
    txt_path = current_path + '/bindash_distance.txt'
    new_df.to_csv(txt_path, index=False, sep='\t')
    data = {}
    with open(txt_path, 'r') as f:
        next(f)
        for line in f:
            seq1, seq2, distance = line.strip().split()
            if seq1 not in data:
                data[seq1] = {}
            if seq2 not in data:
                data[seq2] = {}
            data[seq1][seq2] = float(distance)
            data[seq2][seq1] = float(distance)
    if os.path.exists(txt_path):
        os.remove(txt_path)
        # print("File deleted successfully")
    else:
        print(f"The file {txt_path} does not exist")
    n_seqs = len(data)
    seq_names = sorted(data.keys())
    with open('bindash_dist_matrix.phy', 'w') as f:
        f.write(str(len(seq_names)) + '\n')
        for i in range(n_seqs):
            f.write(seq_names[i])
            for j in range(n_seqs):
                if i == j:
                    f.write('\t{:.5f}'.format(0.0))
                else:
                    if seq_names[j] not in data[seq_names[i]]:
                        data[seq_names[i]].setdefault(seq_names[j], 0)
                    jaccard = data[seq_names[i]][seq_names[j]]
                    if jaccard == 0:
                        mashD = 1
                    else:
                        mashD = -(1 / k) * math.log(2 * jaccard / (1 + jaccard))
                    f.write('\t{:.5f}'.format(mashD))
            f.write('\n')


def merge_nwk(names):
    with open(names[0], 'r') as f:
        real_tree = f.readline()
    merged_lines = []
    for i in range(1, len(names)):
        with open(names[i], 'r') as f:
            lines = f.readlines()
            merged_line = ''.join(lines)
            merged_line = merged_line.replace('\n', '')
            merged_lines.append(merged_line)

    with open('intree.nwk', 'w') as f:
        f.write(str(8) + '\n')
        for i in range(len(merged_lines)):
            f.write(real_tree)
            f.write('\n')
            f.write(merged_lines[i])
            f.write('\n')
            f.write('\n')


def shuffle(args):
    k = args.k
    s = args.s
    l = args.l
    o = args.o
    kssd.write_dim_shuffle_file(k, s, l, o)
    print('shuffle finished!')


def sketch(args):
    k = args.k
    L = args.L
    r = args.r
    o = args.o
    L_path = pkg_resources.resource_filename('kssdtree', '/kssdtree/' + L)
    print(L_path)
    kssd.dist_dispatch(k, L_path, r, o, 0)
    print('sketch finished!')


def dist(args):
    k = args.k
    r = args.r
    o = args.o
    remaining_args = args.remaining_args
    distance_matrix = args.distance_matrix
    kssd.dist_dispatch(k, r, o, remaining_args, 1)
    if distance_matrix != '':
        file_path = os.path.join(os.getcwd(), o, "distance.out")
        create_distance_matrix.create(file_path, distance_matrix)
    print('dist finished!')


def buildtree(args):
    i = args.i
    o = args.o
    state = quicktree.buildtree(i, o)
    nwk_path = os.path.join(os.getcwd(), o)
    with open(nwk_path, 'r') as f:
        lines = f.readlines()
        merged_line = ''.join(lines)
        merged_line = merged_line.replace('\n', '')
    with open(nwk_path, 'w') as f:
        f.write(merged_line)
    from Bio import Phylo
    import matplotlib.pyplot as plt
    tree = Phylo.read(nwk_path, "newick")
    Phylo.draw(tree, do_show=False)
    Phylo.draw_ascii(tree)
    plt.axis('off')
    plt.gcf().set_size_inches(10, 10)
    plt.savefig(o.split('.')[0] + ".png", dpi=300, bbox_inches='tight', pad_inches=0)
    if state == 1:
        print('buildtree finished!')


def compare(args):
    k = args.k
    current_path = os.path.abspath(os.getcwd())
    parent_path = os.path.abspath(os.path.join(current_path, '..'))
    kssd_distance_path = os.path.join(parent_path, "py_kssdtree/distout/distance.out")
    mash_distance_path = os.path.join(parent_path, "mash/mash_distance.out")
    sourmash_distance_path = os.path.join(parent_path, "sourmash/distances.csv")
    bindash_distance_path = os.path.join(parent_path, "bindash/release/bindash_distance.out")
    deal_kssd(kssd_distance_path)
    deal_mash(mash_distance_path)
    deal_sourmash(k, sourmash_distance_path)
    deal_bindash(k, bindash_distance_path)
    quicktree.buildtree('kssd_dist_matrix.phy', 'kssdtree.nwk')
    quicktree.buildtree('mash_dist_matrix.phy', 'mashtree.nwk')
    quicktree.buildtree('sourmash_dist_matrix.phy', 'sourmashtree.nwk')
    quicktree.buildtree('bindash_dist_matrix.phy', 'bindashtree.nwk')
    names = ['RealTree.nwk', 'kssdtree.nwk', 'mashtree.nwk', 'sourmashtree.nwk', 'bindashtree.nwk']
    merge_nwk(names)
    print('merge finished!')


def main():
    parser = argparse.ArgumentParser(
        description='kssdtree:a fast and accurate tool for constructing phylogenetic trees.\n')
    subparsers = parser.add_subparsers(help='', dest='subcommand')
    # shuffle
    parser_shuffle = subparsers.add_parser('shuffle', help='generate shuffle file.')
    parser_shuffle.add_argument('-k', type=int, default=8, required=True,
                                help='a half of the length of k-mer,default k=8.')
    parser_shuffle.add_argument('-s', type=int, default=5, required=True,
                                help='a half of the length of k-mer substring,default s=5.')
    parser_shuffle.add_argument('-l', type=int, default=2, required=True,
                                help='the level of dimensionality reduction,default l=2.')
    parser_shuffle.add_argument('-o', type=str, default='default',
                                help="specify the output file name prefix, if not specify default shuffle named 'default.shuf' generated.")
    parser_shuffle.set_defaults(func=shuffle)

    # sketch
    parser_sketch = subparsers.add_parser('sketch', help='generate sketch files.')
    parser_sketch.add_argument('-k', type=int, default=8, help='a half of the length of k-mer,default k=8.')
    parser_sketch.add_argument('-L', type=str, default='', required=True,
                               help='dimension reduction level or provide .shuf file.')
    parser_sketch.add_argument('-r', type=str, default='', required=True, help='genome files.')
    parser_sketch.add_argument('-o', type=str, default='', required=True, help='folder path for results files.')
    parser_sketch.set_defaults(func=sketch)

    # dist
    parser_dist = subparsers.add_parser('dist',
                                        help='compute the pairwise distance of genomes and generate a distance matrix.')
    parser_dist.add_argument('-k', type=int, default=8, help='a half of the length of k-mer.')
    parser_dist.add_argument('-r', type=str, default='', required=True, help='genome files.')
    parser_dist.add_argument('-o', type=str, default='', required=True, help='folder path for results files.')
    parser_dist.add_argument('remaining_args', type=str, default='', help='genome files.')
    parser_dist.add_argument('-distance-matrix', type=str, default='kssd_dist_matrix', required=True,
                             help='create a distance matrix in phylip format.')
    parser_dist.set_defaults(func=dist)

    # buildtree
    parser_buildtree = subparsers.add_parser('buildtree', help='generate a phylogenetic tree in newick and PNG format.')
    parser_buildtree.add_argument('-i', type=str, default='kssd_dist_matrix.phy', required=True,
                                  help='input file is a distance matrix in phylip format.')
    parser_buildtree.add_argument('-o', type=str, default='kssdtree.nwk', required=True,
                                  help='output file is a tree in Newick format.')
    parser_buildtree.set_defaults(func=buildtree)

    # compare
    parser_compare = subparsers.add_parser('compare', help='compare')
    parser_compare.add_argument('-k', type=int, default=16)
    parser_compare.set_defaults(func=compare)

    args = parser.parse_args()
    subcommands = ['shuffle', 'sketch', 'dist', 'buildtree', 'compare']
    if args.subcommand is None:
        parser.print_help()
        print('Please input a subcommand.')
    elif args.subcommand in subcommands:
        args.func(args)
    else:
        print('The subcommand does not exist.')
