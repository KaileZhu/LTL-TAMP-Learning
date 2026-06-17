# ！/usr/bin/env python3
'''
@Date   : 2023/11 -->  
@Authors: Junjie Wang, Yunyi Zhang
@Contact: pkuwjj1998@163.com
@Version: 1.0
@Descrip: the module contains the class for planner, which is used to solve
        the simultaneous task allocation and planning for multi-agent system.
@Log:
        - 2023/11/20: the first version that contains the class for BnB Search
'''

import time
import copy
import random
import numpy as np
from itertools import product as iter_product
from itertools import combinations as iter_com
import random
import cvxpy as cp
import networkx as nx
from collections import Counter


# from B_A_B2 import Branch_And_Bound

class BnBSearch:
    """
    Class for the branch and bound algorithm.
    """

    def __init__(self, poset, task_data, input_data, costmap):
        """
        ----------
        Args:
            poset: the poset list
            task: 
            input: 
        """
        self.poset = poset
        self.position = input_data.position
        self.agent_data = input_data.agent_data
        self.task_data = task_data
        self.task_type = input_data.task_type
        self.sub_task_type = input_data.sub_task_type
        self.agent_type = input_data.agent_type
        self.costmap = costmap
        self.Astar_table = []
        self.get_horizon()
        self.explored_node_dic = {}
        self.generate_poset_graph()

    def begin_bnb_search(self, time_budget, upper_bound_method, lower_bound_method, search_method):
        time_start = time.time()
        self.generate_time_budget()
        node_root_plan = list([] for _ in self.agent_data)
        assigned_tasks = list()
        node_root = {
            'plan': node_root_plan,
            'tasks': assigned_tasks,
            'time': 0,
            'end_time': 0,
            'solution': None
        }
        self.count_round = 1
        up_bound, solution = self.get_upper_bound(node_root, 'slowly')
        node_root['solution'] = solution
        self.get_lower_bound(lower_bound_method)
        self.upper_bound_list = {}
        self.upper_bound_list[self.count_round] = (up_bound, time.time() - time_start)
        # low_bound=self.get_lower_bound_method(root_node,assigned_tasks)
        self.branch_tree = [node_root]
        self.search_node_list = {}
        self.search_node_list[tuple(assigned_tasks)] = [node_root]
        self.best_solution = solution
        self.best_up_bound = up_bound
        self.max_low_bound = 0
        self.low_bound_list = {}
        # each time explore a node, we say count_round+1
        self.best_up_bound_list = {}
        self.best_up_bound_list[self.count_round] = (up_bound, time.time() - time_start)
        self.astar_list_in_tree = [up_bound]
        addition_time_cost = 0
        while (not self.branch_tree == []) and time.time() - time_start < time_budget:
            iter_start_time = time.time()
            # print('check a branch')
            # node fetch step
            # ===============
            # node fetching is good enough i think
            popi = self.astar_list_in_tree.index(max(self.astar_list_in_tree))
            node = self.branch_tree.pop(popi)
            node_up_bound = self.astar_list_in_tree.pop(popi)
            # =========================
            # this method is bad
            # node_up_bound=self.astar_list_in_tree.pop()
            # node,task=self.branch_tree.pop()
            self.count_round = self.count_round + 1
            # -------------------
            # child_nodes=self.branching_routine(search_method)
            if tuple(node['tasks']) in self.search_node_list.keys():
                if node not in self.search_node_list[tuple(node['tasks'])]:
                    self.search_node_list[tuple(node['tasks'])].append(node['plan'])
                    low_bound = self.get_lower_bound_method(node['plan'], node['tasks'])
                    if low_bound < self.best_up_bound:
                        self.low_bound_list[self.count_round] = (low_bound, time.time() - time_start, 'explore')
                        child_nodes = self.exten_child_nodes(node)
                        self.branch_tree.extend(child_nodes)
                        self.astar_list_in_tree.extend(self.estimate_Astar_value(child_nodes, node_up_bound))
                        up_bound, solution = self.get_upper_bound(node, upper_bound_method)
                        node['solution'] = solution
                        self.upper_bound_list[self.count_round] = (up_bound, time.time() - time_start)
                        if up_bound + 1 < low_bound:
                            s = 1
                        if up_bound < self.best_up_bound:
                            self.best_solution = solution
                            self.best_up_bound = up_bound
                            self.best_up_bound_list[self.count_round] = (self.best_up_bound, time.time() - time_start)
                    else:
                        self.low_bound_list[self.count_round] = (low_bound, time.time() - time_start, 'cut')
                        self.upper_bound_list[self.count_round] = (self.best_up_bound, time.time() - time_start)
                else:
                    child_nodes = self.exten_child_nodes(node)
                    self.branch_tree.extend(child_nodes)
                    self.astar_list_in_tree.extend(self.estimate_Astar_value(child_nodes, node_up_bound))
                    # self.astar_list_in_tree.extend([node_up_bound for node in child_nodes])
            else:
                self.search_node_list[tuple(node['tasks'])] = [node]
                low_bound = self.get_lower_bound_method(node['plan'], node['tasks'])  # xiajie is error ?
                if low_bound < self.best_up_bound:
                    self.low_bound_list[self.count_round] = (low_bound, time.time() - time_start, 'explore')
                    child_nodes = self.exten_child_nodes(node)
                    # self.astar_list_in_tree.extend([node_up_bound for node in child_nodes])
                    self.astar_list_in_tree.extend(self.estimate_Astar_value(child_nodes, node_up_bound))
                    self.branch_tree.extend(child_nodes)
                    up_bound, solution = self.get_upper_bound(node, upper_bound_method)
                    node['solution'] = solution
                    self.upper_bound_list[self.count_round] = (up_bound, time.time() - time_start)
                    # self.branch_tree.append((node,task,up_bound,low_bound))
                    if up_bound < self.best_up_bound:
                        self.best_solution = solution
                        self.best_up_bound = up_bound
                        self.best_up_bound_list[self.count_round] = (self.best_up_bound, time.time() - time_start)
                else:
                    self.low_bound_list[self.count_round] = (low_bound, time.time() - time_start, 'cut')
                    self.upper_bound_list[self.count_round] = (self.best_up_bound, time.time() - time_start)
            # 每一次迭代后都算一下当前最优解
            addition_begin = time.time()
            self.get_time_table_of_best_solution(self.best_solution)
            end_time_list = []
            for i, duration, end in self.task_time_table:
                end_time_list.append(end)
            task_finish_time = max(end_time_list)
            addition_end = time.time()
            addition_time_cost += addition_end - addition_begin
            print('------------------------------------')
            # print('new branch up bound is',self.best_up_bound)
            print('best end time is ', task_finish_time)
            # 减去无关的时间addition_time_cost
            print('total timecost till this iter is', time.time() - time_start - addition_time_cost)

        self.print_answer()
    def print_answer(self):
        print('best value is:', self.best_up_bound)
        for i in range(len(self.agent_data)):
            print('agent', i + 1, 'task list is:', self.best_solution[i])
    def get_time_table_of_best_solution(self, solution):
        task_time_cost_list = [self.task_type[task[1]][0] for task in self.task_data]
        t, end_time = self.opt_for_partial_assigment(solution, range(len(self.task_data)))
        self.task_time_table = [[i, end_time[i][0] - task_time_cost_list[i], end_time[i][0]] for i in
                                range(len(self.task_data))]

    def estimate_Astar_value(self, node_list, upper_bound):
        Astar_list = []
        for node in node_list:
            t2 = 0
            execute_time = 0
            for i in node['tasks']:
                execute_num = 0
                for n in self.task_type[self.task_data[i][1]][1].values():
                    execute_num = execute_num + n
                t2 = t2 + self.task_type[self.task_data[i][1]][0] * execute_num
            Astar_list.append(t2 / upper_bound / len(self.agent_data))
        return Astar_list
    def exten_child_nodes(self, node):
        plan = node['plan']
        assign_task = node['tasks']
        child_node_list = []
        assiged_task_set = set()
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
            to_assig_set.append(self.task_data[task])
        for task in to_assig_set:
            assign_task_set = copy.deepcopy(assign_task)
            assign_task_set.append(task[0])
            sub_task_list = []
            pot_agent_list = []
            agent_num = 0
            for sub_task, num in self.task_type[task[1]][1].items():
                list1 = []
                agent_num = agent_num + num
                for agent_i in self.agent_data:
                    if sub_task in self.agent_type[agent_i[2]]['serve']:
                        list1.append(agent_i[0])
                combina = iter_com(list1, num)
                pot_agent_list.append(list(combina))
                sub_task_list.append(sub_task)
            # print('sub_task_list',sub_task_list)
            agent_list = iter_product(*pot_agent_list)
            for assig_list in agent_list:
                t = []
                for i in assig_list:
                    t.extend(list(i))
                if len(Counter(t)) < agent_num:
                    continue
                child_node = {}
                child_node['plan'] = copy.deepcopy(plan)
                label = 0
                for agent_i in range(len(assig_list)):
                    if label == 1:
                        break
                    for i in assig_list[agent_i]:
                        if self.check_poset_in_agent(child_node['plan'][i], task):
                            # print('sub_task_agent task',task)
                            child_node['plan'][i].append((task, sub_task_list[agent_i]))
                        else:
                            label = 1
                            break
                if label == 0:
                    assign_task_set_num = []
                    for task_3 in assign_task_set:
                        assign_task_set_num.append(self.task_data[task_3][0])
                    assign_task_set_num.sort()
                    # print('child_node',child_node)
                    # print('assign_task_set',assign_task_set_num)
                    child_node['tasks'] = assign_task_set_num
                    child_node_list.append(child_node)
        print('extend child nodes', len(child_node_list))
        return child_node_list
    def generate_time_budget(self):
        self.time_budget = 0
        for i in self.task_data:
            self.time_budget = self.time_budget + self.task_type[self.task_data[i[0]][1]][0]

    def get_upper_bound(self, node, tasks_assigned, upper_bound):
        if upper_bound == 'greedy':#should be finished
            up_bound,solution=self.found_solution_greedy(node,tasks_assigned)
            return up_bound,solution
        elif upper_bound == 'slowly':
            up_bound, solution = self.found_solution_greedy2(node, tasks_assigned)
            return up_bound, solution
        else:
            raise Exception('Undefined upper_bound method!')
            
    def found_solution_greedy2(self, node):
        if not len(node['tasks']) == 0:
            t, _ = self.optimal_partial_assign(node['plan'], node['tasks'])
        else:
            t = 0
        t2 = 0
        for i in node['tasks']:
            t2 = t2 + self.task_type[self.task_data[i][1]][0]

        tstar = t2 / t / len(self.agent_data) if t > 0.1 else 1
        node['time'] = tstar
        nodes_seq = [node, ]  # a sequence of nodes that contains the tasks assignment
        time_seq = [node['time'], ]  # a time sequence of
        un_found = 1
        sample_list = []
        while nodes_seq != None and un_found > 0:
            popi = time_seq.index(max(time_seq))
            root_node = nodes_seq.pop(popi)
            t_label = time_seq.pop(popi)
            tasks_assigned = set(root_node['tasks'])
            init_node_par = root_node['plan']

            assiged_task_set = set()
            to_assig_task = set(self.poset_graph.succ['root'])
            # 
            for task in tasks_assigned:
                assiged_task_set.add(task)
                to_assig_task = to_assig_task | set(self.poset_graph.succ[task])
            un_assig_task1 = to_assig_task - assiged_task_set
            un_assig_task = copy.deepcopy(un_assig_task1)
            # 
            for i in un_assig_task1:
                if len(set(self.poset_graph.pred[i]) - assiged_task_set - {'root'}) != 0:
                    un_assig_task.remove(i)
            nodes_seq = []
            time_seq = []
            for to_assig_task in un_assig_task:
                new_assiged_task = copy.deepcopy(tasks_assigned)
                new_assiged_task.add(to_assig_task)
                subtasks = self.task_type[self.task_data[to_assig_task][1]][1]
                feasible = {}
                for subtask, num in subtasks.items():
                    agents = []
                    for agent_i in self.agent_data:
                        if subtask in self.agent_type[agent_i[2]]['actions']:
                            agents.append(agent_i[0])
                    feasible[subtask] = (agents, num)
                # == get task distribution
                new_node_par = copy.deepcopy(init_node_par)
                while 1:
                    assign_list = {}
                    check_list = []
                    for sub_task, (list, num) in feasible.items():
                        assign_list[sub_task] = random.sample(list, num)
                        check_list.extend(assign_list[sub_task])
                        repet_Num = Counter(check_list)
                    if len(repet_Num) == len(check_list):
                        break
                # print('assign_list',assign_list)
                for sub_task, samb in assign_list.items():
                    for agent_i in samb:
                        new_node_par[agent_i].append((self.task_data[to_assig_task], sub_task))
                if len(new_assiged_task) == len(self.task_data):
                    sample_list.append(new_node_par)
                    un_found = un_found - 1
                else:
                    t, _ = self.opt_for_partial_assigment(new_node_par, new_assiged_task)
                    new_node = {
                                'plan': new_node_par,
                                'tasks': set(new_assiged_task),
                                'time': 0,
                                'end_time': t
                                }
                    # nodes_seq.append((new_assiged_task, new_node_par))
                    # print('time',t)
                    t2 = 0
                    for i in new_assiged_task:
                        t2 = t2 + self.task_type[self.task_data[i][1]][0]
                    if t <= 0.1:
                        tstar = 1
                    else:
                        tstar = t2 / t / len(self.agent_data)
                    new_node['time'] = tstar
                    nodes_seq.append(new_node)
                    time_seq.append(new_node['time'])
        time_list = []
        if sample_list == []:
            return self.horizon, []
        else:
            for node_par in sample_list:
                a, b = self.opt_for_partial_assigment(node_par, range(len(self.task_data)))
                time_list.append(a)
            solution = sample_list[time_list.index(min(time_list))]
            return min(time_list), solution

    def get_lower_bound(self, lower_bound):
        if lower_bound == 'i_j':
            self.get_lower_bound_method = self.get_lower_bound_with_i_j
        if lower_bound == 'i+j':
            self.get_lower_bound_method = self.get_lower_bound_with_i_add_j
        # low_bound1=self.get_lower_bound_with_i_j_k_faster(node,tasks_assigned)
        # return  low_bound1
    def get_lower_bound_with_i_add_j(self, node, assigned_tasks):
        t, time_list = self.opt_for_partial_assigment(node, assigned_tasks)
        unassigned_tasks = list(range(len(self.task_data)))
        assigned_task_dic = {}
        z = 0
        for i in assigned_tasks:
            unassigned_tasks.remove(i)
            assigned_task_dic[i] = z
            z = z + 1
        task_number = len(unassigned_tasks)
        if task_number == 0:
            print('return max time list')
            return max(time_list)
        begin_time_list = []
        for agent in node:
            if len(agent) == 0:
                begin_time_list.append(0)
            else:
                if np.shape(time_list[assigned_task_dic[agent[-1][0][0]]]) == (1,):
                    begin_time_list.append(time_list[assigned_task_dic[agent[-1][0][0]]][0])
                else:
                    begin_time_list.append(time_list[assigned_task_dic[agent[-1][0][0]]])
        # print('begin time list',begin_time_list)
        z = 0
        task_dic = {}
        for i in unassigned_tasks:
            task_dic[i] = z
            z = z + 1
        agent_pose = []
        for agent in self.agent_data:
            if len(node[agent[0]]) == 0:
                agent_pose.append(self.position[agent[1]])
            else:
                pos = self.position[node[agent[0]][-1][0][2]]
                agent_pose.append(pos)
        agent_number = len(self.agent_data)
        t_i = cp.Variable(shape=1, nonneg=True)
        t_j = cp.Variable(shape=(task_number, 1), nonneg=True)
        total_constrain = []
        new_task_time_set = {}
        # begin time constrain
        for task_j in unassigned_tasks:
            time_table = []
            for agent in self.agent_data:
                x1 = self.position[self.task_data[task_j][2]]
                x2 = agent_pose[agent[0]]
                time = ((x1[0] - x2[0]) ** 2 + (x1[1] - x2[1]) ** 2) ** 0.5 / self.agent_type[agent[2]]['velocity']
                time_table.append(time)
            for task in unassigned_tasks:
                if not task == task_j:
                    time = self.get_distance(self.task_data[task_j][2], self.task_data[task][2]) / 10
                    time_table.append(time)
            new_task_time = self.task_type[self.task_data[task_j][1]][0] + min(time_table)
            new_task_time_set[task_j] = new_task_time
        self.new_task_time_set = new_task_time_set
        # poset constrain
        for i, j in self.poset['<=']:
            if (i, j) in self.poset['!='] or (j, i) in self.poset['!=']:
                if not i in task_dic.keys():
                    if j in task_dic.keys():
                        m = [0 for i in range(task_number)]
                        m[task_dic[j]] = 1
                        total_constrain.append(m @ t_j >= time_list[assigned_task_dic[i]])
                else:
                    m = [0 for i in range(task_number)]
                    m[task_dic[i]] = -1
                    m[task_dic[j]] = 1
                    total_constrain.append(m @ t_j >= new_task_time_set[j])
        # t_j constrain
        # total_constrain.append(*constrain_begin_time)
        unassigned_task_time = 0
        # ================provide enough serves for the task j (2)
        for task_j in task_dic.keys():
            task_subs = self.task_type[self.task_data[task_j][1]][1]
            b = 0
            for sub, num in task_subs.items():
                b = b + num
            unassigned_task_time = unassigned_task_time + b * self.task_type[self.task_data[task_j][1]][0]
        constrain_t_i = [agent_number * t_i - sum(begin_time_list) - unassigned_task_time >= 0]

        obj_1 = cp.Minimize(cp.max(t_j))
        obj_2 = cp.Minimize(t_i)
        if not total_constrain == []:
            prob_1 = cp.Problem(obj_1, total_constrain)
        else:
            prob_1 = cp.Problem(obj_1)
        prob_1.solve('GLPK_MI')
        prob_2 = cp.Problem(obj_2, constrain_t_i)
        # solver: GLPK_MI CBC SCIP
        prob_2.solve('GLPK_MI')
        value = max(prob_1.value, prob_2.value, max(begin_time_list))
        print('low bound:', value)
        return value
        if prob_1.status == 'optimal':
            return value
        else:
            return 0
    def get_lower_bound_with_i_j(self, node, tasks_assigned):
        """
        
        ----------
        Parameters:

        ----------
        Returns:

        """
        t, time_list = self.opt_for_partial_assigment(node, tasks_assigned)
        tasks_unassigned = list(range(len(self.task_data)))
        assigned_task_dic = {}
        z = 0
        for i in tasks_assigned:
            tasks_unassigned.remove(i)
            assigned_task_dic[i] = z
            z = z + 1
        task_number = len(tasks_unassigned)
        if task_number == 0:
            print('return max time list')
            return max(time_list)
        begin_time_list = []
        for agent in node:
            if len(agent) == 0:
                begin_time_list.append(0)
            else:
                assigned_task_dic[agent[-1][0][0]]
                if np.shape(time_list[assigned_task_dic[agent[-1][0][0]]]) == (1,):
                    begin_time_list.append(time_list[assigned_task_dic[agent[-1][0][0]]][0])
                else:
                    begin_time_list.append(time_list[assigned_task_dic[agent[-1][0][0]]])
        # print('begin time list',begin_time_list)
        z = 0
        task_dic = {}
        for i in tasks_unassigned:
            task_dic[i] = z
            z = z + 1
        agent_pose = []
        for agent in self.agent_data:
            if len(node[agent[0]]) == 0:
                agent_pose.append(self.position[agent[1]])
            else:
                pos = self.position[node[agent[0]][-1][0][2]]
                agent_pose.append(pos)
        agent_number = len(self.agent_data)
        x_i_j = cp.Variable(shape=(agent_number * task_number, 1), boolean=True)
        t_i = cp.Variable(shape=(agent_number, 1), nonneg=True)
        total_constrain = []
        new_task_time_set = {}
        # begin time constrain
        for task_j in tasks_unassigned:
            time_table = []
            for agent in self.agent_data:
                x1 = self.position[self.task_data[task_j][2]]
                x2 = agent_pose[agent[0]]
                time = ((x1[0] - x2[0]) ** 2 + (x1[1] - x2[1]) ** 2) ** 0.5 / self.agent_type[agent[2]]['velocity']
                time_table.append(time)
            for task in tasks_unassigned:
                if not task == task_j:
                    time = self.get_distance(self.task_data[task_j][2], self.task_data[task][2]) / 10
                    time_table.append(time)
            new_task_time = self.task_type[self.task_data[task_j][1]][0] + min(time_table)
            new_task_time_set[task_j] = new_task_time
        self.new_task_time_set = new_task_time_set
        M_time = [[0 for i in range(agent_number)] for j in range(agent_number * task_number)]
        b_time = [[begin_time_list[j] for j in range(agent_number)]]
        T_time = []
        for agent_i in range(agent_number):
            t = [0 for o in range(agent_number)]
            t[agent_i] = 1
            for task_j in task_dic.keys():
                num = agent_i * task_number + task_dic[task_j]
                M_time[num][agent_i] = -new_task_time_set[task_j]
            T_time.append(t)
        if len(np.shape(b_time)) > 2:
            s = 1
        constrain_begin_time = [M_time @ x_i_j + T_time @ t_i >= b_time]
        total_constrain.append(*constrain_begin_time)

        # ================provide enough serves for the task j (2)
        M1 = [[0 for i in range(task_number)] for j in range(agent_number * task_number)]
        b1 = [[0 for i in range(task_number)]]
        # z=0
        for task_j in task_dic.keys():
            task_subs = self.task_type[self.task_data[task_j][1]][1]
            b = 0
            for sub, num in task_subs.items():
                b = b + num
            b1[0][task_dic[task_j]] = b
            for agent_i in range(agent_number):
                num = agent_i * task_number + task_dic[task_j]
                M1[num][task_dic[task_j]] = 1
        enough_constrain = [M1 @ x_i_j == b1]
        total_constrain.append(*enough_constrain)

        obj_1 = cp.Minimize(cp.max(t_i))

        prob_1 = cp.Problem(obj_1, total_constrain)
        # solver: GLPK_MI CBC SCIP
        prob_1.solve(solver='GLPK_MI')
        self.x_i_j = x_i_j.value
        self.t_i = t_i.value
        self.constrain = total_constrain
        print('low bound:', prob_1.value)
        if prob_1.status == 'optimal':
            return prob_1.value
        else:
            return 0

    def check_poset_in_agent(self, agent, task):
        label = 1
        for i in agent:
            if (task, i) in self.poset:
                label = 0
        return label
    def optimal_partial_assign(self, node_par, tasks_assigned, i=None):
        """
        The optimal assignment according to the partial relation
        ----------
        Parameters:
            node:
            tasks_assigned: 
        ----------
        Returns:
        """
        node_plan = [tuple(plan) for plan in node_par]
        tuple_node = tuple(node_plan)
        tasks_assigned_tuple = tuple(tasks_assigned)
        if tasks_assigned_tuple in self.explored_node_dic.keys():
            # 报错原因：tuple_node是元组，但是元组的元素是列表
            # self.explored_node_dic[tasks_assigned_tuple]的键也是元组，但是元组的元素还是元组
            if tuple_node in self.explored_node_dic[tasks_assigned_tuple].keys():
                max_end_time_value, end_time_value = self.explored_node_dic[tasks_assigned_tuple][tuple_node]
                return max_end_time_value, end_time_value
        tasks_assigned_dic = {}
        t = 0
        # print('tasks_assigned:',tasks_assigned)
        # print(node)
        for i in tasks_assigned:
            tasks_assigned_dic[i] = t
            t = t + 1
        end_time = cp.Variable(shape=(len(tasks_assigned), 1), name='endtime', nonneg=True)
        total_constrain = []
        M1 = []
        B1 = [[]]
        # for i,j in self.poset['<']:
        for i, j in self.poset['<=']:
            if self.task_data[i][0] in tasks_assigned and self.task_data[j][0] in tasks_assigned:
                if not ((i, j) in self.poset['!='] or (j, i) in self.poset['!=']):
                    # <=
                    m = [0 for l in range(len(tasks_assigned))]
                    m[tasks_assigned_dic[self.task_data[i][0]]] = 1
                    m[tasks_assigned_dic[self.task_data[j][0]]] = -1
                    M1.append(m)
                    B1[0].append(-self.task_type[self.task_data[j][1]][0] + self.task_type[self.task_data[i][1]][0])
                else:
                    # <
                    m = [0 for l in range(len(tasks_assigned))]
                    m[tasks_assigned_dic[self.task_data[i][0]]] = 1
                    m[tasks_assigned_dic[self.task_data[j][0]]] = -1
                    M1.append(m)
                    B1[0].append(-self.task_type[self.task_data[j][1]][0])
        for i, j in self.poset['=']:
            if self.task_data[i][0] in tasks_assigned and self.task_data[j][0] in tasks_assigned:
                if self.task_type[self.task_data[i][1]][0] >= self.task_type[self.task_data[j][1]][0]:
                    changelabel = -1
                else:
                    changelabel = 1
                m = [0 for l in range(len(tasks_assigned))]
                m[tasks_assigned_dic[self.task_data[i][0]]] = changelabel
                m[tasks_assigned_dic[self.task_data[j][0]]] = -changelabel
                M1.append(m)
                B1[0].append(0)
                # might remaining to do!!!!!!!!!!!!!!!
                m = [0 for l in range(len(tasks_assigned))]
                m[tasks_assigned_dic[self.task_data[i][0]]] = -changelabel
                m[tasks_assigned_dic[self.task_data[j][0]]] = changelabel
                M1.append(m)
                B1[0].append(
                    -self.task_type[self.task_data[i][1]][0] * changelabel + self.task_type[self.task_data[j][1]][
                        0] * changelabel)
        for i, j in self.poset['!=']:
            if i in tasks_assigned and j in tasks_assigned:
                if not (i, j) in self.poset['<='] and not (j, i) in self.poset['<=']:
                    m = [[0] for l in range(len(tasks_assigned))]
                    m[tasks_assigned_dic[self.task_data[i][0]]][0] = 1
                    m[tasks_assigned_dic[self.task_data[j][0]]][0] = -1
                    bool_for_x = cp.Variable(1, boolean=True)
                    # ei-di - ej  >=0   ti >= ej
                    constrain0 = [m @ end_time - self.task_type[self.task_data[i][1]][
                        0] - bool_for_x * self.time_budget + self.time_budget >= 0]
                    # ei - ej+ dj  <=0  ei<= tj
                    constrain1 = [
                        m @ end_time + self.task_type[self.task_data[j][1]][0] - bool_for_x * self.time_budget <= 0]
                    print(1)
                    total_constrain.append(*constrain0)
                    total_constrain.append(*constrain1)
                    # m=[[0] for l in range(len(tasks_assigned))]
                    # m[tasks_assigned_dic[self.task_data[i][0]]][0]=1
                    # m[tasks_assigned_dic[self.task_data[j][0]]][0]=-1
                    # total_constrain.append(cp.abs(
                    #    m @ end_time + (-self.task_type[self.task_data[i][1]][0] + self.task_type[self.task_data[j][1]][0])) \
                    #                       >= (self.task_type[self.task_data[i][1]][0] + self.task_type[self.task_data[j][1]][
                    #    0]) / 2)
            # total_constrain.append(cp.abs(m @ end_time) >=max(self.task_type[self.task_data[i][1]][0],self.task_type[self.task_data[j][1]][0]))
        if not M1 == []:
            M11 = self.Turn_Matrix(M1)
            constraint1 = [M11 @ end_time <= B1]
            total_constrain.append(*constraint1)
            # print(B1)
        M2 = []
        B2 = [[]]
        for agent_i in range(len(self.agent_data)):
            if len(node_par[agent_i]) > 0:
                m = [0 for i in range(len(tasks_assigned))]
                # print(tasks_assigned_dic)
                # print(node[agent_i][0][0])
                # print(tasks_assigned_dic)
                c = tasks_assigned_dic[node_par[agent_i][0][0][0]]
                m[c] = 1
                # b=self.get_distance(self.agent_data[agent_i][1],node[agent_i][0][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                #    self.task_type[node[agent_i][0][0][1]][0]
                M2.append(m)
                B2[0].append(self.get_distance(self.agent_data[agent_i][1], node_par[agent_i][0][0][2]) /
                             self.agent_type[self.agent_data[agent_i][2]]['velocity'] + \
                             self.task_type[node_par[agent_i][0][0][1]][0])
            if len(node_par[agent_i]) > 1:
                for task in range(len(node_par[agent_i]) - 1):
                    m = [0 for i in range(len(tasks_assigned))]
                    c = tasks_assigned_dic[node_par[agent_i][task][0][0]]
                    m[c] = -1
                    c = tasks_assigned_dic[node_par[agent_i][task + 1][0][0]]
                    m[c] = 1
                    b = self.get_distance(node_par[agent_i][task][0][2], node_par[agent_i][task + 1][0][2]) / \
                        self.agent_type[self.agent_data[agent_i][2]]['velocity'] + \
                        self.task_type[node_par[agent_i][task + 1][0][1]][0]
                    M2.append(m)
                    B2[0].append((b))
        M21 = self.Turn_Matrix(M2)
        constraint2 = [M21 @ end_time >= B2]  # constraint of poset
        total_constrain.append(*constraint2)
        list1 = [[1] for task in tasks_assigned]
        obj = cp.Minimize(list1 @ end_time)
        prob = cp.Problem(obj, total_constrain)
        # prob.solve(solver=cp.SCS)
        prob.solve(solver='GLPK_MI')
        if prob.status == 'optimal':
            if tasks_assigned_tuple in self.explored_node_dic.keys():
                if tuple_node in self.explored_node_dic[tasks_assigned_tuple].keys():
                    max_end_time_value, end_time_value = self.explored_node_dic[tasks_assigned_tuple][tuple_node]
            else:
                self.explored_node_dic[tasks_assigned_tuple] = {}
                self.explored_node_dic[tasks_assigned_tuple][tuple_node] = (max(end_time.value), end_time.value)
            return max(end_time.value), end_time.value
        else:
            return self.horizon, []
    def generate_poset_graph(self):
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
            removable_label = self.find_path(i, j)
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

    def find_path(self, start, end):
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
    def get_horizon(self):
        self.horizon = 10000
        # for i in self.task_data:
        #    self.horizon=self.task_type[i[1]][0]*2+self.horizon+100
    def opt_for_partial_assigment(self, node, assign_task, i=None):
        """
        The optimal assignment according to the partial relation
        ----------
        Parameters:
            node:
            assign_task:
        ----------
        Returns:
        """
        list_node = []
        for agent in node:
            list_node.append(tuple(agent))
        tuple_node = tuple(list_node)
        assign_task_tuple = tuple(assign_task)
        if assign_task_tuple in self.explored_node_dic.keys():
            if tuple_node in self.explored_node_dic[assign_task_tuple].keys():
                max_end_time_value, end_time_value = self.explored_node_dic[assign_task_tuple][tuple_node]
                return max_end_time_value, end_time_value
        assign_task_dic = {}
        t = 0
        # print('assign_Task:',assign_task)
        # print(node)
        for i in assign_task:
            assign_task_dic[i] = t
            t = t + 1
        end_time = cp.Variable(shape=(len(assign_task), 1), name='endtime', nonneg=True)
        total_constrain = []
        M1 = []
        B1 = [[]]
        # for i,j in self.poset['<']:
        for i, j in self.poset['<=']:
            if self.task_data[i][0] in assign_task and self.task_data[j][0] in assign_task:
                if not ((i, j) in self.poset['!='] or (j, i) in self.poset['!=']):
                    # <=
                    m = [0 for l in range(len(assign_task))]
                    m[assign_task_dic[self.task_data[i][0]]] = 1
                    m[assign_task_dic[self.task_data[j][0]]] = -1
                    M1.append(m)
                    B1[0].append(-self.task_type[self.task_data[j][1]][0] + self.task_type[self.task_data[i][1]][0])
                else:
                    # <
                    m = [0 for l in range(len(assign_task))]
                    m[assign_task_dic[self.task_data[i][0]]] = 1
                    m[assign_task_dic[self.task_data[j][0]]] = -1
                    M1.append(m)
                    B1[0].append(-self.task_type[self.task_data[j][1]][0])
        for i, j in self.poset['=']:
            if self.task_data[i][0] in assign_task and self.task_data[j][0] in assign_task:
                if self.task_type[self.task_data[i][1]][0] >= self.task_type[self.task_data[j][1]][0]:
                    changelabel = -1
                else:
                    changelabel = 1
                m = [0 for l in range(len(assign_task))]
                m[assign_task_dic[self.task_data[i][0]]] = changelabel
                m[assign_task_dic[self.task_data[j][0]]] = -changelabel
                M1.append(m)
                B1[0].append(0)
                # might remaining to do!!!!!!!!!!!!!!!
                m = [0 for l in range(len(assign_task))]
                m[assign_task_dic[self.task_data[i][0]]] = -changelabel
                m[assign_task_dic[self.task_data[j][0]]] = changelabel
                M1.append(m)
                B1[0].append(
                    -self.task_type[self.task_data[i][1]][0] * changelabel + self.task_type[self.task_data[j][1]][
                        0] * changelabel)
        for i, j in self.poset['!=']:
            if i in assign_task and j in assign_task:
                if not (i, j) in self.poset['<='] and not (j, i) in self.poset['<=']:
                    m = [[0] for l in range(len(assign_task))]
                    m[assign_task_dic[self.task_data[i][0]]][0] = 1
                    m[assign_task_dic[self.task_data[j][0]]][0] = -1
                    bool_for_x = cp.Variable(1, boolean=True)
                    # ei-di - ej  >=0   ti >= ej
                    constrain0 = [m @ end_time - self.task_type[self.task_data[i][1]][
                        0] - bool_for_x * self.time_budget + self.time_budget >= 0]
                    # ei - ej+ dj  <=0  ei<= tj
                    constrain1 = [
                        m @ end_time + self.task_type[self.task_data[j][1]][0] - bool_for_x * self.time_budget <= 0]
                    print(1)
                    total_constrain.append(*constrain0)
                    total_constrain.append(*constrain1)
                    # m=[[0] for l in range(len(assign_task))]
                    # m[assign_task_dic[self.task_data[i][0]]][0]=1
                    # m[assign_task_dic[self.task_data[j][0]]][0]=-1
                    # total_constrain.append(cp.abs(
                    #    m @ end_time + (-self.task_type[self.task_data[i][1]][0] + self.task_type[self.task_data[j][1]][0])) \
                    #                       >= (self.task_type[self.task_data[i][1]][0] + self.task_type[self.task_data[j][1]][
                    #    0]) / 2)
            # total_constrain.append(cp.abs(m @ end_time) >=max(self.task_type[self.task_data[i][1]][0],self.task_type[self.task_data[j][1]][0]))
        if not M1 == []:
            M11 = self.Turn_Matrix(M1)
            constraint1 = [M11 @ end_time <= B1]
            total_constrain.append(*constraint1)
            # print(B1)
        M2 = []
        B2 = [[]]
        for agent_i in range(len(self.agent_data)):
            if len(node[agent_i]) > 0:
                m = [0 for i in range(len(assign_task))]
                # print(assign_task_dic)
                # print(node[agent_i][0][0])
                # print(assign_task_dic)
                c = assign_task_dic[node[agent_i][0][0][0]]
                m[c] = 1
                # b=self.get_distance(self.agent_data[agent_i][1],node[agent_i][0][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                #    self.task_type[node[agent_i][0][0][1]][0]
                M2.append(m)
                B2[0].append(self.get_distance(self.agent_data[agent_i][1], node[agent_i][0][0][2]) /
                             self.agent_type[self.agent_data[agent_i][2]]['velocity'] + \
                             self.task_type[node[agent_i][0][0][1]][0])
            if len(node[agent_i]) > 1:
                for task in range(len(node[agent_i]) - 1):
                    m = [0 for i in range(len(assign_task))]
                    c = assign_task_dic[node[agent_i][task][0][0]]
                    m[c] = -1
                    c = assign_task_dic[node[agent_i][task + 1][0][0]]
                    m[c] = 1
                    b = self.get_distance(node[agent_i][task][0][2], node[agent_i][task + 1][0][2]) / \
                        self.agent_type[self.agent_data[agent_i][2]]['velocity'] + \
                        self.task_type[node[agent_i][task + 1][0][1]][0]
                    M2.append(m)
                    B2[0].append((b))
        M21 = self.Turn_Matrix(M2)
        constraint2 = [M21 @ end_time >= B2]  # constraint of poset
        total_constrain.append(*constraint2)
        list1 = [[1] for task in assign_task]
        obj = cp.Minimize(list1 @ end_time)
        prob = cp.Problem(obj, total_constrain)
        # prob.solve(solver=cp.SCS)
        prob.solve(solver='GLPK_MI')
        if prob.status == 'optimal':
            if assign_task_tuple in self.explored_node_dic.keys():
                if tuple_node in self.explored_node_dic[assign_task_tuple].keys():
                    max_end_time_value, end_time_value = self.explored_node_dic[assign_task_tuple][tuple_node]
            else:
                self.explored_node_dic[assign_task_tuple] = {}
                self.explored_node_dic[assign_task_tuple][tuple_node] = (max(end_time.value), end_time.value)
            return max(end_time.value), end_time.value
        else:
            return self.horizon, []

    def get_distance(self, i, j):
        # return self.position[(i,j)]
        pos1 = self.position[i][0] - self.position[j][0]
        pos2 = self.position[i][1] - self.position[j][1]
        lenth = (pos1 ** 2 + pos2 ** 2) ** 0.5
        return lenth

    def Turn_Matrix(self, M):
        r = [[] for i in M[0]]
        for i in M:
            for j in range(len(i)):
                r[j].append(i[j])
        return r

class MILP:
    """
    Class for the mixed integer linear programming algorithm.
    """

    def __init__(self, poset, task_data,
                 input_data):  # ,position,agent_data,task_data,task_type,sub_task_type,agent_type):
        self.poset = poset
        self.position = input_data.position  # Regions
        self.agent_data = input_data.agent_data  # Agents
        self.task_data = task_data
        self.task_type = input_data.task_type
        self.sub_task_type = input_data.sub_task_type  #
        self.agent_type = input_data.agent_type  #

    def Base_OPT_MILP_of_cvxpy(self):
        self.get_horizon()
        agent_number = len(self.agent_data)
        task_number = len(self.task_data)
        max_task_list = int(len(self.task_data))
        sub_task_number = len(self.sub_task_type)
        self.x_i_j_k_l = cp.Variable(shape=(agent_number * task_number * max_task_list * sub_task_number, 1),
                                     boolean=True)
        self.t_j = cp.Variable(shape=(task_number, 1), nonneg=True)
        con1 = self.Temporal_con_of_equation_1()  # con1是顺序约束
        con15 = self.Neq_con_of_equation_2()  # con15是不等约束
        con2 = self.enough_con_of_equation_2()
        con3 = self.serve_limit_con_of_equation_3()
        con4 = self.once_task_con_of_equation_4()
        con5 = self.one_task_a_time_con_of_equation_5()
        con6 = self.equation_6()
        con7 = self.equation_7()
        con8 = self.equation_8()
        total_constrain = [*con1, *con2, *con3, *con4, *con5, *con6, *con7, *con8, *con15]
        tim = [[]]
        for i in self.task_data:
            tim[0].append(self.task_type[i[1]][0])
        obj = cp.Minimize(cp.max(self.t_j + tim))  # 目标函数obj
        prob = cp.Problem(obj, total_constrain)  # 将目标函数和约束条件组合起来
        # solver: GLPK_MI CBC SCIP
        prob.solve(solver='GLPK_MI', verbose=True)  # 求解过程，求解器为GLPK_MI，verbose=True表示输出求解过程
        print('最优任务执行时间opt-value:', prob.value)  # 输出最优值
        if prob.status == 'optimal':
            self.valueofx_i_j_k_l = self.x_i_j_k_l.value
            self.valueoft_j = self.t_j.value
            self.print_answer()
            z = 1
            for i in self.assignment:
                print('agent', z, 'task list is:', i)
                z = z + 1
        return prob

    def print_answer(self):
        task_number = len(self.task_data)
        max_task_list = int(len(self.task_data))
        sub_task_number = len(self.sub_task_type)
        self.assignment = [[[] for i in range(len(self.task_data))] for j in range(len(self.agent_data))]
        z = 0
        for i in self.valueofx_i_j_k_l:
            if i[0] == 1:
                agent_i = z // (task_number * max_task_list * sub_task_number)
                left = np.mod(z, task_number * max_task_list * sub_task_number)
                task_j = left // (max_task_list * sub_task_number)
                left = np.mod(left, max_task_list * sub_task_number)
                order_k = left // (sub_task_number)
                sub_l = np.mod(left, sub_task_number)
                sub = (self.task_data[int(task_j)], self.sub_task_type[int(sub_l)])
                self.assignment[agent_i][order_k] = sub
            z = z + 1
        for agent_i in self.assignment:
            remove_list = []
            for i in range(len(agent_i)):
                if agent_i[i] == []:
                    remove_list.append(i)
            for i in reversed(remove_list):
                agent_i.remove([])

    def Temporal_con_of_equation_1(self):  # (1)
        if not self.poset == {}:
            M = [[0 for i in self.poset['<=']] for j in self.task_data]
            b = [[]]
            line = 0
            for j1, j2 in self.poset['<=']:
                M[j1][line] = 1
                M[j2][line] = -1
                # b[0].append(-self.task_type[self.task_data[j1][1]][0])
                b[0].append(0)
                line = line + 1
            return [M @ self.t_j <= b]

    def Neq_con_of_equation_2(self):
        self.time_budget = 10000
        if not self.poset == {}:
            M = []
            count = 0
            for i, j in self.poset['!=']:
                count = count + 1
                # if count>5:
                #    break
                m = [[0] for l in range(len(self.task_data))]
                m[self.task_data[i][0]][0] = 1
                m[self.task_data[j][0]][0] = -1
                bool_for_x = cp.Variable(1, boolean=True)
                constrain0 = [m @ self.t_j - self.task_type[self.task_data[j][1]][
                    0] - bool_for_x * self.time_budget + self.time_budget >= 0]
                constrain1 = [
                    m @ self.t_j + self.task_type[self.task_data[i][1]][0] - bool_for_x * self.time_budget <= 0]
                M.append(*constrain0)
                M.append(*constrain1)
            return M
        if not self.poset == {}:
            M = [[0 for i in self.poset['!=']] for j in self.task_data]
            b = [[]]
            line = 0
            for j1, j2 in self.poset['!=']:
                M[j1][line] = 1
                M[j2][line] = -1
                b[0].append(-self.task_type[self.task_data[j1][1]][0])
                line = line + 1
            return [M @ self.t_j <= b]

    def enough_con_of_equation_2(self):  # (2)
        agent_number = len(self.agent_data)
        task_number = len(self.task_data)
        max_task_list = int(len(self.task_data))
        sub_task_number = len(self.sub_task_type)
        M2 = [[0 for i in range(task_number * sub_task_number)] for j in
              range(agent_number * task_number * max_task_list * sub_task_number)]
        b2 = [[0 for i in range(task_number * sub_task_number)]]
        z = 0
        for task_j in range(task_number):
            for sub_l in range(sub_task_number):
                for agent_i in range(agent_number):
                    if self.sub_task_type[sub_l] in self.agent_type[self.agent_data[agent_i][2]]['serve']:
                        bil = 1
                    else:
                        bil = 0
                    for order_k in range(max_task_list):
                        num = agent_i * task_number * max_task_list * sub_task_number + \
                              task_j * max_task_list * sub_task_number + \
                              order_k * sub_task_number + sub_l
                        M2[num][z] = bil
                if self.sub_task_type[sub_l] in self.task_type[self.task_data[task_j][1]][1].keys():
                    b2[0][z] = self.task_type[self.task_data[task_j][1]][1][self.sub_task_type[sub_l]]
                else:
                    b2[0][z] = 0
                z = z + 1
        enough_constrain = [M2 @ self.x_i_j_k_l == b2]
        return enough_constrain

    def serve_limit_con_of_equation_3(self):
        # ===================one agent con only provide the serve it has:(3)
        agent_number = len(self.agent_data)
        task_number = len(self.task_data)
        max_task_list = int(len(self.task_data))
        sub_task_number = len(self.sub_task_type)
        M3 = [[0 for i in range(agent_number * task_number * max_task_list * sub_task_number)] for j in
              range(agent_number * task_number * max_task_list * sub_task_number)]
        b3 = [[0 for i in range(agent_number * task_number * max_task_list * sub_task_number)]]
        z = 0
        for agent_i in range(agent_number):
            for task_j in range(task_number):
                for order_k in range(max_task_list):
                    for sub_l in range(sub_task_number):
                        num = agent_i * task_number * max_task_list * sub_task_number + \
                              task_j * max_task_list * sub_task_number + \
                              order_k * sub_task_number + sub_l
                        M3[num][z] = 1
                        if self.sub_task_type[sub_l] in self.agent_type[self.agent_data[agent_i][2]]['serve']:
                            b3[0][z] = 1
                        z = z + 1
        once_constrain = [M3 @ self.x_i_j_k_l <= b3]
        return once_constrain

    def once_task_con_of_equation_4(self):
        agent_number = len(self.agent_data)
        task_number = len(self.task_data)
        max_task_list = int(len(self.task_data))
        sub_task_number = len(self.sub_task_type)
        M4 = [[0 for i in range(agent_number * task_number)] for j in
              range(agent_number * task_number * max_task_list * sub_task_number)]
        b4 = [[1 for i in range(agent_number * task_number)]]
        z = 0
        for agent_i in range(agent_number):
            for task_j in range(task_number):
                for order_k in range(max_task_list):
                    for sub_l in range(sub_task_number):
                        num = agent_i * task_number * max_task_list * sub_task_number + \
                              task_j * max_task_list * sub_task_number + \
                              order_k * sub_task_number + sub_l
                        M4[num][z] = 1
                z = z + 1
        constrain4 = [M4 @ self.x_i_j_k_l <= b4]
        return constrain4

    def one_task_a_time_con_of_equation_5(self):
        agent_number = len(self.agent_data)
        task_number = len(self.task_data)
        max_task_list = int(len(self.task_data))
        sub_task_number = len(self.sub_task_type)
        M5 = [[0 for i in range(agent_number * max_task_list)] for j in
              range(agent_number * task_number * max_task_list * sub_task_number)]
        b5 = [[0 for i in range(agent_number * max_task_list)]]
        z = 0
        for agent_i in range(agent_number):
            for order_k in range(max_task_list):
                for task_j in range(task_number):
                    for sub_l in range(sub_task_number):
                        num = agent_i * task_number * max_task_list * sub_task_number + \
                              task_j * max_task_list * sub_task_number + \
                              order_k * sub_task_number + sub_l
                        M5[num][z] = 1
                b5[0][z] = 1
                z = z + 1
        one_task_constrain = [M5 @ self.x_i_j_k_l <= b5]
        return one_task_constrain

    def equation_6(self):
        agent_number = len(self.agent_data)
        task_number = len(self.task_data)
        max_task_list = len(self.task_data)
        sub_task_number = len(self.sub_task_type)
        M6 = [[0 for i in range(agent_number * (max_task_list - 1))] for j in
              range(agent_number * task_number * max_task_list * sub_task_number)]
        B6 = [[0 for i in range(agent_number * (max_task_list - 1))]]
        z = 0
        for agent_i in range(agent_number):
            for order_k in range(max_task_list - 1):
                for task_j in range(task_number):
                    for sub_l in range(sub_task_number):
                        num1 = agent_i * task_number * max_task_list * sub_task_number + \
                               task_j * max_task_list * sub_task_number + \
                               order_k * sub_task_number + sub_l
                        num2 = agent_i * task_number * max_task_list * sub_task_number + \
                               task_j * max_task_list * sub_task_number + \
                               (order_k + 1) * sub_task_number + sub_l
                        M6[num1][z] = 1
                        M6[num2][z] = -1
                z = z + 1
        continue_constrain = [M6 @ self.x_i_j_k_l >= B6]
        return continue_constrain

    def equation_7(self):
        agent_number = len(self.agent_data)
        task_number = len(self.task_data)
        max_task_list = int(len(self.task_data))
        sub_task_number = len(self.sub_task_type)
        M7 = []
        T7 = []
        B7 = []
        for agent_i in range(agent_number):
            for task_j1 in range(task_number):
                for task_j2 in range(task_number):
                    if not task_j1 == task_j2:
                        t = [0 for i in range(task_number)]
                        t[task_j1] = -1
                        t[task_j2] = 1
                        for order_k in range(max_task_list - 1):
                            m = [0 for i in range(agent_number * max_task_list * task_number * sub_task_number)]
                            for sub_l in range(sub_task_number):
                                numj1 = agent_i * task_number * max_task_list * sub_task_number + \
                                        task_j1 * max_task_list * sub_task_number + \
                                        order_k * sub_task_number + sub_l
                                numj2 = agent_i * task_number * max_task_list * sub_task_number + \
                                        task_j2 * max_task_list * sub_task_number + \
                                        (order_k + 1) * sub_task_number + sub_l
                                m[numj1] = -self.horizon
                                m[numj2] = -self.horizon
                            b = self.get_distance(self.task_data[task_j1][2],
                                                  self.task_data[task_j2][2]
                                                  ) / self.agent_type[self.agent_data[agent_i][2]]['velocity'] + \
                                self.task_type[self.task_data[task_j1][1]][0] - 2 * self.horizon
                            M7.append(m)
                            T7.append(t)
                            B7.append([b])
        self.M7 = M7
        self.T7 = T7
        self.B7 = B7
        if not M7 == []:
            M71 = self.Turn_Matrix(M7)
            T71 = self.Turn_Matrix(T7)
            B71 = self.Turn_Matrix(B7)
            motion_constrain = [M71 @ self.x_i_j_k_l + T71 @ self.t_j >= B71]
            return motion_constrain

    def equation_8(self):
        agent_number = len(self.agent_data)
        task_number = len(self.task_data)
        max_task_list = int(len(self.task_data))
        sub_task_number = len(self.sub_task_type)
        M8 = [[0 for i in range(agent_number * task_number)] for j in
              range(agent_number * task_number * max_task_list * sub_task_number)]
        t8 = [[0 for i in range(agent_number * task_number)] for j in range(task_number)]
        B8 = [[0 for i in range(agent_number * task_number)]]
        z = 0
        for agent_i in range(agent_number):
            for task_j in range(task_number):
                for sub_l in range(sub_task_number):
                    num = agent_i * task_number * max_task_list * sub_task_number + \
                          task_j * max_task_list * sub_task_number + sub_l
                    M8[num][z] = -self.horizon
                t8[task_j][z] = 1
                B8[0][z] = self.get_distance(self.agent_data[agent_i][1], self.task_data[task_j][2]) / \
                           self.agent_type[self.agent_data[agent_i][2]]['velocity'] - self.horizon
                z = z + 1
        motion_constrain2 = [M8 @ self.x_i_j_k_l + t8 @ self.t_j >= B8]
        return motion_constrain2

    def Turn_Matrix(self, M):
        r = [[] for i in M[0]]
        for i in M:
            for j in range(len(i)):
                r[j].append(i[j])
        return r

    def get_horizon(self):
        self.horizon = 0
        for i in self.task_data:
            self.horizon = self.task_type[i[1]][0] * 2 + self.horizon + 100

    def get_distance(self, i, j):
        pos1 = self.position[i][0] - self.position[j][0]
        pos2 = self.position[i][1] - self.position[j][1]
        lenth = (pos1 ** 2 + pos2 ** 2) ** 0.5
        return lenth


    def check_the_value(self, node):
        self.get_horizon()
        agent_number = len(self.agent_data)
        task_number = len(self.task_data)
        max_task_list = int(len(self.task_data))
        sub_task_number = len(self.sub_task_type)
        self.x_i_j_k_l = cp.Variable(shape=(agent_number * task_number * max_task_list * sub_task_number, 1),
                                     boolean=True)
        self.t_j = cp.Variable(shape=(task_number, 1), nonneg=True)
        con1 = self.Temporal_con_of_equation_1()
        con2 = self.enough_con_of_equation_2()
        con3 = self.serve_limit_con_of_equation_3()
        con4 = self.once_task_con_of_equation_4()
        con5 = self.one_task_a_time_con_of_equation_5()
        con6 = self.equation_6()
        con7 = self.equation_7()
        con8 = self.equation_8()
        total_constrain = [*con1, *con2, *con3, *con4, *con5, *con6, *con7, *con8]
        M9 = []
        B9 = []
        for agent_i in range(len(node)):
            for order_k in range(len(node[agent_i])):
                sub_l = self.sub_task_type.index(node[agent_i][order_k][1])
                task_j = node[agent_i][order_k][0][0]
                # print('i',agent_i,'j',task_j,'k',order_k,'l',sub_l)
                m = [0 for i in range(agent_number * task_number * max_task_list * sub_task_number)]
                num = (agent_i) * task_number * max_task_list * sub_task_number + \
                      (task_j) * max_task_list * sub_task_number + \
                      (order_k) * sub_task_number + sub_l
                m[num] = 1
                # print('num',num)
                b = 1
                M9.append(m)
                B9.append([b])
        M91 = self.Turn_Matrix(M9)
        B91 = self.Turn_Matrix(B9)
        cons9 = [M91 @ self.x_i_j_k_l == B91]
        total_constrain.append(*cons9)
        tim = [[]]
        for i in self.task_data:
            tim[0].append(self.task_type[i[1]][0])
        obj = cp.Minimize(cp.max(self.t_j + tim))
        prob = cp.Problem(obj, total_constrain)
        # solver: GLPK_MI CBC SCIP
        prob.solve(solver='GLPK_MI', eps=0.1)
        # print('opt-value:',prob.value)
        print(prob.value)
        print(self.t_j.value)
        if prob.status == 'optimal':
            self.valueofx_i_j_k_l = self.x_i_j_k_l.value
            self.valueoft_j = self.t_j.value
            self.print_answer()
            z = 1
            for i in self.assignment:
                # print('agent',z,'task list is:',i)
                z = z + 1
        print(prob.value)
        # print(node)
        # print(self.valueoft_j)
        return prob
