#！/usr/bin/env python3

'''
@Date   : 2023/11 -->  
@Authors: Zesen Liu, Junjie Wang, Qisheng Zhao, Shuo Zhang
@Contact: pkuwjj1998@163.com
@Version: 1.0
@Descrip: generate the set of partial relations.
@Log:
        - bf 2023/11: the initial version by Zesen Liu;
        - 2023/11/20: the first refined version
'''


import time
import copy
import warnings
import numpy as np
import networkx as nx
from itertools import chain,combinations

from .buchi import BuchiAuto
from .LTL2BA.boolean_formulas.parser import parse_guard as parse

warnings.filterwarnings('ignore',category=Warning)


class Buchi_poset_builder(object):
    '''
    this class is build to get the poset from the buchi
    to do :
    prefix to suffix
    remove the useless edges as (1)

    '''
    def __init__(self, task):
        buchi = BuchiAuto(task)     # 根据任务公式生成Buchi自动机
        self._buchi = buchi
        self.find_true_ends()       # 判断并找出真正的可接收node（是否存在自循环path）
        self._new_buchi = copy.deepcopy(self.buchi)     # 将self._buchi的值赋值给self._new_buchi且这两个变量互不干扰
        self.found_action_list=[]

    def main_fun_to_get_poset(self, time_budget):
        # 对BA进行剪枝（论文中prune的前两步在代码中没有，因为不会发生那种情况）
        self.pruning_step_time=time.time()
        
        self.remove_the_1_edge_with_node()      # 删除重复的等价节点(两node不发生任何事就可以相互转移，说明其等价)
        self.remove_pue_negative_edges()    # 删除公式中存在空label''的edges
        self.remove_equivalent_state()  # 删掉edge='(1)'之后完全等价的状态只留1个
        self.delete_the_edges()     # 删除可分解的edges（对应论文prune第三步）
        self.delete_the_self_loop()     # 删除条件为1/True的自循环edges（因为它在DFS找accepting path的时候会导致找到一些冗余的path）
        self.pruning_step_time = time.time()-self.pruning_step_time
        #self.delete_the_unfeasible_edges() # 这应该对应论文中prune的第一步：移除不可执行的边

        # 根据得到的BA进行偏序关系分析
        self.poset_ana_time=time.time()
        self.generate_poset3_anytime(self.new_buchi,time_budget,type='prefix')  # 进行path搜索以及偏序分析
        # still need to choose a better planner and get the best poset to the left calculate
        self.use_essential_for_act_map()    # 把转移公式中的符号以及自循环条件删掉，只留下必要的动作标签(自循环条件通过加入'!='偏序关系来考虑)，'action_map'格式改变！
        self.concurrent_subtask_decomposition()
        # self.poset_language_shorter()   # 对每个poset的language进行评估，然后根据评估值进行升序排列
        self.poset_ana_time=time.time()-self.poset_ana_time
        self.chose_final_poset()
        self.prioritization()

    def remove_equivalent_state(self):      # 删掉edge='(1)'之后完全等价的状态只留1个
        remove_nodes = []
        initial_nodes = []
        for node in self.new_buchi.nodes():
            initial_nodes.append(node)
        for node1 in range(len(initial_nodes)):
            for node2 in range(len(initial_nodes)):
                if node1 < node2:
                    if initial_nodes[node1].split('_')[1] == initial_nodes[node2].split('_')[1]:
                        remove_nodes.append(node2)
        for i in remove_nodes:
            self.new_buchi.remove_node(initial_nodes[i])
        
    def prioritization(self):
        poset = self.final_poset
        action_map = poset['action_map']
        less_equal = poset['<=']
        equal = poset['=']
        # initialization
        priority_dic = {}
        all_action_list = [i for i in range(len(action_map))]    # index of action label:[0,1,...,len-1]
        un_p_action_list = copy.deepcopy(all_action_list)
        for i in all_action_list:
            priority_dic[i] = float('inf')      # 初始时将所有action的priority值都设为正无穷
        for i in all_action_list:
            p0_label = 1       # 表征此action是否能设为0级优先度
            for j in all_action_list:
                if (j,i) in less_equal:
                    p0_label = 0
            if p0_label:
                priority_dic[i] = 0
                un_p_action_list.remove(i)      # 用remove不能用pop，因为索引会在迭代中改变
        # main loop
        while un_p_action_list:
            for un_p_action in un_p_action_list:
                if un_p_action in un_p_action_list:
                    pre_action_list = []
                    for action in all_action_list:
                        if (action,un_p_action) in less_equal:
                            pre_action_list.append(action)
                    all_pre_p_label = 1     # 表征此action的前置动作是否都已经完成优先级计算
                    for pre_action in pre_action_list:
                        if pre_action in un_p_action_list:
                            all_pre_p_label = 0
                    if all_pre_p_label:
                        p_of_pre_action = []    # 存放pre_action优先级的列表
                        for pre_action in pre_action_list:
                            p_of_pre_action.append(priority_dic[pre_action])
                        priority_dic[un_p_action] = max(p_of_pre_action) + 1
                        un_p_action_list.remove(un_p_action)     #！！！          
                        con_action_list = []     # 用于收集与任务un并行的任务index
                        for con_set in equal:
                            if un_p_action in con_set:
                                for con_action in con_set:
                                    con_action_list.append(con_action)
                        if con_action_list:
                            a = priority_dic[un_p_action]
                            for con_action in con_action_list:
                                priority_dic[con_action] = a
                                if con_action in un_p_action_list:
                                    un_p_action_list.remove(con_action)
        
        self.priority_dic = {}
        for i in all_action_list:
            self.priority_dic[poset['action_map'][i]] = priority_dic[i]
        
        # # ---------------------------------------------------------------------------- #
        # #   针对智能体子群能力部分，暂时用不到了
        # # ---------------------------------------------------------------------------- #  
        # 新增部分，方便后续的任务分配
        # Agent_Cap_dic = {'g1':{'a','s'},
        #     'g2':{'b','s'},
        #     'g3':{'c','s'},
        #     'g4':{'d','e','s'}
        #         }       # 表征每个智能体子群拥有的能力，s是探测区域的能力，每个智能体都具备
        
        # # priority_set = set()        # 存放所有适合分配的、可能的优先级字典的集合
        # new_priority_dic = copy.deepcopy(priority_dic)      # 生成适合分配的优先级字典
        
        # priority_level_dic = {}     # 每一级优先级对应的所有action索引列表 e.g. {0:[1,3,4],1:[0,2],...}
        # max_level = max(priority_dic.values())      # 计算初始时优先级的最大值
        # for i in range(max_level + 1):
        #     priority_level_dic[i] = []
        # for key,value in priority_dic.items():
        #     priority_level_dic[value].append(key)
        
        # for priority_value in priority_level_dic.keys():            
        #     for action1 in priority_level_dic[priority_value]:       # 对所有处于同一优先级的动作        
        #         con_list1 = []       # 列表存放action1的并行动作
        #         for con_set in equal:
        #             if action1 in con_set:
        #                 for con_action in con_set:
        #                     con_list1.append(con_action)
                
        #         for action2 in priority_level_dic[priority_value]:
        #             if action2 in con_list1:     # 并行动作肯定是不用重新计算优先级的
        #                 continue
        #             recalculate_label = 0     # 表征是否需要进行新的优先级计算（当两个子任务并非并行关系又需要同一个智能体子群来完成时）
        #             for j in Agent_Cap_dic.values():
        #                 if (action1 in j) and (action2 in j):
        #                     recalculate_label = 1
        #             if recalculate_label:   # 把两个子任务的优先级有意错开（两种情况）并更新优先级字典，这里暂时选择将action1的优先级加1
        #                 max_level = max(new_priority_dic.values())      # 更新此时优先级的最大值
        #                 for i in range(max_level + 1):
        #                     priority_level_dic[i] = []      # 更新每一级优先级对应的所有action索引列表
        #                 for key,value in new_priority_dic.items():
        #                     priority_level_dic[value].append(key)                      
                        
        #                 new_priority_dic[action2] = new_priority_dic[action2] + 1
        #                 con_list2 = []       # 列表存放action1的并行动作
        #                 for con_set in equal:
        #                     if action2 in con_set:
        #                         for con_action in con_set:
        #                             con_list2.append(con_action)
        #                 for con_action in con_list2:     # 更新其并行子任务的优先级
        #                     if con_action != action2:
        #                         new_priority_dic[con_action] = new_priority_dic[con_action] + 1
        #                 for k in range(priority_value,max_level+1):     # 把优先级值高于action1的子任务优先级全部+1
        #                     for m in priority_level_dic[k]:
        #                         new_priority_dic[m] = new_priority_dic[m] + 1                                                                                     
               
        # self.assign_priority_dic = {}
        # for i in all_action_list:
        #     self.assign_priority_dic[poset['action_map'][i]] = new_priority_dic[i]      
        
    
    def find_true_ends(self):   # 判断并找出真正的可接收状态/节点
        pot_ends=self.buchi.graph['accept']
        true_ends=[]
        for node in pot_ends:
            n=self.if_has_circle(self.buchi,node,node)  # 看它有没有从自己到自己的循环路径
            if not n==[]:
                true_ends.append(node)
        self.buchi.graph['accept']=true_ends
        return true_ends

    def if_has_circle(self, graph, start, end):     # 从Buchi自动机图中找从start到end的path
        path = []
        paths = []
        queue = [(start, path)]
        while queue:
            start, path = queue.pop()
            path = path + [start]
            if start==end:
                if len(path)>1:
                    paths.append(path)
            for node in set(graph.neighbors(start)).difference(path):
                queue.append((node, path))
        if self.buchi.has_edge(end,end):
            paths.append([end])
        return paths
    
    # ---------------------------------------------------------------------------- #
    def delete_the_self_loop(self):     # 删除条件为1/True的自循环edges
        print('\n----------------------------------')
        print('[Buchi]: begin to delete the self loop of NBA')
        for node in self.new_buchi.nodes:
            #print(node)
            if self.new_buchi.has_edge(node,node):
                #print('node is :',node,'edge is ',self.new_buchi.edges[node,node]['guard_formula'])
                if self.new_buchi.edges[node,node]['guard_formula']=='(1)':
                    self.new_buchi.remove_edge(node,node)
                    # self.buchi.remove_edge(node,node)
        #self.check_if_self_loop()

    def check_if_self_loop(self):
        for node in self.new_buchi.nodes:
            if self.new_buchi.has_edge(node,node):
                print(self.new_buchi.edges(node,node))

    # ---------------------------------------------------------------------------- #
    def remove_the_1_edge_with_node(self):  # 若两个node之间转移条件为1，说明二者等效，把其中一个删掉（node2）
        '''
        Sometime will occur that the initial node was remove situation!
        '''
        edge1_list=[]
        print('--------------')
        for (node1,node2) in self.new_buchi.edges:
            if node1 != node2:
                if self.new_buchi.edges[(node1,node2)]['guard_formula']=='(1)':     #从一个node到另一个node的转移条件为1/true
                    edge1_list.append((node1,node2))
        self.edge1_list=edge1_list.copy()
        while not edge1_list==[]:
            (node1,node2)=edge1_list.pop()
            #if self.buchi.in_edges:
            if self.buchi.has_edge(node2,node1):
                if not self.buchi[node2][node1]['guard_formula']=='(1)':
                    continue
            if node2=='T0_init':
                node_mid=copy.deepcopy(node1)
                node1=copy.deepcopy(node2)
                node2=node_mid
            for succ_node2 in self.new_buchi.succ[node2]:
                guard_formula=self.new_buchi.edges[(node2,succ_node2)]['guard_formula']
                guard_expr=self.new_buchi.edges[(node2,succ_node2)]['guard_express']
                if not node1==succ_node2 :
                    self.new_buchi.add_edge(node1,succ_node2,guard_formula=guard_formula, guard=guard_expr)
            for pred_node2 in self.new_buchi.pred[node2]:
                guard_formula=self.new_buchi.edges[(pred_node2,node2)]['guard_formula']
                guard_expr=self.new_buchi.edges[(pred_node2,node2)]['guard_express']
                if not node1==pred_node2 :
                    self.new_buchi.add_edge(pred_node2,node1,guard_formula=guard_formula, guard=guard_expr)
            # print('remove node:',node2)
            self.new_buchi.remove_node(node2)
            # here is the label
            if node2 in self.buchi.graph['accept']:
                self.buchi.graph['accept'].remove(node2)
            new_edge1_list=[]
            for (node3,node4) in edge1_list:
                if node3==node2:
                    node3=node1
                if node4==node2:
                    node4=node1
                new_edge1_list.append((node3,node4))
            edge1_list=new_edge1_list.copy()
        self.old_new_buchi=copy.deepcopy(self.new_buchi)
        #self.check_if_1()

    def check_if_1(self):
        for (node1,node2) in self.new_buchi.edges:
            if self.new_buchi.edges[(node1,node2)]['guard_formula']=='(1)':
                print('there still has an (1) edge as :',node1,node2)
                print('error!!')

    # ---------------------------------------------------------------------------- #
    def remove_pue_negative_edges(self):    # 删除公式中存在空label''的edges
        to_remove_edge_list=[]
        print('--------------')
        for (node1,node2) in self.new_buchi.edges:
            gama=self.new_buchi[node1][node2]['guard_formula']
            if self.pue_negative(gama)==0:
                print(gama,node1,node2)
                to_remove_edge_list.append((node1,node2))
        s=1
        while not to_remove_edge_list==[]:
            (node1,node2)=to_remove_edge_list.pop()
            if node1==node2:
                continue
            #if self.buchi.in_edges:
            if self.new_buchi.has_edge(node2,node1):
                if not self.buchi[node2][node1]['guard_formula']=='(1)':
                    continue
            if node2=='T0_init':
                node_mid=copy.deepcopy(node1)
                node1=copy.deepcopy(node2)
                node2=node_mid
            for succ_node2 in self.new_buchi.succ[node2]:
                guard_formula=self.new_buchi.edges[(node2,succ_node2)]['guard_formula']
                guard_expr=self.new_buchi.edges[(node2,succ_node2)]['guard_express']
                if not node1==succ_node2 :
                    self.new_buchi.add_edge(node1,succ_node2,guard_formula=guard_formula, guard=guard_expr)
            for pred_node2 in self.new_buchi.pred[node2]:
                guard_formula=self.new_buchi.edges[(pred_node2,node2)]['guard_formula']
                guard_expr=self.new_buchi.edges[(pred_node2,node2)]['guard_express']
                if not node1==pred_node2 :
                    self.new_buchi.add_edge(pred_node2,node1,guard_formula=guard_formula, guard=guard_expr)
            if node2=='T0_init':
                break
            # print('remove node:',node2)
            self.new_buchi.remove_node(node2)
            # here is the label
            if node2 in self.buchi.graph['accept']:
                self.buchi.graph['accept'].remove(node2)
            new_to_remove_edge_list=[]
            for (node3,node4) in to_remove_edge_list:
                if node3==node2:
                    node3=node1
                if node4==node2:
                    node4=node1
                new_to_remove_edge_list.append((node3,node4))
            to_remove_edge_list=new_to_remove_edge_list.copy()
        self.old_new_buchi=copy.deepcopy(self.new_buchi)

    def pue_negative(self,gama):
        checker=parse(gama)
        #sub_list=list(self.powerset(self.symbols_extracter(gama)))
        #label=0
        #sub_list.remove(())
        if checker.check(' ')==1:   # 检查是否有空的label
            return 0
        else:
            return 1
        #     for sub_task in sub_list:
        #         if checker.check(' '.join(sub_task)) == 1:
        #             label=1
        #             return  label
        #     return  label
        # else:
        #     return  1

    # ---------------------------------------------------------------------------- #
    def delete_the_edges(self):     # 删除可分解的edges;这是prune的最后一步，得到pruned NBA
        '''
        node1 ------> node2
          |          |
          |       |
          V    V
        node3
              label:(1)
        node1 ------> node2
        delete node1
        '''
        #self.delete_edge_buchi=self.buchi
        self.symbols_formula_dic={}
        self.buchi_before_dec=copy.deepcopy(self.new_buchi)     # !!!self.buchi_before_dec为用于后续判定偏序关系的自动机，self.new_buchi是经过完全prune的自动机
        new_buchi_before_cut=copy.deepcopy(self.new_buchi)
        for node1 in new_buchi_before_cut.nodes:
            for node2 in new_buchi_before_cut.successors(node1):
                for node3 in new_buchi_before_cut.successors(node1):
                    if new_buchi_before_cut.has_edge(node2,node3):
                        gama1=new_buchi_before_cut.edges[node1,node2]['guard_formula']
                        gama2=new_buchi_before_cut.edges[node2,node3]['guard_formula']
                        gama3=new_buchi_before_cut.edges[node1,node3]['guard_formula']
                        if not ((node1==node2) or (node1==node3) or (node2==node3)):
                            #here add a new judgement becasue when gama2==gama3 ,there might be lose
                            #a situation if we cut off the gama3 directory
                            #for example <> (a && <> b) && <>( d && <> c)
                            #date May. 9th.
                            if gama2==gama3:
                            #if     gama1==gama2 and gama2==gama3:
                                continue
                            if self.check_symbols_and_formula1(gama1,gama2,gama3):
                                if self.new_buchi.has_edge(node1,node3):
                                    self.new_buchi.remove_edge(node1,node3)
                                    # print(node1,node2,node3,'are delate and the labels are :',gama1,gama2,gama3)
        #edgesset=copy.deepcopy(self.new_buchi.edges)
        print('create new buchi with',len(self.new_buchi.nodes),'states and',len(self.new_buchi.edges),'edges')

    def check_symbols_and_formula1(self,gama1,gama2,gama3):
        '''due to the difficulty of check two formula is equal,
           here I choose to check the truth table of two formula
           '''

        replan_list1=(gama1,gama2,gama3)
        replan_list2=(gama2,gama1,gama3)
        if replan_list1 in self.symbols_formula_dic.keys():
            return self.symbols_formula_dic[replan_list1]
        if  replan_list2 in self.symbols_formula_dic.keys():
            return self.symbols_formula_dic[replan_list2]
        gama3_hat='('+gama1+')'+' && '+'('+gama2+')'
        #print(gama1,' ',gama2,' ',gama3)
        formula_old=parse(gama3)
        formula_in=parse(gama3_hat)
        formula_old_subset=list(self.powerset(self.symbols_extracter(gama3)))
        formula_in_subset=list(self.powerset(self.symbols_extracter(gama3_hat)))
        if not len(formula_old_subset)==len(formula_in_subset):
            self.symbols_formula_dic[replan_list1]=0
            self.symbols_formula_dic[replan_list2]=0
            return 0
        for subset in formula_in_subset:
            if not formula_in.check(' '.join(subset)) == formula_old.check(' '.join(subset)):
                self.symbols_formula_dic[replan_list1]=0
                self.symbols_formula_dic[replan_list2]=0
                #print(' '.join(subset))
                return  0
        #for subset in formula_old_subset:
            #if not formula_in.check(' '.join(subset)) == formula_old.check(' '.join(subset)):
                #return  0
        self.symbols_formula_dic[replan_list1]=1
        self.symbols_formula_dic[replan_list2]=1
        return 1

    # ---------------------------------------------------------------------------- #
    def generate_poset3_anytime(self,graph,time_budget,type='prefix'):
        #the bug is that some edge is truely same as a->b and a->c so it is difficult to found out
        #begin DFS
        #once find a accepting path,begin to find the poset
        #save the accepting language of the poset
        #save the poset
        #continue the DFS
        # 泽森师兄第一篇论文Alg.1 Compute_poset()
        self.feasible_edges_list=[]
        self.unfeasible_edges_list=[]
        start=list(self.buchi.graph['initial'])[0]     # 将初始节点集合变为列表并取出第一个元素
        ends=self.buchi.graph['accept']     # ends为可接收节点集合
        self._prefix_path=[]
        path = []
        paths = []
        self.poset_list=[]
        queue = [(start, path)]
        start_time=time.time()
        self.poset_start_time=time.time()
        self.poset_start_time_list=[]
        search_list=[]
        self.language_list=[]
        while queue and time.time()-start_time<time_budget:     # 这个while循环用于不断生成path（DFS）
            start, path = queue.pop()
            path = path + [start]
            if start in ends:   # 找到了一个accepting path
                if path not in paths:
                    paths.append(path)
                    # begin to poset search
                    act_list=self.change_state_path_into_edge(graph,path)   # 将path(node序列)转换成word(edge序列) 格式：['(scout_b01)', '(attack_b02)']
                    if act_list in self.found_action_list:      # 初始化的时候self.found_action_list是空列表
                        paths.extend(poset_language_state)   # 把括号列表中的元素添加到paths列表中
                        continue
                    poset,poset_potential_language=self.find_poset_due_to_one_path(self._buchi,path)  # 根据一个path输出它的poset和可行的words
                    poset_language_state,poset_language=self.general_poset_language(graph,poset,poset_potential_language,path)   # 根据上一步得到的poset和language输出最终符合偏序关系的runs和language
                    end=time.time()
                    self.poset_list.append(poset)
                    self.language_list.append(-len(poset_language))     # ！！这里添加的是language中word数量的负数，关注一下self.language_list后面是怎么用的
                    self.poset_start_time_list.append(end-start_time)   # 记录完成每个path的偏序分析过程的时刻
                    paths.extend(poset_language_state)
                    break       # 只要找到一条accepting path即可
            for node in set(self.new_buchi.neighbors(start)).difference(path):   # difference返回只存在于graph.neighbors而不存在于path中的元素集合
                queue.append((node, path))
            #print('queue', queue)

    def find_poset_due_to_one_path(self,graph,path):    # 根据一个path输出它的偏序集以及可行的words（Alg.1的核心部分）
        action_list = self.change_state_path_into_edge(self.new_buchi,path)    # 通过path得到edge公式序列 'action_map'格式: ['(a1 && a2)', '(b1 && b2)']
        # for task_i in range(len(task_map)):
        #     if len(task_map[task_i]) > 1:
        #         double_label=1     
        poset={'||':set(),'<=':set(),'<':set(),'!=':set(),'=':set(),'action_map':action_list}
        #'parallel':(a,b) a||b
        # 'stirt less-than': (a,b)  a<b
        #'less-than': (a,b)  a<=b
        # 'not equal': (a,b)  a\= b
        act_list_map=list(range(len(action_list)))  # [0,1,2,...,len-1]，映射成它们的索引
        queue=[[[i] for i in act_list_map]] # [[[0],[1],...]]
        explored_word=[]
        explored_word.append([[i] for i in act_list_map])
        unfeasible_word=[]
        while queue:
            base_action_map=queue.pop()     # [[0],[1],...,[len(action_list)-1]]
            for i in np.arange(len(base_action_map)-1):     # ≤关系判定
                if not (base_action_map[i][0],base_action_map[i+1][0]) in poset['<=']:
                    new_list_map_1=copy.deepcopy(base_action_map)
                    new_list_map_1[i]=base_action_map[i+1]  # 对应论文中的swap操作，交换相邻action的位置
                    new_list_map_1[i+1]=base_action_map[i]
                    new_action1=[action_list[x[0]] for x in new_list_map_1]  # 生成对应顺序的新的action_list
                    if new_list_map_1 in explored_word:
                        label1=1
                    elif new_list_map_1 in unfeasible_word:
                        label1=0
                    else:
                        label1=self.check_if_action_feasible(graph,new_action1,path[0])  # 检测new_action1动作序列是否可行以及最终能否到达一个accepting state
                    if action_list[new_list_map_1[i][0]]==action_list[new_list_map_1[i+1][0]]:
                        label1=0
                    if not label1:
                        if base_action_map[i][0]<base_action_map[i+1][0]:   # 对这部分的if else仍存在疑问？？？
                            poset['<='].add(tuple((base_action_map[i][0],base_action_map[i+1][0])))
                        else:
                            poset['<='].add(tuple((base_action_map[i+1][0],base_action_map[i][0])))
                        #poset['<='].add(tuple((base_action_map[i][0],base_action_map[i+1][0]))) 
                        if not new_list_map_1 in unfeasible_word:
                            unfeasible_word.append(new_list_map_1)
                    else:
                        if not new_list_map_1 in explored_word:
                            queue.append(new_list_map_1)
                            explored_word.append(new_list_map_1)
        
        # 给self.buchi_before_dec加上标签为"(1)"的自循环edge
        for node in self.buchi_before_dec.nodes():
            if 'init' in node:
                self.buchi_before_dec.add_edge(node,node,guard_formula='(1)')
        
        
        for j in range(len(action_list)):     # !=关系判定
            for k in range(len(action_list)):
                if j < k:
                    new_action2 = copy.deepcopy(action_list)        # 需要考虑公式前后放置两种情况，因为在buchi自动机中只会有一种形式
                    concaction1 = '(' + action_list[j].replace('(', '').replace(')', '') + ' && ' + action_list[k].replace('(', '').replace(')', '') + ')'
                    concaction2 = '(' + action_list[k].replace('(', '').replace(')', '') + ' && ' + action_list[j].replace('(', '').replace(')', '') + ')'
                    label2 = 0
                    action_j = action_list[j]
                    action_k = action_list[k]
                    new_action2[k] = concaction1
                    if self.check_if_action_feasible(self.buchi_before_dec,new_action2,path[0]):
                        label2 = 1      # 检测new_action2动作序列是否可行以及最终能否到达一个accepting state
                    new_action2[k] = concaction2
                    if self.check_if_action_feasible(self.buchi_before_dec,new_action2,path[0]):
                        label2 = 1
                    new_action2[k] = action_k
                    new_action2[j] = concaction1
                    if self.check_if_action_feasible(self.buchi_before_dec,new_action2,path[0]):
                        label2 = 1
                    new_action2[j] = concaction2
                    if self.check_if_action_feasible(self.buchi_before_dec,new_action2,path[0]):
                        label2 = 1
                    if not label2:
                        poset['!='].add(tuple((j,k))) 
                        poset['!='].add(tuple((k,j)))
      
        return poset, explored_word

    def check_if_action_feasible(self,graph,new_action,begin_state):    # 检测一个动作序列是否可行以及最终能否到一个accepting的节点
        # if new_action in self.feasible_edges_list:
        #     return 1
        # if new_action in self.unfeasible_edges_list:
        #     return 0
        pre_state_set=[begin_state]
        for act in new_action:
            currect_label=0
            suf_state_set=[]
            for pre_state in pre_state_set:
                for suf_state in graph.successors(pre_state):   # graph.successors返回子节点列表
                    if graph[pre_state][suf_state]['guard_formula'] in [act, '(1)'] :
                        suf_state_set.append(suf_state)
                        currect_label=1
                if currect_label==0:# if one transition is unfeasible, then break down and return 0
                    self.unfeasible_edges_list.append(new_action)
                    return 0
            # print(suf_state_set)
            pre_state_set=suf_state_set.copy()  # 这里copy之后pre_state_set的前一个节点就已经不存在了
        for state in suf_state_set:     # 这里的suf_state_set为动作序列执行之后到达的状态节点集合（列表）
            if state in graph.graph['accept']:
                self.feasible_edges_list.append(new_action)
                return 1
        return 0

    def change_state_path_into_edge(self,graph,path):   # 将path(node序列)转换成word(edge序列) return的数据格式：['(scout_b01)', '(attack_b02)']
        edge_list=[]
        for i in range(len(path)-1):
            edge_list.append(graph[path[i]][path[i+1]]['guard_formula'])
        return  edge_list
    
    def general_poset_language(self,graph,poset,potential_language,path):   # 根据上一步得到的poset和language输出最终符合偏序关系的runs和language
        true_language_num=copy.deepcopy(potential_language)
        for act_number_list in potential_language:
            for i,j in poset['<=']:     # 把不符合偏序关系的word从language中删掉
                num_i=act_number_list.index([i])
                num_j=act_number_list.index([j])
                if num_i > num_j:
                    true_language_num.remove(act_number_list)   # 最终的language
                    break
        true_language=[]
        for act_number_list in true_language_num:
            act_list=[poset['action_map'][i[0]] for i in act_number_list]
            node_list=self.change_edges_into_nodes(graph,act_list,path)     # 根据act_list和给定path的初始点寻找相应的path（edge to path）
            true_language.append(node_list)
        self.found_action_list.extend([[poset['action_map'][i[0]] for i in number_list] for number_list in true_language_num])
        return true_language,true_language_num
    
    def change_edges_into_nodes(self,graph,act_list,path):  # 根据act_list和给定path的初始点寻找相应的path
        node_path=[]
        start=path[0]
        node_path.append(start)
        pre_state=start
        for act in act_list:
            for suf_state in graph.successors(pre_state):
                if graph[pre_state][suf_state]['guard_formula']==act:
                    if pre_state==suf_state:
                        s=1
                    node_path.append(suf_state)
                    pre_state=suf_state
                    break
        return node_path

    # ---------------------------------------------------------------------------- #
    def use_essential_for_act_map(self):    # essential sequence定义，把符号以及自循环条件删掉，只留下必要的动作标签(自循环条件通过加入'!='偏序关系来考虑)
        path_action=[]
        for poset in self.poset_list:
            path = poset['action_map']    # 'action_map'为最初path的edge公式序列，格式：['(c1 && !d1)', '(d2 && d3)']
            for i in np.arange(len(path)):  # 返回数组[0 1 2 ... len(path)-1]
                formula = list(self.powerset(self.symbols_extracter(path[i])))  # 对每个转移的公式进行label的提取并进行排列组合得到新的列表 e.g.[(), ('a2',), ('a1',), ('a2', 'a1')]
                sequence_checker=parse(path[i])     # 解析公式，判断出and关系
                subset_list=[]
                for subset in formula:
                    test = sequence_checker.check(' '.join(subset))
                    if sequence_checker.check(' '.join(subset)) ==1:    # join把列表中的label用空格连成一个string;sequence_checker.check是公式判断器，正确则return 1
                        subset_list.append(subset)
                        break
                #only remain the subset
                subset_list_num=[len(subset) for subset in subset_list]
                subset_list_sort=sorted(range(len(subset_list_num)),key=lambda  k:subset_list_num[k])   # 按照数值进行升序排列
                new_subset_list=[subset_list[i] for i in subset_list_sort]  # 按照label数量从小到大进行升序排列
                if () in new_subset_list:
                    new_subset_list=[()]
                else:
                    for subset in new_subset_list:
                        for new_subset in new_subset_list:
                            remove_label=1
                            for act in subset:
                                if not act in new_subset:
                                    #print(act,new_subset)
                                    remove_label=0
                            if remove_label==1:
                                if not subset==new_subset:
                                    subset_list.remove(new_subset)
                                    new_subset_list.remove(new_subset)
                path_action.append(subset_list)     # path_action格式：[[公式1的最简subset],[公式2的最简subset]...]
            path_action_list=[]
            while not len(path_action)==0:
                act_list=path_action.pop(0)     # act_list格式为[公式n的最简subset] e.g.[('c1',)]
                new_path_action_list=[]
                for act in act_list :   # act数据格式：（'a1','a2'）e.g. ('c1',)
                    if len(path_action_list)==0:
                        new_path_action_list.append([[i for i in act]])
                    else:
                        for path in path_action_list:
                            new_path_action_list.append([*path,[i for i in act]])
                path_action_list=new_path_action_list.copy() # 格式：[[['并行动作集1'], ['并行动作集2']]]
            poset['action_map']=path_action_list[0]     # 这一步之后poset['action_map']的格式变成了：[['c1'], ['d3', 'd2']]

    def symbols_extracter(self,string):    # 从formula中提取label并统计在一个set中
        symbols_set = set()
        symbol = ''
        for i in string:
            if i not in '|() &!':
                symbol = symbol + i
            else:
                if symbol != '':
                    symbols_set.add(symbol)
                    symbol = ''
        return symbols_set

    def powerset(self,iterable):    # 对得到的label集合中的label进行排列组合
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))   # 对列表中的元素进行排列组合，r规定了最终列表元素个数

    # ---------------------------------------------------------------------------- #
    def concurrent_subtask_decomposition(self):   # 删除poset['action_map']中的空列表、分解并行动作标签、计算'='关系并更新'≤'关系
        
        self.num_actionset_of_poset = []     # 用于统计每个poset的并行动作集数量
        self.task_data_list=[]
        for poset_n in range(len(self.poset_list)):     # self.poset_list:[poset1,poset2,...]
            poset=self.poset_list[poset_n]
            task_map=poset['action_map']    # 得到的task_map是一个列表 [[formula中包含的需要并行的动作标签],['a1','a2'],['b1','b2','b3']...]
            double_label=0  # 用于判断有没有并行的多个action label
            zero_list=[]    # 用于存放空的动作标签列表的index
            for task_i in range(len(task_map)):
                if len(task_map[task_i]) > 1:
                    double_label=1      # 表示有需要并行的action label
                if len(task_map[task_i]) == 0:
                    zero_list.append(task_i)
            new_dic_list={}     # 字段：存放非空动作标签列表的index映射关系，用于后续偏序关系的变更
            t=0
            for i in range(len(task_map)):
                if not i in zero_list:
                    new_dic_list[i]=t
                    t=t+1
            new_leq=set()   # leq:less equal
            for i,j in poset['<=']:     # 更新≤关系
                if not i in zero_list and not j in zero_list:
                    new_leq.add(tuple((new_dic_list[i],new_dic_list[j])))
            poset['<=']=new_leq
            new_neq=set()   # neq:not equal
            for i,j in poset['!=']:     # 更新!=关系
                if not i in zero_list and not j in zero_list:
                    new_neq.add(tuple((new_dic_list[i],new_dic_list[j])))
            poset['!=']=new_neq
            if [] in task_map:
                task_map.remove([])
            
            self.num_actionset_of_poset.append(len(poset['action_map']))
            
            task_data=[]    
            if double_label:
                #to rebuild the number list
                num_dict={}     # 统计每个并行动作标签集的index集合 e.g. {0:[0,1],1:[2],2:[3,4,5]}
                z=0
                for i in range(len(task_map)):
                    num_dict[i]=list(range(z,z+len(task_map[i])))
                    z=z+len(task_map[i])
                    
                for old_num,new_num_list in num_dict.items():
                    for i in range(len(new_num_list)):
                        num = task_map[i][0].find('_')
                        task_master = task_map[i][0][0:num]
                        task_place=task_map[i][0][num+1:]
                        num2=task_place.find('_')
                        task_name=task_place[0:num2]
                        task_goal=task_place[num2+1:]
                        num3=task_goal.find('_')
                        task_area=task_goal[0:num3]
                        task_goal=task_goal[num3+1:]
                        task = (i, task_master, task_name,task_area, task_goal)
                        task_data.append(task)
                self.task_data_list.append(task_data)
            
                #rebuild poset
                new_poset={}
                for key,sub_dict in poset.items():      # 把'≤'关系更新到每个具体的action上
                    if not key == 'action_map':
                        new_poset[key]=set()
                        for i,j in poset[key]:
                            for new_i in num_dict[i]:
                                for new_j in num_dict[j]:
                                    new_poset[key].add((new_i,new_j))
                    if key == '=':      # 计算等于关系 '='
                        new_poset[key]=set()
                        for old_num,new_num in num_dict.items():
                            if len(new_num)>1:
                                coactions = set(i for i in new_num)
                                new_poset[key].add(frozenset(coactions))
                
                new_action_map = []     # 把所有并行动作集拆开成单个动作的颗粒度
                for m in task_map:
                    for n in m:
                        new_action_map.append(n)                                   
                                
                new_poset['action_map']=new_action_map
                self.poset_list[poset_n]=new_poset
                
            else:
                for i in range(len(task_map)):      # 根据'_'标识符将任务string中相关信息提取出来,这部分需要根据具体的公式定义去改，这个是适用于JK的
                    num=task_map[i][0].find('_')    # 在公式string中找有无'_',有的话返回index，没有的话返回-1
                    task_master=task_map[i][0][0:num]   # 执行任务的我方智能体
                    task_place=task_map[i][0][num+1:]
                    num2=task_place.find('_')
                    task_name=task_place[0:num2]    # 执行动作
                    task_goal=task_place[num2+1:]
                    num3=task_goal.find('_')
                    task_area=task_goal[0:num3]     # 目标区域
                    task_goal=task_goal[num3+1:]    # 目标敌方智能体
                    task=(i,task_master,task_name,task_area,task_goal)  # task格式：五元组 (0, 'scout', 'b0', 'b0', 'b01')
                    task_data.append(task)     # tasK_data:元素为五元组的列表
                self.task_data_list.append(task_data)
                new_action_map = []     # 对于不存在并行动作集的公式，只需要把外面的一层列表拆掉就好
                for m in task_map:
                    for n in m:
                        new_action_map.append(n)                                   
                                
                self.poset_list[poset_n]['action_map']=new_action_map

    # ---------------------------------------------------------------------------- #
    def chose_final_poset(self):    # 选择并行动作集数量最多的poset(这说明它的公式分解比较彻底，能够囊括完备的偏序关系)
        max_cnt = max(self.num_actionset_of_poset)
        max_idx = self.num_actionset_of_poset.index(max_cnt)
        self.final_poset = self.poset_list[max_idx]
        
    
    
    # ---------------------------------------------------------------------------- #
    #                      以下函数都未被调用，留着备用                               #
    # ---------------------------------------------------------------------------- #
    


    def exstract_action_from_formula(self,action_list):     # 从带&&的公式中抽取出必要的action label
        path_action = []    # 'action_map'为最初path的edge公式序列，格式：['(c1 && !d1)', '(d2 && d3)']
        path = action_list
        for i in np.arange(len(path)):  # 返回数组[0 1 2 ... len(path)-1]
            formula = list(self.powerset(self.symbols_extracter(path[i])))  # 对每个转移的公式进行label的提取并进行排列组合得到新的列表 e.g.[(), ('a2',), ('a1',), ('a2', 'a1')]
            sequence_checker=parse(path[i])     # 解析公式，判断出and关系
            subset_list=[]
            for subset in formula:
                test = sequence_checker.check(' '.join(subset))
                if sequence_checker.check(' '.join(subset)) ==1:    # join把列表中的label用空格连成一个string;sequence_checker.check是公式判断器，正确则return 1
                    subset_list.append(subset)
                    break
            #only remain the subset
            subset_list_num=[len(subset) for subset in subset_list]
            subset_list_sort=sorted(range(len(subset_list_num)),key=lambda  k:subset_list_num[k])   # 按照数值进行升序排列
            new_subset_list=[subset_list[i] for i in subset_list_sort]  # 按照label数量从小到大进行升序排列
            if () in new_subset_list:
                new_subset_list=[()]
            else:
                for subset in new_subset_list:
                    for new_subset in new_subset_list:
                        remove_label=1
                        for act in subset:
                            if not act in new_subset:
                                #print(act,new_subset)
                                remove_label=0
                        if remove_label==1:
                            if not subset==new_subset:
                                subset_list.remove(new_subset)
                                new_subset_list.remove(new_subset)
            path_action.append(subset_list)     # path_action格式：[[公式1的最简subset],[公式2的最简subset]...]
        path_action_list=[]
        while not len(path_action)==0:
            act_list=path_action.pop(0)     # act_list格式为[公式n的最简subset] e.g.[('c1',)]
            new_path_action_list=[]
            for act in act_list :   # act数据格式：（'a1','a2'）e.g. ('c1',)
                if len(path_action_list)==0:
                    new_path_action_list.append([[i for i in act]])
                else:
                    for path in path_action_list:
                        new_path_action_list.append([*path,[i for i in act]])
            path_action_list=new_path_action_list.copy() # 格式：[[['并行动作集1'], ['并行动作集2']]]
        return path_action_list[0]    # [['c1'], ['d3', 'd2']]

    def poset_language_shorter(self):   # 对每个poset的language进行评估，然后根据评估值进行升序排列
        log_evaluater=[]
        evaluater=[]
        for i in range(len(self.language_list)):    # self.language_list中记录的是每个poset对应的language中word数量的负数
            if not self.language_list[i]==0:
                evaluater.append(-self.language_list[i]/np.math.factorial(len(self.poset_list[i]['action_map'])))   # math.factorial返回后面数字的阶乘结果：n*(n-1)*...*1
                #log_evaluater.append(np.math.log(np.math.factorial(len(self.poset_list[i]['action_map'])),-self.language_list[i])/
                       #len(self.poset_list[i]['action_map']))
            else:
                evaluater.append(-1)
                #log_evaluater.append(-1)
        #log_evaluater=[np.math.log(np.math.factorial(len(self.poset_list[i]['action_map'])),-self.language_list[i])/
                       #len(self.poset_list[i]['action_map']) for i in range(len(self.language_list)) ]
        #evaluater=[-self.language_list[i]/np.math.factorial(len(self.poset_list[i]['action_map'])) for i in range(len(self.language_list)) ]
        evaluater_sorter=sorted(range(len(self.language_list)),key=lambda k:evaluater[k])   # 根据evaluater列表的值对language的index进行升序排列
        self.poset_list=[self.poset_list[i] for i in evaluater_sorter]

    def get_next_state(self,pre_state,action):
        state_list=[]
        for suf_state in self.new_buchi.successors(pre_state):
            if self.new_buchi[pre_state][suf_state]['guard_formula']==action:
                state_list.append(suf_state)
        return state_list


    def find_all_paths(self, graph,start, ends):
        """
        Finds all paths between nodes start and end in graph.
        Returns:
        A list of paths (node index lists) between start and end node
        """
        #print('start',list(start))
        #print('end',list(end))
        path = []
        paths = []
        queue = [(start, path)]
        while queue:
            start, path = queue.pop()
            #print('PATH', path)
            path = path + [start]
            #print('PATH after adding start ', path)
            if start in ends:
                #print('end')
                paths.append(path)
            for node in set(graph.neighbors(start)).difference(path):
                if not node in path:
                    queue.append((node, path))
            #print('queue', queue)
        return paths

    def find_all_circles(self,graph,starts):
        #print(start)
        paths=[]
        for start in starts:
            nodes=graph.neighbors(start)
            #print(nodes)
            for node in nodes:
                path2=self.find_all_paths(graph,node,start)
                for path in path2:
                    paths.append(path)
        return paths

    def find_one_path(self,graph,start,end):
        path = []
        paths = []
        queue = [(start, path)]
        while queue:
            start, path = queue.pop()
            #print('PATH', path)
            path = path + [start]
            #print('PATH after adding start ', path)
            if start == end:
                #print('end')
                paths.append(path)
                if len(paths)>=2:
                    return 1
            for node in set(graph.neighbors(start)).difference(path):
                queue.append((node, path))
            #print('queue', queue)
        return 0

    def delete_the_unfeasible_edges(self,with_label=['||']):
        unfeasible_edges=[]
        for edge in self.new_buchi.edges:
            a=0
            for label in with_label:
                if label in self.new_buchi.edges[edge]['guard_formula']:
                    a=1
            if a==1:
                unfeasible_edges.append(edge)
        for edge in unfeasible_edges:
            self.new_buchi.remove_edge(edge)


    @property
    def buchi(self):
        return self._buchi

    @property
    def prefix_path(self):
        return  self._prefix_path

    @property
    def suffix_path(self):
        return self._suffix_path

    @property
    def new_buchi(self):
        return self._new_buchi