#!/usr/bin/env python3

import math
import numpy as np

from scipy.interpolate import splprep, splev

from .motion import MotionFts, ActionModel
from .product import ProdMotAct, ProdTsBuchi


class Agent:
    """
    The class of agent.
    """
    def __init__(self, info, regions, motionmap):
        self.id = info['id']  # %d
        self.type = info['type']
        self.init_reg = info['reg']
        self.init_pos = tuple()
        self.vel = info['vel']  # [linear, angle]
        self.actions = info['act']  # [actions]
        self.regions = regions
        self.motionfts = motionmap
        self.plan = self._gener_init_plan()
        self.path = self._gener_init_path()

    def _gener_init_plan(self):
        plan = [{
            'task': 'settle',
            'task_id': -1,
            'act': None,
            'dur': 5,
            'reg': self.init_reg,
            # 'pos': self.gener_gaussian_points(self.regions[self.init_reg])
        }, ]
        return plan
    
    @staticmethod
    def gener_gaussian_points(center, std_dev=10, num_points=1):
        cov_matrix = np.diag([std_dev**2, std_dev**2])
        points = np.random.multivariate_normal(center, cov_matrix, size=num_points).T
        points = np.around(points, 3)
        points = [(points[0][k], points[1][k]) 
                    for k in range(len(points[0]))]
        return points

    def _gener_init_path(self):
        path = list()
        init_plan = self.plan[0]
        for t in range(init_plan['dur']):
            pos = self.gener_gaussian_points(self.regions[init_plan['reg']])
            self.init_pos = tuple(np.array(pos[0]))
            path.append((self.init_pos, init_plan['act']))
        return path

    def add_new_tasks(self, tasks):
        for task in tasks:
            self.plan.append(task)
            pos_s = self.regions[self.plan[-2]['reg']]
            pos_t = self.regions[self.plan[-1]['reg']]
            _, points_discre = self.motionfts.single_source_dijkstra(pos_s, pos_t)
            points_discre[0] = self.gener_gaussian_points(pos_s)[0]
            points_discre[-1] = self.gener_gaussian_points(pos_t)[0]
            points_smooth = self.get_smooth_path(points_discre, self.vel[0])
            path = [(p, None) for p in points_smooth[:-1]]
            path_dur = [(points_smooth[-1], self.plan[-1]['act']) 
                        for _ in range(self.plan[-1]['dur'])]
            self.path.extend(path + path_dur)

    def _gener_path_by_plan(self):
        pos_s = self.regions[self.plan[-2]['reg']]
        pos_t = self.regions[self.plan[-1]['reg']]
        _, path = self.motionfts.single_source_dijkstra(pos_s, pos_t)

    @staticmethod
    def get_smooth_path(path, vel, c=1.0):
        # convert the input path to np.array format
        path = np.array(path)
        # perform cubic spline interpolation
        if len(path) == 1:
            return path
        else:
            k = len(path)-1 if len(path) <= 3 else 3
            tck, u = splprep(path.T, k=k, s=0, per=False)
            # evaluate the spline at more points
            curve_points = splev(np.linspace(0, 1, 100), tck)
            # calculate the arc length of the curve
            length = np.sum(np.sqrt(np.sum(np.diff(curve_points, axis=1)**2, axis=0)))
            time_eval = math.ceil(length / vel * c)
            # calculate curve points according to the evaluate time seqsuence
            t_eval = np.linspace(0, 1, time_eval)
            curve_points = np.around(splev(t_eval, tck), 3)
            smooth_path = [(curve_points[0][k], curve_points[1][k]) 
                            for k in range(len(curve_points[0]))]
            return smooth_path
