import sys
sys.path.append('D:\PycharmProjects\JK_project1\planning')
sys.path.append('D:\PycharmProjects\JK_project1\planning/test')
sys.path.append('D:\PycharmProjects\JK_project1\planning/src')
sys.path.append('C:/Users\MSI1\Documents\LTL\JK_game\planning')
sys.path.append('C:/Users\MSI1\Documents\LTL\JK_game\planning/test')
sys.path.append('C:/Users\MSI1\Documents\LTL\JK_game\planning/src')
from src.ltl_mas.tools import optimize_method
import time
from src.ltl_mas.formula_generater.LTL_formula_generater import LTL_generater
from src.ltl_mas.tools.Data_pre_treatment import Data_pretreat
from src.ltl_mas.tools.poset_product import  Poset_producter
from src.ltl_mas.tools.order_anylises.py_decisions.topsis.fuzzy_topsis import fuzzy_topsis_method
#from data.input_data.first_data import software_input_data
import numpy as np
from planning.data.input_data.LTL_formula import *


def calculate_assignment_method(input_data):
    env_type=input_data['场景选择']
    if env_type == '想定场景1':
        num = 1
        from planning.data.input_data.first_data_ZYBJ import software_input_data
    elif env_type == '想定场景2':
        num = 2
        from planning.data.input_data.second_Data import software_input_data
    elif env_type == '想定场景3':
        num = 3
        from planning.data.input_data.third_Data import software_input_data
    Data_manager=Data_pretreat()
    if env_type == '想定场景1':
        num = 1
        import planning.data.input_data.first_map_data as map_data

    elif env_type == '想定场景2':
        num = 2
        import planning.data.input_data.second_map_data as map_data
    elif env_type == '想定场景3':
        num = 3
        import planning.data.input_data.third_map_data as map_data
    method_type=input_data['算法选择']
    Data_manager.get_map_data(map_data, env_type)
    Data_manager.manage_software_data(software_input_data)
    value_place_dic = Data_manager.get_value_place_dic()
    method_name=input_data['战法选择']
    task = LTL_generater(Data_manager)
    planning_structure = task.pre_calculate_the_goal_data2(value_place_dic, method_name)
    #planning_structure=change_goal_task_pair(planning_structure)
    #task = LTL_generater(Data_manager)
    task.creat_LTL_formula_with_wave_picking(planning_structure, method_name)
    # 生成形式化语言公式
    task.create_final_formula()
    LTL_formula = task.final_formula
    # 进行任务分解，获取任务偏序集
    Poset_product = Poset_producter(LTL_formula)
    Poset_product.generate_poset()
    Poset_product.prodocter()
    poset = Poset_product.final_poset
    # 根据环境，评估子任务的内容，以及价值
    Data_manager.estimate_cost_of_tasks(Poset_product,input_data['场景选择'])
    dataset = Data_manager.task_information
    print('开始根据模糊算法计算优先度')
    print('采用 topsis 法')
    weights = list([
        [(0.1, 0.2, 0.3), (0.7, 0.8, 0.9), (0.3, 0.5, 0.8)]
    ])

    # Load Criterion Type: 'max' or 'min'
    criterion_type = ['max', 'max', 'min']
    mohu_subtask_value = fuzzy_topsis_method(Data_manager.task_information, weights, criterion_type,
                                                  graph=False)
    input_data2 = Data_manager.input_data
    optimize_method1 = optimize_method.Branch_And_Bound(Poset_product.final_poset,
                                                            Poset_product.final_task_data_list,
                                                            Data_manager.input_data)
    subtask_value=[]
    for i in range(len(Data_manager.task_information['time_cost'])):
        row = {'priority': mohu_subtask_value[i][0]}
        subtask_value.append(row)
    optimize_method1.subtask_value=subtask_value
    optimize_method1.prefer_type='最短时间'
    optimize_method1.algorithm_type=method_type
    optimize_method1.Begin_branch_search(15, up_bound_method='greedy', low_bound_method='i+j',
                                             search_method='DFS')
    current_solution = optimize_method1.best_solution
    task_time_table = optimize_method1.task_time_table

    f = open(input_data['战法选择']+input_data['场景选择'] + '.txt', 'w')
    f.write(str(current_solution))
    f.close()
    return current_solution, task_time_table

calculate_assignment_method({'场景选择':'想定场景1','战法选择':'占场扫描','算法选择': '两级合同网'})
#calculate_assignment_method({'场景选择':'想定场景1','战法选择':'全面进攻'})
#输入 {'场景选择':'想定场景1','战法选择':'步步为营'}
#                想定场景2              '步步为营'，'占场扫描'，'全面进攻'，'围点打援'，'重点防御'，'防守反击'
#                想定场景3