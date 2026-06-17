# -*- coding: utf-8 -*-

from networkx.classes.digraph import DiGraph
from itertools import product
from src.baseline.simultaneous.ts import Fts, MotionFts
from src.baseline.simultaneous.action import LocalActionModel
from src.baseline.simultaneous.buchi import Buchi

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
        for reg in self.motion_model.nodes():
            for act in self.action_model.action.keys():
                #prod_node = self._compose_and_add_node(reg, act)
                prod_node=(reg,act)
                self._add_edges_by_action(prod_node)
                self._add_edges_by_motion(prod_node)
        #add init node
        self.add_init_node()
        print('[ProdMotAct]: full motion and action model constructed with'
              ' %d states and %s transitions' % (self.number_of_nodes(),
                                                 self.number_of_edges()))
    def add_init_node(self):
        init_node=((358,15),'None')
        self.add_node(init_node,label={'b1'})
        for node in self.motion_model.nodes:
            cost=((node[0]-init_node[0][0])**2+(node[0]-init_node[0][1])**2)**0.5
            self.add_edge(init_node,(node,'None'),cost=0)
        self.graph['initial']={init_node}

    def _add_edges_by_action(self, prod_node):
        reg, act = prod_node[0], prod_node[1]
        reg_labels = self.motion_model.nodes[reg]['label']
        if (act == 'None'):
            for act_to in self.action_model.find_allowed_local_actions(reg_labels):
                prod_node_to = self._compose_and_add_node(reg, act_to)
                act_to_cost = self.action_model.action[act_to][0]
                if act_to != 'None':
                    self.add_edge(prod_node, prod_node_to, cost=act_to_cost,label=act_to)
                    self.add_edge(prod_node_to, prod_node, cost=0.01,label=act_to)

    def _add_edges_by_motion(self, prod_node):
        if self.has_node(prod_node):
            reg, act = prod_node[0], prod_node[1]
            #here is error

            for reg_to in self.motion_model.successors(reg):
                if self.has_node((reg_to,act)):
                    prod_node_to = self._compose_and_add_node(reg_to, act)
                    #here cost is error!!
                    if act!='None':
                        reg_to_cost = self.motion_model[reg][reg_to]['cost']+self.action_model.action[act][0]
                    else:
                        reg_to_cost = self.motion_model[reg][reg_to]['cost']
                    self.add_edge(prod_node, prod_node_to, cost=reg_to_cost, label='goto')

    def _compose_and_add_node(self, reg, act):
        prod_node = (reg, act)
        #if not self.has_node(prod_node):
        if 1:
            reg_labels = self.motion_model.nodes[reg]['label']
            act_labels = self.action_model.action[act][2]
            label=self.action_model.action[act][3]
            if reg_labels==label:
            # here should be changed so the act need label for local
                new_labels = reg_labels.union(act_labels)
                #print(reg_labels,act)
                self.add_node(prod_node, label=new_labels)
                if ((reg in self.motion_model.graph['initial']) and (act == 'None')):
                    self.graph['initial'].add(prod_node)
            if act_labels==set():
                new_labels = reg_labels.union(act_labels)
                #print(reg_labels,act)
                self.add_node(prod_node, label=new_labels)
                if ((reg in self.motion_model.graph['initial']) and (act == 'None')):
                    self.graph['initial'].add(prod_node)
        return prod_node

    @property
    def action_model(self):
        return self._action_model

    @property
    def motion_model(self):
        return self._motion_model


