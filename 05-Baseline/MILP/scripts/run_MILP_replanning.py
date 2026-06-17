#！/usr/bin/env python3
import os
import re
import time
import numpy as np
import networkx as nx
import matplotlib.patches as patches
from PIL import Image
from matplotlib import pyplot as plt
from MAS_TL_STAP import *
from MAS_TL_STAP.poset_builder import Buchi_poset_builder
from MAS_TL_STAP.B_A_B2 import Branch_And_Bound
from MAS_TL_STAP.planner import MILP
from MAS_TL_STAP.poset_product import Poset_producter
from MAS_TL_STAP.replanning import Replanning


def poset_product(task):
    # 获取偏序关系poset
    # poset = Buchi_poset_builder(TASK)
    begin_time = time.time()
    Poset_product = Poset_producter(task)
    Poset_product.generate_poset()
    Poset_product.prodocter()  
    # Poset_product.draw_poset()  # 绘制poset图(Hesse diagram)
    poset = Poset_product.final_poset
    end_time = time.time()
    print('任务分析的执行时间为:', end_time-begin_time)
    return poset


def map_generation(REGION, AGENT, scene, path_img):
    # generate the grid map according to the figure
    res = 50  # ？？
    init_node = (50, 50)  # ？？
    motionmap = MotionFts(Image.open(path_img), res, init_node)
    motionmap.add_full_regions(REGION)
    motionmap.full_regions_dijkstra()
    agents = [Agent(at, scene.position, motionmap) for at in AGENT]
    return agents, motionmap


def subtask_generation(poset):
    # get the subtasks
    subtasks = ([(act[0], act[2], act[3]) for act in poset['action_map']])
    return subtasks


def MILP_planner(poset, subtasks, scene, round):
    begin_time = time.time()
    milp_solver = MILP(poset, subtasks, scene)  # 实例化MILP求解器
    milp_solution = milp_solver.Base_OPT_MILP_of_cvxpy()
    assignment = milp_solver.assignment
    end_time = time.time()
    run_time_cost = end_time - begin_time
    task_finish_time = milp_solution.value
    print('第', round,'轮MILP求解时间为：', run_time_cost)
    print('完成所有任务的总时长：', task_finish_time)
    return assignment


def run_one_case(scene_index):

    #=============================================
    # Initialization of the task and environment
    #=============================================

    # get the path of the yaml file
    path = os.path.abspath(os.path.dirname(
                            os.path.dirname(__file__)))
    path_file = f'{path}/scenes/scene_0'+str(scene_index)+'.yaml'
    path_img = f'{path}/figures/zybj_dl.png'


    # get the initial setting from yaml file
    scene = InputData()
    task, agent, region = scene.read_from_yaml(path_file)
    # buchi, agents, subtasks, regions = None, list(), list(), dict()


    #==============================================
    #   MILP Replanning
    #==============================================

    MILP_replanning = True
    round = 0
    while MILP_replanning == True:
        round += 1

        # 规划阶段
        post = poset_product(task)  # 得到偏序关系
        # agents, motionmap = map_generation(region, agent, scene, path_img)
        subtasks = subtask_generation(post)
        assignment = MILP_planner(post, subtasks, scene, round)


        # 更新阶段
        update = Replanning(assignment, task, scene)
        # task = update.task_update()
        # scene = update.scene_update()
        MILP_replanning = not update.finish()  # 任务执行完毕，结束循环


if __name__ == '__main__':
    run_MILP_time_cost = {}
    opt_method = 'MILP'
    scene_index = 2
    print('===============================================================')
    print('running case 0' + str(scene_index) + ' by ' + opt_method)
    print('===============================================================')
    if opt_method == 'MILP':
        run_MILP_time_cost[scene_index] = run_one_case(scene_index)

