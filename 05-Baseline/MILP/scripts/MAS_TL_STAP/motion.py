#!/usr/bin/env python3

import numpy as np
import networkx as nx

from PIL import Image
# from sklearn.cluster import MeanShift
from networkx.classes.digraph import DiGraph

# from .dijkstra import *
from .utils import *


import math
from itertools import product
from networkx.classes.digraph import DiGraph

from .buchi import BuchiAuto
from .LTL2BA.boolean_formulas.parser import parse_guard
from .utils import norm_distance


class MotionFts(DiGraph):
    def __init__(self, img, res, init_node):
        super().__init__()
        self._img = img.transpose(Image.FLIP_TOP_BOTTOM)  # flip the img top to down
        self._res = res
        self._init_node = init_node
        self.regions = dict()
        self.img_to_gridmap()

    def img_to_gridmap(self, self_loop=False):
        """
        Read the file to get the figure and flip it top to down,
        then discretize it into grid map.
        ----------
        Args:
            self_loop: (bool), False for no self-loop, True for self-loop
        """
        # grid discretization
        for x in range(self.init_node[0], self.img.width, self.res):
            for y in range(self.init_node[1], self.img.height, self.res):
                self.add_node((x,y), label=None)
        # Generate the edges in a grid mode
        for node_s in self.nodes():
            for node_t in self.nodes():
                dis = np.linalg.norm(np.array(node_s)-np.array(node_t), ord=2)
                dis = np.around(dis, 3)
                if dis == 0 and self_loop:
                    self.add_edge(node_s, node_t, cost=dis, )
                elif dis > 0 and dis <= 1.5*self.res:
                    self.add_edge(node_s, node_t, cost=dis, )

    def add_full_regions(self, regions):
        """
        Add regions of interest according to the task demo.
        ----------
        Args:
            regions:(list), [{'name': , 'type': , 'pos': , 'range': , 'color': }, ]
        """
        for roi in regions:
            # find the closest node
            x_init, y_init = self.init_node
            node = (
                np.round((roi['pos'][0]-x_init)/self.res)*self.res + x_init,
                np.round((roi['pos'][1]-y_init)/self.res)*self.res + y_init
            )
            self.add_node(node, label=roi['name'])
            self.regions[node] = {
                'name': roi['name'],
                'range': roi['range'],
                'color': roi['color'],
            }
            if roi['name'] == 'obstacle':
                # edges_t_node = [(node, adj) for adj in self.adj[node]]
                edges_t_node = [(s,t) for s,t in self.edges if s == node]
                edges_f_node = [(s,t) for s,t in self.edges if t == node]
                self.remove_edges_from(edges_t_node + edges_f_node)

    def single_source_dijkstra(self, source, target):
        """
        Find the path by dijkstra algorithm.
        ----------
        Args:
            source:(list or tuple), source node;
            target:(list or tuple), target node.
        ----------
        Returns:
            distance, path: pair of dictionaries, or numeric and list.
        """
        source = tuple(source)
        target = tuple(target)
        return nx.single_source_dijkstra(self, source, target, weight='cost')

    def full_regions_dijkstra(self):
        """
        Find the path by bidirectional dijkstra algorithm.
        ----------
        Args:
            sources:(list), a list of source nodes;
            targest:(list), a list of target nodes.
        ----------
        Returns:
            distance, path: pair of dictionaries, or numeric and list.
        """
        self.costmap = dict()
        for s in self.regions:
            self.costmap[s] = dict()
            for t in self.regions:
                len, path = nx.bidirectional_dijkstra(self, s, t, weight='cost')
                self.costmap[s][t] = {'len': len, 'path': path, }

    @property
    def img(self):
        return self._img

    @property
    def res(self):
        return self._res

    @property
    def init_node(self):
        return self._init_node

class Fts(DiGraph):
    """
    Base class for finite transition systems.
    """
    def __init__(self, **kwargs):
        super(Fts, self).__init__(initial=set())
        # super().__init__(initial=set())

class ActionModel(object):
    """
    class for actions.
    """
    def __init__(self, action_dict, under_flow=0.001):
        self.action = dict()
        for act_name, attrib in action_dict.items():
            cost, guard_formula, labels = attrib[0:3]
            if guard_formula is None:
                guard_expr = parse_guard('1')  # gurad experssion
            else:
                guard_expr = parse_guard(guard_formula)
            self.action[act_name] = (cost, guard_expr, labels)
        self.action['None'] = (under_flow, parse_guard('1'), set())

    def find_allowed_actions(self, props):
        """
        Args:
            props (set): set of propositions that are true.
        """
        allowed_actions = set()
        for act_name, attrib in self.action.items():
            guard_expr = attrib[1]
            if guard_expr.check(props):
                allowed_actions.add(act_name)
        return allowed_actions


class LocalActionModel(object):
    """
    class for local actions.
    """
    def __init__(self, action_dict, under_flow=0.001):
        self.action = dict()
        for act_name, attrib in action_dict.items():
            cost, guard_formula, labels = attrib[0:3]
            if guard_formula is None:
                guard_expr = parse_guard('1')  # guard experssion
            else:
                guard_expr = parse_guard(guard_formula)
            self.action[act_name] = (cost, guard_expr, labels)
        self.action['None'] = (under_flow, parse_guard('1'), set())

    def find_allowed_local_actions(self, props):
        """
        Args:
            props (set): set of propositions that are true.
        """
        allowed_actions = set()
        for act_name, attrib in self.action.items():
            guard_expr = attrib[1]
            if guard_expr.check(props):
                allowed_actions.add(act_name)
        return allowed_actions