# -*- coding: utf-8 -*-
from src.baseline.sampling_based.buchi import Buchi
from src.baseline.sampling_based.product import ProdTsBuchi
from src.baseline.sampling_based.utils import add_labels_of_macro_action
import collections
from src.baseline.sampling_based.product import ProdFBA
from src.baseline.sampling_based.planner import ltl_planner

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


    def compute_buchi(self):
        self._buchi = Buchi(self.team_task)
        #self.buchi.graph['accept']=['accept_all']

    def construct_product_ts_buchi(self):
        self._PBA={'NBA':self._buchi,'PTS':self.agents}


    def compute_product_ts_buchi(self):
        '''
        for each agent
        buchi * NBA
        for each agent, we can get the NBA*WTS
        and virtual
        '''
        self.PBA_swarm = []
        i=0
        for agent in self.agents:
            agent_PBA = ProdTsBuchi(agent._motact_model, self.buchi.buchi)
            agent_PBA.construct_full_product(i)
            self.PBA_swarm.append(agent_PBA)
            i=i+1


    def compute_product_fianl_ts_buchi(self):
        """
        Product of Ts_Buchi
        """
        self._prod_marco_ts_buchi = ProdFBA(self.PBA_swarm,self.buchi.buchi)
        self._prod_marco_ts_buchi.construct_full_product()

    @property
    def PBA(self):
        return self._PBA

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