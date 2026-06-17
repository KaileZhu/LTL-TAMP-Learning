# -*- coding: utf-8 -*-

from networkx.classes.digraph import DiGraph
from itertools import product
from src.ltl_mas.models.ts import Fts, MotionFts
from src.ltl_mas.models.action import LocalActionModel
from src.ltl_mas.models.buchi import Buchi

class ProdMotAct(Fts):
    """
    Class for the product between the motion transition system and the local action model.
    Note the product is also a finite transition system.
    """
    def __init__(self, motion_model, action_model):
        super(ProdMotAct, self).__init__(initial=set())#调用父类的构造方法
        self._check_input_format(motion_model, action_model)

    def _check_input_format(self, motion_model, action_model):
        if isinstance(motion_model, MotionFts):
            self._motion_model = motion_model
        else:
            raise ValueError('[ProdMotAct]: Input motion model is not an'
                             ' instance of MotionFts')
        if isinstance(action_model, LocalActionModel):
            self._action_model = action_model
        else:
            raise ValueError('[ProdMotAct]: Input action model is not an'
                             ' instance of LocalActionModel')

    def construct_full_product(self):        
        for reg in self.motion_model.nodes():
            for act in self.action_model.action.keys():
                prod_node = self._compose_and_add_node(reg, act)
                self._add_edges_by_action(prod_node)
                self._add_edges_by_motion(prod_node)
        print('[ProdMotAct]: full motion and action model constructed with'
              ' %d states and %s transitions' % (self.number_of_nodes(),
                                                 self.number_of_edges()))

    def _add_edges_by_action(self, prod_node):
        reg, act = prod_node[0], prod_node[1]
        reg_labels = self.motion_model.nodes[reg]['labels']
        if (act == 'None'):
            for act_to in self.action_model.find_allowed_local_actions(reg_labels):
                prod_node_to = self._compose_and_add_node(reg, act_to)
                act_to_cost = self.action_model.action[act_to][0]
                if act_to != 'None':
                    self.add_edge(prod_node, prod_node_to, cost=act_to_cost,labels=act_to)

    def _add_edges_by_motion(self, prod_node):
        reg, act = prod_node[0], prod_node[1]
        for reg_to in self.motion_model.successors(reg):
            prod_node_to = self._compose_and_add_node(reg_to, 'None')
            reg_to_cost = self.motion_model[reg][reg_to]['cost']
            self.add_edge(prod_node, prod_node_to, cost=reg_to_cost, labels='goto')        

    def _compose_and_add_node(self, reg, act):
        prod_node = (reg, act)
        if not self.has_node(prod_node):
            reg_labels = self.motion_model.nodes[reg]['labels']
            act_labels = self.action_model.action[act][2]
            new_labels = reg_labels.union(act_labels)
            self.add_node(prod_node, labels=new_labels)
            if ((reg in self.motion_model.graph['initial']) and (act == 'None')):
                self.graph['initial'].add(prod_node)
        return prod_node

    @property
    def action_model(self):
        return self._action_model

    @property
    def motion_model(self):
        return self._motion_model


