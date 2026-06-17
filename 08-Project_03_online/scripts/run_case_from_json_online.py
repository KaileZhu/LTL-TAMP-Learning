import os
import re
import time
import sys

import numpy as np
import networkx as nx
import matplotlib.patches as patches
import json

from PIL import Image
from matplotlib import pyplot as plt
from MAS_TL_STAP import *
from MAS_TL_STAP.new_poset_builder import Buchi_poset_builder
from MAS_TL_STAP.New_B_A_B import Branch_And_Bound
from MAS_TL_STAP.poset_product import Poset_producter



def run_one_online_scene():
    # =============================================
    # Initialization of the task and environment
    # =============================================
    # get the initial setting from yaml file
    scene = InputData()
    path1 = os.path.abspath(os.path.dirname(__file__))
    
    # 从yaml文件中读取相关参数
    path_file_yaml = f'{path1}/parameter setting.yaml'
    offline_time_budget, offline_missile_assign_strategy, online_time_budget, online_missile_assign_strategy = scene.read_from_yaml(path_file_yaml)
    
    # 从json文件中读取相关信息
    path_file_ssl = f'{path1}/ssl_list.json'
    path_file_dlgh = f'{path1}/dlgh.json'
    path_file_weapon = f'{path1}/weapons.json'
    path_file_offline_solution = f'{path1}/offline_solution.json'
    path_file_time_failed_ssl = f'{path1}/time_and_failed_ssl.json'
    TASK, ssl_info, dlgh_info = scene.read_from_json_online(path_file_ssl, path_file_dlgh, path_file_weapon, path_file_offline_solution, path_file_time_failed_ssl)
    
    # poset = Buchi_poset_builder(TASK)
    begin_time = time.time()
    Poset_product = Poset_producter(TASK)
    Poset_product.generate_poset()
    Poset_product.prodocter()
    poset = Poset_product.final_poset
    end_time = time.time()
    online_poset_extraction_time = end_time - begin_time
    print('任务分析的执行时间为:', end_time - begin_time)

    # find all matches in the input string
    matches = poset['action_map']
    # extracted components
    subtasks = list()
    subtasks.extend([(i, matches[i][1], matches[i][-1])
                     for i in range(len(matches))])

    # =========================
    # Calculation process
    # =========================
    begin_time = time.time()
    solver = Branch_And_Bound(poset, subtasks, scene)
    solver.Begin_branch_search2(online_time_budget, up_bound_method='greedy',
                                low_bound_method='i+j', select_agent_method = online_missile_assign_strategy)
    # print('solver_low_bound_list',solver.low_bound_list)
    solver.get_time_table_of_best_solution(solver.best_solution)
    end_time = time.time()
    online_task_assign_time = end_time - begin_time
    print('初始的离线任务分配计算时间为：', end_time - begin_time)
    online_calculate_time = online_poset_extraction_time + online_task_assign_time
    # 输出online下每个智能体的发射时间，结束时间及对应的子任务
    new_plan = {}
    for agent in scene.agent_data:
        new_plan[agent[1]+'-'+str(agent[3])] = []
        agent_tid = agent[0]
        for task in solver.best_solution[agent_tid]:
            task_id = task[0][0]
            task_name = task[0][1]+'_'+task[0][2]
            missile_num = task[2]   # 记录每个智能体执行每个任务的用弹量
            duration = agent[2][task_name][0]
            end_time = solver.task_time_table[task_id][1]
            new_plan[agent[1]+'-'+str(agent[3])].append(tuple([task_name, missile_num, (end_time-duration,end_time)]))
    # 生成online下选择的ssl
    online_ssl = list()
    for key,value in new_plan.items():
        if value:
            for task in value:
                selected_ssl = dict()
                for ssl in ssl_info:
                    if ssl["hlptbs"] in key and ssl["mbbs"] in task[0]:
                        selected_ssl["rwbs"] = ssl["rwbs"]
                        selected_ssl["sslbs"] = ssl["sslbs"]
                        selected_ssl["mbbs"] = ssl["mbbs"]
                        selected_ssl["zcptbs"] = ssl["zcptbs"]
                        selected_ssl["zckssj"] = ssl["zckssj"]
                        selected_ssl["zcjssj"] = ssl["zcjssj"]
                        selected_ssl["zhptbs"] = ssl["zhptbs"]
                        selected_ssl["hlptbs"] = ssl["hlptbs"]
                        selected_ssl["djbhsj"] = ssl["djbhsj"]      # 运行时间
                        selected_ssl["djkssj"] = scene.convert_to_absolute_time(scene.online_reference_time, task[2][0])     # 打击开始时间
                        selected_ssl["djjssj"] = scene.convert_to_absolute_time(scene.online_reference_time, task[2][1])     # 打击结束时间
                        selected_ssl["ydsl"] = task[1]      # 用弹数量
                        for dlgh in dlgh_info:
                            if dlgh["rwbs"] == ssl["rwbs"]:
                                selected_ssl["ssyabs"] = dlgh["ssyabs"]
                                break
                        online_ssl.append(selected_ssl)
                        break
                        
    
    
    # 输出online下每个子任务的time table
    new_subtask_time_table = {}
    for i in solver.task_time_table:
        action = subtasks[i[0]][1]
        region = subtasks[i[0]][2]
        # new_subtask_time_table[action + region] = [int(i[1]), int(i[2])]
        new_subtask_time_table[action + region] = i[1]
    
    # Poset_product.gantt_plotter(scene.agent_data, poset, solver.best_solution,
    #                                 solver.task_time_table,path, online_scene_idx)
   
    return new_plan, online_ssl


if __name__ == '__main__':
    # 这3个列表只用于记录每次循环的输出信息
    broken_time_list = []
    broken_agent_list = []
    cal_time_list = []
    finish_time_list = []
    new_subtask_time_table_1 = []
    online_time_table_1 = []
    print('正在进行任务分解与分配...')
    original_stdout = sys.stdout
    sys.stdout = open('nul', 'w')
    
    new_plan, online_ssl = run_one_online_scene()
    # cal_time_list.append(cal_time)
    # finish_time_list.append(finish_time)
    sys.stdout = original_stdout
    # print('场景'+str(scene_idx)+'已完成...')
    sys.stdout = open('nul', 'w')
    
    mylog = open('online_scene_output.log', mode='w', encoding='utf-8')
    # 统一打印这些场景的信息,并将计算结果写到online_scene_output.log文档中
    sys.stdout = original_stdout

    print('在线时智能体计划:', file=mylog)
    print(new_plan, file=mylog)
    print('在线新预案:', file=mylog)
    json_online_ssl = json.dumps(online_ssl, indent=4)
    print(json_online_ssl, file=mylog)
    print('在线新预案:')
    print(json_online_ssl)