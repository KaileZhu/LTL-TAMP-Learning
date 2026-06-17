#！/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@Date   : 2023/06 -->  
@Author : Icarus Wang
@Contact: pkuwjj1998@163.com
@Version: 1.0
@Descrip: 
'''

import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
import matplotlib.patches as patches

from MAS_TL_STAP import Buchi_poset_builder


if __name__ == '__main__':
    #==================================
    #==== Set the model parameters ====
    #==================================
    # Bringup the agents swarm
    num_agent = 1
    agents = dict()
    for a in range(1, num_agent+1):
        agents[a] = AgentModel(id=a, vel=1, omega=0.5)

    # Generate the grid map according to the figure
    img = plt.imread(r'code/zybj.png')
    res = 50
    map_x, map_y, _, = img.shape
    nodes_list = list()
    for x in range(int(res/2),map_x,res):
        for y in range(int(res/2),map_y,res):
            nodes_list.append((x,y))
    
    # Given the regions of interestd
    agents[1].initnode = (275, 75)
    agents[1].regions = {
        (75,175):set(['r1','s']), (75,275):set(['r3','s']), 
        (175,275):set(['r2','s']), 
        (125,175):set(['o']), (225,175):set(['o']), (225,225):set(['o']),
        (125,125):set(['o']),
        (125,275):set(['o']),
    }

    # Given the LTL formula
    tasks = {
        'task_1': '<>((scout && r1) && <>((scout && r2)  && <>(scout && r3)))',
        'task_2': '[](<>(scout && r1) && <>(scout && r2)  && <>(scout && r3))',
        'task_3': '<>((scout && r1) && <>((scout && r2)  && <>(scout && r3))) && [](! o)',
        'task_4': '[]<>((scout && r1) && <>((scout && r2)  && <>(scout && r3))) && [](! o)',
        'task_5': '<> r1',
    }
    is_suffix = False
    task = 'task_3'
    agents[1].local_task = tasks[task]

    agents[1].actions = {
        'Attack': (4.0, 'a', set(['attack'])), 
        'Scout': (4.0, 's', set(['scout'])),
    }

    # Generate the edges in a grid mode
    edges, edges_dis = gen_edges_from_nodes(nodes_list, 1.5*res, mode=2)

    # Prepare the node set for each agent
    for agent in agents.values():
        agent.edges = edges_dis
        for node in nodes_list:
            if node in agent.regions:
                agent.nodes[node] = agent.regions[node]
            else:
                agent.nodes[node] = set(['None'])

        # Generate the Buchi Automaton with Poset
        agent.poset = Buchi_poset_builder(agent.local_task)

    #==========================
    #==== Show the figures ====
    #==========================
    # Create figure and axes
    fig, ax = plt.subplots(figsize=(24,12))

    #-------------------------------------
    #== Draw the origin Buchi automaton ==
    #-------------------------------------
    buchi = agents[1].poset.buchi
    pos = nx.circular_layout(buchi)

    # fig = plt.figure(layout='constrained', figsize=(6, 6))

    subfig_1 = plt.subplot(121)
    nx.draw(buchi, pos, edge_color='black', width=2, linewidths=10, 
            node_size=2000, node_color='pink', alpha=1.0,
            labels={node: node for node in buchi.nodes()},
            font_size=20, font_color='black'
            )
    nx.draw_networkx_edge_labels(buchi, pos,
    edge_labels=nx.get_edge_attributes(buchi,'guard_formula'),
    font_size=14, font_color='black')


    #-------------------------------------
    #== Draw the pruned Buchi automaton ==
    #-------------------------------------
    # buchi.find_true_accepted()
    agents[1].poset.prune_automaton()
    buchi = agents[1].poset.new_buchi
    pos = nx.circular_layout(buchi)

    subfig_2 = plt.subplot(122)
    nx.draw(buchi, pos, edge_color='black', width=2, linewidths=10, 
    node_size=2000, node_color='pink', alpha=1.0,
    labels={node: node for node in buchi.nodes()},
    font_size=20, font_color='black'
    )
    nx.draw_networkx_edge_labels(buchi, pos,
    edge_labels=nx.get_edge_attributes(buchi,'guard_formula'),
    font_size=14, font_color='black')
    plt.savefig('figures/buchi.png', dpi=200, bbox_inches='tight')
    plt.show()