class ProdFts(Fts):
    """
    Class for the product between *arbitrary* number of finite transition systems.
    Note the product is also a finite transition system.
    """
    def __init__(self, all_fts):
        """
        Args:
            all_fts: List or Tuple. List of all fts that should be multiplied.
        """
        super(ProdFts, self).__init__(initial=set())
        self._check_input_format(all_fts)

    def _check_input_format(self, all_fts):
        if (not isinstance(all_fts, list)) and (not isinstance(all_fts, tuple)):
            raise ValueError('[ProdFts]: Input all_fts is not a list of tuple')
        for single_fts in all_fts:
            if not isinstance(single_fts,Fts):
                raise ValueError('[ProdFts]: Input fts is not an instance of Fts')
        self._all_fts = all_fts

    def construct_full_product(self):
        for f_prod_node in product(*[single_fts.nodes() for single_fts in self.all_fts]):
            self._add_prod_node(f_prod_node)
            successors = self._find_all_successors(f_prod_node)
            for t_prod_node in product(*successors):
                full_cost = self._compute_full_cost(f_prod_node, t_prod_node)
                self.add_edge(f_prod_node, t_prod_node, cost=full_cost)
        print('[ProdFts]: full product Fts of %d Fts is computed with '
              ' %d states and %s transitions' % (len(self.all_fts),
                                                 self.number_of_nodes(),
                                                 self.number_of_edges()))

    def _add_prod_node(self, prod_node):
        #if not self.has_node(prod_node):#th
        full_labels = self._compute_full_labels(prod_node)
        self.add_node(prod_node, labels=full_labels)
        if self._check_initial_node(prod_node):
            self.graph['initial'].add(prod_node)

    
    def _compute_full_labels(self, prod_node):
        full_labels = set()
        for k, k_ts_node in enumerate(prod_node):
            k_labels = self.all_fts[k].nodes[k_ts_node]['labels']
            full_labels.update(k_labels)
        return full_labels

    def _check_initial_node(self, prod_node):
        for k, k_ts_node in enumerate(prod_node):
            if k_ts_node not in self.all_fts[k].graph['initial']:
                return False
        return True

    def _find_all_successors(self, prod_node):
        successors = []
        for k, k_ts_node in enumerate(prod_node):
            k_successors = self.all_fts[k].successors(k_ts_node)
            successors.append(k_successors)
        return successors

    def _compute_full_cost(self, f_prod_node, t_prod_node):
        full_cost = 0.0
        for k, k_f_ts_node in enumerate(f_prod_node):
            k_t_ts_node = t_prod_node[k]
            k_cost = self.all_fts[k][k_f_ts_node][k_t_ts_node]['cost']
            full_cost += k_cost
        return full_cost

    @property
    def all_fts(self):
        return self._all_fts


class ProdTsBuchi(DiGraph):
    """
    Class for the product between a transition system and a buchi automaton.
    """
    def __init__(self, ts, buchi):
        super(ProdTsBuchi, self).__init__(initial=set(), accept=set())
        self._check_input_format(ts, buchi)

    def _check_input_format(self, ts, buchi):
        if isinstance(ts, Fts):
            self._ts = ts
        else:
            raise ValueError('[ProdTsBuchi]: Input transition system is not an'
                             ' instance of Fts')
        if isinstance(buchi, Buchi):
            self._buchi = buchi
        else:
            raise ValueError('[ProdTsBuchi]: Input buchi automaton is not an'
                             ' instance of Buchi')
        
    def construct_full_product(self):
        for f_ts_node in self.ts.nodes():
            for f_buchi_node in self.buchi.nodes():
                f_prod_node = self._compose_and_add_node(f_ts_node, f_buchi_node)
                for t_ts_node in self.ts.successors(f_ts_node):
                    for t_buchi_node in self.buchi.successors(f_buchi_node):
                        t_prod_node = self._compose_and_add_node(t_ts_node, t_buchi_node)
                        #print(self.ts.nodes[f_ts_node],'',f_ts_node)
                        label = self.ts.nodes[f_ts_node]['labels']
                        cost = self.ts[f_ts_node][t_ts_node]['cost']
                        truth, dist = self.buchi.check_label_for_buchi_edge(label, f_buchi_node, t_buchi_node)
                        # NOTE here soft satisfaction is not added here, i.e., cost + alpha * dist
                        if truth:
                            self.add_edge(f_prod_node, t_prod_node, cost=cost)
        print('[ProdTsBuchi]: full product buchi automaton constructed with'
              ' %d states and %s transitions' % (self.number_of_nodes(),
                                                 self.number_of_edges()))

    def _compose_and_add_node(self, ts_node, buchi_node):
        prod_node = (ts_node, buchi_node)
        if not self.has_node(prod_node):
            self.add_node(prod_node)
            if ((ts_node in self.ts.graph['initial']) and
                (buchi_node in self.buchi.graph['initial'])):
                self.graph['initial'].add(prod_node)
            if (buchi_node in self.buchi.graph['accept']):
                self.graph['accept'].add(prod_node)
        return prod_node

    @property
    def ts(self):
        return self._ts

    @property
    def buchi(self):
        return self._buchi
