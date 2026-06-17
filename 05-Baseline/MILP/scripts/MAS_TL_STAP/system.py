#!/usr/bin/env python3

import copy
import collections

from .product import ProdFts, ProdTsBuchi


def add_labels_of_macro_action(Product_TS, regions, macro_action):
    Product_macro_ts=copy.deepcopy(Product_TS)
    for node in Product_TS.nodes:
        regions_set=counter_node_regions(node)
        #here we need to change to fit the new transition of the label as each action+placename
        #and the check of label need to corresponding to the current place
        #the place label are added for
        for region,index in regions_set.items():
            pos=regions[region]
            label=check_if_macro_actions(macro_action,index,pos)
            Product_macro_ts.nodes[node]['label']=Product_TS.nodes[node]['label'] | label
    return Product_macro_ts

def counter_node_regions(nodes):
    nodes_set = list()
    regions_set = dict()
    for node in nodes:
        nodes_set.append(node[0])
    node_dic = collections.Counter(nodes_set)
    for key,number in node_dic.items():
        regions_set[key] = (number,[i for i,x in enumerate(nodes_set) if x==key],
                            dict(collections.Counter([nodes[i][1] for i,x in enumerate(nodes_set) if x==key])))
    return regions_set

def check_if_macro_actions(macro_action, index, pos):
    act_set = set(index[2].items())
    for act, tuple in macro_action.items():
        if tuple[1].issubset(act_set):
            return set([act + pos])
        else:
            return set()

class MultiAgentSystem(object):
    """
    Class for a multi-agent system (mas).
    """
    def __init__(self, agents, env_map=None):
        """
        Constructor.

        Args:
            agents (list): list of agent objects, see Agent class.
            env_map: map of the environment. (Optional)
        """
        self._agents = agents()
        self._env_map = env_map
        self._team_task = None
        self._macro_actions = None
        self._product_ts = None
        self._product_marco_ts = None
        self._regions = None

    def add_team_task(self, team_task):
        """
        Add team task as LTL formulas.

        Args:
            team_task: String. LTL formulas.
        """
        self._team_task = team_task

    def add_marco_actions(self, marco_actions):
        """
        Add object of marco_actions.

        Args:
            marco_actions (list): list of marco actions, see MarcoAction class.
        """
        self._marco_actions = marco_actions

    def compute_team_product_ts(self, only_agents=None):
        """
        Compute the product transition system of all agents without macro actions.

        Args:
            only_agents (set): if given, only these agents will be used to 
                    compute the product ts. (Optional, default: None)
        Raises:
            ValueError: if agents are not defined.
        """
        if self.agents is None:
            raise ValueError('[System]: System has no agents defined yet')
        agents = self.agents if only_agents is None else only_agents
        self._product_ts = ProdFts([agent.motact_model for agent in agents])
        self._product_ts.construct_full_product()

    def compute_product_marco_ts(self, only_agents=None):
        """
        Compute the product transition system of all agents with given marco actions.
        
        Args:
            only_agents (set): if given, only these agents will be used to
                            compute the product ts. (Optional, default: None)
        
        Raises:
            ValueError: if marco_actions are not defined.
        """
        if self.marco_actions is None:
            raise ValueError('[System]: Marco actions are not defined yet')
        if self.product_ts is None:
            self.compute_team_product_ts(only_agents)
        self._product_marco_ts = add_labels_of_macro_action(self.product_ts, self.regions, self.marco_actions)

    def compute_buchi(self):
        """
        Compute the Buchi automaton of the team task.
        """
        self._buchi = Buchi(self.team_task)
        self._buchi._construct_buchi_automaton()

    def compute_product_ts_buchi(self):
        """
        Product of ts without marco action and Buchi automaton.
        """
        self._prod_ts_buchi = ProdTsBuchi(self.product_ts, self.buchi)
        self._prod_ts_buchi.construct_full_product()
    
    def compute_product_macro_ts_buchi(self):
        """
        Product of ts with macro action and Buchi automaton.
        """
        self._prod_macro_ts_buchi = ProdTsBuchi(self.product_marco_ts, self.buchi)
        self._prod_macro_ts_buchi.construct_full_product()

    @property
    def agents(self):
        return self._agents

    @property
    def regions(self):
        return self._regions

    @property
    def env_map(self):
        return self._env_map

    @property
    def marco_actions(self):
        return self._marco_actions

    @property
    def team_task(self):
        return self._team_task

    @property
    def buchi(self):
        return self._buchi

    @property
    def product_ts(self):
        return self._product_ts

    @property
    def prod_ts_buchi(self):
        return self._prod_ts_buchi

    @property
    def product_marco_ts(self):
        return self._product_marco_ts

    @property
    def prod_marco_ts_buchi(self):
        return self._prod_marco_ts_buchi