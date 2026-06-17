#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from collections import defaultdict
from networkx import dijkstra_predecessor_and_distance

from .product import ProdAut_Run


class LTLPlanner(object):
    """
    
    """
    def __init__(self, product):
        self.product = product
        self.Time = 0
        self.pose_current = None
        self.trace = []  # record the regions been visited
        self.trajectory = []  # record the full trajectory
        self.log_opti = [] # record [(time, prefix, suffix, prefix_cost, suffix_cost, total_cost)]
        self.log_comm = [] # record [(time, no_messages)]

    def optimal(self, beta=10, style='static'):
        self.beta = beta
        if style == 'static':
            # full graph construction
            self.run, plantime = dijkstra_plan_networkx(self.product, self.beta)
        elif style == 'centralize':
            pass
        if self.run == None:
            print('No valid plan solution!')
            return
        print('------------------------------')
        print('the prefix of plan **states**:')
        print([n for n in self.run.line])
        print('the suffix of plan **states**:')
        print([n for n in self.run.loop])
        print('------------------------------')
        print('the prefix of plan **aps**:')
        print([self.product.graph['ts'].nodes[n]['label'] for n in self.run.line])
        print('the suffix of plan **aps**:')
        print([self.product.graph['ts'].nodes[n]['label'] for n in self.run.loop])
        print('------------------------------')
        self.log_opti.append((self.Time, self.run.pre_plan, self.run.suf_plan, 
                            self.run.precost, self.run.sufcost, self.run.totalcost))
        self.time_last = self.Time
        self.Time += 1
        self.acc_change = 0
        self.index = 1
        self.segment = 'line' #line or loop
        self.next_move = self.run.pre_plan[self.index]
        return self.run.line, self.run.loop


#===================================
#==== Optimal initial synthesis ====
#===================================
def dijkstra_plan_networkx(product, beta=10):
    """
    Dijkstra

    Args:
        product (instance): product automaton.
        beta (int): .
    """
    time_start = time.time()
    runs = dict()
    loop = dict()
    #==================
    #== Minimum Loop ==
    #==================
    for state in product.graph['accept']:
        # accepting state in self-loop
        if state in product.predecessors(state):
            loop[state] = (product.edges[state, state]['cost'], [state, state])
            continue
        else:
            cost_loop = dict()
            loop_pre, loop_dis = dijkstra_predecessor_and_distance(product, state, weight='cost')
            # print('loop_dis: ', loop_dis)
            for state_pre in product.predecessors(state):
                if state_pre in loop_dis:
                    cost_loop[state_pre] = product.edges[state_pre, state]['cost'] + loop_dis[state_pre]
            if cost_loop:
                opti_pre = min(cost_loop, key=cost_loop.get)
                cost_suf = cost_loop[opti_pre]
                suffix = compute_path_from_pre(loop_pre, opti_pre)
                loop[state] = (cost_suf, suffix)
    #===================
    #== Shortest Line ==
    #===================
    for prod_init in product.graph['initial']:
        cost_line = dict()
        line_pre, line_dis = dijkstra_predecessor_and_distance(product, prod_init, weight='cost')
        # print('line_dis: ', line_dis)
        for state in loop.keys():
            if state in line_dis:
                cost_line[state] = line_dis[state] + beta*loop[state][0]
        if cost_line:
            opti = min(cost_line, key=cost_line.get)
            prefix = compute_path_from_pre(line_pre, opti)
            prefix.pop()
            cost_pre = line_dis[opti]
            suffix = loop[opti][1]
            cost_suf = loop[opti][0]
            runs[(prod_init, opti)] = (prefix, cost_pre, suffix, cost_suf)
    #=========================
    #== Optimal Combination ==
    #=========================
    if runs:
        prefix, cost_pre, suffix, cost_suf = min(runs.values(), key=lambda p: p[1]+beta*p[3])
        run = ProdAut_Run(product, prefix, cost_pre, suffix, cost_suf, cost_pre+beta*cost_suf)
        print('-------------------------------------------------------------------')
        print('Dijkstra_plan_networkx done within %.4f: precost %.4f, sufcost %.4f' 
                %(time.time()-time_start, cost_pre, cost_suf))
        return run, time.time()-time_start
    print('!!!!!!!!!!!!!!!!')
    print('No accepting run found in optimal planning!')
    return None, None

def dijkstra_plan_optimal(product, beta=10, set_start=None):
    time_start = time.time()
    runs = {}
    set_accept = product.graph['accept']
    if set_start == None:
        set_init = product.graph['initial']
    else:
        set_init == set_start
    loop_dict = dict()
    for prod_node_init in set_init:
        for prefix, precost in dijkstra_targets(product, prod_node_init, set_accept):
            pass

def dijkstra_targets(product, prod_source, prod_targets):
    """
    For product graph only, find the shortest path from source to a set of targets.
    """
    tovisit = set()
    visited = set()
    dist = defaultdict(lambda: float('inf'))
    node_pre = dict()
    dist[prod_source] = 0
    tovisit.add(prod_source)
    feasible_targets = set()
    for pord_accept in prod_targets:
        accept_pre_set = product.accept_predecessors(pord_accept)

def compute_path_from_pre(pre_dict, goal):
    gn = goal  # goal node
    path = [gn]
    while gn in pre_dict:
        pn_list = pre_dict[gn]
        if not pn_list:
            break
        # there might be multi pre states
        if pn_list[0] == gn:
            break
        pn = pn_list[0]
        path.append(pn)
        gn = pn
    path.reverse()  # Reverse the elements in the list.
    return path
