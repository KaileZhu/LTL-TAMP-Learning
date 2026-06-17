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
    def __init__(self,poset,task_data,input_data):
                 #agent_data,task_data,task_type,sub_task_type,agent_type):
        self.poset=poset
        self.position=input_data.position
        self.agent_data=input_data.agent_data
        self.task_data=task_data
        self.task_type=input_data.task_type
        self.sub_task_type=input_data.sub_task_type
        self.agent_type=input_data.agent_type
        self.Astar_table=[]
        self.get_horizon()
        self.explored_node_dic={}
        self.generate_poset_graph()


    def Begin_branch_search_online(self,time_limit,extro_constrain,assigned_task):
        #here rebuild the time table
        self.generate_time_budget()
        root_node=[[] for agent in self.agent_data]#(solution,assigned_task)
        #up_bound,solution=self.get_upper_bound_online(root_node,assigned_task,extro_constrain)
        up_bound,solution=self.get_upper_bound_online(root_node,assigned_task,extro_constrain)
        self.branch_tree=[(root_node,assigned_task)]
        self.search_node_list={}
        self.search_node_list[tuple(assigned_task)]=[root_node]
        self.best_solution=solution
        self.best_up_bound=up_bound
        self.max_low_bound=0
        start=time.time()
        while (not self.branch_tree==[]) and time.time()-start<time_limit:
            #print('check a branch')
            node,task=self.branch_tree.pop()
            #label_to_update_best_solution=0
            if tuple(task) in self.search_node_list.keys():
                if node not in self.search_node_list[tuple(task)]:
                    self.search_node_list[tuple(task)].append(node)
                    low_bound=self.get_lower_bound_online(node,task,extro_constrain)
                    if low_bound<self.best_up_bound:
                        child_nodes=self.exten_child_nodes_online(node,task)
                        self.branch_tree.extend(child_nodes)
                        up_bound,solution=self.get_upper_bound_online(node,task,extro_constrain)
                        if up_bound<self.best_up_bound:
                            #label_to_update_best_solution=1
                            self.best_solution=solution
                            self.best_up_bound=up_bound
                else:
                    child_nodes=self.exten_child_nodes_online(node,task)
                    self.branch_tree.extend(child_nodes)
            else:
                self.search_node_list[tuple(task)]=[node]
                low_bound=self.get_lower_bound_online(node,task,extro_constrain)
                if low_bound<self.best_up_bound:
                    child_nodes=self.exten_child_nodes_online(node,task)
                    self.branch_tree.extend(child_nodes)
                    up_bound,solution=self.get_upper_bound_online(node,task,extro_constrain)
                    if up_bound<self.best_up_bound:
                        self.best_solution=solution
                        self.best_up_bound=up_bound
            #print('new branch up bound is',self.best_up_bound)
            #if label_to_update_best_solution:
                #self.prune_tree()
        self.print_answer()
        self.get_time_table_of_best_solution_online(self.best_solution,extro_constrain)# remain to update

    def Begin_branch_search2(self,time_limit,up_bound_method=1,low_bound_method=1,search_method='DFS'):
        start = time.time()
        self.generate_time_budget()
        root_node=[[] for i in self.agent_data]#(solution,assigned_task)
        assigned_tasks=[]
        self.get_lower_bound(low_bound_method)
        self.count_round=1
        up_bound,solution=self.get_upper_bound(root_node,assigned_tasks,'slowly')
        #up_bound,solution=self.get_upper_bound(root_node,assigned_tasks,up_bound_method)
        #if up_bound<2400:
         #   print(up_bound)
          #  return 0
        self.upper_bound_list={}
        self.upper_bound_list[self.count_round] = (up_bound, time.time() - start)
        #low_bound=self.get_lower_bound_method(root_node,assigned_tasks)
        self.branch_tree=[(root_node,assigned_tasks)]
        self.search_node_list={}
        self.search_node_list[tuple(assigned_tasks)]=[root_node]
        self.best_solution=solution
        self.best_up_bound=up_bound
        self.max_low_bound=0
        #give a count for the bnb method to get a better solution
        # get upper bound with time
        # get lower bound with time/round
        # both time and round
        self.low_bound_list={}
        #each time explore a node, we say count_round+1
        self.best_up_bound_list={}
        self.best_up_bound_list[self.count_round]=(up_bound,time.time()-start)
        self.astar_list_in_tree=[up_bound]
        while (not self.branch_tree==[]) and time.time()-start<time_limit:
            #print('check a branch')
            #node fetch step
            #===============
            #node fetching is good enough i think
            popi = self.astar_list_in_tree.index(max(self.astar_list_in_tree))
            node,task=self.branch_tree.pop(popi)
            node_up_bound=self.astar_list_in_tree.pop(popi)
            #=========================
            #this method is bad
            #node_up_bound=self.astar_list_in_tree.pop()
            #node,task=self.branch_tree.pop()
            self.count_round=self.count_round+1
            #-------------------
        #child_nodes=self.branching_routine(search_method)
            if tuple(task) in self.search_node_list.keys():
                if node not in self.search_node_list[tuple(task)]:
                    self.search_node_list[tuple(task)].append(node)
                    low_bound=self.get_lower_bound_method(node,task)
                    if low_bound<self.best_up_bound:
                        self.low_bound_list[self.count_round]=(low_bound,time.time()-start,'explore')
                        child_nodes=self.exten_child_nodes(node,task)

                        self.branch_tree.extend(child_nodes)
                        self.astar_list_in_tree.extend(self.estimate_Astar_value(child_nodes,node_up_bound))
                        up_bound,solution=self.get_upper_bound(node,task,up_bound_method)
                        self.upper_bound_list[self.count_round]=(up_bound,time.time()-start)
                        if up_bound+1<low_bound:
                            s=1
                        if up_bound<self.best_up_bound:
                            self.best_solution=solution
                            self.best_up_bound=up_bound
                            self.best_up_bound_list[self.count_round]=(self.best_up_bound,time.time()-start)
                    else:
                        self.low_bound_list[self.count_round]=(low_bound,time.time()-start,'cut')
                        self.upper_bound_list[self.count_round]=(self.best_up_bound,time.time()-start)
                else:
                    child_nodes=self.exten_child_nodes(node,task)
                    self.branch_tree.extend(child_nodes)
                    self.astar_list_in_tree.extend(self.estimate_Astar_value(child_nodes, node_up_bound))
                    #self.astar_list_in_tree.extend([node_up_bound for node in child_nodes])
            else:
                self.search_node_list[tuple(task)]=[node]
                low_bound=self.get_lower_bound_method(node,task)#xiajie is error ?
                if low_bound<self.best_up_bound:
                    self.low_bound_list[self.count_round]=(low_bound,time.time()-start,'explore')
                    child_nodes=self.exten_child_nodes(node,task)
                    #self.astar_list_in_tree.extend([node_up_bound for node in child_nodes])
                    self.astar_list_in_tree.extend(self.estimate_Astar_value(child_nodes, node_up_bound))
                    self.branch_tree.extend(child_nodes)
                    up_bound,solution=self.get_upper_bound(node,task,up_bound_method)
                    self.upper_bound_list[self.count_round] = (up_bound, time.time() - start)
                    #self.branch_tree.append((node,task,up_bound,low_bound))
                    if up_bound<self.best_up_bound:
                        self.best_solution=solution
                        self.best_up_bound=up_bound
                        self.best_up_bound_list[self.count_round] = (self.best_up_bound, time.time() - start)
                else:
                    self.low_bound_list[self.count_round]=(low_bound,time.time()-start,'cut')
                    self.upper_bound_list[self.count_round] = (self.best_up_bound, time.time() - start)
            print('new branch up bound is',self.best_up_bound)

        self.print_answer()
        self.get_time_table_of_best_solution(self.best_solution)


    def estimate_Astar_value(self,node_list,upper_bound):
        Astar_list=[]
        for node,task in node_list:
            t2=0
            execute_time=0
            for i in task:
                execute_num = 0
                for n in self.task_type[self.task_data[i][1]][1].values():
                    execute_num = execute_num + n
                t2 = t2 + self.task_type[self.task_data[i][1]][0] * execute_num
            Astar_list.append(t2/upper_bound/len(self.agent_data))
        return Astar_list

    def get_upper_bound_online(self,init_node,assigned_task,extro_constrain):
        if len(assigned_task) ==len(self.task_data):
            t,time_list,_=self.opt_for_partial_assigment_online(init_node,assigned_task,extro_constrain)


            return  max(time_list),init_node
        un_found=1
        sample_list=[]
        assigned_tasks=[task[0] for task in assigned_task]
        while un_found>0:
            #================
            assiged_task_set=set()
            to_assig_task=set(self.poset_graph.succ['root'])
            for task in assigned_tasks:
                assiged_task_set.add(task)
                to_assig_task=to_assig_task|set(self.poset_graph.succ[task])
            un_assig_task1=to_assig_task-assiged_task_set
            un_assig_task=copy.deepcopy(un_assig_task1)
            for i in un_assig_task1:
                #check if pre_task is satisfied
                if not len(set(self.poset_graph.pred[i])-assiged_task_set-{'root'})==0:
                    un_assig_task.remove(i)
            to_assig_task = random.sample( un_assig_task,1)
            #get feasible assig_task
            assigned_tasks.extend(to_assig_task)
            sub_task_list=self.task_type[self.task_data[to_assig_task[0]][1]][1]
            feasible={}
            for sub_task,num in sub_task_list.items():
                list_n=[]
                for agent_i in self.agent_data:
                    if sub_task in self.agent_type[agent_i[2]]['serve']:
                        list_n.append(agent_i[0])
                feasible[sub_task]=(list_n,num)
            #=====================get task distribution
                #new_node=copy.deepcopy(init_node)
            assign_list_set=[]
            #get n round assignment
            for i in range(3):
                while 1:
                    assign_list={}
                    check_list=[]
                    for sub_task,(list_n,num) in feasible.items():
                        assign_list[sub_task]=random.sample(list_n,num)
                        check_list.extend(assign_list[sub_task])
                        repet_Num=Counter(check_list)
                    if len(repet_Num)==len(check_list):
                        break
                assign_list_set.append(assign_list)
            #print('assign_list',assign_list)
            time_list=[]
            node_list=[]
            #assign and calculate the task
            for assign_list in assign_list_set:
                new_node=copy.deepcopy(init_node)
                for sub_task,samb in assign_list.items():
                    for agent_i in samb:
                        new_node[agent_i].append((tuple(self.task_data[to_assig_task[0]]),sub_task))
                node_list.append(new_node)
                if len(assigned_tasks)==len(self.task_data):
                    sample_list.append(new_node)
                    un_found=un_found-1
                unfinished_assigned_task=list(set(assigned_tasks).intersection(set(extro_constrain.task_dic.keys())))
                unfinished_assigned_task_list=[]
                for i in unfinished_assigned_task:
                    unfinished_assigned_task_list.append(tuple(self.task_data[i]))
                t,time_list_i,dic_t=self.opt_for_partial_assigment_online(new_node,unfinished_assigned_task_list,extro_constrain)
                time_list.append(t)
            if len(time_list)==0:
                s=1
            l=time_list.index(min(time_list))
            init_node=node_list[l]
        finished_time_list=[time for task,time in extro_constrain.finished_time_list.items()]
        finished_time_list.append(min(time_list))
        #time_list=[]
        if sample_list==[]:
            return self.horizon,[]
        else:
            return max(finished_time_list),init_node

    def get_upper_bound(self,node,assigned_tasks,up_bound_method):
        if up_bound_method=='greedy':#should be finished
            up_bound,solution=self.found_solution_greedy(node,assigned_tasks)
            #modified upper bound
            up_bound=self.modified_upper_bound(solution)
            #print('get up_bound',up_bound)
            return up_bound,solution

        elif up_bound_method=='slowly':
            up_bound, solution = self.found_solution_greedy2(node, assigned_tasks)
            # print('get up_bound',up_bound)
            return up_bound, solution
        else:
            raise Exception('Undefined up bound method')
            return up_bound,solution

    def modified_upper_bound(self,solution):
        t, end_time = self.opt_for_partial_assigment(solution, range(len(self.task_data)))
        if t>5000:
            return t
        modified_time_list=[]
        agent_id=0
        for agent in solution:
            if len(agent)>=2:
                t_end=end_time[agent[-1][0][0]]
                distance=self.get_distance(agent[0][0][2],agent[-1][0][2])
                delte_t=distance/self.agent_type[self.agent_data[agent_id][2]]['velocity']
                modified_time_list.append(t_end+delte_t)
            agent_id=agent_id+1
        modified_time_list.extend(end_time)
        print(modified_time_list)
        return max(modified_time_list)

    def found_solution_greedy(self,init_node,assigned_tasks,repeat_number=1):
        '''
        input: init_node, assigned_tasks
        output: upper_bound, solution

        '''
        #print('assigned_task',assigned_tasks)
        if not len(assigned_tasks)==0:
            t,_=self.opt_for_partial_assigment(init_node,assigned_tasks)
        else:
            t=0
        t2=0
        for i in assigned_tasks:
            execute_num = 0
            for n in self.task_type[self.task_data[i][1]][1].values():
                execute_num = execute_num + n
            t2 = t2 + self.task_type[self.task_data[i][1]][0] * execute_num
            #t2=t2+self.task_type[self.task_data[i][1]][0]
        if t<=0.01:
            tstar=1
        else:
            tstar=t2/t/len(self.agent_data)
        sequence = [(set(assigned_tasks), init_node)]
        sequence_t=[tstar]
        un_found=1
        sample_list=[]
        while sequence!=[] and un_found>0:
            popi=sequence_t.index(max(sequence_t))
            root_node=sequence.pop(popi)
            t_label=sequence_t.pop(popi)
            assiged_task=root_node[0]
            init_node=root_node[1]
            #================get to assign task
            assiged_task_set=set()
            to_assig_task=set(self.poset_graph.succ['root'])
            for task in assiged_task:
                assiged_task_set.add(task)
                to_assig_task=to_assig_task|set(self.poset_graph.succ[task])
            un_assig_task1=to_assig_task-assiged_task_set
            un_assig_task=copy.deepcopy(un_assig_task1)
            for i in un_assig_task1:
                if not len(set(self.poset_graph.pred[i])-assiged_task_set-{'root'})==0:
                    un_assig_task.remove(i)
            #-===== already get feasible assgin task
            sequence=[]
            sequence_t=[]
            for to_assig_task in un_assig_task:
                new_assiged_task=assiged_task |{to_assig_task}
                #print(self.task_type.keys())
                sub_task_list=self.task_type[self.task_data[to_assig_task][1]][1]
                feasible={}
                for sub_task,num in sub_task_list.items():
                    list=[]
                    for agent_i in self.agent_data:
                        if sub_task in self.agent_type[agent_i[2]]['serve']:
                            list.append(agent_i[0])
                    feasible[sub_task]=(list,num)
            #=====================get task distribution
                #new_node=copy.deepcopy(init_node)
                #here need to consider how many here seems only once?.
                #get a serious assignmnet
                #if self.count_round>20:
                #    repeat_number=self.count_round//10%5
                #repeat_number=3
                for z in range(repeat_number):
                    new_node=copy.deepcopy(init_node)
                    while 1:
                        assign_list={}
                        check_list=[]
                        for sub_task,(list,num) in feasible.items():
                            assign_list[sub_task]=random.sample(list,num)
                            check_list.extend(assign_list[sub_task])
                            repet_Num=Counter(check_list)
                        if len(repet_Num)==len(check_list):
                            break
                    #print('assign_list',assign_list)
                    for sub_task,samb in assign_list.items():
                        for agent_i in samb:
                            new_node[agent_i].append((self.task_data[to_assig_task],sub_task))
                    #calculate t *
                    if len(new_assiged_task)==len(self.task_data):
                        sample_list.append(new_node)
                        un_found=un_found-1
                    else:
                        sequence.append((new_assiged_task,new_node))
                        t,_=self.opt_for_partial_assigment(new_node,new_assiged_task)
                        #print('time',t)
                        t2=0
                        for i in new_assiged_task:
                            execute_num=0
                            for n in self.task_type[self.task_data[i][1]][1].values():
                                execute_num=execute_num+n
                            t2=t2+self.task_type[self.task_data[i][1]][0]*execute_num
                            #t2=t2+self.task_type[self.task_data[i][1]][0]
                        if t<=0.1:
                            tstar=1
                        else:
                            tstar=t2/t/len(self.agent_data)
                        sequence_t.append(tstar)
        time_list=[]
        if sample_list==[]:
            return self.horizon,[]
        else:
            for node in sample_list:
                a,b=self.opt_for_partial_assigment(node,range(len(self.task_data)))
                time_list.append(a)
            solution=sample_list[time_list.index(min(time_list))]
            return min(time_list),solution

    def found_solution_greedy2(self,init_node,assigned_tasks):
        #print('assigned_task',assigned_tasks)
        if not len(assigned_tasks)==0:
            t,_=self.opt_for_partial_assigment(init_node,assigned_tasks)
        else:
            t=0
        t2=0
        for i in assigned_tasks:
            t2=t2+self.task_type[self.task_data[i][1]][0]
        if t<=0.1:
            tstar=1
        else:
            tstar=t2/t/len(self.agent_data)
        sequence = [(set(assigned_tasks), init_node)]
        sequence_t=[tstar]
        un_found=1
        sample_list=[]
        while sequence!=[] and un_found>0:
            popi=sequence_t.index(min(sequence_t))
            root_node=sequence.pop(popi)
            t_label=sequence_t.pop(popi)
            assiged_task=root_node[0]
            init_node=root_node[1]
            #================
            assiged_task_set=set()
            to_assig_task=set(self.poset_graph.succ['root'])
            for task in assiged_task:
                assiged_task_set.add(task)
                to_assig_task=to_assig_task|set(self.poset_graph.succ[task])
            un_assig_task1=to_assig_task-assiged_task_set
            un_assig_task=copy.deepcopy(un_assig_task1)
            for i in un_assig_task1:
                if not len(set(self.poset_graph.pred[i])-assiged_task_set-{'root'})==0:
                    un_assig_task.remove(i)
            #print('unassig:',un_assig_task)
            #print('assig:',assiged_task)
            sequence = []
            sequence_t = []
            for to_assig_task in un_assig_task:
                new_assiged_task=assiged_task |{to_assig_task}
                #print(self.task_type.keys())
                sub_task_list=self.task_type[self.task_data[to_assig_task][1]][1]
                feasible={}
                for sub_task,num in sub_task_list.items():
                    list=[]
                    for agent_i in self.agent_data:
                        if sub_task in self.agent_type[agent_i[2]]['serve']:
                            list.append(agent_i[0])
                    feasible[sub_task]=(list,num)
            #=====================get task distribution
                new_node=copy.deepcopy(init_node)
                while 1:
                    assign_list={}
                    check_list=[]
                    for sub_task,(list,num) in feasible.items():
                        assign_list[sub_task]=random.sample(list,num)
                        check_list.extend(assign_list[sub_task])
                        repet_Num=Counter(check_list)
                    if len(repet_Num)==len(check_list):
                        break
                #print('assign_list',assign_list)
                for sub_task,samb in assign_list.items():
                    for agent_i in samb:
                        new_node[agent_i].append((self.task_data[to_assig_task],sub_task))
                if len(new_assiged_task)==len(self.task_data):
                    sample_list.append(new_node)
                    un_found=un_found-1
                else:
                    sequence.append((new_assiged_task,new_node))
                    t,_=self.opt_for_partial_assigment(new_node,new_assiged_task)
                    #print('time',t)
                    t2=0
                    for i in new_assiged_task:
                        t2=t2+self.task_type[self.task_data[i][1]][0]
                    if t<=0.1:
                        tstar=1
                    else:
                        tstar=t2/t/len(self.agent_data)
                    sequence_t.append(tstar)
        time_list=[]
        if sample_list==[]:
            return self.horizon,[]
        else:
            for node in sample_list:
                a,b=self.opt_for_partial_assigment(node,range(len(self.task_data)))
                time_list.append(a)
            solution=sample_list[time_list.index(min(time_list))]
            return min(time_list),solution


    def generate_poset_graph(self):
        poset_graph=nx.DiGraph()
        for i,j in self.poset['<']:
            poset_graph.add_edge(i,j)
        for i,j in self.poset['<=']:
            poset_graph.add_edge(i,j)
        for i in range(len(self.task_data)):
            if not poset_graph.has_node(i):
                poset_graph.add_node(i)
        new_poset_graph=copy.deepcopy(poset_graph)
        self.poset_graph=poset_graph
        remove_list=[]
        for i,j in poset_graph.edges:
            removable_label=self.find_path(i,j)
            if removable_label:
                remove_list.append((i,j))
        for i,j in remove_list:
            self.poset_graph.remove_edge(i,j)
        node_set=[]
        for i in self.poset_graph.nodes:
            if len(self.poset_graph.pred[i])==0:
                node_set.append(i)
        for i in node_set:
            self.poset_graph.add_edge('root',i)


    def get_time_table_of_best_solution(self,solution):
        task_time_cost_list=[self.task_type[task[1]][0] for task in self.task_data]
        t,end_time=self.opt_for_partial_assigment(solution,range(len(self.task_data)))
        self.task_time_table=[[i,end_time[i][0]-task_time_cost_list[i],end_time[i][0]] for i in range(len(self.task_data))]

    def get_time_table_of_best_solution_online(self,solution,extron_constrain):
        full_assigned_Task=set()
        for task in self.task_data:
            if task[0] not in extron_constrain.finished_time_list.keys():
                full_assigned_Task.add(task)
        max_time,end_time,task_dic=self.opt_for_partial_assigment_online(solution,full_assigned_Task,extron_constrain)
        self.task_time_table=[]
        for i in range(len(self.task_data)):
            if i in task_dic.keys():
                self.task_time_table.append([i,end_time[task_dic[i]][0]-extron_constrain.task_execute_time[i],end_time[task_dic[i]][0]])
            else:
                self.task_time_table.append([i,extron_constrain.finished_time_list[i]-extron_constrain.task_execute_time[i],extron_constrain.finished_time_list[i]])



    def find_path(self,start,end):
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
            for node in set(self.poset_graph.neighbors(start)).difference(path):
                queue.append((node, path))
            #print('queue', queue)
        if len(paths)>=2:
            removable_label=1
            return removable_label
        else:
            removable_label=0
            return removable_label

    def get_lower_bound(self,low_bound_method):
        if low_bound_method=='i_j':
            self.get_lower_bound_method=self.get_lower_bound_with_i_j
        if low_bound_method=='i+j':
            self.get_lower_bound_method=self.get_lower_bound_with_i_add_j
        #low_bound1=self.get_lower_bound_with_i_j_k_faster(node,assigned_tasks)
        #return  low_bound1

    def get_lower_bound_online2(self,node,assigned_tasks,extro_constrain):

        assigned_tasks_2=copy.deepcopy(assigned_tasks)
        for task in assigned_tasks:
            if task[0] in extro_constrain.finished_time_list.keys():
                assigned_tasks_2.remove(task)
        t,time_list,assigned_task_dic=self.opt_for_partial_assigment_online(node,assigned_tasks_2,extro_constrain)
        unassigned_tasks=list(range(len(self.task_data)))
        for i in assigned_tasks:
            unassigned_tasks.remove(i[0])
        task_number=len(unassigned_tasks)
        #task_dic=assigned_task_dic
        finished_time_list=copy.deepcopy(extro_constrain.finished_time_list)
        for task,num in assigned_task_dic.items():
            finished_time_list[task]=time_list[num][0]
        z=0
        task_dic={}
        for i in unassigned_tasks:
            task_dic[i]=z
            z=z+1
        if task_number==0:
            t,time_list,_=self.opt_for_partial_assigment_online(node,assigned_tasks,extro_constrain)
            return max(time_list)
        agent_number=len(self.agent_data)
        t_j=cp.Variable(shape=(task_number,1),boolean=True)
        t_i=cp.Variable(shape=(agent_number,1),nonneg=True)
        total_constrain=[]
        new_task_time_set={}
        for task_j in task_dic.keys():
            time_table=[]
            for agent in self.agent_data:
                x1=self.position[self.task_data[task_j][2]]
                x2=extro_constrain.agent_pose[agent[0]]
                time=((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)**0.5/self.agent_type[agent[2]]['velocity']
                time_table.append(time)
            for task in task_dic.keys():
                if not task==task_j:
                    time=self.get_distance(self.task_data[task_j][2],self.task_data[task][2])/10
                    time_table.append(time)
            new_task_time=extro_constrain.task_execute_time[task_j]+min(time_table)
            new_task_time_set[task_j]=new_task_time
        M_time=[[0  for i in range(agent_number)] for j in range(agent_number * task_number)]
        b_time=[[0] for j in range(agent_number)]

        for agent_i in range(agent_number):
        #for begin_time in extro_constrain.begin_time_list:
            for task_j in task_dic.keys():
                num=agent_i*task_number+task_dic[task_j]
                M_time[num][agent_i]=-new_task_time_set[task_j]
                self.task_data[task_j][0]
            b_time[agent_i][0]=extro_constrain.begin_time[agent_i]
        constrain_begin_time=[M_time @ x_i_j + t_i >= b_time]
        total_constrain.append(*constrain_begin_time)
        #constrain_begin_time=[M_time @ t_i >= b_time]
        # ================provide enough serves for the task j (2)
        M1=[[0 for i in range(task_number)] for j in range(agent_number*task_number)]
        b1=[[0 for i in range(task_number)]]
        #z=0
        for task_j in task_dic.keys():
            task_subs=self.task_type[self.task_data[task_j][1]][1]
            b=0
            for sub,num in task_subs.items():
                b=b+num
            b1[0][task_dic[task_j]]=b
            for agent_i in range(agent_number):
                num=agent_i*task_number+task_dic[task_j]
                M1[num][task_dic[task_j]]=1
        enough_constrain=[M1 @ x_i_j == b1]
        total_constrain.append(*enough_constrain)
        #=============partial node constrain
    #================= minium motion
        new_task_time_set={}
        for task_j in task_dic.keys():
            time_table=[]
            for agent in self.agent_data:
                time=self.get_distance(self.task_data[task_j][2],agent[1])/self.agent_type[agent[2]]['velocity']
                time_table.append(time)
            for task in self.task_data:
                time=self.get_distance(self.task_data[task_j][2],self.task_data[task[0]][2])/2
                time_table.append(time)
            new_task_time=self.task_type[self.task_data[task_j][1]][0]+min(time_table)
            new_task_time_set[task_j]=new_task_time
        M5=[]
        T5=[]
        for agent_i in range(len(self.agent_data)):
            t=[0 for o in range(agent_number)]
            t[agent_i]=1
            m=[0 for o in range(agent_number*task_number)]
            for task_j in task_dic.keys():
                num=agent_i*task_number+task_dic[task_j]

                m[num]=-new_task_time_set[task_j]
            #print(m)
            M5.append(m)
            T5.append(t)
        M51=self.Turn_Matrix(M5)
        #T51=self.Turn_Matrix(T5)
        b=[[extro_constrain.begin_time[i]] for i in range(agent_number)]
        #[M51 @ x_i_j]
        #[T5 @ t_i]
        constrain5=[M51 @ x_i_j+T5 @ t_i >=b]
        total_constrain.append(*constrain5)
        obj_1 = cp.Minimize(cp.max(t_i))

        prob_1=cp.Problem(obj_1,total_constrain)
        #solver: GLPK_MI CBC SCIP
        prob_1.solve(solver='GLPK_MI')

        #print('low bound:',prob_1.value)
        if prob_1.status=='optimal':
            return prob_1.value
        else:
            return 0

    def get_lower_bound_online(self,node,assigned_tasks,extro_constrain):
        #here the lower bound seems to be error
        assigned_tasks_2=copy.deepcopy(assigned_tasks)
        for task in assigned_tasks:
            if task[0] in extro_constrain.finished_time_list.keys():
                assigned_tasks_2.remove(task)
        #get new assigned tasks
        #t,time_list,assigned_task_dic=self.opt_for_partial_assigment_online(node,assigned_tasks_2,extro_constrain)
        unassigned_tasks=list(range(len(self.task_data)))
        for i in assigned_tasks:
            unassigned_tasks.remove(i[0])
        task_number=len(unassigned_tasks)
        #task_dic=assigned_task_dic
        #finished_time_list=copy.deepcopy(extro_constrain.finished_time_list)
        #for task,num in assigned_task_dic.items():
        #    finished_time_list[task]=time_list[num][0]
        z=0
        task_dic={}
        for i in unassigned_tasks:
            task_dic[i]=z
            z=z+1
        if task_number==0:
            t,time_list,_=self.opt_for_partial_assigment_online(node,assigned_tasks,extro_constrain)
            return max(time_list)
        agent_number=len(self.agent_data)
        x_i_j=cp.Variable(shape=(agent_number*task_number,1),boolean=True)
        t_i=cp.Variable(shape=(agent_number,1),nonneg=True)
        total_constrain=[]
        new_task_time_set={}
        for task_j in task_dic.keys():
            time_table=[]
            for agent in self.agent_data:
                x1=self.position[self.task_data[task_j][2]]
                x2=extro_constrain.agent_pose[agent[0]]
                time=((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)**0.5/self.agent_type[agent[2]]['velocity']
                time_table.append(time)
            for task in task_dic.keys():
                if not task==task_j:
                    time=self.get_distance(self.task_data[task_j][2],self.task_data[task][2])/10
                    time_table.append(time)
            new_task_time=extro_constrain.task_execute_time[task_j]+min(time_table)
            new_task_time_set[task_j]=new_task_time
        #constrain 1
        M_time=[[0  for i in range(agent_number)] for j in range(agent_number * task_number)]
        b_time=[[extro_constrain.begin_time[j] for j in range(agent_number)]]
        for agent_i in extro_constrain.broken_agent_list:
            b_time[0][agent_i]=0
        T_time=[]
        for agent_i in range(agent_number):
            t=[0 for o in range(agent_number)]
            t[agent_i]=1
        #for begin_time in extro_constrain.begin_time_list:
            for task_j in task_dic.keys():
                num=agent_i*task_number+task_dic[task_j]
                M_time[num][agent_i]=-new_task_time_set[task_j]
            T_time.append((t))
        constrain_begin_time=[M_time @ x_i_j + T_time @ t_i >= b_time]
        total_constrain.append(*constrain_begin_time)
        #constrain_begin_time=[M_time @ t_i >= b_time]
        # ================provide enough serves for the task j (2)
        M1=[[0 for i in range(task_number)] for j in range(agent_number*task_number)]
        b1=[[0 for i in range(task_number)]]
        #z=0
        for task_j in task_dic.keys():
            task_subs=self.task_type[self.task_data[task_j][1]][1]
            b=0
            for sub,num in task_subs.items():
                b=b+num
            b1[0][task_dic[task_j]]=b
            for agent_i in range(agent_number):
                num=agent_i*task_number+task_dic[task_j]
                M1[num][task_dic[task_j]]=1
        enough_constrain=[M1 @ x_i_j == b1]
        total_constrain.append(*enough_constrain)
        #broken constrain
        M2=[[0 for i in range(len(extro_constrain.broken_agent_list))] for j in range(agent_number*task_number)]
        b2=[[0 for i in range(len(extro_constrain.broken_agent_list))]]
        #z=0
        broken_agent_dic={}
        for i in range(len(extro_constrain.broken_agent_list)):
            broken_agent_dic[extro_constrain.broken_agent_list[i]]=i
        for task_j in task_dic.keys():
            for agent_i in extro_constrain.broken_agent_list:
                num=agent_i*task_number+task_dic[task_j]
                M2[num][broken_agent_dic[agent_i]]=1
        broken_agent_constrain=[M2 @ x_i_j == b2]
        total_constrain.append(*broken_agent_constrain)
        obj_1 = cp.Minimize(cp.max(t_i))
        prob_1=cp.Problem(obj_1,total_constrain)
        #solver: GLPK_MI CBC SCIP
        prob_1.solve(solver='GLPK_MI')

        #print('low bound:',prob_1.value)
        if prob_1.status=='optimal':
            return prob_1.value
        else:
            return 0

    def get_lower_bound_online_i_add_j(self,node,assigned_tasks,extro_constrain):
        assigned_tasks_2=copy.deepcopy(assigned_tasks)
        for task in assigned_tasks:
            if task[0] in extro_constrain.finished_time_list.keys():
                assigned_tasks_2.remove(task)
        unassigned_tasks=list(range(len(self.task_data)))
        for i in assigned_tasks:
            unassigned_tasks.remove(i[0])
        task_number=len(unassigned_tasks)
        z=0
        task_dic={}
        for i in unassigned_tasks:
            task_dic[i]=z
            z=z+1
        t,time_list,_=self.opt_for_partial_assigment_online(node,assigned_tasks,extro_constrain)
        if task_number==0:
            return max(time_list)
        agent_number=len(self.agent_data)
        t_i = cp.Variable(shape=1, nonneg=True)
        t_j = cp.Variable(shape=(task_number, 1), nonneg=True)
        total_constrain = []
        new_task_time_set = {}
        # begin time constrain
        for task_j in unassigned_tasks:
            time_table = []
            for agent in self.agent_data:
                x1 = self.position[self.task_data[task_j][2]]
                x2 = extro_constrain.agent_pose[agent[0]]
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
        prob_1.solve()
        prob_2 = cp.Problem(obj_2, constrain_t_i)
        # solver: GLPK_MI CBC SCIP
        prob_2.solve()
        value = max(prob_1.value, prob_2.value, max(begin_time_list))
        print('low bound:', value)
        if prob_1.status == 'optimal':
            return prob_1.value
        else:
            return 0

    def prune_tree(self):
        check_node=[[((0, 'goto', 'c'), 'goto')],[((1, 'surround', 'g'), 'surrounder')],[((1, 'surround', 'g'), 'surrounder')],[],[],[]]
        i=0
        to_prune_set=[]
        for root_node,assigned_tasks,up_bound,low_bound in self.branch_tree:
            #if low_bound>=self.best_up_bound:
            #if root_node==check_node:
            #    print('low_bound!!!!',low_bound)
            #    if low_bound>27:
            #        print('error')
            if low_bound+0.1>=self.best_up_bound:
                to_prune_set.append(i)
            i=i+1
        for i in reversed(to_prune_set):
            del self.branch_tree[i]
        print('in this step deleta',len(to_prune_set),'banch')

    def get_lower_bound_with_i_j(self,node,assigned_tasks):
        t,time_list=self.opt_for_partial_assigment(node,assigned_tasks)
        unassigned_tasks=list(range(len(self.task_data)))
        assigned_task_dic={}
        z=0
        for i in assigned_tasks:
            unassigned_tasks.remove(i)
            assigned_task_dic[i]=z
            z=z+1
        task_number=len(unassigned_tasks)
        if task_number==0:
            print('return max time list')
            return max(time_list)
        begin_time_list=[]
        for agent in node:
            if len(agent)==0:
                begin_time_list.append(0)
            else:
                assigned_task_dic[agent[-1][0][0]]
                if np.shape(time_list[assigned_task_dic[agent[-1][0][0]]])==(1,):
                    begin_time_list.append(time_list[assigned_task_dic[agent[-1][0][0]]][0])
                else:
                    begin_time_list.append(time_list[assigned_task_dic[agent[-1][0][0]]])
        #print('begin time list',begin_time_list)
        z=0
        task_dic={}
        for i in unassigned_tasks:
            task_dic[i]=z
            z=z+1
        agent_pose=[]
        for agent in self.agent_data:
            if len(node[agent[0]])==0:
                agent_pose.append(self.position[agent[1]])
            else:
                pos=self.position[node[agent[0]][-1][0][2]]
                agent_pose.append(pos)
        agent_number=len(self.agent_data)
        x_i_j=cp.Variable(shape=(agent_number*task_number,1),boolean=True)
        t_i=cp.Variable(shape=(agent_number,1),nonneg=True)
        total_constrain=[]
        new_task_time_set={}
        # begin time constrain
        for task_j in unassigned_tasks:
            time_table=[]
            for agent in self.agent_data:
                x1=self.position[self.task_data[task_j][2]]
                x2=agent_pose[agent[0]]
                time=((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)**0.5/self.agent_type[agent[2]]['velocity']
                time_table.append(time)
            for task in unassigned_tasks:
                if not task==task_j:
                    time=self.get_distance(self.task_data[task_j][2],self.task_data[task][2])/10
                    time_table.append(time)
            new_task_time=self.task_type[self.task_data[task_j][1]][0]+min(time_table)
            new_task_time_set[task_j]=new_task_time
        self.new_task_time_set=new_task_time_set
        M_time=[[0  for i in range(agent_number)] for j in range(agent_number * task_number)]
        b_time=[[begin_time_list[j] for j in range(agent_number)]]
        T_time=[]
        for agent_i in range(agent_number):
            t=[0 for o in range(agent_number)]
            t[agent_i]=1
            for task_j in task_dic.keys():
                num=agent_i*task_number+task_dic[task_j]
                M_time[num][agent_i]=-new_task_time_set[task_j]
            T_time.append(t)
        if len(np.shape(b_time))>2:
            s=1
        constrain_begin_time=[M_time @ x_i_j + T_time @ t_i >= b_time]
        total_constrain.append(*constrain_begin_time)

        # ================provide enough serves for the task j (2)
        M1=[[0 for i in range(task_number)] for j in range(agent_number*task_number)]
        b1=[[0 for i in range(task_number)]]
        #z=0
        for task_j in task_dic.keys():
            task_subs=self.task_type[self.task_data[task_j][1]][1]
            b=0
            for sub,num in task_subs.items():
                b=b+num
            b1[0][task_dic[task_j]]=b
            for agent_i in range(agent_number):
                num=agent_i*task_number+task_dic[task_j]
                M1[num][task_dic[task_j]]=1
        enough_constrain=[M1 @ x_i_j == b1]
        total_constrain.append(*enough_constrain)

        obj_1 = cp.Minimize(cp.max(t_i))

        prob_1=cp.Problem(obj_1,total_constrain)
        #solver: GLPK_MI CBC SCIP
        prob_1.solve(solver='GLPK_MI')
        self.x_i_j=x_i_j.value
        self.t_i=t_i.value
        self.constrain=total_constrain
        print('low bound:',prob_1.value)
        if prob_1.status=='optimal':
            return prob_1.value
        else:
            return 0

    def get_lower_bound_with_i_add_j(self,node,assigned_tasks):
        t,time_list=self.opt_for_partial_assigment(node,assigned_tasks)
        unassigned_tasks=list(range(len(self.task_data)))
        assigned_task_dic={}
        z=0
        for i in assigned_tasks:
            unassigned_tasks.remove(i)
            assigned_task_dic[i]=z
            z=z+1
        task_number=len(unassigned_tasks)
        if task_number==0:
            print('return max time list')
            return max(time_list)
        begin_time_list=[]
        for agent in node:
            if len(agent)==0:
                begin_time_list.append(0)
            else:
                if np.shape(time_list[assigned_task_dic[agent[-1][0][0]]])==(1,):
                    begin_time_list.append(time_list[assigned_task_dic[agent[-1][0][0]]][0])
                else:
                    begin_time_list.append(time_list[assigned_task_dic[agent[-1][0][0]]])
        #print('begin time list',begin_time_list)
        z=0
        task_dic={}
        for i in unassigned_tasks:
            task_dic[i]=z
            z=z+1
        agent_pose=[]
        for agent in self.agent_data:
            if len(node[agent[0]])==0:
                agent_pose.append(self.position[agent[1]])
            else:
                pos=self.position[node[agent[0]][-1][0][2]]
                agent_pose.append(pos)
        agent_number=len(self.agent_data)
        t_i=cp.Variable(shape=1,nonneg=True)
        t_j=cp.Variable(shape=(task_number,1),nonneg=True)
        total_constrain=[]
        new_task_time_set={}
        # begin time constrain
        for task_j in unassigned_tasks:
            time_table=[]
            for agent in self.agent_data:
                x1=self.position[self.task_data[task_j][2]]
                x2=agent_pose[agent[0]]
                time=((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)**0.5/self.agent_type[agent[2]]['velocity']
                time_table.append(time)
            for task in unassigned_tasks:
                if not task==task_j:
                    time=self.get_distance(self.task_data[task_j][2],self.task_data[task][2])/10
                    time_table.append(time)
            new_task_time=self.task_type[self.task_data[task_j][1]][0]+min(time_table)
            new_task_time_set[task_j]=new_task_time
        self.new_task_time_set=new_task_time_set
        #poset constrain
        for i,j in self.poset['<=']:
            if (i,j) in self.poset['!='] or (j,i) in self.poset['!=']:
                if not i in task_dic.keys():
                    if j in task_dic.keys():
                        m=[0 for i in range(task_number)]
                        m[task_dic[j]]=1
                        total_constrain.append(m @ t_j >= time_list[assigned_task_dic[i]])
                else:
                    m=[0 for i in range(task_number)]
                    m[task_dic[i]]=-1
                    m[task_dic[j]]=1
                    total_constrain.append(m @ t_j >= new_task_time_set[j])
        # t_j constrain
        #total_constrain.append(*constrain_begin_time)
        unassigned_task_time=0
        #================provide enough serves for the task j (2)
        for task_j in task_dic.keys():
            task_subs=self.task_type[self.task_data[task_j][1]][1]
            b=0
            for sub,num in task_subs.items():
                b=b+num
            unassigned_task_time=unassigned_task_time+b*self.task_type[self.task_data[task_j][1]][0]
        constrain_t_i=[agent_number*t_i-sum(begin_time_list) -unassigned_task_time >=0]


        obj_1 = cp.Minimize(cp.max(t_j))
        obj_2 = cp.Minimize(t_i)
        if not total_constrain==[]:
            prob_1=cp.Problem(obj_1,total_constrain)
        else:
            prob_1=cp.Problem(obj_1)
        prob_1.solve('GLPK_MI')
        prob_2=cp.Problem(obj_2,constrain_t_i)
        #solver: GLPK_MI CBC SCIP
        prob_2.solve('GLPK_MI')
        value=max(prob_1.value,prob_2.value,max(begin_time_list))
        print('low bound:',value)
        return value
        if prob_1.status=='optimal':
            return value
        else:
            return 0

    def exten_child_nodes(self,node,assign_task):
        child_node_list=[]
        assiged_task_set=set()
        to_assig_task=set(self.poset_graph.succ['root'])
        for task in assign_task:
            assiged_task_set.add(task)
            to_assig_task=to_assig_task|set(self.poset_graph.succ[task])
        un_assig_task1=to_assig_task-assiged_task_set
        un_assig_task=copy.deepcopy(un_assig_task1)
        for i in un_assig_task1:
            if not len(set(self.poset_graph.pred[i])-assiged_task_set-{'root'})==0:
                un_assig_task.remove(i)
        to_assig_set=[]
        for task in un_assig_task:
            to_assig_set.append(self.task_data[task])
        for task in to_assig_set:
            assign_task_set=copy.deepcopy(assign_task)
            assign_task_set.append(task[0])
            sub_task_list=[]
            pot_agent_list=[]
            agent_num=0
            for sub_task,num in self.task_type[task[1]][1].items():
                list1=[]
                agent_num=agent_num+num
                for agent_i in self.agent_data:
                    if sub_task in self.agent_type[agent_i[2]]['serve']:
                        list1.append(agent_i[0])
                combina=iter_com(list1,num)
                pot_agent_list.append(list(combina))
                sub_task_list.append(sub_task)
            #print('sub_task_list',sub_task_list)
            agent_list=iter_product(*pot_agent_list)
            for assig_list in agent_list:
                t=[]
                for i in assig_list:
                    t.extend(list(i))
                if len(Counter(t))<agent_num:
                    continue
                child_node=copy.deepcopy(node)
                label=0
                for agent_i in range(len(assig_list)):
                    if label==1:
                        break
                    for i in assig_list[agent_i]:
                        if self.check_poset_in_agent(child_node[i],task):
                            #print('sub_task_agent task',task)
                            child_node[i].append((task,sub_task_list[agent_i]))
                        else:
                            label=1
                            break
                if label==0:
                    assign_task_set_num=[]
                    for task_3 in assign_task_set:
                        assign_task_set_num.append(self.task_data[task_3][0])
                    assign_task_set_num.sort()
                    #print('child_node',child_node)
                    #print('assign_task_set',assign_task_set_num)
                    child_node_list.append((child_node,assign_task_set_num))
        print('extend child nodes',len(child_node_list))
        return  child_node_list

    def exten_child_nodes_online(self,node,assign_task):
        child_node_list=[]
        assiged_task_set=set()
        to_assig_task=set(self.poset_graph.succ['root'])
        for task in assign_task:
            assiged_task_set.add(task[0])
            to_assig_task=to_assig_task|set(self.poset_graph.succ[task[0]])
        un_assig_task1=to_assig_task-assiged_task_set
        un_assig_task=copy.deepcopy(un_assig_task1)
        for i in un_assig_task1:
            if i ==9:
                s=1
            if not len(set(self.poset_graph.pred[i])-assiged_task_set-{'root'})==0:
                un_assig_task.remove(i)
        to_assig_set=[]
        for task in un_assig_task:
            to_assig_set.append(self.task_data[task])
        for task in to_assig_set:
            assign_task_set=copy.deepcopy(assign_task)
            assign_task_set.add(tuple(task))
            sub_task_list=[]
            pot_agent_list=[]
            agent_num=0
            for sub_task,num in self.task_type[task[1]][1].items():
                list1=[]
                agent_num=agent_num+num
                for agent_i in self.agent_data:
                    if sub_task in self.agent_type[agent_i[2]]['serve']:
                        list1.append(agent_i[0])
                combina=iter_com(list1,num)
                pot_agent_list.append(list(combina))
                sub_task_list.append(sub_task)
            #print('sub_task_list',sub_task_list)
            agent_list=iter_product(*pot_agent_list)
            for assig_list in agent_list:
                t=[]
                for i in assig_list:
                    t.extend(list(i))
                if len(Counter(t))<agent_num:
                    continue
                child_node=copy.deepcopy(node)
                for agent_i in range(len(assig_list)):
                    for i in assig_list[agent_i]:
                        child_node[i].append((task,sub_task_list[agent_i]))

                child_node_list.append((child_node,assign_task_set))
        print('extend child nodes',len(child_node_list))
        return  child_node_list

    def check_poset(self,agent,y,task):
        label=1
        if len(agent)>=1:
            for i in agent[:y]:
                if (task[0][0],i[0][0]) in self.poset:
                    label=0
            for i in agent[y:]:
                if (i[0][0],task[0][0]) in self.poset:
                    label=0
        return  label

    def check_poset_in_agent(self,agent,task):
        label=1
        for i in agent:
            if (task,i) in self.poset:
                label=0
        return  label

    def opt_for_partial_assigment(self, node, assign_task, i=None):
        list_node=[]
        for agent in node:
            list_node.append(tuple(agent))
        tuple_node=tuple(list_node)
        assign_task_tuple=tuple(assign_task)
        if assign_task_tuple in self.explored_node_dic.keys():
            if tuple_node in self.explored_node_dic[assign_task_tuple].keys():
                max_end_time_value,end_time_value=self.explored_node_dic[assign_task_tuple][tuple_node]
                return max_end_time_value,end_time_value
        assign_task_dic={}
        t=0
        #print('assign_Task:',assign_task)
        #print(node)
        for i in assign_task:
            assign_task_dic[i]=t
            t=t+1
        end_time=cp.Variable(shape=(len(assign_task),1),name='endtime',nonneg=True)
        total_constrain=[]
        M1=[]
        B1=[[]]
        #for i,j in self.poset['<']:
        for i,j in self.poset['<=']:
            if self.task_data[i][0] in assign_task and self.task_data[j][0] in assign_task:
                if not ((i,j) in self.poset['!='] or (j,i) in self.poset['!=']):
                    #<=
                    m=[0 for l in range(len(assign_task))]
                    m[assign_task_dic[self.task_data[i][0]]]=1
                    m[assign_task_dic[self.task_data[j][0]]]=-1
                    M1.append(m)
                    B1[0].append(-self.task_type[self.task_data[j][1]][0]+self.task_type[self.task_data[i][1]][0])
                else:
                    #<
                    m=[0 for l in range(len(assign_task))]
                    m[assign_task_dic[self.task_data[i][0]]]=1
                    m[assign_task_dic[self.task_data[j][0]]]=-1
                    M1.append(m)
                    B1[0].append(-self.task_type[self.task_data[j][1]][0])
        for i,j in self.poset['=']:
            if self.task_data[i][0] in assign_task and self.task_data[j][0] in assign_task:
                if self.task_type[self.task_data[i][1]][0]>= self.task_type[self.task_data[j][1]][0]:
                    changelabel=-1
                else:
                    changelabel=1
                m=[0 for l in range(len(assign_task))]
                m[assign_task_dic[self.task_data[i][0]]]=changelabel
                m[assign_task_dic[self.task_data[j][0]]]=-changelabel
                M1.append(m)
                B1[0].append(0)
                #might remaining to do!!!!!!!!!!!!!!!
                m=[0 for l in range(len(assign_task))]
                m[assign_task_dic[self.task_data[i][0]]]=-changelabel
                m[assign_task_dic[self.task_data[j][0]]]=changelabel
                M1.append(m)
                B1[0].append( -self.task_type[self.task_data[i][1]][0]*changelabel+self.task_type[self.task_data[j][1]][0]*changelabel)
        for i,j in self.poset['!=']:
            if i in assign_task and j in assign_task:
                if not (i,j) in self.poset['<='] and not (j,i) in self.poset['<=']:
                    m=[[0] for l in range(len(assign_task))]
                    m[assign_task_dic[self.task_data[i][0]]][0]=1
                    m[assign_task_dic[self.task_data[j][0]]][0]=-1
                    bool_for_x=cp.Variable(1,boolean=True)
                    #ei-di - ej  >=0   ti >= ej
                    constrain0=[m @ end_time -self.task_type[self.task_data[i][1]][0] +bool_for_x * self.time_budget-self.time_budget>=0]
                    #ei - ej+ dj  <=0  ei<= tj
                    constrain1=[m @ end_time + self.task_type[self.task_data[j][1]][0] - bool_for_x * self.time_budget <=0]
                    print(1)
                    total_constrain.append(*constrain0)
                    total_constrain.append(*constrain1)
                    #m=[[0] for l in range(len(assign_task))]
                    #m[assign_task_dic[self.task_data[i][0]]][0]=1
                    #m[assign_task_dic[self.task_data[j][0]]][0]=-1
                    #total_constrain.append(cp.abs(
                    #    m @ end_time + (-self.task_type[self.task_data[i][1]][0] + self.task_type[self.task_data[j][1]][0])) \
                    #                       >= (self.task_type[self.task_data[i][1]][0] + self.task_type[self.task_data[j][1]][
                    #    0]) / 2)
            #total_constrain.append(cp.abs(m @ end_time) >=max(self.task_type[self.task_data[i][1]][0],self.task_type[self.task_data[j][1]][0]))
        if not M1==[]:
            M11=self.Turn_Matrix(M1)
            constraint1=[M11 @ end_time <= B1]
            total_constrain.append(*constraint1)
            #print(B1)
        M2=[]
        B2=[[]]
        for agent_i in range(len(self.agent_data)):
            if len(node[agent_i])>0:
                m=[0 for i in range(len(assign_task))]
                #print(assign_task_dic)
                #print(node[agent_i][0][0])
                #print(assign_task_dic)
                c=assign_task_dic[node[agent_i][0][0][0]]
                m[c]=1
                #b=self.get_distance(self.agent_data[agent_i][1],node[agent_i][0][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                #    self.task_type[node[agent_i][0][0][1]][0]
                M2.append(m)
                B2[0].append(self.get_distance(self.agent_data[agent_i][1],node[agent_i][0][0][2])/100000+\
                    self.task_type[node[agent_i][0][0][1]][0])
            if len(node[agent_i])>1:
                for task in range(len(node[agent_i])-1):
                    m=[0 for i in range(len(assign_task))]
                    c=assign_task_dic[node[agent_i][task][0][0]]
                    m[c]=-1
                    c=assign_task_dic[node[agent_i][task+1][0][0]]
                    m[c]=1
                    b=self.get_distance(node[agent_i][task][0][2],node[agent_i][task+1][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                        self.task_type[node[agent_i][task+1][0][1]][0]
                    M2.append(m)
                    B2[0].append((b))
        M21=self.Turn_Matrix(M2)
        constraint2=[M21 @ end_time >= B2]# constraint of poset
        total_constrain.append(*constraint2)
        list1=[[1] for task in assign_task]
        obj = cp.Minimize(list1 @ end_time)
        prob=cp.Problem(obj,total_constrain)
        #prob.solve(solver=cp.SCS)
        prob.solve(solver='GLPK_MI')
        if prob.status=='optimal':
            if assign_task_tuple in self.explored_node_dic.keys():
                if tuple_node in self.explored_node_dic[assign_task_tuple].keys():
                    max_end_time_value, end_time_value = self.explored_node_dic[assign_task_tuple][tuple_node]
            else:
                self.explored_node_dic[assign_task_tuple]={}
                self.explored_node_dic[assign_task_tuple][tuple_node]=(max(end_time.value),end_time.value)
            return max(end_time.value),end_time.value
        else:
            return self.horizon,[]

    def opt_for_partial_assigment_online(self,node,assign_task,extro_constrain):
        #assign_task is error!
        if len(assign_task)==0:
            t=0
            for i ,j in extro_constrain.begin_time.items():
                t=max(t,j)
            return t,0,0
        t=0
        assign_task_dic={}
        for i in assign_task:
            if not isinstance(i,tuple):
                s=1
        for i in assign_task:
            assign_task_dic[i[0]]=t
            t=t+1
        assign_task=[i[0] for i in assign_task]
        end_time=cp.Variable(shape=(len(assign_task),1),name='endtime',nonneg=True)
        total_constrain=[]
        M1=[]
        B1=[[]]
        for i,j in self.poset['<']:
            if i in assign_task :
                if j in assign_task:
                    m=[0 for l in range(len(assign_task))]
                    m[assign_task_dic[self.task_data[i][0]]]=1
                    m[assign_task_dic[self.task_data[j][0]]]=-1
                    M1.append(m)
                    B1[0].append(-extro_constrain.task_execute_time[j])
            else:
                if j in assign_task:
                    m=[0 for l in range(len(assign_task))]
                    m[assign_task_dic[self.task_data[j][0]]]=-1
                    M1.append(m)
                    B1[0].append(-extro_constrain.task_execute_time[j]-extro_constrain.finished_time_list[i])
        #M1=[]
        #B1=[[]]
        for i,j in self.poset['<=']:
            if i in assign_task :
                if j in assign_task:
                    m=[0 for l in range(len(assign_task))]
                    m[assign_task_dic[self.task_data[i][0]]]=1
                    m[assign_task_dic[self.task_data[j][0]]]=-1
                    M1.append(m)
                    B1[0].append(-extro_constrain.task_execute_time[j]+extro_constrain.task_execute_time[i])
            else:
                if j in assign_task:
                    m=[0 for l in range(len(assign_task))]
                    m[assign_task_dic[self.task_data[j][0]]]=-1
                    M1.append(m)
                    B1[0].append(-extro_constrain.task_execute_time[j]-extro_constrain.finished_time_list[i]+extro_constrain.task_execute_time[i])
        for i,j in self.poset['=']:
            if i in assign_task and j in assign_task:
                if self.task_type[self.task_data[i][1]][0]>= self.task_type[self.task_data[j][1]][0]:
                    changelabel=-1
                else:
                    changelabel=1
                m=[0 for l in range(len(assign_task))]
                m[assign_task_dic[self.task_data[i][0]]]=changelabel
                m[assign_task_dic[self.task_data[j][0]]]=-changelabel
                M1.append(m)
                B1[0].append(0)
                #might remaining to do!!!!!!!!!!!!!!!
                m=[0 for l in range(len(assign_task))]
                m[assign_task_dic[self.task_data[i][0]]]=-changelabel
                m[assign_task_dic[self.task_data[j][0]]]=changelabel
                M1.append(m)
                B1[0].append(-extro_constrain.task_execute_time[i]*changelabel+extro_constrain.task_execute_time[j]*changelabel)
            elif i in assign_task:
                m=[0 for l in range(len(assign_task))]
                m[assign_task_dic[self.task_data[j][0]]]=-1
                M1.append(m)
                B1[0].append(-extro_constrain.task_execute_time[j]-extro_constrain.task_execute_time[i]-extro_constrain.finished_time_list[i])
                m=[0 for l in range(len(assign_task))]
                m[assign_task_dic[self.task_data[j][0]]]=1
                M1.append(m)
                B1[0].append(-extro_constrain.task_execute_time[j]-extro_constrain.finished_time_list[i])
            elif j in assign_task:
                m=[0 for l in range(len(assign_task))]
                m[assign_task_dic[self.task_data[i][0]]]=-1
                M1.append(m)
                B1[0].append(-extro_constrain.task_execute_time[i]-extro_constrain.finished_time_list[j])
            if i in assign_task :
                if j in assign_task:
                    m=[0 for l in range(len(assign_task))]
                    m[assign_task_dic[self.task_data[i][0]]]=1
                    m[assign_task_dic[self.task_data[j][0]]]=-1
                    M1.append(m)
                    B1[0].append(-extro_constrain.task_execute_time[j])
            else:
                if j in assign_task:
                    m=[0 for l in range(len(assign_task))]
                    m[assign_task_dic[self.task_data[j][0]]]=-1
                    M1.append(m)
                    B1[0].append(-extro_constrain.task_execute_time[j]-extro_constrain.finished_time_list[i])
        for i,j in self.poset['!=']:
            if not (i,j) in self.poset['<='] and not (j,i) in self.poset['<=']:
            #if 1:
                if  i in assign_task:
                    if  j in assign_task:
                        m = [[0] for l in range(len(assign_task))]
                        m[assign_task_dic[self.task_data[i][0]]][0] = 1
                        m[assign_task_dic[self.task_data[j][0]]][0] = -1
                        bool_for_x = cp.Variable(1, boolean=True)
                        constrain0 = [m @ end_time - self.task_type[self.task_data[i][1]][0] + bool_for_x * self.time_budget - self.time_budget >= 0]
                        constrain1 = [m @ end_time + self.task_type[self.task_data[j][1]][0] - bool_for_x * self.time_budget <= 0]
                        total_constrain.append(*constrain0)
                        total_constrain.append(*constrain1)
                    elif j in extro_constrain.finished_time_list.keys():
                        m = [[0] for l in range(len(assign_task))]
                        m[assign_task_dic[self.task_data[i][0]]][0] = 1
                        #m[assign_task_dic[self.task_data[j][0]]][0] = -1
                        bool_for_x = cp.Variable(1, boolean=True)
                        constrain0 = [m @ end_time - self.task_type[self.task_data[i][1]][
                            0] + bool_for_x * self.time_budget-extro_constrain.finished_time_list[j] - self.time_budget >= 0]
                        constrain1 = [m @ end_time + self.task_type[self.task_data[j][1]][
                            0] - bool_for_x * self.time_budget-extro_constrain.finished_time_list[j] <= 0]
                        total_constrain.append(*constrain0)
                        total_constrain.append(*constrain1)

                else:
                    if j in assign_task:
                        #here is error!!!!
                        if i in extro_constrain.finished_time_list.keys():

                            m = [[0] for l in range(len(assign_task))]
                            m[assign_task_dic[self.task_data[j][0]]][0] = 1
                            # m[assign_task_dic[self.task_data[j][0]]][0] = -1
                            bool_for_x = cp.Variable(1, boolean=True)
                            constrain0 = [m @ end_time - self.task_type[self.task_data[i][1]][
                                0] - bool_for_x * self.time_budget - extro_constrain.finished_time_list[
                                              i] + self.time_budget >= 0]
                            constrain1 = [m @ end_time + self.task_type[self.task_data[i][1]][
                                0] + bool_for_x * self.time_budget - extro_constrain.finished_time_list[i] >= 0]
                            total_constrain.append(*constrain0)
                            total_constrain.append(*constrain1)
        if not M1==[]:
            M11=self.Turn_Matrix(M1)
            constraint1=[M11 @ end_time <= B1]
            total_constrain.append(*constraint1)
#=======motion_constrain
        M2=[]
        B2=[[]]
        print(assign_task_dic)
        for agent_i in range(len(self.agent_data)):
            if len(node[agent_i])>0:
                s=1
                #计算第一个部分的路径，但是由于循环的问题，第一部分过去的路径可以忽略
                m=[0 for i in range(len(assign_task))]
                c=assign_task_dic[node[agent_i][0][0][0]]
                m[c]=1
                #print(node[agent_i][0][0][2])
                x1=extro_constrain.agent_pose[agent_i]
                x2=self.position[node[agent_i][0][0][2]]
                dis=((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)**0.5
                M2.append(m)
                B2[0].append(dis/10000+\
                   extro_constrain.task_execute_time[node[agent_i][0][0][0]]+extro_constrain.begin_time[agent_i])
            if len(node[agent_i])>1:
                for task in range(len(node[agent_i])-1):
                    m=[0 for i in range(len(assign_task))]
                    c=assign_task_dic[node[agent_i][task][0][0]]
                    m[c]=-1
                    #print(assign_task_dic)
                    #print(node[agent_i][task+1][0][0])
                    if not node[agent_i][task+1][0][0] in assign_task_dic.keys():
                        s=1
                    c=assign_task_dic[node[agent_i][task+1][0][0]]
                    m[c]=1
                    b=self.get_distance(node[agent_i][task][0][2],node[agent_i][task+1][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                        extro_constrain.task_execute_time[node[agent_i][task+1][0][0]]
                    M2.append(m)
                    B2[0].append((b))
        if not M2==[]:
            M21=self.Turn_Matrix(M2)
            constraint2=[M21 @ end_time >= B2]# constraint of poset
            total_constrain.append(*constraint2)
        list1=[[1] for task in assign_task]
        obj = cp.Minimize(list1 @ end_time)
        prob=cp.Problem(obj,total_constrain)
        prob.solve(solver='GLPK_MI')
        max_time=0
        for _,task_end_time in extro_constrain.finished_time_list.items():
            max_time=max(max_time,task_end_time)
        for n in end_time.value:
            max_time=max(n,max_time)
        if prob.status=='optimal':
            return max_time,end_time.value,assign_task_dic
        else:
            return self.horizon,[],assign_task_dic

    def plot_bnb_graph_phi1(self,load=0,save=0):
        if not load==0:
            self.upper_bound_list=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task'+load+'/bnb_upper_bound_list.npy').item()
            self.low_bound_list=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task'+load+'/bnb_low_bound_list.npy').item()
            self.best_up_bound_list=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task'+load+'/bnb_best_up_bound_list.npy').item()
        if not save == 0:
            np.save(
                '/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task' + save + '/bnb_upper_bound_list.npy',self.upper_bound_list)
            np.save(
                '/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task' + save + '/bnb_low_bound_list.npy',self.low_bound_list)
            np.save(
                '/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task' + save+ '/bnb_best_up_bound_list.npy',self.best_up_bound_list)
        fig=plt.figure(figsize=(20,15))
        ax=fig.add_subplot()
        nu0_list=[]
        nu1_list=[]
        rn=0
        for n,nu in self.upper_bound_list.items():
             #plt.plot(n,nu[0],'r')
             if nu[0]>1300:
                nu0_list.append(1290)
                nu0_list.append(1290)
                nu1_list.append(n)
                nu1_list.append(n)
             else:
                nu0_list.append(nu[0])
                nu0_list.append(nu[0])
                nu1_list.append(n)
                nu1_list.append(n)
        nu0_list.pop()
        nu1_list.pop(0)
        nu0_list.pop(0)
        nu1_list.pop(0)
        plt.plot(nu1_list,nu0_list,'r',linewidth=7,label='$\overline{T}$')
        best_up_round=n
        first_cut_time=0
        cut_node_count=0
        nu0_list = []
        nu1_list = []
        for n,nu in self.low_bound_list.items():
            if n%2==0:
                #nu0_list.append(nu[0])
                #nu1_list.append(nu[1])
                if nu[2]=='cut':
                    plt.plot(n,nu[0],'g.',markersize=10)
                    if first_cut_time==0:
                        first_cut_time=nu[1]
                    cut_node_count=cut_node_count+1
                else:
                    nu0_list.append(nu[0])
                    nu1_list.append(n)
                    plt.plot(n,nu[0],'y.')
        plt.plot(n,nu[0],'g.',label='bounded node',markersize=10)
        value_round=[]
        plt.plot(nu1_list,nu0_list,'y',linewidth=7,label='$T$\u0332')
        for n in self.best_up_bound_list.values():
            value_round.append(n[0])
            value_round.append(n[0])
        value_round2=[]
        for n in self.best_up_bound_list.keys():
            value_round2.append(n)
            value_round2.append(n)
        value_round2.pop(0)
        value_round2.append(best_up_round)
        plt.plot(value_round2,value_round,'b',linewidth=7,label='$T^\star$')
        plt.xlim(0,len(self.low_bound_list))
        plt.ylim(500,1300)
        x_tick=range(0,len(self.low_bound_list)//10)
        xlabels=range(0,len(self.low_bound_list)//10,5)
        xticks=[label*10 for label in xlabels]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xlabels,fontsize=30)
        plt.yticks(fontsize=20)
        #============================= draw patches

        plt.legend(loc=2,bbox_to_anchor=(0,1.18),fontsize=35,ncol=4)
        #plt.xticks(x_tick, fontsize=20)
        plt.ylabel('Executimg time/s',fontsize=40)
        plt.xlabel('Searching round',fontsize=40)
        print('search node',self.count_round)
        print('best upper bound',self.best_up_bound_list)
        print('first solution',self.upper_bound_list[1])
        print('first cut off node',first_cut_time)
        print('cut off node rate',cut_node_count/self.count_round)
        plt.show()

    def plot_bnb_graph_phi2(self,load=0,save=0):
        if not load==0:
            self.upper_bound_list=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task'+load+'/bnb_upper_bound_list.npy').item()
            self.low_bound_list=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task'+load+'/bnb_low_bound_list.npy').item()
            self.best_up_bound_list=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task'+load+'/bnb_best_up_bound_list.npy').item()
        if not save == 0:
            np.save(
                '/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task' + save + '/bnb_upper_bound_list.npy',self.upper_bound_list)
            np.save(
                '/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task' + save + '/bnb_low_bound_list.npy',self.low_bound_list)
            np.save(
                '/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task' + save+ '/bnb_best_up_bound_list.npy',self.best_up_bound_list)
        #rc('text',usetex=True)
        fig=plt.figure(figsize=(20,15))
        ax=fig.add_subplot()
        nu0_list=[]
        nu1_list=[]
        rn=0
        for n,nu in self.upper_bound_list.items():
             #plt.plot(n,nu[0],'r')
             if nu[0]>2400:
                 nu0_list.append(2350)
                 nu0_list.append(2350)
                 nu1_list.append(n)
                 nu1_list.append(n)
             else:
                 nu0_list.append(nu[0])
                 nu0_list.append(nu[0])
                 nu1_list.append(n)
                 nu1_list.append(n)
        nu0_list.pop()
        nu1_list.pop(0)
        plt.plot(nu1_list,nu0_list,'r',linewidth=7,label=r'$\overline{T}$')
        best_up_round=n
        first_cut_time=0
        cut_node_count=0
        print('nu0',nu0_list)
        print('nu1',nu1_list)
        nu0_list = []
        nu1_list = []
        for n,nu in self.low_bound_list.items():
            if n%2==0:
                #nu0_list.append(nu[0])
                #nu1_list.append(nu[1])
                if nu[2]=='cut':
                    plt.plot(n,nu[0],'g.',markersize=25)
                    if first_cut_time==0:
                        first_cut_time=nu[1]
                    cut_node_count=cut_node_count+1
                else:
                    nu0_list.append(nu[0])
                    nu1_list.append(n)
                    plt.plot(n,nu[0],'y.')
        plt.plot(n,nu[0],'g.',label='bounded node',markersize=25)
        value_round=[]
        print("\033[4mT\033[0m")
        plt.plot(nu1_list,nu0_list,'y',linewidth=7,label="$T$\u0332")
        for n in self.best_up_bound_list.values():
            value_round.append(n[0])
            value_round.append(n[0])
        value_round2=[]
        for n in self.best_up_bound_list.keys():
            value_round2.append(n)
            value_round2.append(n)
        value_round2.pop(0)
        value_round2.append(best_up_round)
        print('x',value_round2)
        print('y',value_round)
        plt.plot(value_round2,value_round,'b',linewidth=7,label='$T^\star$')
        plt.xlim(0,len(self.low_bound_list))
        plt.ylim(600,2400)
        x_tick=range(0,len(self.low_bound_list)//10)
        xlabels=range(0,len(self.low_bound_list),50)
        xticks=[label for label in xlabels]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xlabels,fontsize=30)
        plt.yticks(fontsize=20)
        #============================= draw patches
        plt.legend(loc=2, bbox_to_anchor=(0, 1.18), fontsize='38', ncol=4)
        #plt.legend(loc='lower right',fontsize=20,ncol=3)
        #plt.xticks(x_tick, fontsize=20)
        plt.ylabel('Executimg time/s',fontsize=40)
        plt.xlabel('Searching round',fontsize=40)
        print('search node',self.count_round)
        print('best upper bound',self.best_up_bound_list)
        print('first solution',self.upper_bound_list[1])
        print('first cut off node',first_cut_time)
        print('cut off node rate',cut_node_count/self.count_round)
        plt.show()

    def plot_bnb_graph_phi4(self,load=0,save=0):
        if not load=='0':
            self.upper_bound_list=np.load('C:/Users\MSI1\Documents\LTL_MAS_C-action\data\output_data/taskfinal/bnb_upper_bound_list_'+load+'.npy',allow_pickle=True).item()
            self.low_bound_list=np.load('C:/Users\MSI1\Documents\LTL_MAS_C-action\data\output_data/taskfinal/bnb_low_bound_list_'+load+'.npy',allow_pickle=True).item()
            self.best_up_bound_list=np.load('C:/Users\MSI1\Documents\LTL_MAS_C-action\data\output_data/taskfinal/bnb_best_up_bound_list_'+load+'.npy',allow_pickle=True).item()
        if not save == '0':
            np.save(
                'C:/Users\MSI1\Documents\LTL_MAS_C-action\data\output_data/taskfinal/bnb_upper_bound_list_'+save+'.npy',self.upper_bound_list)
            np.save(
                'C:/Users\MSI1\Documents\LTL_MAS_C-action\data\output_data/taskfinal/bnb_low_bound_list_'+save+'.npy',self.low_bound_list)
            np.save(
                'C:/Users\MSI1\Documents\LTL_MAS_C-action\data\output_data/taskfinal/bnb_best_up_bound_list_'+save+'.npy',self.best_up_bound_list)
        fig=plt.figure(figsize=(20,15))
        ax=fig.add_subplot(111)
        nu0_list=[]
        nu1_list=[]
        rn=0
        n_dic={}
        for i in range(2000):
            if i<=100:
                n_dic[i]=i
            if i>100 and i <=200:
                n_dic[i]=50+i/2
            if i>200 and i <=400:
                n_dic[i]=100+i/4
            if i > 400 and i <= 800:
                n_dic[i]=150+i/8
            if i>800 and i <=1600:
                n_dic[i]=200+i/16
        for n,nu in self.upper_bound_list.items():
             n=n_dic[n]
             #plt.plot(n,nu[0],'r')
             if nu[0]>3000:
                 nu0_list.append(2950)
                 nu0_list.append(2950)
                 nu1_list.append(n)
                 nu1_list.append(n)
                 #if rn==0:
                 #    plt.plot(n,4000,'r*',label='bad upper bound')
                 #    rn=1
                 #else:
                     #plt.plot(n,4000,'r*')
             else:
                nu0_list.append(nu[0])
                nu0_list.append(nu[0])
                nu1_list.append(n)
                nu1_list.append(n)
        nu0_list.pop()
        nu1_list.pop(0)
        plt.plot(nu1_list,nu0_list,'r',linewidth=7,label='$\overline{T}$')
        best_up_round=n
        first_cut_time=0
        cut_node_count=0
        nu0_list = []
        nu1_list = []
        for n,nu in self.low_bound_list.items():
            if n%2==0:
                n = n_dic[n]
                #nu0_list.append(nu[0])
                #nu1_list.append(nu[1])
                if nu[2]=='cut':
                    plt.plot(n,nu[0],'g.',markersize=15)
                    if first_cut_time==0:
                        first_cut_time=nu[1]
                    cut_node_count=cut_node_count+1
                else:
                    nu0_list.append(nu[0])
                    nu1_list.append(n)
                    plt.plot(n,nu[0],'y.')
        plt.plot(n,nu[0],'g.',markersize=25,label='bounded node')
        value_round=[]
        plt.plot(nu1_list,nu0_list,'y',linewidth=7,label="$T$\u0332")
        for n in self.best_up_bound_list.values():

            value_round.append(n[0])
            value_round.append(n[0])
        value_round2=[]
        for n in self.best_up_bound_list.keys():

            value_round2.append(n)
            value_round2.append(n)
        value_round2.pop(0)
        value_round2.append(best_up_round)
        plt.plot(value_round2,value_round,'b',linewidth=7,label='$T^\star$')
        plt.xlim(0,250)
        plt.ylim(700,3000)
        x_tick=range(0,len(self.low_bound_list)//20)
        xlabels=[0,50,100,200,400,800]#range(0,300,50)
        xticks=[label for label in range(0,300,50)]
        ax.set_xticks(xticks)
        ax.set_xticklabels(xlabels,fontsize=30)
        ylabels=range(600,3000,300)
        yticks=[label-120 for label in ylabels]
        ax.set_yticks(yticks)
        ax.set_yticklabels(ylabels,fontsize=20)
        #plt.yticks(fontsize=20)
        #============================= draw patches
        plt.legend(loc=2,bbox_to_anchor=(0,1.18),fontsize=35,ncol=4)
        #plt.xticks(x_tick, fontsize=20)
        plt.ylabel('Executimg time/s',fontsize=40)
        plt.xlabel('Searching round',fontsize=40)
        #print('search node',self.count_round)
        print('best upper bound',self.best_up_bound_list)
        print('first solution',self.upper_bound_list[1])
        print('first cut off node',first_cut_time)
        #print('cut off node rate',cut_node_count/self.count_round)
        plt.show()

    def Turn_Matrix(self,M):
        if len(M)==0:
            return M
        r = [[] for i in M[0]]
        for i in M:
            for j in range(len(i)) :
                r[j].append(i[j])
        return  r

    def get_horizon(self):
        self.horizon=10000
        #for i in self.task_data:
        #    self.horizon=self.task_type[i[1]][0]*2+self.horizon+100

    def generate_time_budget(self):
        self.time_budget=0
        for i in self.task_data:
            self.time_budget=self.time_budget+self.task_type[self.task_data[i[0]][1]][0]

    def get_distance(self,i,j):
        #return self.position[(i,j)]
        pos1=self.position[i][0]-self.position[j][0]
        pos2=self.position[i][1]-self.position[j][1]
        lenth=(pos1**2+pos2**2)**0.5
        return lenth

    def print_answer(self):
        print('best value is:',self.best_up_bound)
        for i in range(len(self.agent_data)):
            print('agent',i+1,'task list is:',self.best_solution[i])
