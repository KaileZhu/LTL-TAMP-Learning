# -*- coding: utf-8 -*-

from cmath import inf
import math
import time
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse, Circle
from matplotlib import colors
from matplotlib import ticker

from map import Map
from searchmethod import Dijkstra

def if_graphconnect(G):
    """
    #Warshell algorithm to judge whether the graph is connected.
    Core: find the transitive closure of a graph (it can be directed or undirected)

    Input: 
        G: the adjacency matrix G of the graph with n vertices
        radius: the connected radius
    Args:
        R: the reachability matrix

    Output: True or False

    """
    dim = np.shape(G)[0]  # dimension of the graph

    G = np.mat(G)
    R = np.mat(np.zeros((dim, dim)))

    for i in range(dim):
        R += G ** i
    
    if R.all() > 0:
        return True

    return False


if __name__ == '__main__':

    map_size = 100
    agent_radius = 1.5
    comm_radius = 5
    map = Map(map_size, map_size, agent_radius)

    #==============================================
    # Set obstacle vertexs
    #==============================================
    obstacle_points = []

    edges = list(np.arange(19, 26)) + list(np.arange(35, 46)) \
            + list(np.arange(55, 66)) + list(np.arange(75, 82))
    for i in edges:
        for j in range(49, 52):
            obstacle_points.append((i,j))
    
    edges = list(np.arange(19, 22)) + list(np.arange(79, 82))
    for i in edges:
        for j in range(49, 72):
            obstacle_points.append((i,j))

    edges = list(np.arange(39, 42)) + list(np.arange(59, 62))
    for i in edges:
        for j in range(29, 72):
            obstacle_points.append((i,j))
    
    edges = list(np.arange(19, 26)) + list(np.arange(35, 42)) \
             + list(np.arange(59, 66)) + list(np.arange(75, 82))
    for i in edges:
        for j in range(69, 72):
            obstacle_points.append((i,j))

    edges = list(np.arange(39, 46)) + list(np.arange(55, 62))
    for i in edges:
        for j in range(29, 32):
            obstacle_points.append((i,j))

    obstacle_points = list(set(obstacle_points))
    map.obstacle(obstacle_points)

    #==============================================
    # Dijkstra discrete planning
    #==============================================    
    dijkstra = Dijkstra(map.obstacle_map)
    start_points = [(30,60), (30,55), 
                    (75,65), (70,40), 
                    (25,35), (75,25)]
    agent_num = int(len(start_points)/2)
    time_start = time.process_time()

    costmap_dict_multi, costmap_list_multi, costmap_xy_multi = dijkstra.planning_map_multiagent(start_points)
    comm_pos_set, agent_distance = dijkstra.min_max_distance(start_points, costmap_list_multi)
    print("This process 1 executes for %.4f s" %((time.process_time()-time_start)))
    #finalpath = dijkstra.path_generate_multi(start_points, comm_pos_set)
    region_radius = (agent_num - 1) * comm_radius

    adjacency = np.zeros((agent_num, agent_num))
    
    num_comm_point = 0  # choose a communication point
    i_set = [k for k in range(comm_pos_set[num_comm_point][0]-region_radius, comm_pos_set[num_comm_point][0]+region_radius+1)]
    j_set = [k for k in range(comm_pos_set[num_comm_point][1]-region_radius, comm_pos_set[num_comm_point][1]+region_radius+1)]
    # generate search set
    search_point_set = []
    for i in i_set:
        for j in j_set:
            if not map.obstacle_map[i][j]:
                search_point_set.append((i,j))

    max_distance = np.inf
    comm_pos_multi_set = [[[(0,0) for n in range(agent_num)]] for i in range(5)] #initial five position
    comm_agent_distance = [0.0 for i in range(5)]
    time_start = time.process_time()
    count = 1
    for i1, j1 in search_point_set:
        for i2, j2 in search_point_set:
            for i3, j3 in search_point_set:
                # construct the adjacency matrix
                """
                adjacency_4 = [[inf,math.hypot(i1-i2, j1-j2),math.hypot(i1-i3, j1-j3),math.hypot(i1-i4, j1-j4)],
                            [inf,inf,math.hypot(i2-i3, j2-j3),math.hypot(i2-i4, j2-j4)],
                            [inf,inf,inf,math.hypot(i3-i4, j3-j4)],
                            [inf,inf,inf,inf]]
                """
                adjacency = [[inf,math.hypot(i1-i2, j1-j2),math.hypot(i1-i3, j1-j3)],
                            [inf,inf,math.hypot(i2-i3, j2-j3)],
                            [inf,inf,inf]]

                for i in range(agent_num):
                    for j in range(agent_num):
                        if adjacency[i][j] <= comm_radius:
                            adjacency[i][j] = 1
                        else:
                            adjacency[i][j] = 0

                adjacency = np.mat(adjacency) + np.mat(adjacency).transpose()

                if if_graphconnect(adjacency):
                    p_distance = [costmap_list_multi[0][i1][j1] + costmap_list_multi[1][i1][j1],
                                    costmap_list_multi[2][i2][j2] + costmap_list_multi[3][i2][j2],
                                    costmap_list_multi[4][i3][j3] + costmap_list_multi[5][i3][j3]]
                
                    if max(p_distance) <= max_distance:
                        max_distance = max(p_distance)
                        for k in range(4):
                            comm_pos_multi_set[k] = comm_pos_multi_set[k+1]
                            comm_agent_distance[k] = comm_agent_distance[k+1]

                        comm_pos_multi_set[4] = [(i1,j1), (i2,j2), (i3,j3)]
                        comm_agent_distance[4] = max_distance
                count += 1
        print(count)

    print("This process 2 executes for %.4f s" %((time.process_time()-time_start)))
    print("The distance of each agents is " + str(comm_agent_distance))
    print("The position of each agents is " + str(comm_pos_multi_set))