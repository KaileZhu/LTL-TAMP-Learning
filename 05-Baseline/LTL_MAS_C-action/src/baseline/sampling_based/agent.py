# -*- coding: utf-8 -*-
from src.baseline.sampling_based.ts import MotionFts
from src.baseline.sampling_based.action import LocalActionModel
from src.baseline.sampling_based.product import ProdMotAct, ProdTsBuchi
from src.baseline.sampling_based.buchi import Buchi


class Agent(object):
    """
    Class for an agent.
    """
    def __init__(self, name='agent'):
        self._name = name
        
    def build_motion_fts(self, field,agent_type='UAV'):
        self.velocity=field.input_data.agent_type[agent_type]['velocity']
        nodes={}
        symbols=None
        for label,pose in field.photovoltaic_list.items():
            nodes[tuple(pose)]=set([label])
        for label,pose in field.station_list.items():
            nodes[tuple(pose)]=set([label])

        self._motion_fts = MotionFts(nodes, self.velocity)
        self._motion_fts.add_edges()

    def add_action_model(self, actions):
        self._action_model = LocalActionModel(actions)

    def compute_motact_model(self):
        self._motact_model = ProdMotAct(self.motion_fts, self.action_model)
        self._motact_model.construct_full_product()

    def add_local_task(self, local_task):
        self._local_task = local_task

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