#!/usr/bin/env python
# coding: utf-8
# author yjw

# In[77]:


import os
import pickle
import numpy as np
import networkx as nx
from glob import glob
from os.path import basename

path = os.path.split(os.path.realpath("__file__"))[0] #源代码所在的路径

labeled = True #表明数据是否带有标记


# In[78]:


def load_graph(dir):
    
    graphs = []

    for file in glob(dir + "\\*.gexf"):
        gid = int(basename(file).split('.')[0])
        g = nx.read_gexf(file)
        g.graph["gid"] = gid
        graphs.append(g)
        if not nx.is_connected(g):  #判断连通性
            raise RuntimeError('{} not connected'.format(gid))

    return graphs


# In[79]:


def load_data(dataset): #eg: dataset = "AIDS700nef"
    
    tmp_path = path + "\\" + dataset
    
    train_graphs = []
    test_graphs = []
    
    train_path = tmp_path + "\\train"
    test_path = tmp_path + "\\test"
    
    train_graphs = load_graph(train_path)
    test_graphs = load_graph(test_path)

    return train_graphs, test_graphs


# In[108]:


def get_graph_massage(g):
    """
    输入一张图，返回 edges 和 labels
    """
    v = len(g.nodes())
    labels = [1 for i in range(v)]
    
    """重新编号"""
    id = 0
    new_id = {}
    for node in g.nodes():
        new_id[node] = id
        id += 1
    
    if labeled == True:
        hsh = list(g.nodes())
        for node in g.nodes().data(): #形如 ('7', {'type': 'C', 'label': '7'})
            labels[new_id[node[0]]] = int(node[1]["label"]) + 1
            
    edges = []
    for edge in g.edges().data(): #形如 ('7', '4', {'valence': 2, 'id': '6'})
        edges.append([new_id[edge[0]], new_id[edge[1]]])
        
    return edges, labels


# In[81]:


def make_graph_pair(g_1, g_2):
    """
    输入两张图，输出一个dict
    """
    
    graph_1, labels_1 = get_graph_massage(g_1)
    graph_2, labels_2 = get_graph_massage(g_2)
    ged = ged_dict[(g_1.graph["gid"], g_2.graph["gid"])]
    
    ret = {}
    ret["graph_1"] = graph_1
    ret["graph_2"] = graph_2
    ret["labels_1"] = labels_1
    ret["labels_2"] = labels_2
    ret["ged"] = ged
    
    return ret


# In[82]:


train_g, test_g = load_data("AIDS700nef")


# In[83]:


with open(path + "\\aids700nef_ged_astar_gidpair_dist_map.pickle", "rb") as handle:
    ged_dict = pickle.load(handle)


# In[112]:


#print(len(ged_dict)) #len(ged_dict) = 560 * 560 + 140 * 560
train_pair = []
test_pair = []
n = len(train_g)
m = len(test_g)

for i in range(n):
    for j in range(i, n, 1):
        train_pair.append(make_graph_pair(train_g[i], train_g[j]))
    for j in range(m):
        test_pair.append(make_graph_pair(test_g[j], train_g[i]))
        
print(len(train_pair), len(test_pair))


# In[115]:


with open("train_data.pickle", "wb") as handle:
    pickle.dump(train_pair, handle)
with open("test_data.pickle", "wb") as handle:
    pickle.dump(test_pair, handle)


# In[ ]:




