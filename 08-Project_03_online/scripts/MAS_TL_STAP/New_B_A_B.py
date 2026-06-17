import cvxpy as cp
import matplotlib.pyplot as plt
from matplotlib import rc
import networkx as nx
import numpy as np
import time
from collections import Counter
from itertools import product as iter_product
from itertools import combinations as iter_com
import copy
import random


class Branch_And_Bound(object):
    def __init__(self, poset, task_data, input_data):
        # agent_data,task_data,task_type,sub_task_type,agent_type):
        self.poset = poset
        self.agent_data = input_data.agent_data
        self.task_data = task_data
        self.task_type = input_data.task_type
        self.Astar_table = []
        self.get_horizon()
        self.explored_node_dic = {}
        self.generate_poset_graph()

    def Begin_branch_search_online(self, time_limit, extro_constrain, assigned_task, select_agent_method):
        # here rebuild the time table
        # self.generate_time_budget()
        self.select_agent_method = select_agent_method      # 提供平均用弹"uniform"和集中用弹"concentrate"两种策略
        root_node = [[] for agent in self.agent_data]  # (solution,assigned_task)
        finished_task = list(extro_constrain.finished_time_list.keys())
        up_bound, solution = self.get_upper_bound_online(root_node, finished_task, extro_constrain)
        self.branch_tree = [(root_node, finished_task)]
        self.search_node_list = {}
        self.search_node_list[tuple(assigned_task)] = [root_node]
        self.best_solution = solution
        self.best_up_bound = up_bound
        self.max_low_bound = 0
        start = time.time()
        while (not self.branch_tree == []) and time.time() - start < time_limit:
            # print('check a branch')
            node, task = self.branch_tree.pop()
            # print('finish pop')
            # label_to_update_best_solution=0
            if tuple(task) in self.search_node_list.keys():
                if node not in self.search_node_list[tuple(task)]:
                    self.search_node_list[tuple(task)].append(node)
                    # print('begin lower boud')
                    # low_bound = self.get_lower_bound_online(node, task, extro_constrain)
                    # print('finishe lower bound')
                    low_bound = 10      # 不考虑求下界了
                    if low_bound < self.best_up_bound:
                        child_nodes = self.exten_child_nodes_online(node, task, extro_constrain)
                        self.branch_tree.extend(child_nodes)
                        # print('calculate to here')
                        up_bound, solution = self.get_upper_bound_online(node, task, extro_constrain)
                        if up_bound < self.best_up_bound:
                            # label_to_update_best_solution=1
                            self.best_solution = solution
                            self.best_up_bound = up_bound
                else:
                    child_nodes = self.exten_child_nodes_online(node, task, extro_constrain)
                    # print('goto 3')
                    self.branch_tree.extend(child_nodes)
                    # print('goto 5')
            else:
                self.search_node_list[tuple(task)] = [node]
                print('begin lower bound 3')
                # low_bound = self.get_lower_bound_online(node, task, extro_constrain)
                low_bound = 10
                if low_bound < self.best_up_bound:
                    child_nodes = self.exten_child_nodes_online(node, task, extro_constrain)
                    # print('goto 4')
                    self.branch_tree.extend(child_nodes)
                    up_bound, solution = self.get_upper_bound_online(node, task, extro_constrain)
                    if up_bound < self.best_up_bound:
                        self.best_solution = solution
                        self.best_up_bound = up_bound
            # print('new branch up bound is',self.best_up_bound)
            # if label_to_update_best_solution:
            # self.prune_tree()
        self.print_answer()
        self.get_time_table_of_best_solution_online(self.best_solution, extro_constrain)  # remain to update
        # print('online update finished')

    def Begin_branch_search2(self, time_limit, up_bound_method, low_bound_method, select_agent_method):
        start = time.time()
        # self.generate_time_budget()
        self.select_agent_method = select_agent_method      # 提供平均用弹"uniform"和集中用弹"concentrate"两种策略
        root_node = [[] for i in self.agent_data]  # (solution,assigned_task)
        assigned_tasks = []
        # self.get_lower_bound(low_bound_method)
        self.count_round = 1
        up_bound, solution = self.get_upper_bound(root_node, assigned_tasks, up_bound_method)
        # up_bound,solution=self.get_upper_bound(root_node,assigned_tasks,up_bound_method)
        # if up_bound<2400:
        #   print(up_bound)
        #  return 0
        self.upper_bound_list = {}
        self.upper_bound_list[self.count_round] = (up_bound, time.time() - start)
        # low_bound=self.get_lower_bound_method(root_node,assigned_tasks)
        self.branch_tree = [(root_node, assigned_tasks)]
        self.search_node_list = {}
        self.search_node_list[tuple(assigned_tasks)] = [root_node]
        self.best_solution = solution
        self.best_up_bound = up_bound
        self.max_low_bound = 0
        # give a count for the bnb method to get a better solution
        # get upper bound with time
        # get lower bound with time/round
        # both time and round
        self.low_bound_list = {}
        # each time explore a node, we say count_round+1
        self.best_up_bound_list = {}
        self.best_up_bound_list[self.count_round] = (up_bound, time.time() - start)
        self.astar_list_in_tree = [up_bound]
        while (not self.branch_tree == []) and time.time() - start < time_limit:
            # print('check a branch')
            # node fetch step
            # ===============
            # node fetching is good enough i think
            popi = self.astar_list_in_tree.index(max(self.astar_list_in_tree))
            node, task = self.branch_tree.pop(popi)
            node_up_bound = self.astar_list_in_tree.pop(popi)
            # =========================
            # this method is bad
            # node_up_bound=self.astar_list_in_tree.pop()
            # node,task=self.branch_tree.pop()
            self.count_round = self.count_round + 1
            # -------------------
            # child_nodes=self.branching_routine(search_method)
            if tuple(task) in self.search_node_list.keys():
                if node not in self.search_node_list[tuple(task)]:
                    self.search_node_list[tuple(task)].append(node)
                    # low_bound = self.get_lower_bound_method(node, task)
                    low_bound = 10
                    if low_bound < self.best_up_bound:
                        self.low_bound_list[self.count_round] = (low_bound, time.time() - start, 'explore')
                        child_nodes = self.exten_child_nodes(node, task)

                        self.branch_tree.extend(child_nodes)
                        self.astar_list_in_tree.extend(self.estimate_Astar_value(child_nodes, node_up_bound))
                        up_bound, solution = self.get_upper_bound(node, task, up_bound_method)
                        self.upper_bound_list[self.count_round] = (up_bound, time.time() - start)
                        if up_bound + 1 < low_bound:
                            s = 1
                        if up_bound < self.best_up_bound:
                            self.best_solution = solution
                            self.best_up_bound = up_bound
                            self.best_up_bound_list[self.count_round] = (self.best_up_bound, time.time() - start)
                    else:
                        self.low_bound_list[self.count_round] = (low_bound, time.time() - start, 'cut')
                        self.upper_bound_list[self.count_round] = (self.best_up_bound, time.time() - start)
                else:
                    child_nodes = self.exten_child_nodes(node, task)
                    self.branch_tree.extend(child_nodes)
                    self.astar_list_in_tree.extend(self.estimate_Astar_value(child_nodes, node_up_bound))
                    # self.astar_list_in_tree.extend([node_up_bound for node in child_nodes])
            else:
                self.search_node_list[tuple(task)] = [node]
                # low_bound = self.get_lower_bound_method(node, task)  # xiajie is error ?
                low_bound = 10
                if low_bound < self.best_up_bound:
                    self.low_bound_list[self.count_round] = (low_bound, time.time() - start, 'explore')
                    child_nodes = self.exten_child_nodes(node, task)
                    # print('label 1')
                    # self.astar_list_in_tree.extend([node_up_bound for node in child_nodes])
                    self.astar_list_in_tree.extend(self.estimate_Astar_value(child_nodes, node_up_bound))
                    # print('calculate_ to here')
                    self.branch_tree.extend(child_nodes)
                    up_bound, solution = self.get_upper_bound(node, task, up_bound_method)
                    self.upper_bound_list[self.count_round] = (up_bound, time.time() - start)
                    # self.branch_tree.append((node,task,up_bound,low_bound))
                    if up_bound < self.best_up_bound:
                        self.best_solution = solution
                        self.best_up_bound = up_bound
                        self.best_up_bound_list[self.count_round] = (self.best_up_bound, time.time() - start)
                else:
                    self.low_bound_list[self.count_round] = (low_bound, time.time() - start, 'cut')
                    self.upper_bound_list[self.count_round] = (self.best_up_bound, time.time() - start)
            print('new branch up bound is', self.best_up_bound)

        self.print_answer()
        # self.get_time_table_of_best_solution(self.best_solution)

    def estimate_Astar_value(self, node_list, upper_bound):
        Astar_list = []
        print('begin node list')
        for node, task in node_list:    # task: [0]
            t2 = 0
            execute_time = 0
            for i in task:
                execute_num = 0
                for key in self.task_type.keys():   # 在self.task_type的key中找到对应的子任务
                    if self.task_data[i][1] in key and self.task_data[i][2] in key:
                        subtask_label = key
                for n in self.task_type[subtask_label].values():
                    execute_num = execute_num + n
                t2 = t2 + 10 * execute_num
            Astar_list.append(t2 / upper_bound / len(self.agent_data))
        # print(Astar_list)
        return Astar_list

    def get_upper_bound_online(self, init_node, assigned_task, extro_constrain):
        # print('online')
        if len(assigned_task) == len(self.task_data):
            t, time_list, _ = self.opt_for_partial_assigment_online(init_node, assigned_task, extro_constrain)
            return max(time_list), init_node
        un_found = 1
        sample_list = []
        assigned_tasks = set(copy.deepcopy(assigned_task))
        while un_found > 0:
            # 根据new_init_node内容统计出每个智能体当前的剩余弹量，存放进字典remain_missile_num {0/智能体id:2/当前剩余弹量,...}
            remain_missile_num = dict()
            agent_id = 0
            for agenti_task_list in init_node:
                used_missile_num = 0
                for task_info in agenti_task_list:
                    used_missile_num = used_missile_num + task_info[2]
                agenti_missile_num = self.agent_data[agent_id][5]
                remain_missile_num[agent_id] = agenti_missile_num - used_missile_num
                agent_id = agent_id + 1
            
            # 收集该节点下一步可分配的子任务集合
            assiged_task_set = set()
            to_assig_task = set(self.poset_graph.succ['root'])
            for task in assigned_tasks:
                assiged_task_set.add(task)
                to_assig_task = to_assig_task | set(self.poset_graph.succ[task])
            un_assig_task1 = to_assig_task - assiged_task_set - set(extro_constrain.finished_time_list.keys())
            un_assig_task = copy.deepcopy(un_assig_task1)
            for i in un_assig_task1:
                # check if pre_task is satisfied
                if not len(set(self.poset_graph.pred[i]) - assiged_task_set - {'root'}) == 0:
                    un_assig_task.remove(i)     # un_assig_task集合中是真正下一步可以分配的任务
            # to_assig_task = random.sample(list(un_assig_task), 1)   # e.g. [2]
            to_assig_task = [random.choice(list(un_assig_task))]
            # get feasible assig_task
            assigned_tasks.add(to_assig_task[0])
            for key in self.task_type.keys():   # 在self.task_type的key中找到对应的子任务标签，e.g. attack_b01
                if self.task_data[to_assig_task[0]][1] in key and self.task_data[to_assig_task[0]][2] in key:
                    subtask_label = key
            
            pot_agent_list = []
            assign_dic = dict()     # 记录对于该任务而言可用的智能体 {('A-Missile',4): [0,1,2,...]}
            for agent_type, num in self.task_type[subtask_label].items():
                assign_dic[(agent_type,num)] = list()
                for agent in self.agent_data:
                     # 1.任务会指定种类;2.智能体也规定了可做任务;3.需判断智能体还有没有剩余弹量;4.判断智能体有没有损毁
                    if (agent[1] == agent_type) and (subtask_label in agent[2].keys()) and (remain_missile_num[agent[0]] != 0) and (agent[0] not in extro_constrain.broken_agent_list):
                        assign_dic[(agent_type,num)].append(agent[0])
            
            agent_com_dic = dict()      # 存储每类智能体可用的组合及时间窗, {'A-Missile': [([1,2,3],(t1,t2)),([],()),...]}
            for type_and_num, agent_list in assign_dic.items():
                # 首先收集导弹量足够的智能体组合 !改了个bug
                agent_com_list_init = self.generate_agent_combinations(agent_list)
                agent_com_list = copy.deepcopy(agent_com_list_init)
                for agent_com in agent_com_list_init:
                    total_remain_missile_num = 0
                    for agent in agent_com:
                        total_remain_missile_num += remain_missile_num[agent]
                    if total_remain_missile_num < type_and_num[1]:
                        agent_com_list.remove(agent_com)
                # 对每个智能体组合计算是否时间窗重叠，并存入字典agent_com_dic中
                agent_com_dic[type_and_num[0]] = []
                for agent_com in agent_com_list:
                    tw_list = []
                    for agent_id in agent_com:
                        tw_list.append(self.agent_data[agent_id][2][subtask_label][1])
                    overlap_tw_or_false = self.judge_and_calculate_overlap(tw_list)
                    if overlap_tw_or_false:
                        agent_com_dic[type_and_num[0]].append((list(agent_com), overlap_tw_or_false))
            # agent_com_dic = dict()      # 存储每类智能体可用的组合及时间窗, {'A-Missile': [([1,2,3],(t1,t2)),([],()),...]}
            # for type_and_num, agent_list in assign_dic.items():
            #     tw_id_list = []     # 存储每个智能体对该任务的时间窗及它的id [[t1, t2, id],...]
            #     for agent_id in agent_list:
            #         tw = self.agent_data[agent_id][2][subtask_label][1]
            #         tw.append(agent_id)
            #         tw_id_list.append(tw)
            #     agent_com_and_oltw = self.find_three_exact_overlapping_windows(tw_id_list, type_and_num[1])
            #     agent_com_dic[type_and_num[0]] = agent_com_and_oltw
            if len(self.task_type[subtask_label].keys()) > 1:   
                for i in range(5):      # 找5次时间窗有重叠的智能体组合
                    agent_id_tw_list = []
                    for agent_id_tw_all in agent_com_dic.values():
                        # 每种类型随机选择一个智能体组合
                        agent_id_tw_list.append(random.choice(agent_id_tw_all))
                    agent_com = []
                    overlap_tw_list = []
                    for agent_id_tw in agent_id_tw_list:
                        agent_com.extend(agent_id_tw[0])
                        overlap_tw_list.append(agent_id_tw[1])
                    if self.judge_and_calculate_overlap(overlap_tw_list) and (agent_com not in pot_agent_list):
                        pot_agent_list.append(agent_com)
            else:
                for agent_id_tw_all in agent_com_dic.values():
                    for agent_id_tw in agent_id_tw_all:
                        pot_agent_list.append(agent_id_tw[0])

            if pot_agent_list:
                # 根据智能体时间窗可开始时间贪婪选择智能体组合
                selected_agent_com = self.select_best_agent_com_greedy(subtask_label, pot_agent_list)
                assign_list = {}
                assign_list[subtask_label] = selected_agent_com

                for sub_task, com in assign_list.items():
                    # 创建一个字典用于记录每个智能体在此次任务中使用的弹量 {agent_id: assigned_missile_num}
                    missile_assign_dic = dict()
                    for agent_type, num in self.task_type[subtask_label].items():
                        type_i_agent_list = list()  # 收集整个智能体组合中每个类型的智能体
                        for agent_id in com:
                            if self.agent_data[agent_id][1] == agent_type:
                                type_i_agent_list.append(agent_id)

                        if self.select_agent_method == 'uniform':
                            # 根据智能体所剩弹量进行从小到大排列（升序）
                            sorted_agent_list = sorted(type_i_agent_list, key=lambda x: remain_missile_num[x])
                            basic_size = num // len(sorted_agent_list)
                            remainder = num % len(sorted_agent_list)
                            if basic_size < 1:
                                for i in range(num):
                                    missile_assign_dic[sorted_agent_list[i]] = 1
                            else:
                                for i in range(len(sorted_agent_list)):
                                    remain_num = remain_missile_num[sorted_agent_list[i]]
                                    if remain_num <= basic_size:
                                        missile_assign_dic[sorted_agent_list[i]] = remain_num
                                        remainder = remainder + basic_size - remain_num
                                    elif remainder > 0:
                                        missile_assign_dic[sorted_agent_list[i]] = basic_size + 1
                                        remainder -= 1
                                    else:
                                        missile_assign_dic[sorted_agent_list[i]] = basic_size
                                # 如果弹量需求还未被满足
                                if remainder > 0:
                                    for i in range(len(sorted_agent_list)):
                                        remain_num = remain_missile_num[sorted_agent_list[i]]
                                        if missile_assign_dic[sorted_agent_list[i]] - remain_num >= remainder:
                                            missile_assign_dic[sorted_agent_list[i]] += remainder
                                            remainder = 0
                                            break
                                        elif missile_assign_dic[sorted_agent_list[i]] - remain_num > 0:
                                            init_assign_num = missile_assign_dic[sorted_agent_list[i]]
                                            missile_assign_dic[sorted_agent_list[i]] = remain_num
                                            remainder = remainder - (remain_num - init_assign_num)
                                if remainder > 0:
                                    print('该智能体组合无法满足目标的弹量要求')
                        if self.select_agent_method == 'concentrate':
                            # 根据智能体所剩弹量进行从大到小排列（降序）
                            sorted_agent_list = sorted(type_i_agent_list, key=lambda x: remain_missile_num[x], reverse=True)
                            remain_to_assign_num = num
                            for agent_id in sorted_agent_list:
                                if remain_to_assign_num > remain_missile_num[agent_id]:
                                    missile_assign_dic[agent_id] = remain_missile_num[agent_id]
                                    remain_to_assign_num = remain_to_assign_num - remain_missile_num[agent_id]
                                else:
                                    missile_assign_dic[agent_id] = remain_to_assign_num
                                    break
            
                    new_node = copy.deepcopy(init_node)
                    for agent_id, missile_num in missile_assign_dic.items():
                        new_node[agent_id].append((tuple(self.task_data[to_assig_task[0]]), sub_task, missile_num))    # ((0, 'attack', 'b01'), 'attack_b01',2/missile_num)
            else:
                print('导弹车无法满足弹量需求')
                return float('inf'), None
                
            if len(assigned_tasks) == len(self.task_data):
                sample_list.append(new_node)
                un_found = un_found - 1
                t, time_list_i, dic_t = self.opt_for_partial_assigment_online(new_node, assigned_tasks, extro_constrain)
            # unfinished_assigned_task = list(set(assigned_tasks).intersection(set(extro_constrain.task_dic.keys())))
            # unfinished_assigned_task_list = []
            # for i in unfinished_assigned_task:
            #     unfinished_assigned_task_list.append(tuple(self.task_data[i]))
            # t, time_list_i, dic_t = self.opt_for_partial_assigment_online(new_node, unfinished_assigned_task_list,
            #                                                                 extro_constrain)

            init_node = new_node
        finished_time_list = [time for task, time in extro_constrain.finished_time_list.items()]
        finished_time_list.append(t)
        # time_list=[]
        if sample_list == []:
            return float('inf'), None
        else:
            return max(finished_time_list), init_node

    def get_upper_bound(self, node, assigned_tasks, up_bound_method):
        if up_bound_method == 'greedy':  # should be finished
            up_bound, solution = self.found_solution_greedy(node, assigned_tasks)
            # print('get up_bound',up_bound)
            return up_bound, solution
        else:
            raise Exception('Undefined up bound method')
            return up_bound, solution

    def found_solution_greedy(self, init_node, assigned_tasks):
        '''
        input: init_node, assigned_tasks
        output: upper_bound, solution

        '''
        # print('assigned_task',assigned_tasks)
        if not len(assigned_tasks) == 0:
            t, _ = self.opt_for_partial_assigment(init_node, assigned_tasks)
        else:
            t = 0
        t2 = 0
        for i in assigned_tasks:
            num = 0
            action_label = self.task_data[i][1]
            region_label = self.task_data[i][2]
            for key in self.task_type.keys():   # 在self.task_type的key中找到对应的子任务
                if action_label in key and region_label in key:
                    subtask_label = key     # e.g.'attack_b01'
            for n in self.task_type[subtask_label].values():
                num = num + n
            t2 = t2 + 10 * num     # t2不同
            # t2=t2+self.task_type[subtask_label]][0]
        if t <= 0.01:
            tstar = 1
        else:
            tstar = t2 / t / len(self.agent_data)
        sequence = [(set(assigned_tasks), init_node)]
        sequence_t = [tstar]
        un_found = 1
        sample_list = []
        while sequence != [] and un_found > 0:
            popi = sequence_t.index(max(sequence_t))
            root_node = sequence.pop(popi)
            t_label = sequence_t.pop(popi)
            assiged_task = root_node[0]
            new_init_node = root_node[1]
            # 根据new_init_node内容统计出每个智能体当前的剩余弹量，存放进字典remain_missile_num {0/智能体id:2/当前剩余弹量,...}
            remain_missile_num = dict()
            agent_id = 0
            for agenti_task_list in new_init_node:
                used_missile_num = 0
                for task_info in agenti_task_list:
                    used_missile_num = used_missile_num + task_info[2]
                agenti_missile_num = self.agent_data[agent_id][5]
                remain_missile_num[agent_id] = agenti_missile_num - used_missile_num
                agent_id = agent_id + 1
            
            # 收集该节点下一步可分配的子任务集合
            assiged_task_set = set()
            to_assig_task = set(self.poset_graph.succ['root'])
            for task in assiged_task:
                assiged_task_set.add(task)
                to_assig_task = to_assig_task | set(self.poset_graph.succ[task])
            un_assig_task1 = to_assig_task - assiged_task_set
            un_assig_task = copy.deepcopy(un_assig_task1)
            for i in un_assig_task1:
                if not len(set(self.poset_graph.pred[i]) - assiged_task_set - {'root'}) == 0:
                    un_assig_task.remove(i)     # 要保证其parent subtask都已经分配完了
            # -===== already get feasible assgin task
            sequence = []
            sequence_t = []
            for to_assig_task in un_assig_task:     # un_assig_task: {0, 2, 4, 6}
                new_assiged_task = assiged_task | {to_assig_task}
                pot_agent_list = []
                # print(self.task_type.keys())
                for key in self.task_type.keys():   # 在self.task_type的key中找到对应的子任务
                    if self.task_data[to_assig_task][1] in key and self.task_data[to_assig_task][2] in key:
                        subtask_label = key
            
                assign_dic = dict()     # 记录对于该任务而言可用的智能体 {('A-Missile',4): [0,1,2,...]}
                for agent_type, num in self.task_type[subtask_label].items():
                    assign_dic[(agent_type,num)] = list()
                    for agent in self.agent_data:
                         # 1.任务会指定种类;2.智能体也规定了可做任务;3.需判断智能体还有没有剩余弹量
                        if (agent[1] == agent_type) and (subtask_label in agent[2].keys()) and (remain_missile_num[agent[0]] != 0):
                            assign_dic[(agent_type,num)].append(agent[0])
                
                agent_com_dic = dict()      # 存储每类智能体可用的组合及时间窗, {'A-Missile': [([1,2,3],(t1,t2)),([],()),...]}
                for type_and_num, agent_list in assign_dic.items():
                    # 首先收集导弹量足够的智能体组合 !改了个bug
                    agent_com_list_init = self.generate_agent_combinations(agent_list)
                    agent_com_list = copy.deepcopy(agent_com_list_init)
                    for agent_com in agent_com_list_init:
                        total_remain_missile_num = 0
                        for agent in agent_com:
                            total_remain_missile_num += remain_missile_num[agent]
                        if total_remain_missile_num < type_and_num[1]:
                            agent_com_list.remove(agent_com)
                    # 对每个智能体组合计算是否时间窗重叠，并存入字典agent_com_dic中
                    agent_com_dic[type_and_num[0]] = []
                    for agent_com in agent_com_list:
                        tw_list = []
                        for agent_id in agent_com:
                            tw_list.append(self.agent_data[agent_id][2][subtask_label][1])
                        overlap_tw_or_false = self.judge_and_calculate_overlap(tw_list)
                        if overlap_tw_or_false:
                            agent_com_dic[type_and_num[0]].append((list(agent_com), overlap_tw_or_false))
                # agent_com_dic = dict()      # 存储每类智能体可用的组合及时间窗, {'A-Missile': [([1,2,3],(t1,t2)),([],()),...]}
                # for type_and_num, agent_list in assign_dic.items():
                #     tw_id_list = []     # 存储每个智能体对该任务的时间窗及它的id [[t1, t2, id],...]
                #     for agent_id in agent_list:
                #         tw = self.agent_data[agent_id][2][subtask_label][1]
                #         tw.append(agent_id)
                #         tw_id_list.append(tw)
                #     agent_com_and_oltw = self.find_three_exact_overlapping_windows(tw_id_list, type_and_num[1])
                #     agent_com_dic[type_and_num[0]] = agent_com_and_oltw
                if len(self.task_type[subtask_label].keys()) > 1:   
                    for i in range(5):      # 找5次时间窗有重叠的智能体组合
                        agent_id_tw_list = []
                        for agent_id_tw_all in agent_com_dic.values():
                            # 每种类型随机选择一个智能体组合
                            agent_id_tw_list.append(random.choice(agent_id_tw_all))
                        agent_com = []
                        overlap_tw_list = []
                        for agent_id_tw in agent_id_tw_list:
                            agent_com.extend(agent_id_tw[0])
                            overlap_tw_list.append(agent_id_tw[1])
                        if self.judge_and_calculate_overlap(overlap_tw_list) and (agent_com not in pot_agent_list):
                            pot_agent_list.append(agent_com)
                else:
                    for agent_id_tw_all in agent_com_dic.values():
                        for agent_id_tw in agent_id_tw_all:
                            pot_agent_list.append(agent_id_tw[0])

                if pot_agent_list:
                    # 根据智能体时间窗可开始时间贪婪选择智能体组合
                    selected_agent_com = self.select_best_agent_com_greedy(subtask_label, pot_agent_list)
                    assign_list = {}
                    assign_list[subtask_label] = selected_agent_com
                    for sub_task, com in assign_list.items():
                        # 创建一个字典用于记录每个智能体在此次任务中使用的弹量 {agent_id: assigned_missile_num}
                        missile_assign_dic = dict()
                        for agent_type, num in self.task_type[subtask_label].items():
                            type_i_agent_list = list()  # 收集整个智能体组合中每个类型的智能体
                            for agent_id in com:
                                if self.agent_data[agent_id][1] == agent_type:
                                    type_i_agent_list.append(agent_id)

                            if self.select_agent_method == 'uniform':
                                # 根据智能体所剩弹量进行从小到大排列（升序）
                                sorted_agent_list = sorted(type_i_agent_list, key=lambda x: remain_missile_num[x])
                                basic_size = num // len(sorted_agent_list)
                                remainder = num % len(sorted_agent_list)
                                if basic_size < 1:
                                    for i in range(num):
                                        missile_assign_dic[sorted_agent_list[i]] = 1
                                else:
                                    for i in range(len(sorted_agent_list)):
                                        remain_num = remain_missile_num[sorted_agent_list[i]]
                                        if remain_num <= basic_size:
                                            missile_assign_dic[sorted_agent_list[i]] = remain_num
                                            remainder = remainder + basic_size - remain_num
                                        elif remainder > 0:
                                            missile_assign_dic[sorted_agent_list[i]] = basic_size + 1
                                            remainder -= 1
                                        else:
                                            missile_assign_dic[sorted_agent_list[i]] = basic_size
                                    # 如果弹量需求还未被满足
                                    if remainder > 0:
                                        for i in range(len(sorted_agent_list)):
                                            remain_num = remain_missile_num[sorted_agent_list[i]]
                                            if missile_assign_dic[sorted_agent_list[i]] - remain_num >= remainder:
                                                missile_assign_dic[sorted_agent_list[i]] += remainder
                                                remainder = 0
                                                break
                                            elif missile_assign_dic[sorted_agent_list[i]] - remain_num > 0:
                                                init_assign_num = missile_assign_dic[sorted_agent_list[i]]
                                                missile_assign_dic[sorted_agent_list[i]] = remain_num
                                                remainder = remainder - (remain_num - init_assign_num)
                                    if remainder > 0:
                                        print('该智能体组合无法满足目标的弹量要求')
                            if self.select_agent_method == 'concentrate':
                                # 根据智能体所剩弹量进行从大到小排列（降序）
                                sorted_agent_list = sorted(type_i_agent_list, key=lambda x: remain_missile_num[x], reverse=True)
                                remain_to_assign_num = num
                                for agent_id in sorted_agent_list:
                                    if remain_to_assign_num > remain_missile_num[agent_id]:
                                        missile_assign_dic[agent_id] = remain_missile_num[agent_id]
                                        remain_to_assign_num = remain_to_assign_num - remain_missile_num[agent_id]
                                    else:
                                        missile_assign_dic[agent_id] = remain_to_assign_num
                                        break                   
                    
                        new_node = copy.deepcopy(new_init_node)
                        for agent_id, missile_num in missile_assign_dic.items():
                            new_node[agent_id].append((self.task_data[to_assig_task], sub_task, missile_num))    # ((0, 'attack', 'b01'), 'attack_b01',2/missile_num)
                else:
                    print('导弹车无法满足弹量需求')
                    return float('inf'), None
                    
                if len(new_assiged_task) == len(self.task_data):    # 判断是不是所有子任务都分配完了
                    sample_list.append(new_node)
                    un_found = un_found - 1
                else:
                    sequence.append((new_assiged_task, new_node))
                    t, _ = self.opt_for_partial_assigment(new_node, new_assiged_task)
                    t2 = 0
                    for i in new_assiged_task:
                        num = 0
                        action_label = self.task_data[i][1]
                        region_label = self.task_data[i][2]
                        for key in self.task_type.keys():   # 在self.task_type的key中找到对应的子任务
                            if action_label in key and region_label in key:
                                subtask_label = key     # e.g.'attack_b01'
                        for n in self.task_type[subtask_label].values():
                            num = num + n
                        t2 = t2 + 10 * num    # duration*num求和
                        # t2=t2+self.task_type[self.task_data[i][1]][0]
                    if t <= 0.1:
                        tstar = 1
                    else:
                        tstar = t2 / t / len(self.agent_data)
                    sequence_t.append(tstar)
                        
        time_list = []
        if sample_list == []:
            return self.horizon, []
        else:
            for node in sample_list:
                a, b = self.opt_for_partial_assigment(node, range(len(self.task_data)))
                time_list.append(a)
            solution = sample_list[time_list.index(min(time_list))]     # solution就是整体makespan最小的node
            return min(time_list), solution

    
    def select_best_agent_com_greedy(self, subtask, pot_agent_list):    # 根据智能体时间窗可开始时间贪婪选择智能体组合
        est_list = []
        for agent_com in pot_agent_list:
            # 当只有一个智能体时
            if len(agent_com) == 1:
                tw = self.agent_data[agent_com[0]][2][subtask][1]
                est_list.append(tw[0])
            else:
                tw_list = []
                for agent_id in agent_com:
                    tw_list.append(self.agent_data[agent_id][2][subtask][1])
                if self.judge_and_calculate_overlap(tw_list):
                    overlap_tw = self.judge_and_calculate_overlap(tw_list)
                est_list.append(overlap_tw[0])
        selected_agent_com = pot_agent_list[est_list.index(min(est_list))] 
        return selected_agent_com


    def generate_poset_graph(self):     # 根据偏序关系画出偏序图，没考虑"!="关系，后续"="关系可以加在这里
        poset_graph = nx.DiGraph()
        for i, j in self.poset['<']:
            poset_graph.add_edge(i, j)
        for i, j in self.poset['<=']:
            poset_graph.add_edge(i, j)
        for i in range(len(self.task_data)):
            if not poset_graph.has_node(i):
                poset_graph.add_node(i)
        new_poset_graph = copy.deepcopy(poset_graph)
        self.poset_graph = poset_graph
        remove_list = []
        for i, j in poset_graph.edges:
            removable_label = self.find_path(i, j)      # 当1<=3和1<=2<=3都存在时，需要把1<=3删掉（考虑是一个一个子任务进行分配的）
            if removable_label:
                remove_list.append((i, j))
        for i, j in remove_list:
            self.poset_graph.remove_edge(i, j)
        node_set = []
        for i in self.poset_graph.nodes:
            if len(self.poset_graph.pred[i]) == 0:
                node_set.append(i)
        for i in node_set:
            self.poset_graph.add_edge('root', i)

    def get_time_table_of_best_solution(self, solution):
        t, end_time = self.opt_for_partial_assigment(solution, range(len(self.task_data)))
        self.task_time_table = [[i, end_time[i][0]] for i in
                                range(len(self.task_data))]

    def get_time_table_of_best_solution_online(self, solution, extron_constrain):
        full_assigned_Task = set()
        for task in self.task_data:
            if task[0] not in extron_constrain.finished_time_list.keys():
                full_assigned_Task.add(task[0])
        max_time, end_time, task_dic = self.opt_for_partial_assigment_online(solution, full_assigned_Task,
                                                                             extron_constrain)
        self.task_time_table = []
        for i in range(len(self.task_data)):
            if i in task_dic.keys():
                self.task_time_table.append(
                    [i, end_time[task_dic[i]][0]])
            # else:
            #     self.task_time_table.append(
            #         [i, extron_constrain.finished_time_list[i] - extron_constrain.task_execute_time[i],
            #          extron_constrain.finished_time_list[i]])

    def find_path(self, start, end):    # 在偏序图中如果有两条从start到end的路径
        path = []
        paths = []
        queue = [(start, path)]
        while queue:
            start, path = queue.pop()
            # print('PATH', path)
            path = path + [start]
            # print('PATH after adding start ', path)
            if start == end:
                # print('end')
                paths.append(path)
            for node in set(self.poset_graph.neighbors(start)).difference(path):
                queue.append((node, path))
            # print('queue', queue)
        if len(paths) >= 2:
            removable_label = 1
            return removable_label
        else:
            removable_label = 0
            return removable_label

    

    def prune_tree(self):
        check_node = [[((0, 'goto', 'c'), 'goto')], [((1, 'surround', 'g'), 'surrounder')],
                      [((1, 'surround', 'g'), 'surrounder')], [], [], []]
        i = 0
        to_prune_set = []
        for root_node, assigned_tasks, up_bound, low_bound in self.branch_tree:
            # if low_bound>=self.best_up_bound:
            # if root_node==check_node:
            #    print('low_bound!!!!',low_bound)
            #    if low_bound>27:
            #        print('error')
            if low_bound + 0.1 >= self.best_up_bound:
                to_prune_set.append(i)
            i = i + 1
        for i in reversed(to_prune_set):
            del self.branch_tree[i]
        print('in this step deleta', len(to_prune_set), 'banch')

    

    def exten_child_nodes(self, node, assign_task):     # 根据R-poset Graph以及动作所需智能体数量扩展子节点
        # 根据node内容统计出每个智能体当前的剩余弹量，存放进字典remain_missile_num {0/智能体id:2/当前剩余弹量,...}
        remain_missile_num = dict()
        agent_id = 0
        for agenti_task_list in node:
            used_missile_num = 0
            for task_info in agenti_task_list:
                used_missile_num = used_missile_num + task_info[2]
            agenti_missile_num = self.agent_data[agent_id][5]
            remain_missile_num[agent_id] = agenti_missile_num - used_missile_num
            agent_id = agent_id + 1
        
        child_node_list = []
        assiged_task_set = set()    # node中已分配的子任务
        to_assig_task = set(self.poset_graph.succ['root'])
        for task in assign_task:
            assiged_task_set.add(task)
            to_assig_task = to_assig_task | set(self.poset_graph.succ[task])    # |是取并集的意思
        un_assig_task1 = to_assig_task - assiged_task_set
        un_assig_task = copy.deepcopy(un_assig_task1)
        for i in un_assig_task1:
            if not len(set(self.poset_graph.pred[i]) - assiged_task_set - {'root'}) == 0:   # 判断parent_subtask是否已经分配完了
                un_assig_task.remove(i)
        to_assig_set = []
        for task in un_assig_task:
            to_assig_set.append(self.task_data[task])   # to_assig_set数据格式：[(6, 'scout', 'b05'), (8, 'attack', 'b01'),...]
        for task in to_assig_set:   # task: (0, 'scout', 'b01')
            assign_task_set = copy.deepcopy(assign_task)
            assign_task_set.append(task[0])     # 父节点已分配子任务集合再加上这个子任务
            pot_agent_list = []
            for key in self.task_type.keys():   # 在self.task_type的key中找到对应的子任务
                if task[1] in key and task[2] in key:
                    subtask_label = key
            assign_dic = dict()     # 记录对于该任务而言可用的智能体 {('A-Missile',4): [0,1,2,...]}
            for agent_type, num in self.task_type[subtask_label].items():
                assign_dic[(agent_type,num)] = list()
                for agent in self.agent_data:
                     # 1.任务会指定种类;2.智能体也规定了可做任务;3.需判断智能体还有没有剩余弹量
                    if (agent[1] == agent_type) and (subtask_label in agent[2].keys()) and (remain_missile_num[agent[0]] != 0):
                        assign_dic[(agent_type,num)].append(agent[0])
            
            agent_com_dic = dict()      # 存储每类智能体可用的组合及时间窗, {'A-Missile': [([1,2,3],(t1,t2)),([],()),...]}
            for type_and_num, agent_list in assign_dic.items():
                # 首先收集导弹量足够的智能体组合
                agent_com_list = self.generate_agent_combinations(agent_list)
                for agent_com in agent_com_list:
                    total_remain_missile_num = 0
                    for agent in agent_com:
                        total_remain_missile_num += remain_missile_num[agent]
                    if total_remain_missile_num < type_and_num[1]:
                        agent_com_list.remove(agent_com)
                # 对每个智能体组合计算是否时间窗重叠，并存入字典agent_com_dic中
                agent_com_dic[type_and_num[0]] = []
                for agent_com in agent_com_list:
                    tw_list = []
                    for agent_id in agent_com:
                        tw_list.append(self.agent_data[agent_id][2][subtask_label][1])
                    overlap_tw_or_false = self.judge_and_calculate_overlap(tw_list)
                    if overlap_tw_or_false:
                        agent_com_dic[type_and_num[0]].append((list(agent_com), overlap_tw_or_false))

            # agent_com_dic = dict()      # 存储每类智能体可用的组合及时间窗, {'A-Missile': [([1,2,3],(t1,t2)),([],()),...]}
            # for type_and_num, agent_list in assign_dic.items():
            #     tw_id_list = []     # 存储智能体对该任务的时间窗及它的id [[t1, t2, id],...]
            #     for agent_id in agent_list:
            #         tw = self.agent_data[agent_id][2][subtask_label][1]
            #         tw.append(agent_id)
            #         tw_id_list.append(tw)
            #     agent_com_and_oltw = self.find_three_exact_overlapping_windows(tw_id_list, type_and_num[1])
            #     agent_com_dic[type_and_num[0]] = agent_com_and_oltw
            
            if len(self.task_type[subtask_label].keys()) > 1:
                for i in range(10):      # 找5次时间窗有重叠的智能体组合
                    agent_id_tw_list = []
                    for agent_id_tw_all in agent_com_dic.values(): 
                        # 每种类型随机选择一个智能体组合
                        agent_id_tw_list.append(random.choice(agent_id_tw_all))
                    agent_com = []
                    overlap_tw_list = []
                    for agent_id_tw in agent_id_tw_list:
                        agent_com.extend(agent_id_tw[0])
                        overlap_tw_list.append(agent_id_tw[1])
                    if self.judge_and_calculate_overlap(overlap_tw_list) and (agent_com not in pot_agent_list):
                        pot_agent_list.append(agent_com)
            else:
                for agent_id_tw_all in agent_com_dic.values():
                    for agent_id_tw in agent_id_tw_all:
                        pot_agent_list.append(agent_id_tw[0])
            
            if pot_agent_list:
                for assig_list in pot_agent_list:   # assig_list: (1,2,3,4)
                    # 创建一个字典用于记录每个智能体在此次任务中使用的弹量 {agent_id: assigned_missile_num}
                    missile_assign_dic = dict()
                    for agent_type, num in self.task_type[subtask_label].items():
                        type_i_agent_list = list()  # 收集整个智能体组合中每个类型的智能体
                        for agent_id in assig_list:
                            if self.agent_data[agent_id][1] == agent_type:
                                type_i_agent_list.append(agent_id)

                        if self.select_agent_method == 'uniform':
                            # 根据智能体所剩弹量进行从小到大排列（升序）
                            sorted_agent_list = sorted(type_i_agent_list, key=lambda x: remain_missile_num[x])
                            basic_size = num // len(sorted_agent_list)
                            remainder = num % len(sorted_agent_list)
                            if basic_size < 1:
                                for i in range(num):
                                    missile_assign_dic[sorted_agent_list[i]] = 1
                            else:
                                for i in range(len(sorted_agent_list)-1):
                                    remain_num = remain_missile_num[sorted_agent_list[i]]
                                    if remain_num <= basic_size:
                                        missile_assign_dic[sorted_agent_list[i]] = remain_num
                                        remainder = remainder + basic_size - remain_num
                                    elif remainder > 0:
                                        missile_assign_dic[agent_id] = basic_size + 1
                                        remainder -= 1
                                    else:
                                        missile_assign_dic[agent_id] = basic_size
                                # 要给最后一个智能体分配剩余需求的弹量
                                final_agent_id = sorted_agent_list[-1]
                                missile_assign_dic[final_agent_id] = basic_size + remainder
                        if self.select_agent_method == 'concentrate':
                            # 根据智能体所剩弹量进行从大到小排列（降序）
                            sorted_agent_list = sorted(type_i_agent_list, key=lambda x: remain_missile_num[x], reverse=True)
                            remain_to_assign_num = num
                            for agent_id in sorted_agent_list:
                                if remain_to_assign_num > remain_missile_num[agent_id]:
                                    missile_assign_dic[agent_id] = remain_missile_num[agent_id]
                                    remain_to_assign_num = remain_to_assign_num - remain_missile_num[agent_id]
                                else:
                                    missile_assign_dic[agent_id] = remain_to_assign_num
                                    break
                                
                    child_node = copy.deepcopy(node)
                    for agent_id, missile_num in missile_assign_dic.items():
                        child_node[agent_id].append((task, subtask_label, missile_num))    # ((0, 'attack', 'b01'), 'attack_b01',2/missile_num)

                    child_node_list.append((child_node, assign_task_set))
        print('extend child nodes', len(child_node_list))
        return child_node_list

    def exten_child_nodes_online(self, node, assign_task, extro_constrain):
        # 根据node内容统计出每个智能体当前的剩余弹量，存放进字典remain_missile_num {0/智能体id:2/当前剩余弹量,...}
        remain_missile_num = dict()
        agent_id = 0
        for agenti_task_list in node:
            used_missile_num = 0
            for task_info in agenti_task_list:
                used_missile_num = used_missile_num + task_info[2]
            agenti_missile_num = self.agent_data[agent_id][5]
            remain_missile_num[agent_id] = agenti_missile_num - used_missile_num
            agent_id = agent_id + 1
        
        child_node_list = []
        assiged_task_set = set()    # {0,1,2,...}
        to_assig_task = set(self.poset_graph.succ['root'])
        for task in assign_task:
            assiged_task_set.add(task)
            to_assig_task = to_assig_task | set(self.poset_graph.succ[task])
        un_assig_task1 = to_assig_task - assiged_task_set
        un_assig_task = copy.deepcopy(un_assig_task1)
        for i in un_assig_task1:
            if not len(set(self.poset_graph.pred[i]) - assiged_task_set - {'root'}) == 0:
                un_assig_task.remove(i)
        to_assig_set = []
        for task in un_assig_task:
            to_assig_set.append(self.task_data[task])   # to_assig_set数据格式：[(6, 'scout', 'b05'), (8, 'attack', 'b01'),...]
        for task in to_assig_set:   # task: (0, 'scout', 'b01')
            assign_task_set = set(copy.deepcopy(assign_task))
            assign_task_set.add(task[0])
            pot_agent_list = []
            for key in self.task_type.keys():   # 在self.task_type的key中找到对应的子任务
                if task[1] in key and task[2] in key:
                    subtask_label = key 
            assign_dic = dict()     # 记录对于该任务而言可用的智能体 {('A-Missile',4): [0,1,2,...]}
            for agent_type, num in self.task_type[subtask_label].items():
                assign_dic[(agent_type,num)] = list()
                for agent in self.agent_data:
                     # 1.任务会指定种类;2.智能体也规定了可做任务;3.需判断智能体还有没有剩余弹量;4.判断智能体有没有损毁
                    if (agent[1] == agent_type) and (subtask_label in agent[2].keys()) and (remain_missile_num[agent[0]] != 0) and (agent[0] not in extro_constrain.broken_agent_list):
                        assign_dic[(agent_type,num)].append(agent[0])
            
            agent_com_dic = dict()      # 存储每类智能体可用的组合及时间窗, {'A-Missile': [([1,2,3],(t1,t2)),([],()),...]}
            for type_and_num, agent_list in assign_dic.items():
                # 首先收集导弹量足够的智能体组合
                agent_com_list = self.generate_agent_combinations(agent_list)
                for agent_com in agent_com_list:
                    total_remain_missile_num = 0
                    for agent in agent_com:
                        total_remain_missile_num += remain_missile_num[agent]
                    if total_remain_missile_num < type_and_num[1]:
                        agent_com_list.remove(agent_com)
                # 对每个智能体组合计算是否时间窗重叠，并存入字典agent_com_dic中
                agent_com_dic[type_and_num[0]] = []
                for agent_com in agent_com_list:
                    tw_list = []
                    for agent_id in agent_com:
                        tw_list.append(self.agent_data[agent_id][2][subtask_label][1])
                    overlap_tw_or_false = self.judge_and_calculate_overlap(tw_list)
                    if overlap_tw_or_false:
                        agent_com_dic[type_and_num[0]].append((list(agent_com), overlap_tw_or_false))
            # agent_com_dic = dict()      # 存储每类智能体可用的组合及时间窗, {'A-Missile': [([1,2,3],(t1,t2)),([],()),...]}
            # for type_and_num, agent_list in assign_dic.items():
            #     tw_id_list = []     # 存储智能体对该任务的时间窗及它的id [[t1, t2, id],...]
            #     for agent_id in agent_list:
            #         tw = self.agent_data[agent_id][2][subtask_label][1]
            #         tw.append(agent_id)
            #         tw_id_list.append(tw)
            #     agent_com_and_oltw = self.find_three_exact_overlapping_windows(tw_id_list, type_and_num[1])    # 按任务需求数量生成三个可用的智能体组合及对应的重叠时间窗
            #     agent_com_dic[type_and_num[0]] = agent_com_and_oltw
                 
            if len(self.task_type[subtask_label].keys()) > 1:
                for i in range(10):      # 找5次时间窗有重叠的智能体组合
                    agent_id_tw_list = []
                    for agent_id_tw_all in agent_com_dic.values():
                        # 每种类型随机选择一个智能体组合
                        agent_id_tw_list.append(random.choice(agent_id_tw_all))
                    agent_com = []
                    overlap_tw_list = []
                    for agent_id_tw in agent_id_tw_list:
                        agent_com.extend(agent_id_tw[0])    # 做这个任务的智能体组合
                        overlap_tw_list.append(agent_id_tw[1])      # 不同类型的智能体组合的重叠时间窗
                    if (self.judge_and_calculate_overlap(overlap_tw_list)) and (agent_com not in pot_agent_list):
                        pot_agent_list.append(agent_com)
            else:
                for agent_id_tw_all in agent_com_dic.values():
                    for agent_id_tw in agent_id_tw_all:
                        pot_agent_list.append(agent_id_tw[0])                    
            
            if pot_agent_list:
                for assig_list in pot_agent_list:   # assig_list: (1,2,3,4)
                    # 创建一个字典用于记录每个智能体在此次任务中使用的弹量 {agent_id: assigned_missile_num}
                    missile_assign_dic = dict()
                    for agent_type, num in self.task_type[subtask_label].items():
                        type_i_agent_list = list()  # 收集整个智能体组合中每个类型的智能体
                        for agent_id in assig_list:
                            if self.agent_data[agent_id][1] == agent_type:
                                type_i_agent_list.append(agent_id)

                        if self.select_agent_method == 'uniform':
                            # 根据智能体所剩弹量进行从小到大排列（升序）
                            sorted_agent_list = sorted(type_i_agent_list, key=lambda x: remain_missile_num[x])
                            basic_size = num // len(sorted_agent_list)
                            remainder = num % len(sorted_agent_list)
                            if basic_size < 1:
                                for i in range(num):
                                    missile_assign_dic[sorted_agent_list[i]] = 1
                            else:
                                for i in range(len(sorted_agent_list)-1):
                                    remain_num = remain_missile_num[sorted_agent_list[i]]
                                    if remain_num <= basic_size:
                                        missile_assign_dic[sorted_agent_list[i]] = remain_num
                                        remainder = remainder + basic_size - remain_num
                                    elif remainder > 0:
                                        missile_assign_dic[agent_id] = basic_size + 1
                                        remainder -= 1
                                    else:
                                        missile_assign_dic[agent_id] = basic_size
                                # 要给最后一个智能体分配剩余需求的弹量
                                final_agent_id = sorted_agent_list[-1]
                                missile_assign_dic[final_agent_id] = basic_size + remainder
                        if self.select_agent_method == 'concentrate':
                            # 根据智能体所剩弹量进行从大到小排列（降序）
                            sorted_agent_list = sorted(type_i_agent_list, key=lambda x: remain_missile_num[x], reverse=True)
                            remain_to_assign_num = num
                            for agent_id in sorted_agent_list:
                                if remain_to_assign_num > remain_missile_num[agent_id]:
                                    missile_assign_dic[agent_id] = remain_missile_num[agent_id]
                                    remain_to_assign_num = remain_to_assign_num - remain_missile_num[agent_id]
                                else:
                                    missile_assign_dic[agent_id] = remain_to_assign_num
                                    break
                
                    child_node = copy.deepcopy(node)
                    for agent_id, missile_num in missile_assign_dic.items():
                        child_node[agent_id].append((task, subtask_label, missile_num))    # ((0, 'attack', 'b01'), 'attack_b01',2/missile_num)
                    finished_task_set = set(extro_constrain.finished_time_list.keys())
                    assign_task_set = assign_task_set | finished_task_set
                    child_node_list.append((child_node, list(assign_task_set)))
        print('extend child nodes online', len(child_node_list))
        return child_node_list

    def generate_agent_combinations(self, agent_id_list):
        combinations_list = []
        if len(agent_id_list) <= 2:
            for r in range(1, len(agent_id_list) + 1):
                combinations_list.extend(iter_com(agent_id_list, r))
        else:
            for r in range(len(agent_id_list)-2, len(agent_id_list) + 1):
                combinations_list.extend(iter_com(agent_id_list, r))
        return combinations_list
    
    def uniform_assign(self, required_missile_num, agent_num):
        # 计算每个部分的基本大小
        base_size = required_missile_num // agent_num
        # 计算余数
        remainder = required_missile_num % agent_num
        
        # 初始化结果列表
        parts = [base_size] * agent_num
        
        # 将余数依次分配给前几个部分
        for i in range(remainder):
            parts[i] += 1
        
        return parts
    
    def check_poset(self, agent, y, task):
        label = 1
        if len(agent) >= 1:
            for i in agent[:y]:
                if (task[0][0], i[0][0]) in self.poset:
                    label = 0
            for i in agent[y:]:
                if (i[0][0], task[0][0]) in self.poset:
                    label = 0
        return label

    def check_poset_in_agent(self, agent, task):
        label = 1
        for i in agent:
            if (task, i) in self.poset:
                label = 0
        return label

    def opt_for_partial_assigment(self, node, assign_task, i=None):     # 根据节点已分配的任务计算出在满足约束下的最优方案
        list_node = []
        for agent in node:
            list_node.append(tuple(agent))
        tuple_node = tuple(list_node)
        assign_task_tuple = tuple(assign_task)
        if assign_task_tuple in self.explored_node_dic.keys():      # self.explored_node_dic: {assign_task(0,1):{node:(max_end_time_value,end_time_value)}}
            if tuple_node in self.explored_node_dic[assign_task_tuple].keys():
                max_end_time_value, end_time_value = self.explored_node_dic[assign_task_tuple][tuple_node]
                return max_end_time_value, end_time_value
        assign_task_dic = {}    # 存放子任务id和index之间的映射关系
        t = 0
        # print('assign_Task:',assign_task)
        # print(node)
        for i in assign_task:
            assign_task_dic[i] = t
            t = t + 1
        end_time = cp.Variable(shape=(len(assign_task), 1), name='endtime', nonneg=True)    # 定义模型变量end_time，表示每个子任务的结束时间
        total_constrain = []
        tw_of_assigned_task = dict()    # 存储每个任务的时间窗
        for i in assign_task:   # 对每个任务收集执行的智能体id以及对应的时间窗，然后算出它们的重合时间窗生成约束
            subtask_label = self.task_data[i][1]+'_'+self.task_data[i][2]
            task_agentcom = list()
            total_tw = list()
            agent_id = 0
            for agent_task_sequence in node:
                for task in agent_task_sequence:
                    if i == task[0][0]:
                        task_agentcom.append(agent_id)
                agent_id = agent_id + 1
            for agent in task_agentcom:
                total_tw.append(self.agent_data[agent][2][subtask_label][1])
            tw_of_assigned_task[i] = self.judge_and_calculate_overlap(total_tw)
        
        # Time Window Constrain
        M3 = []
        B3 = [[]]
        TW = tw_of_assigned_task
        for i in assign_task:
            tw_i = TW[i]
            m = [0 for l in range(len(assign_task))]
            m[assign_task_dic[self.task_data[i][0]]] = 1
            M3.append(m)
            B3[0].append(tw_i[1])   # ei <= lfti
            m[assign_task_dic[self.task_data[i][0]]] = -1
            M3.append(m)
            B3[0].append(-tw_i[0])  # ei >= esti
        M31 = self.Turn_Matrix(M3)
        constraint3 = [M31 @ end_time <= B3]
        total_constrain.append(*constraint3)   
                
        # 偏序约束
        M1 = []
        B1 = [[]]
        # for i,j in self.poset['<']:
        for i, j in self.poset['<=']:
            if self.task_data[i][0] in assign_task and self.task_data[j][0] in assign_task:     #self.task_data[i][0]表示子任务id
                m = [0 for l in range(len(assign_task))]
                m[assign_task_dic[self.task_data[i][0]]] = 1
                m[assign_task_dic[self.task_data[j][0]]] = -1
                M1.append(m)
                B1[0].append(-4)    # eti - etj <= 0
        if not M1 == []:
            M11 = self.Turn_Matrix(M1)
            constraint1 = [M11 @ end_time <= B1]
            total_constrain.append(*constraint1)
            # print(B1)
        
        # 准备时间约束
        M2 = []
        B2 = [[]]   # 表示矩阵的一列
        for agent_i in range(len(self.agent_data)):     # 对于每个agent循环
            if len(node[agent_i]) > 1:     # 智能体i要执行多个子任务时，要考虑智能体导弹装填准备时间
                prepare_time = self.agent_data[agent_i][4]
                for task in range(len(node[agent_i]) - 1):
                    m = [0 for i in range(len(assign_task))]
                    c = assign_task_dic[node[agent_i][task][0][0]]
                    m[c] = -1
                    c = assign_task_dic[node[agent_i][task + 1][0][0]]
                    m[c] = 1
                    task1_name = node[agent_i][task][1]
                    task2_name = node[agent_i][task+1][1]
                    task1_duration = self.agent_data[agent_i][2][task1_name][0]
                    task2_duration = self.agent_data[agent_i][2][task2_name][0]
                    b = task2_duration - task1_duration + prepare_time     # et(task2)-durtion2>=et(task1)-duration1+prepare_time
                    M2.append(m)
                    B2[0].append((b))
        if not M2 == []:
            M21 = self.Turn_Matrix(M2)
            constraint2 = [M21 @ end_time >= B2]
            total_constrain.append(*constraint2)
        
        # 设置优化目标并求解
        # list1 = [[1] for task in assign_task]
        # obj = cp.Minimize(list1 @ end_time)     # 优化目标
        obj = cp.Minimize(cp.sum(end_time))
        prob = cp.Problem(obj, total_constrain)
        # prob.solve(solver=cp.SCS)
        prob.solve(solver='GLPK_MI')
        if prob.status == 'optimal':
            if assign_task_tuple in self.explored_node_dic.keys():
                if tuple_node in self.explored_node_dic[assign_task_tuple].keys():
                    max_end_time_value, end_time_value = self.explored_node_dic[assign_task_tuple][tuple_node]
            else:
                self.explored_node_dic[assign_task_tuple] = {}
                self.explored_node_dic[assign_task_tuple][tuple_node] = (max(end_time.value), end_time.value)   # max(end_time.value)就是makespan
            return max(end_time.value), end_time.value
        else:
            return self.horizon, []

    def opt_for_partial_assigment_online(self, node, assign_task, extro_constrain):
        # assign_task is error!
        if len(assign_task) == 0:
            t = 0
            for i, j in extro_constrain.begin_time.items():
                t = max(t, j)
            return t, 0, 0
        t = 0
        assign_task_dic = {}
        finished_task = []
        for i in assign_task:      # 把重规划之前已完成的任务剔除掉
            if i in extro_constrain.finished_time_list.keys():
                finished_task.append(i)
        for j in finished_task:
            assign_task.remove(j)
        
        for i in assign_task:
            assign_task_dic[i] = t
            t = t + 1
        # assign_task = [i[0] for i in assign_task]
        end_time = cp.Variable(shape=(len(assign_task), 1), name='endtime', nonneg=True)
        total_constrain = []
        tw_of_assigned_task = dict()    # 存储每个任务的时间窗
        for i in assign_task:   # 对每个任务收集执行的智能体id以及对应的时间窗，然后算出它们的重合时间窗生成约束
            subtask_label = self.task_data[i][1]+'_'+self.task_data[i][2]
            task_agentcom = list()
            total_tw = list()
            agent_id = 0
            for agent_task_sequence in node:
                for task in agent_task_sequence:
                    if i == task[0][0]:
                        task_agentcom.append(agent_id)
                agent_id = agent_id + 1
            for agent in task_agentcom:
                total_tw.append(self.agent_data[agent][2][subtask_label][1])
            tw_of_assigned_task[i] = self.judge_and_calculate_overlap(total_tw)
        # Time Window Constrain
        M3 = []
        B3 = [[]]
        TW = tw_of_assigned_task
        duration_list = []
        for agent in self.agent_data:
            for value in agent[2].values():
                duration_list.append(value[0])
        max_duration = max(duration_list)
        est1 = extro_constrain.break_time + max_duration
        for i in assign_task:
            tw_i = TW[i]
            m = [0 for l in range(len(assign_task))]
            m[assign_task_dic[self.task_data[i][0]]] = 1
            M3.append(m)
            B3[0].append(tw_i[1])   # ei <= lfti
            m[assign_task_dic[self.task_data[i][0]]] = -1
            M3.append(m)
            est = max(est1, tw_i[0])
            B3[0].append(-est)  # ei >= esti
        M31 = self.Turn_Matrix(M3)
        constraint3 = [M31 @ end_time <= B3]
        total_constrain.append(*constraint3)
        
        # 偏序约束
        M1 = []
        B1 = [[]]
        for i, j in self.poset['<=']:
            if self.task_data[i][0] in assign_task and self.task_data[j][0] in assign_task:     #self.task_data[i][0]表示子任务id
                m = [0 for l in range(len(assign_task))]
                m[assign_task_dic[self.task_data[i][0]]] = 1
                m[assign_task_dic[self.task_data[j][0]]] = -1
                M1.append(m)
                B1[0].append(-4)    # eti - etj <= 0

        if not M1 == []:
            M11 = self.Turn_Matrix(M1)
            constraint1 = [M11 @ end_time <= B1]
            total_constrain.append(*constraint1)
        
        # 准备时间约束
        M2 = []
        B2 = [[]]   # 表示矩阵的一列
        for agent_i in range(len(self.agent_data)):     # 对于每个agent循环
            # first_task_index = 0    # 记录智能体任务列表中第一个需要执行的任务的index
            # for i in range(len(node[agent_i])):
            #     if node[agent_i][i][0][0] in assign_task:
            #         first_task_index = i
            #         break
            if len(node[agent_i])> 1:     # 智能体i要执行多个子任务时，要考虑智能体导弹装填准备时间
                prepare_time = self.agent_data[agent_i][4]
                for task in range(len(node[agent_i]) - 1):
                    m = [0 for i in range(len(assign_task))]
                    c = assign_task_dic[node[agent_i][task][0][0]]
                    m[c] = -1
                    c = assign_task_dic[node[agent_i][task + 1][0][0]]
                    m[c] = 1
                    task1_name = node[agent_i][task][1]
                    task2_name = node[agent_i][task+1][1]
                    task1_duration = self.agent_data[agent_i][2][task1_name][0]
                    task2_duration = self.agent_data[agent_i][2][task2_name][0]
                    b = task2_duration - task1_duration + prepare_time     # et(task2)-durtion2>=et(task1)-duration1+prepare_time
                    M2.append(m)
                    B2[0].append((b))
        if not M2 == []:
            M21 = self.Turn_Matrix(M2)
            constraint2 = [M21 @ end_time >= B2]
            total_constrain.append(*constraint2)
        
        obj = cp.Minimize(cp.sum(end_time))
        prob = cp.Problem(obj, total_constrain)
        prob.solve(solver='GLPK_MI')
        max_time = 0
        # 先从已经完成的任务中找到最末尾的时刻
        for _, task_end_time in extro_constrain.finished_time_list.items():
            max_time = max(max_time, task_end_time)
        # 再从新规划出的所有任务中找到最末尾的时刻
        for n in end_time.value:
            max_time = max(n, max_time)
        if prob.status == 'optimal':
            return max_time, end_time.value, assign_task_dic
        else:
            return self.horizon, [], assign_task_dic

    def Turn_Matrix(self, M):
        r = [[] for i in M[0]]
        for i in M:
            for j in range(len(i)):
                r[j].append(i[j])
        return r

    def get_horizon(self):
        self.horizon = 1000000
        # for i in self.task_data:
        #    self.horizon=self.task_type[i[1]][0]*2+self.horizon+100

    def generate_time_budget(self):    # 把每个子任务的duration相加
        self.time_budget = 0
        for i in self.task_type.values():
            self.time_budget = self.time_budget + i[0]

    def get_distance(self, i, j):
        # return self.position[(i,j)]
        pos1 = self.position[i][0] - self.position[j][0]
        pos2 = self.position[i][1] - self.position[j][1]
        lenth = (pos1 ** 2 + pos2 ** 2) ** 0.5
        return lenth

    def print_answer(self):
        print('best value is:', self.best_up_bound)
        for i in range(len(self.agent_data)):
            print('agent', i + 1, 'task list is:', self.best_solution[i])

    def generate_online_adapt_extro_constrain(self, pre_solution, break_time, broken_agent_list):
        finished_task = set()
        unfinished_task = set()

        for task in self.task_time_table:   # self.task_time_table: [[0, 45.0], [1, 55.0],...]
            task_id = task[0]
            subtask_label = self.task_data[task_id][1]+'_'+self.task_data[task_id][2]
            task_agentcom = list()
            agent_id = 0
            duration_list = []
            for agent_task_sequence in pre_solution:
                for task_info in agent_task_sequence:
                    if task_id == task_info[0][0]:
                        task_agentcom.append(agent_id)
                        duration_list.append(self.agent_data[agent_id][2][subtask_label][0])
                agent_id = agent_id + 1
            min_duration = min(duration_list)
            if task[1] - min_duration <= break_time:
                finished_task.add(self.task_data[task[0]])
            else:
                unfinished_task.add(self.task_data[task[0]])
                # 正在执行但是未完成的任务 unfinished_task_list = {(3, 'washp21', 'p21'): ['washp21']}
        begin_time = {}
        id = 0
        for agent in self.best_solution:
            # 在找到正在执行的任务之前，默认第id个智能体的begin_time就是break_time
            begin_time[id] = break_time
            id = id + 1
        # broken的agent begin_time 是一个很大的数字
        for agent in broken_agent_list:
            begin_time[agent] = 10000
        # 还没有完成的任务重新排序
        task_dic = {}
        round = 0
        id_finished_task = [task[0] for task in finished_task]
        for task in self.task_time_table:
            if task[0] not in id_finished_task:
                task_dic[task[0]] = round
                round = round + 1
        # task_dic = {2: 0, 5: 1, 6: 2, 7: 3, 8: 4, 9: 5, 3: 6}

        # 已经完成的任务的时间
        finished_time_list = {}
        for task in finished_task:
            finished_time_list[task[0]] = self.task_time_table[task[0]][1]

        extro_condition = The_extro_condition(finished_time_list,
                                              unfinished_task,
                                              begin_time,
                                              break_time,
                                              task_dic,
                                              broken_agent_list)
        return extro_condition, id_finished_task

    def get_agent_pose(self, break_time):
        agent_pos = {}
        agent_flag = {}
        for agent_id in range(len(self.best_solution)):
            agent_solution = self.best_solution[agent_id]
            executing_flag, executing_task = self.check_if_executing(break_time, agent_solution)
            moving_flag, next_task, moving_current_pos = self.check_if_moving(break_time, agent_solution, agent_id)
            waiting_flag, next_task, waiting_current_pos = self.check_if_waiting(break_time, agent_solution, agent_id)
            if executing_flag == 1:
                agent_pos[agent_id] = self.position[executing_task[0][2]]
                agent_flag[agent_id] = 'executing'
            elif moving_flag == 1:
                agent_pos[agent_id] = moving_current_pos
                agent_flag[agent_id] = 'moving'
            elif waiting_flag == 1:
                agent_pos[agent_id] = waiting_current_pos
                agent_flag[agent_id] = 'waiting'
            else:
                agent_pos[agent_id] = 'error'

        return agent_pos, agent_flag

    # 检查某个智能体是否正在执行任务
    def check_if_executing(self, break_time, agent_solution):
        executing_flag = 0
        task = None
        for task in agent_solution:
            if self.task_time_table[task[0][0]][1] < break_time < self.task_time_table[task[0][0]][2]:
                executing_flag = 1
                return executing_flag, task
        return executing_flag, None

    # 检查该智能体是否在移动中
    def check_if_moving(self, break_time, agent_solution, agent_id):
        moving_flag = 0
        solu_task_id = 0
        if len(agent_solution) == 0:
            moving_flag = 0
            next_task = None
            x_current = None
            return moving_flag, next_task, x_current

        for solu_task_id in range(len(agent_solution)-1):
            # 这个任务结束后，下一个任务开始前
            if self.task_time_table[agent_solution[solu_task_id][0][0]][2] \
                < break_time < self.task_time_table[agent_solution[solu_task_id + 1][0][0]][1]:
                task_1 = agent_solution[solu_task_id]
                task_2 = agent_solution[solu_task_id+1]
                x1 = tuple(self.position[task_1[0][2]])
                x2 = tuple(self.position[task_2[0][2]])
                dis = ((x1[0] - x2[0]) ** 2 + (x1[1] - x2[1]) ** 2) ** 0.5
                move_time = dis / self.agent_type[self.agent_data[agent_id][2]]['velocity']
                if self.task_time_table[task_1[0][0]][2] + move_time > break_time:
                    moving_flag = 1
                    next_task = task_2
                    # 先写一个走直线的版本
                    x_current = [0,0]
                    x_current[0] = x1[0] + self.agent_type[self.agent_data[agent_id][2]]['velocity'] \
                                * (break_time - self.task_time_table[task_1[0][0]][2]) * (x2[0] - x1[0])/dis
                    x_current[1] = x1[1] + self.agent_type[self.agent_data[agent_id][2]]['velocity'] \
                                * (break_time - self.task_time_table[task_1[0][0]][2]) * (x2[1] - x1[1])/dis
                    return moving_flag, next_task, x_current
        # 如果breaktime小于第一个任务的开始时间
        if break_time < self.task_time_table[agent_solution[0][0][0]][1]:
            x0 = self.position[self.agent_data[agent_id][1]]
            task_1 = agent_solution[0]
            x1 = self.position[task_1[0][2]]
            dis = ((x0[0] - x1[0]) ** 2 + (x0[1] - x1[1]) ** 2) ** 0.5
            move_time = dis / self.agent_type[self.agent_data[agent_id][2]]['velocity']
            # 认为从t=0开始运动move_time时间后可到达第一个任务的执行地点，若breaktime小于move_time则在运动中
            if break_time < move_time:
                moving_flag = 1
                next_task = agent_solution[0]
                x_current = [0, 0]
                x_current[0] = x0[0] + self.agent_type[self.agent_data[agent_id][2]]['velocity'] \
                               * (break_time - 0) * (x1[0] - x0[0]) / dis
                x_current[1] = x0[1] + self.agent_type[self.agent_data[agent_id][2]]['velocity'] \
                               * (break_time - 0) * (x1[1] - x0[1]) / dis
                return moving_flag, next_task, x_current

        return 0, None, None

    def check_if_waiting(self, break_time, agent_solution, agent_id):
        # 首先检查是否任务为空
        if len(agent_solution) == 0:
            waiting_flag = 1
            next_task = None
            x_current_name = self.agent_data[agent_id][1]
            x_current = self.position[x_current_name]
            return waiting_flag, next_task, x_current

        for solu_task_id in range(len(agent_solution)-1):
            # 这个任务结束后，下一个任务开始前
            if self.task_time_table[agent_solution[solu_task_id][0][0]][2] \
                    < break_time < self.task_time_table[agent_solution[solu_task_id + 1][0][0]][1]:
                task_1 = agent_solution[solu_task_id]
                task_2 = agent_solution[solu_task_id + 1]
                x1 = self.position[task_1[0][2]]
                x2 = self.position[task_2[0][2]]
                dis = ((x1[0] - x2[0]) ** 2 + (x1[1] - x2[1]) ** 2) ** 0.5
                move_time = dis / self.agent_type[self.agent_data[agent_id][2]]['velocity']
                # 已经移动到了下一个任务的地点
                if self.task_time_table[task_1[0][0]][2] + move_time < break_time:
                    waiting_flag = 1
                    next_task = task_2
                    x_current = self.position[next_task[0][2]]
                    return waiting_flag, next_task, x_current
        # 如果break_time比最后一个任务的完成时间还要大，那么就等在原地
        if break_time > self.task_time_table[agent_solution[-1][0][0]][2]:
            waiting_flag = 1
            next_task = None
            x_current = self.position[agent_solution[-1][0][2]]
            return waiting_flag, next_task, x_current

        # 如果break_time比第一个任务的开始时间小，且已经移动到了第一个任务的执行地点
        if break_time < self.task_time_table[agent_solution[0][0][0]][1]:
            x0 = self.position[self.agent_data[agent_id][1]]
            task_1 = agent_solution[0]
            x1 = self.position[task_1[0][2]]
            dis = ((x0[0] - x1[0]) ** 2 + (x0[1] - x1[1]) ** 2) ** 0.5
            move_time = dis / self.agent_type[self.agent_data[agent_id][2]]['velocity']
            if break_time > move_time:
                waiting_flag = 1
                next_task = agent_solution[0]
                x_current = x1
                return waiting_flag, next_task, x_current
        return 0, None, None

    def judge_and_calculate_overlap(self, time_windows):   # 用于判断多个时间窗是否有重叠部分,有的话返回重叠部分
        if not time_windows:
            return False  # No windows to compare
        # Sort the time windows based on the start time
        time_windows.sort()

        # Initialize the overlap range using the first window
        latest_start = time_windows[0][0]
        earliest_end = time_windows[0][1]

        # Iterate through the windows to find the common overlap
        for tw in time_windows:
            # Update the latest start time to the maximum of current values
            latest_start = max(latest_start, tw[0])
            # Update the earliest end time to the minimum of current values
            earliest_end = min(earliest_end, tw[1])

            # If the latest start time is greater than the earliest end time, no common overlap exists
            if latest_start > earliest_end:
                return False

        return (latest_start, earliest_end)
    

    def find_three_exact_overlapping_windows(self, time_windows, exact_overlap_count):
        # Sort the time windows based on the start time
        time_windows.sort()
        
        # List to hold up to three combinations of overlapping windows with exact overlap intervals
        three_overlapping_details = []
        
        # Iterate through each time window and check for overlaps
        for i in range(len(time_windows)):
            # Check every possible combination starting from each window
            for j in range(i, len(time_windows)):
                # Initialize with the current window
                current_overlap = [time_windows[j][2]]     # 存储时间窗有重叠的智能体id
                # Define the current overlap interval as the first window's range
                current_start = time_windows[j][0]
                current_end = time_windows[j][1]
                # Check following windows to find all overlaps
                for k in range(j + 1, len(time_windows)):
                    next_start, next_end = time_windows[k][0], time_windows[k][1]
                    
                    # Update the overlap interval to the maximum start time and minimum end time
                    if next_start <= current_end:
                        new_start = max(current_start, next_start)
                        new_end = min(current_end, next_end)
                        
                        # Only continue if there is still an overlap
                        if new_start <= new_end:
                            current_overlap.append(time_windows[k][2])
                            current_start, current_end = new_start, new_end
                            # If we reached the exact number of overlaps required
                            if len(current_overlap) == exact_overlap_count:
                                three_overlapping_details.append((current_overlap, (current_start, current_end)))
                                # Break if we already have three combinations
                                if len(three_overlapping_details) == 3:     # 返回3个智能体组合
                                    return three_overlapping_details    # [([1,2,3],(t1,t2)),([],()),...]
                                break
                        else:
                            break
                    else:
                        break
                
                # Continue to next starting point if current set does not meet the required count
                if len(current_overlap) < exact_overlap_count:
                    continue
        
        return three_overlapping_details

class The_extro_condition:
    def __init__(self, finished_time_list, unfinished_task, begin_time, break_time, task_dic,
                 broken_agent_list):
        self.finished_time_list = finished_time_list
        self.unfinished_task_list = unfinished_task
        self.begin_time = begin_time
        self.task_dic = task_dic
        self.broken_agent_list = broken_agent_list
        self.break_time = break_time
