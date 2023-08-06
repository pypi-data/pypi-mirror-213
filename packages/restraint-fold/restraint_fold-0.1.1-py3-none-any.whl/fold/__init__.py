# MIT License
#
# Copyright (c) 2023 Dechin Chen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
sys.setrecursionlimit(90000000)

import numpy as np
from hadder.parsers import read_pdb
from hadder.constants import hnames

def get_hbonds(pdb_name, hbond_length=3.5):
    res = read_pdb(pdb_name)
    atom_names = res[5]
    group_names = res[0]
    crds = res[6]
    res_names = res[7]
    res_ids = res[8]
    n_index = []
    o_index = []
    h_index = []
    for i, name in enumerate(atom_names):
        if name.startswith('H'):
            h_index.append(i)
        elif name.startswith('N'):
            n_index.append(i)
        elif name.startswith('O'):
            o_index.append(i)
        else:
            continue
    n_index = np.array(n_index, np.int32)
    o_index = np.array(o_index, np.int32)
    h_index = np.array(h_index, np.int32)

    n_crd = crds[n_index]
    o_crd = crds[o_index]
    h_crd = crds[h_index]

    dis_oh = np.linalg.norm(o_crd - h_crd[:, None, :], axis=-1)
    mask_oh = np.where(dis_oh <= hbond_length)
    mh_index_o = mask_oh[0]
    mo_index = mask_oh[1]
    xh_index_o = []
    for idx in mh_index_o:
        h_idx = h_index[idx]
        res_name = res_names[h_idx]
        res_id = res_ids[h_idx]
        res_dict = hnames[res_name]
        for key in res_dict:
            if atom_names[h_idx] not in res_dict[key]:
                continue
            for cbk in range(30):
                if atom_names[h_idx - cbk - 1] == key and res_ids[h_idx - cbk - 1] == res_id:
                    xh_index_o.append(h_idx - cbk - 1)
                    break
    xh_index_o = np.array(xh_index_o, np.int32)
    dis_nh = np.linalg.norm(n_crd - h_crd[:, None, :], axis=-1)
    mask_nh = np.where(dis_nh <= hbond_length)
    mh_index_n = mask_nh[0]
    mn_index = mask_nh[1]
    xh_index_n = []

    for idx in mh_index_n:
        h_idx = h_index[idx]
        res_name = res_names[h_idx]
        res_id = res_ids[h_idx]
        res_dict = hnames[res_name]
        for key in res_dict:
            if atom_names[h_idx] not in res_dict[key]:
                continue
            for cbk in range(30):
                if atom_names[h_idx - cbk - 1] == key and res_ids[h_idx - cbk - 1] == res_id:
                    xh_index_n.append(h_idx - cbk - 1)
                    break
    xh_index_n = np.array(xh_index_n, np.int32)

    hbonds = []
    res_bonds = []
    for i, idx in enumerate(mo_index):
        if res_ids[o_index[idx]] == res_ids[h_index[mh_index_o[i]]]:
            continue
        hbonds.append([xh_index_o[mh_index_o[i]], h_index[mh_index_o[i]], o_index[idx]])
        res_bonds.append([res_ids[o_index[idx]], res_ids[h_index[mh_index_o[i]]]])

    for i, idx in enumerate(mn_index):
        if res_ids[n_index[idx]] == res_ids[h_index[mh_index_n[i]]]:
            continue
        hbonds.append([xh_index_n[mh_index_n[i]], h_index[mh_index_n[i]], n_index[idx]])
        res_bonds.append([res_ids[n_index[idx]], res_ids[h_index[mh_index_n[i]]]])

    hbonds = np.array(hbonds, np.int32)
    res_bonds = np.array(res_bonds, np.int32)

    xy_vector = crds[hbonds[:, 2]] - crds[hbonds[:, 1]]
    xy = np.linalg.norm(xy_vector, axis=-1)
    xy_filter = np.where(xy <= hbond_length)
    hbonds = hbonds[xy_filter]
    res_bonds = res_bonds[xy_filter]

    xh_vector = crds[hbonds[:, 1]] - crds[hbonds[:, 0]]
    hy_vector = crds[hbonds[:, 2]] - crds[hbonds[:, 0]]

    cos_h = np.einsum('ij,ij->i', xh_vector, hy_vector) / (np.linalg.norm(xh_vector, axis=-1) + 1e-08) / (
            np.linalg.norm(hy_vector, axis=-1) + 1e-08)
    angle_filter = np.where(cos_h > np.cos(np.pi * 43.1 / 180))

    hbonds = hbonds[angle_filter]
    res_bonds = res_bonds[angle_filter]

    res_bonds = np.unique(res_bonds, axis=0)
    return res_bonds

