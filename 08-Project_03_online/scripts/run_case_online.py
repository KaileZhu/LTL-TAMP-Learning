# ！/usr/bin/env python3

'''
@Date   : 2023/11 -->  
@Authors: Junjie Wang, 
@Contact: pkuwjj1998@163.com
@Version: 1.0
@Descrip: Based on the given LTL task formula, assign the collaborative subtasks to
        multi-agent system efficiently, and guarantee asymptotic optimization.
'''

import os
import re
import time
import sys

import numpy as np
import networkx as nx
import matplotlib.patches as patches

from PIL import Image
from matplotlib import pyplot as plt
from MAS_TL_STAP import *
from MAS_TL_STAP.new_poset_builder import Buchi_poset_builder
from MAS_TL_STAP.New_B_A_B import Branch_And_Bound
from MAS_TL_STAP.poset_product import Poset_producter

'''
这个是测试在线性能的脚本，在线性能主要涉及3个方面
1 solver.task_type的设定，通过修改task type对应的时间，来展示指标中任务执行时长的波动
2 extro_constrain的计算，设定在线重新规划的时刻，以及损坏的agent列表，然后基于之前的分配方案计算出新的边界条件
   这里边界条件还有一些问题，如何根据当前的截止时间，获取agent的位置，这个我目前是这些写死了，但是不应该这样做
   应该根据以下原则确定：a，当前时间在工作，则agent应该设置在工作地点
                      b. 当前时间在移动，计算出移动到的位置
                      c. 当前时间在等待，那应该在下一个任务的位置，如果没有下一个任务，则在上一个任务结束的位置
3 根据新的边界条件，进行计算solver2 = Branch_And_Bound(poset, subtasks, scene)
    solver2.Begin_branch_search_online(5,extro_constrain,assigned_task)

目前的问题：移动时用直线距离还是Dijkstra?
          损坏的智能体若设置为很大的begin_time可能会出问题，依然会求解出一个结果，能否在调用优化器时就把损坏的智能体从决策变量中删除？
          poset['action_map']中有重复的元素,即同一个任务会被映射到多个编号
'''
# if __name__ == '__main__':
def run_one_online_scene(online_scene_idx):
    # =============================================
    # Initialization of the task and environment
    # =============================================
    path = os.path.abspath(os.path.dirname(
        os.path.dirname(__file__)))
    path_file = f'{path}/scenes/online_scene_0'+str(online_scene_idx)+'.yaml'
    path_img = f'{path}/figures/zybj_dl.png'
    buchi, agents, subtasks, regions = None, list(), list(), dict()
    res = 50
    init_node = (50, 50)
    # get the initial setting from yaml file
    scene = InputData()
    scene1 = InputData()
    # 在yaml文件中新加入了损坏的智能体，损坏的时间，任务波动信息
    TASK, AGENT= scene.read_from_yaml(path_file)
    TASK1, AGENT1= scene1.read_from_yaml(path_file)
    # poset = Buchi_poset_builder(TASK)
    begin_time = time.time()
    Poset_product = Poset_producter(TASK)
    Poset_product.generate_poset()
    Poset_product.prodocter()
    poset = Poset_product.final_poset
    end_time = time.time()
    offline_poset_extraction_time = end_time - begin_time
    print('任务分析的执行时间为:', end_time - begin_time)
    # generate the grid map according to the figure
    motionmap = MotionFts(Image.open(path_img), res, init_node)
    # agents = [Agent(at, motionmap) for at in AGENT]
    agents = AGENT

    # define a regular expression pattern to match the desired substrings
    pattern = re.compile(r'\b(\w+)_([a-zA-Z0-9]+)\b')
    # find all matches in the input string
    matches = poset['action_map']
    # extracted components
    subtasks.extend([(i, matches[i][1], matches[i][-1])
                     for i in range(len(matches))])

    # =========================
    # Calculation process
    # =========================
    begin_time = time.time()
    solver = Branch_And_Bound(poset, subtasks, scene)
    solver.Begin_branch_search2(10, up_bound_method='greedy',
                                low_bound_method='i+j', select_agent_method = 'concentrate')
    # print('solver_low_bound_list',solver.low_bound_list)
    solver.get_time_table_of_best_solution(solver.best_solution)
    end_time = time.time()
    offline_task_assign_time = end_time - begin_time
    print('初始的离线任务分配计算时间为：', end_time - begin_time)
    offline_calculate_time = offline_poset_extraction_time + offline_task_assign_time
    # 输出offline下每个智能体的发射时间，结束时间及对应的子任务
    static_plan = {}
    for agent in scene.agent_data:
        static_plan[agent[1]+'-'+str(agent[3])] = []
        agent_tid = agent[0]
        for task in solver.best_solution[agent_tid]:
            task_id = task[0][0]
            task_name = task[0][1]+'_'+task[0][2]
            missile_num = task[2]   # 记录每个智能体执行每个任务的用弹量
            duration = agent[2][task_name][0]
            end_time = solver.task_time_table[task_id][1]
            static_plan[agent[1]+'-'+str(agent[3])].append(tuple([task_name, missile_num, (end_time-duration,end_time)]))
    # 输出offline下每个子任务的time table
    static_subtask_time_table = {}
    for i in solver.task_time_table:
        action = subtasks[i[0]][1]
        region = subtasks[i[0]][2]
        # static_subtask_time_table[action + region] = [int(i[1]), int(i[2])]
        static_subtask_time_table[action + region] = i[1]
    
    Poset_product.gantt_plotter(scene.agent_data, poset, solver.best_solution,
                                    solver.task_time_table,path, online_scene_idx)
    # 在线部分
    # assiged_task是已经执行的任务
    # 任务的执行时长 task_execute_time
    break_time = scene1.broken_time
    broken_agent_list = scene1.broken_agent_list
    # 重新定义子任务集合，任务种类和数量都要和offline时一致
    # solver.task_type = scene.fluctuated_task_type
    pre_solution = solver.best_solution
    extro_constrain, assigned_task = solver.generate_online_adapt_extro_constrain(pre_solution, break_time, broken_agent_list)
    solver2 = Branch_And_Bound(poset, subtasks, scene1)
    online_start = time.time()
    solver2.Begin_branch_search_online(2, extro_constrain, assigned_task, select_agent_method = 'concentrate')
    # 100s最优是 240   10s 值是260
    # Poset_product.gantt_plotter(poset, solver2.best_solution, solver2.task_time_table)
    online_end = time.time()
    online_calculate_time = online_end - online_start

    Poset_product.gantt_plotter_online(scene.agent_data, poset, solver.best_solution, solver.task_time_table,
                                       solver2.best_solution, solver2.task_time_table, break_time,
                                       online_calculate_time, broken_agent_list, path, online_scene_idx)
    offline_finish_time = max([time_list[1] for time_list in solver.task_time_table])
    online_finish_time = max([time_list[1] for time_list in solver2.task_time_table])
    online_time_table = solver2.task_time_table
    # for age in agents:
    #     for plan in solver.best_solution[age.id-1]:
    #         task = [{
    #             'task': plan[0][1]+'_'+plan[0][2],
    #             'task_id': plan[0][0],
    #             'dur': scene.task_type[plan[0][1]+'_'+plan[0][2]][0],
    #             'reg': plan[0][2],
    #             'pos': age.regions[plan[0][2]]
    #         }]
    #         age.add_new_tasks(task)
    # 以下作为函数返回值
    broken_time_info = [break_time]
    broken_agent_info = broken_agent_list
    # fluctuate_info = []
    # for task_name, _ in scene.task_type.items():
    #     exe_time_before_fluc = scene.task_type[task_name][0]
    #     exe_time_after_fluc = exe_time_before_fluc  # 暂且不考虑任务时间波动这部分
    #     # exe_time_after_fluc = scene.fluctuated_task_type[task_name][0]
    #     fluctuate_info.append([task_name+' : '+str(exe_time_before_fluc)+' -> ' +
    #                                   str(exe_time_after_fluc)])
    cal_time_info = [offline_calculate_time, online_calculate_time]
    finish_time_info = [offline_finish_time, online_finish_time]
    # 输出online下每个智能体的发射时间，结束时间及对应的子任务
    online_plan = {}
    for agent in scene.agent_data:
        if agent[0] not in broken_agent_list:
            online_plan[agent[1]+'-'+str(agent[3])] = []
            agent_tid = agent[0]
            for task in solver2.best_solution[agent_tid]:
                task_id = task[0][0]
                task_name = task[0][1]+'_'+task[0][2]
                duration = agent[2][task_name][0]
                for time_table in solver2.task_time_table:
                    if task_id in time_table:
                        end_time = time_table[1]
                online_plan[agent[1]+'-'+str(agent[3])].append(tuple([task_name, end_time-duration, end_time]))
   
    return broken_time_info, broken_agent_info, cal_time_info, finish_time_info, static_plan, static_subtask_time_table, online_plan, online_time_table


