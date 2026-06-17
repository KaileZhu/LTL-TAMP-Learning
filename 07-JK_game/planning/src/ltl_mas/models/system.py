# -*- coding: utf-8 -*-
from ltl_mas.tools.boolean_formulas.parser import parse as parse_guard
from ltl_mas.models.agent import Agent
from ltl_mas.models.product import ProdFts
from ltl_mas.models.buchi import Buchi
from ltl_mas.models.product import ProdTsBuchi
from ltl_mas.tools.utils import add_labels_of_macro_action
import collections

class MultiAgentSystem(object):
    """
    Class for a multi-agent system (mas).
    """
    def __init__(self, agents, env_map=None):
        """
        Constructor.

        Args:
            agents: List. List of agent objects, see Agent Class.
            env_map: Optional. Map of the environment. Format to be decided. Default: None.
        """
        self._agents = agents
        self._map = env_map
        self._team_task = None
        self._marco_actions = None
        self._product_ts = None
        self._product_marco_ts = None
        self._regions=None

    def add_team_task(self, team_task):
        """
        Add team task as LTL formulas.

        Args:
            team_task: String. LTL formulas.
        """
        self._team_task = team_task        

    def add_regions_for_marco_action(self,regions):
        """
        regions is the subscript of the macro_action labels.
        for example: region (0,0):1
        the marcro_action C take place in the (0,0),then we creat the labels C1
        """
        self._regions=regions

    def add_marco_actions(self, marco_actions):
        """
        Add object of marco_actions.
 
        Args:
            marco_actions: List. List of marco actions, see MarcoAction Class.
        """
        self._marco_actions = marco_actions

    def compute_team_product_ts(self, only_agents=None):
        """
        Compute the product transition system of all agents.
        Note macro actions are not considered yet.

        Args:
            only_agents: Set (optional). If given, only these agents will be used
                         to compute the product ts. Default: None.

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
        Compute the product transition system of all agents, given marco actions.

        Args:
            only_agents: Set (optional). If given, only these agents will be used
                         to compute the product ts. Default: None.

        Raises:
            ValueError: if marco_actions are not defined.
        """
        if self.marco_actions is None:
            raise ValueError('[System]: Marco actions are not defined yet')
        if self.product_ts is None:
            self.compute_team_product_ts(only_agents)
        self._product_marco_ts = add_labels_of_macro_action(self.product_ts,self.regions, self.marco_actions)

    def compute_buchi(self):
        self._buchi = Buchi(self.team_task)
        self._buchi._construct_buchi_automaton()

    def compute_product_ts_buchi(self):
        """
        Product of ts without marco action and buchi
        """
        self._prod_ts_buchi = ProdTsBuchi(self.product_ts, self.buchi)
        self._prod_ts_buchi.construct_full_product()

    def compute_product_marco_ts_buchi(self):
        """
        Product of ts with marco action and buchi
        """
        self._prod_marco_ts_buchi = ProdTsBuchi(self.product_marco_ts, self.buchi)
        self._prod_marco_ts_buchi.construct_full_product()


    @property
    def prod_marco_ts_buchi(self):
        return self._prod_marco_ts_buchi

    @property
    def prod_ts_buchi(self):
        return self._prod_ts_buchi

    @property
    def buchi(self):
        return self._buchi

    @property
    def agents(self):
        return self._agents

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
    def product_ts(self):
        return self._product_ts

    @property
    def product_marco_ts(self):
        return self._product_marco_ts

    @property
    def regions(self):
        return self._regions