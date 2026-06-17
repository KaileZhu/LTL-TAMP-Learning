#！/usr/bin/env python3

import math
import yaml
import numpy as np

from PIL import Image
from matplotlib import pyplot as plt
from scipy.interpolate import splprep, splev

class InputData:
    def __init__(self):
        self.position = dict()
        self.task_type = dict()
        self.sub_task_type = list()
        self.agent_type = dict()
        self.agent_data = list()

    def read_from_yaml(self, file_path):
        """
        Initialize the information of task and environment.
        ----------
        Parameters:
            file_path:(str), the path of the yaml file.
        """
        task, agents, regions = str(), list(), list()

        # read data from file.yaml
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            print('----------------------------------------')
            print('Read from %s' %file_path)


        # get the task
        task = data['Task']
        # print('== LTL task: %s' %task)


        # get the regions of interest
        regions = data['Regions']
        # print('== Regions: %s' %data['Regions'])


        # get the information of agents
        i = 0
        agent_reg = {r['type']: r['name'] for r in regions}
        for at in data['Agents']:  # 各个类型
            for k in range(at['num']):
                agents.append({
                    'id': i,
                    'type': at['type'],
                    'name': '%s_%s' %(at['type'], k),
                    'reg': at['reg'],
                    'vel': at['vel'],
                    'act': at['act'],
                })
                i += 1
        # print('== Agents: %s' %data['Agents'])
        

        # assign these data to the class
        # add the subtasks
        subtasks = {k['type']: (k['dur'], k['req']) for k in data['Subtasks']}
        self.task_type = subtasks


        # add the actions
        actions = data['Actions']
        self.sub_task_type = actions


        # add the regions
        position = {roi['name']: roi['pos'] for roi in data['Regions']}  # region of interest
        self.position = position


        # add the agent types
        agent_type = {v['type']: {
            'actions': v['act'],
            'serve': v['act'],
            'velocity': v['vel'][0] 
        } for v in data['Agents']}
        self.agent_type = agent_type
        
        # add the agent data
        agent_data = [(a['id'], a['reg'], a['type']) for a in agents]
        self.agent_data = agent_data
        
        return task, agents, regions



def norm_distance(pose1, pose2, ord=2, unit=1.0, under_flow=0.001):
    pose1 = np.array(pose1)
    pose2 = np.array(pose2)
    pose_relative = [pose1[i]-pose2[i] for i in range(len(pose1))]
    return np.linalg.norm(pose_relative, ord) + under_flow

def distance(pos_f, pos_t):
    dis = math.hypot(pos_f[0]-pos_t[0], pos_f[1]-pos_t[1])
    return round(dis, 4)

def gener_path(path, vel, k=3, c=1.0):
    # convert the input path to np.array format
    path = np.array(path)
    # perform cubic spline interpolation
    tck, u = splprep(path.T, k=k, s=0, per=False)
    # evaluate the spline at more points
    curve_points = splev(np.linspace(0, 1, 100), tck)
    # calculate the arc length of the curve
    length = np.sum(np.sqrt(np.sum(np.diff(curve_points, axis=1)**2, axis=0)))
    time_eval = math.ceil(length/vel*c)
    # calculate curve points according to the evaluate time seqsuence
    t_eval = np.linspace(0, 1, time_eval)
    curve_points = np.array(splev(t_eval, tck))
    return curve_points
