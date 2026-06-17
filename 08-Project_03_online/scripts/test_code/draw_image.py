#！/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Date   : 2023/06 -->  
@Author : Icarus Wang
@Contact: pkuwjj1998@163.com
@Version: 1.0
@Descrip: 
'''
from matplotlib import pyplot as plt
import matplotlib.patches as patches

from MAS_TL_STAP.Model.utils import *

if __name__ == '__main__':
    #==================================
    #==== Set the model parameters ====
    #==================================
    # Bringup the agents swarm

    # Generate the grid map according to the figure
    img = plt.imread(r'code/zybj.png')
    res = 50
    map_x, map_y, _, = img.shape
    nodes_list = list()
    for x in range(int(res/2),map_x,res):
        for y in range(int(res/2),map_y,res):
            nodes_list.append((x,y))
    
    # Given the regions of interestd
    regions = {
        (75,175):set(['r1','a']), (75,275):set(['r3','a']), 
        (175,275):set(['r2','a']), 
        (125,175):set(['o']), (225,175):set(['o']), (225,225):set(['o']),
        (125,125):set(['o']),
    }

    # Generate the edges in a grid mode
    edges, edges_dis = gen_edges_from_nodes(nodes_list, 1.5*res, mode=2)

    #==========================
    #==== Show the figures ====
    #==========================
    # Create figure and axes
    fig, ax = plt.subplots(figsize=(12,12))
    # Display the image
    ax.imshow(img)
    # ax.axis('off')
    ax.grid(ls='--', zorder=0)

    for node_s, node_t in edges:
        x = [node_s[0], node_t[0]]
        y = [node_s[1], node_t[1]]
        ax.plot(x, y, linewidth=0.5)
    ax.scatter([x for x,y in nodes_list], [y for x,y in nodes_list],
    color='red')

    # Create a circle base patch
    circle = patches.Circle((275, 75), radius=50, edgecolor='r', 
                            facecolor='pink', alpha=0.6)
    ax.add_patch(circle)
    ax.text(x=275, y=75, s='Base', fontsize=20, color = 'black', weight='heavy',
            verticalalignment='center', horizontalalignment='center',
            bbox=dict(boxstyle='round', facecolor='red', alpha=0.5))

    # Create attack regions
    width, height = 50, 50
    for roi, labels in regions.items():
        if 'a' in labels:
            rectangle = plt.Rectangle((roi[0]-width/2, roi[1]-height/2), 
                                    width=width, height=height, 
                                    facecolor='cyan', edgecolor='black', 
                                    linestyle='-', alpha=0.6)
            ax.add_patch(rectangle)
            roi_labels = []
            for label in labels:
                if label != 'a':
                    roi_label = label
            ax.text(x=roi[0]-12.5, y=roi[1]+12.5, s=roi_label, 
                    fontsize=20, color = 'black', weight='heavy',
                    verticalalignment='center', horizontalalignment='center',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.5)
                )

    # Create obstacle regions
    for roi, labels in regions.items():
        if 'o' in labels:
            rectangle = plt.Rectangle((roi[0]-width/2, roi[1]-height/2), 
                                    width=width, height=height, 
                                    facecolor='black', edgecolor='black', 
                                    linestyle='-', alpha=0.7)
            ax.add_patch(rectangle)
            for label in labels:
                if label != 'a':
                    roi_label = label
            ax.text(x=roi[0]-12.5, y=roi[1]+12.5, s=roi_label, 
                    fontsize=20, color = 'black', weight='heavy',
                    verticalalignment='center', horizontalalignment='center',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.6)
                )

    plt.plot()
    plt.savefig('figures/map_3.png', dpi=200, bbox_inches='tight')
    plt.show()