class ProdTsBuchi(DiGraph):
    """
    Class for the product between a transition system and a buchi automaton.
    """
    def __init__(self, ts, buchi):
        super(ProdTsBuchi, self).__init__(initial=set(), accept=set(),ts=ts,buchi=buchi)
        self._ts=ts
        self._buchi=buchi
        
    def construct_full_product(self,agent_ID):
        for f_ts_node in self.ts.nodes():
            for f_buchi_node in self.buchi.nodes():
                f_prod_node = self._compose_and_add_node(f_ts_node, f_buchi_node,agent_ID)
                for t_ts_node in self.ts.successors(f_ts_node):
                    for t_buchi_node in self.buchi.successors(f_buchi_node):
                        t_prod_node = self._compose_and_add_node(t_ts_node, t_buchi_node,agent_ID)
                        #print(self.ts.nodes[f_ts_node],'',f_ts_node)
                        #print(self.ts.nodes[f_ts_node])

                        label = self.ts.nodes[f_ts_node]['label']
                        cost = self.ts[f_ts_node][t_ts_node]['cost']
                        truth, dist = self.buchi.check_label_for_buchi_edge(label, f_buchi_node, t_buchi_node)
                        # NOTE here soft satisfaction is not added here, i.e., cost + alpha * dist
                        if truth:
                            self.add_edge(f_prod_node, t_prod_node, cost=cost)
        print('[ProdTsBuchi]: full product buchi automaton constructed with'
              ' %d states and %s transitions' % (self.number_of_nodes(),
                                                 self.number_of_edges()))

    def _compose_and_add_node(self, ts_node, buchi_node,agent_ID):
        prod_node = (agent_ID,ts_node, buchi_node)
        if not self.has_node(prod_node):
            virtual_label=self.buchi.nodes[buchi_node]
            self.add_node(prod_node,ts=ts_node,buchi=buchi_node,ID=agent_ID,virtual_label=virtual_label)
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


class ProdFBA(DiGraph):

    def __init__(self, PBA_list,buchi):
        super(ProdFBA, self).__init__(initial=set(), accept=set(),buchi=buchi)
        self.PBA_list=PBA_list

    def construct_full_product(self):
        for sub_PBA in self.PBA_list:
            for PBA_node in sub_PBA.nodes:
                ts_node=PBA_node[1]
                agent_ID=PBA_node[0]
                buchi_node=PBA_node[2]
                virtual=sub_PBA.nodes[PBA_node]['virtual_label']
                self.add_node(PBA_node, ts=ts_node, buchi=buchi_node, ID=agent_ID,virtual_edge=virtual)
                if PBA_node in sub_PBA.graph['accept']:
                    self.graph['accept'].add(PBA_node)
            for pre_node,sub_node in sub_PBA.edges:
                cost=sub_PBA.edges[(pre_node,sub_node)]['cost']
                self.add_edge(pre_node,sub_node,cost=cost)
        self.add_virtual_edges()
        self.graph['initial']=self.PBA_list[0].graph['initial']


    def add_virtual_edges(self):
        for node in self.graph['buchi'].nodes:
            if self.graph['buchi'].nodes[node]['virtual_edge']==1:
                if not node=='accept_all':
                    deco_set=[]
                    for pro_node in self.nodes:
                        if node==pro_node[2]:
                            deco_set.append(pro_node)
                    for pro_node in deco_set:
                        for init_node in self.PBA_list[pro_node[0]].graph['initial']:
                            if pro_node[0]<len(self.PBA_list)-1:
                                self.add_edge(pro_node,(pro_node[0]+1,init_node[1],pro_node[2]),cost=0)




    def construct_full_product1(self):

        for f_ts_node in self.ts.nodes():
            for f_buchi_node in self.buchi.nodes():
                f_prod_node = self._compose_and_add_node(f_ts_node, f_buchi_node)
                for t_ts_node in self.ts.successors(f_ts_node):
                    for t_buchi_node in self.buchi.successors(f_buchi_node):
                        t_prod_node = self._compose_and_add_node(t_ts_node, t_buchi_node)
                        # print(self.ts.nodes[f_ts_node],'',f_ts_node)
                        label = self.ts.nodes[f_ts_node]['label']
                        cost = self.ts[f_ts_node][t_ts_node]['cost']
                        truth, dist = self.buchi.check_label_for_buchi_edge(label, f_buchi_node, t_buchi_node)
                        # NOTE here soft satisfaction is not added here, i.e., cost + alpha * dist
                        if truth:
                            self.add_edge(f_prod_node, t_prod_node, cost=cost)
        print('[ProdTsBuchi]: full product buchi automaton constructed with'
              ' %d states and %s transitions' % (self.number_of_nodes(),
                                                 self.number_of_edges()))

    def _compose_and_add_node(self, ts_node, buchi_node):
        prod_node = (agent_ID, ts_node, buchi_node)
        if not self.has_node(prod_node):
            self.add_node(prod_node, ts=ts_node, buchi=buchi_node, ID=agent_ID)
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