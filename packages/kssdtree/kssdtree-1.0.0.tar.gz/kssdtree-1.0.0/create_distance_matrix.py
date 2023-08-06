import pandas as pd
import warnings
import os

warnings.filterwarnings('ignore')


def create(path, name):
    current_path = os.getcwd()
    print('dealing distance.out...')
    df = pd.read_csv(path, delimiter='\t')
    new_df = df[['Qry', 'Ref', 'MashD']]
    # deal fasta.gz and fastaq.gz
    if '.fasta.gz' in new_df['Qry'][0] or '.fastq.gz' in new_df['Qry'][0] or '.fna.gz' in new_df['Qry'][0]:
        new_df['Ref'] = new_df['Ref'].apply(lambda x: x.split('.')[-3].split('/')[-1])
        new_df['Qry'] = new_df['Qry'].apply(lambda x: x.split('.')[-3].split('/')[-1])
    # deal .fa
    elif new_df['Qry'][0][-3:] == '.fa':
        new_df['Qry'] = new_df['Qry'].apply(lambda x: x.split('.')[-2].split('/')[-1].split('_')[0])
        new_df['Ref'] = new_df['Ref'].apply(lambda x: x.split('.')[-2].split('/')[-1].split('_')[0])
    elif new_df['Qry'][0][-6:] == '.fasta':
        new_df['Qry'] = new_df['Qry'].apply(lambda x: x.split('/')[1][:-6])
        new_df['Ref'] = new_df['Ref'].apply(lambda x: x.split('/')[1][:-6])
    else:
        pass
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
    example: a distance matrix in phylip format
    3
    Seq1         0.00000    0.10000    0.30000
    Seq2         0.10000    0.00000    0.20000
    Seq3         0.30000    0.20000    0.00000
    '''
    with open(current_path + '/' + name + '.phy', 'w') as f:
        f.write(str(len(seq_names)) + '\n')
        for i in range(n_seqs):
            f.write(seq_names[i])
            for j in range(n_seqs):
                if i == j:
                    f.write('\t{:.5f}'.format(0.0))
                else:
                    f.write('\t{:.5f}'.format(data[seq_names[i]][seq_names[j]]))
            f.write('\n')
    print('create distance_matrix finished!')


