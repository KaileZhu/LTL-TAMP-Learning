# -*- coding: utf-8 -*-
import numpy as np
import copy
import collections

def compute_distance(pose1, pose2, measure='2-norm', unit=1.0, under_flow=0.001):
    if measure == '2-norm':
        relative_pose = [pose1[k] - pose2[k] for k in range(len(pose1))]
        return np.linalg.norm(relative_pose) + under_flow

    
def find_closest_node(nodes, pose):
    node = min(nodes, key=lambda n: compute_distance(n, pose))
    return node


def reach_waypoint(pose, waypoint, margin):
    if compute_distance(pose, waypoint) <= margin:
        return  True
    else:
        return  False

def add_labels_of_macro_action(Product_TS,regions,macro_action):
    Product_macro_ts=copy.deepcopy(Product_TS)
    for node in Product_TS.nodes:
        regions_set=counter_node_regions(node)
        #here we need to change to fit the new transition of the label as each action+placename
        #and the check of label need to corresponding to the currenct place
        #the place label are added for
        for region,index in regions_set.items():
            pos=regions[region]
            label=check_if_macro_actions(macro_action,index,pos)
            Product_macro_ts.nodes[node]['labels']=Product_TS.nodes[node]['labels'] | label
    return Product_macro_ts


def counter_node_regions(nodes):
    nodes_set=[]
    regions_set={}
    for node in nodes:
        nodes_set.append(node[0])
    node_dic=collections.Counter(nodes_set)
    for key,number in node_dic.items():
        regions_set[key]=(number,[i for i,x in enumerate(nodes_set) if x==key],
                          dict(collections.Counter([nodes[i][1] for i,x in enumerate(nodes_set) if x==key])))
    return regions_set

def check_if_macro_actions(macro_action, index, pos):
    act_set = set(index[2].items())
    for act, tuple in macro_action.items():
        if tuple[1].issubset(act_set):
            return set([act + pos])
        else:
            return set()