if __name__ == '__main__':
    # 这3个列表只用于记录每次循环的输出信息
    broken_time_list = []
    broken_agent_list = []
    cal_time_list = []
    finish_time_list = []
    static_subtask_time_table_1 = []
    online_time_table_1 = []
    print('正在进行任务分解与分配...')
    original_stdout = sys.stdout
    sys.stdout = open('nul', 'w')
    
    # 循环处理5个场景
    # for idx in range(5):
    #     scene_idx = idx + 1
    #     broken_time, broken_agent, fluc_task, cal_time, finish_time = run_one_online_scene(scene_idx)
    #     broken_time_list.append(broken_time)
    #     broken_agent_list.append(broken_agent)
    #     fluc_task_list.append(fluc_task)
    #     cal_time_list.append(cal_time)
    #     finish_time_list.append(finish_time)
    #     sys.stdout = original_stdout
    #     print('场景'+str(scene_idx)+'已完成...')
    #     sys.stdout = open('nul', 'w')

    # 处理单个场景online_scene_01，便于调试
    scene_idx = 7
    broken_time, broken_agent, cal_time, finish_time, static_plan, static_subtask_time_table, online_plan, online_time_table = run_one_online_scene(scene_idx)
    broken_time_list.append(broken_time)
    broken_agent_list.append(broken_agent)
    cal_time_list.append(cal_time)
    finish_time_list.append(finish_time)
    static_subtask_time_table_1.append(static_subtask_time_table)
    online_time_table_1.append(online_time_table)
    sys.stdout = original_stdout
    print('场景'+str(scene_idx)+'已完成...')
    sys.stdout = open('nul', 'w')
    
    mylog = open('online_scene_output.log', mode='w', encoding='utf-8')
    # 统一打印这些场景的信息,并将计算结果写到online_scene_output.log文档中
    sys.stdout = original_stdout
    # 循环处理5个场景
    # for idx in range(5):
    #     scene_idx = idx + 1
    #     print('-------------------------------------', file=mylog)
    #     print('              第'+str(scene_idx)+'个场景', file=mylog)
    #     print('-------------------------------------', file=mylog)
    #     print('智能体发生损毁的时间：', file=mylog)
    #     print(broken_time_list[idx][0], file=mylog)
    #     print('损坏的智能体编号：', file=mylog)
    #     for i in broken_agent_list[idx]:
    #         print(i+1, file=mylog)
    #     print('任务时长波动情况：', file=mylog)
    #     for fluc in fluc_task_list[idx]:
    #         print(fluc[0], file=mylog)
    #     print('重规划的计算耗时：', file=mylog)
    #     print(cal_time_list[idx], file=mylog)
    #     print('初始离线规划的任务总时长：', file=mylog)
    #     print(finish_time_list[idx][0], file=mylog)
    #     print('重规划后的任务总时长：', file=mylog)
    #     print(finish_time_list[idx][1], file=mylog)
    
    # 处理单个场景online_scene_01    
    scene_idx = 7
    idx = 0
    print('-------------------------------------', file=mylog)
    print('              第'+str(scene_idx)+'个场景', file=mylog)
    print('-------------------------------------', file=mylog)
    print('智能体发生损毁的时间：', file=mylog)
    print(broken_time_list[idx][0], file=mylog)
    print('损坏的智能体编号：', file=mylog)
    for i in broken_agent_list[idx]:
        print(i+1, file=mylog)
    print('离线规划的计算耗时：', file=mylog)
    print(cal_time_list[idx][0], file=mylog)
    print('重规划的计算耗时：', file=mylog)
    print(cal_time_list[idx][1], file=mylog)
    print('初始离线规划的任务总时长：', file=mylog)
    print(finish_time_list[idx][0], file=mylog)
    print('重规划后的任务总时长：', file=mylog)
    print(finish_time_list[idx][1], file=mylog)
    print('离线时智能体计划:', file=mylog)
    print(static_plan, file=mylog)
    print('在线时智能体计划:', file=mylog)
    print(online_plan, file=mylog)


