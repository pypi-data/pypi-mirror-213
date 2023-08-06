import kssd
import quicktree
import os
import create_distance_matrix
import pkg_resources


def shuffle(k=8, s=5, l=2, o='default'):
    kssd.write_dim_shuffle_file(k, s, l, o)
    print('shuffle finished!')


def sketch(L, r, o, k=8):
    L_path = pkg_resources.resource_filename('kssdtree', '/kssdtree/' + L)
    print(L_path)
    kssd.dist_dispatch(k, L_path, r, o, 0)
    print('sketch finished!')


def dist(r, o, remaining, distance_matrix, k=8):
    kssd.dist_dispatch(k, r, o, remaining, 1)
    if distance_matrix != '':
        file_path = os.path.join(os.getcwd(), o, "distance.out")
        create_distance_matrix.create(file_path, distance_matrix)
    print('dist finished!')


def buildtree(i, o, show_branch_length=False):
    state = quicktree.buildtree(i, o)
    nwk_path = os.path.join(os.getcwd(), o)
    with open(nwk_path, 'r') as f:
        lines = f.readlines()
        merged_line = ''.join(lines)
        merged_line = merged_line.replace('\n', '')
    with open(nwk_path, 'w') as f:
        f.write(merged_line)
    from ete3 import Tree, TreeStyle, NodeStyle, TextFace
    t = Tree('kssdtree.nwk')
    n_leaves = len(t.get_leaves())
    ts = TreeStyle()
    if n_leaves > 30:
        ts.mode = "c"
    ts.show_leaf_name = False
    ts.show_branch_length = show_branch_length
    ts.show_scale = True
    ts.margin_bottom = 4
    ts.margin_top = 4
    ts.margin_left = 4
    ts.margin_right = 4
    ts.extra_branch_line_type = 0
    nstyle = NodeStyle()
    for node in t.traverse():
        node.set_style(nstyle)
        node.img_style['size'] = 0
        if node.is_leaf():
            nameF = TextFace(node.name, ftype='Verdana', fsize=8, fgcolor='black', tight_text=False, bold=False)
            node.add_face(nameF, column=0, position='branch-right')
    t.render(file_name='%%inline', w=500, tree_style=ts)
    if state == 1:
        print('buildtree finished!')
