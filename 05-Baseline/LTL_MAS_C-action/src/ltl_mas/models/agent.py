# -*- coding: utf-8 -*-
from src.ltl_mas.models.ts import MotionFts
from src.ltl_mas.models.action import LocalActionModel
from src.ltl_mas.models.product import ProdMotAct, ProdTsBuchi
from src.ltl_mas.models.buchi import Buchi


class Agent(object):
    """
    Class for an agent.
    """
    def __init__(self, name='agent'):
        self._name = name
        
    def build_motion_fts(self, nodes, symbols, edges):
        self._motion_fts = MotionFts(nodes, symbols)
        self._motion_fts.add_edges(edges)

    def add_action_model(self, actions):
        self._action_model = LocalActionModel(actions)

    def compute_motact_model(self):
        self._motact_model = ProdMotAct(self.motion_fts, self.action_model)
        self._motact_model.construct_full_product()

    def add_local_task(self, local_task):
        self._local_task = local_task

    def compute_buchi(self):
        self._buchi = Buchi(self.local_task)
        self._buchi._construct_buchi_automaton()


    def compute_product_mot_buchi(self):
        self._prod_mot_buchi = ProdTsBuchi(self.motion_fts, self.buchi)
        self._prod_mot_buchi.construct_full_product()

    def compute_product_motact_buchi(self):
        self._prod_motact_buchi = ProdTsBuchi(self.motact_model, self.buchi)
        self._prod_motact_buchi.construct_full_product()

    @property
    def local_task(self):
        return self._local_task        

    @property
    def motact_model(self):
        return self._motact_model

    @property
    def action_model(self):
        return self._action_model

    @property
    def motion_fts(self):
        return self._motion_fts
        
    @property
    def name(self):
        return self._name

    @property
    def buchi(self):
        return self._buchi

    @property
    def prod_mot_buchi(self):
        return  self._prod_mot_buchi

    @property
    def prod_motact_buchi(self):
        return  self._prod_motact_buchi