def get_alpha(pdb_name, hbond_length=3.5):
    res_bonds = get_hbonds(pdb_name, hbond_length=hbond_length)
    alpha = []
    counter = 0
    min_alpha = 4
    for index in range(np.max(res_bonds) - 3):
        tmp_bond_1 = np.array([index, index + 4])
        tmp_bond_2 = tmp_bond_1 + 1
        tmp_bond_3 = tmp_bond_1 + 2
        tmp_bond_4 = np.array([index, index + 3])
        if np.sum(np.isin(res_bonds, tmp_bond_1).sum(axis=-1) == 2) > 0:
            counter += 1
            continue
        elif np.sum(np.isin(res_bonds, tmp_bond_4).sum(axis=-1) == 2) > 0:
            counter += 1
            continue
        elif counter > 2 and np.sum(np.isin(res_bonds, tmp_bond_2).sum(axis=-1) == 2) > 0:
            counter += 1
            continue
        # elif counter>0 and np.sum(np.isin(res_bonds, tmp_bond_3).sum(axis=-1)==2)>0:
        #     counter += 1
        #     continue
        elif counter < min_alpha:
            counter = 0
            continue
        else:
            alpha.extend([index])
            alpha.extend([index - 1 - i for i in range(counter)])
            counter = 0
            continue
    alpha = np.sort(np.array(alpha, np.int32))
    return alpha

tmp_beta = []
beta = []
counter = 0

def _get_beta(res_bonds, start, end):
    global beta
    global counter
    global tmp_beta
    pair = np.array([start-1, end+1])
    pair_2 = np.array([start-2, end+2])
    if np.sum(np.isin(res_bonds, pair).sum(axis=-1)==2)>0:
        if start-1 not in tmp_beta:
            tmp_beta.extend([start-1])
        if end+1 not in tmp_beta:
            tmp_beta.extend([end+1])
        counter += 1
        return _get_beta(res_bonds, start-1, end+1)
    elif counter > 1 and np.sum(np.isin(res_bonds, pair).sum(axis=-1)==2)>0:
        if start-2 not in tmp_beta:
            tmp_beta.extend([start-2])
        if end+2 not in tmp_beta:
            tmp_beta.extend([end+2])
        counter += 1
    else:
        if counter > 4:
            beta.extend(tmp_beta)
        counter = 1
        tmp_beta = []
        return 0

def get_beta(pdb_name, hbond_length=3.5):
    res_bonds = get_hbonds(pdb_name, hbond_length=hbond_length)
    global tmp_beta
    global beta
    for index, bond in enumerate(res_bonds):
        start = bond[0]
        end = bond[1]
        pair = np.array([start-1, end+1])
        if np.sum(np.isin(res_bonds, pair).sum(axis=-1)==2)>0:
            tmp_beta.extend([start, end])
            _ = _get_beta(res_bonds, start, end)
        else:
            continue
    beta = np.array(beta, np.int32)
    beta = np.unique(beta)
    beta = np.sort(beta)
    return beta

def get_residue_type(pdb_name, alpha, beta):
    res = read_pdb(pdb_name)
    res_ids = res[8]
    final_res = np.unique(res_ids)
    res_dict = {re:0 for re in final_res}
    for key in alpha:
        res_dict[key] = 1
    for key in beta:
        res_dict[key] = -1
    return res_dict
