# -*- coding: utf-8 -*-
from networkx.classes.digraph import DiGraph
from itertools import product

from ltl_mas.tools.utils import compute_distance, find_closest_node


class Fts(DiGraph):
    """
    Base class for finite transition systems.
    """
    def __init__(self, **kwargs):
        super(Fts, self).__init__(initial=set())


class MotionFts(Fts):
    '''
    Class for motion transition systems.
    '''
    def __init__(self, nodes, symbols):
        """
        Args:
            nodes: dict. {node_pose : {'l1', ...}} pair of node pose
                   and list of node labels.
        """
        super(MotionFts, self).__init__()
        for (node, labels) in nodes.items():
            self.add_node(node, labels=labels)

    def add_edges(self, edges, undirected=True, unit_cost=1.0,
                  self_loop=True, under_flow=0.001):
        """
        Args:
            edges: list. [(from_node, to_node),...] list of edges.
            undirected: boolean. True if both directions are added.
            unit_cost: positive float. Unit cost of each edge.
            self_loop: boolean. If self loop is added.
            under_flow: float. Minimum distance for computation.
        """
        for edge in edges:
            f_node, t_node = edge[0], edge[1]
            dist = compute_distance(f_node, t_node, measure='2-norm',
                                    unit=unit_cost, under_flow=under_flow)
            self.add_edge(f_node, t_node, cost=dist)
            if undirected:
                self.add_edge(t_node, f_node, cost=dist)
        if self_loop:
            for node in self.nodes():
                self.add_edge(node, node, cost=under_flow)

    def add_edges_by_node_label(self, edges, undirected=True, unit_cost=1.0,
                                self_loop=True, under_flow=0.001):
        """
        Args:
            edges: list. [(from_label, to_label),...] list of node labels.
            undirected: boolean. True if both directions are added.
            unit_cost: positive float. Unit cost of each edge.
            self_loop: boolean. If self loop is added.
            under_flow: float. Minimum distance for computation.
        """
        actual_edges = list(edges)
        for nd, data in self.nodes.data():
            labels = data['labels']
            for k, label_edge in enumerate(edges):
                for j, label in enumerate(label_edge):
                    if label in labels:
                        actual_edges[k][j] = nd
        self.add_edges(actual_edges, undirected=undirected, unit_cost=unit_cost,
                       self_loop=self_loop, under_flow=under_flow)

    def add_full_edges(self, unit_cost=1.0, under_flow=0.001):
        """
        Construct complete graph.
        """
        full_edges = product(self.nodes, self.nodes)
        self.add_edges(full_edges, undirected=False, unit_cost=unit_cost,
                       self_loop=False, under_flow=under_flow)

    def set_initial(self, pose):
        init_node = find_closest_node(self.nodes, pose)
        self.graph['initial'] = set([init_node])
        return init_node
