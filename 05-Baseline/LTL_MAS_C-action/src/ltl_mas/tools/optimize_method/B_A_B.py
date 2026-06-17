import cvxpy as cp
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
        self.generate_poset_graph()


    def Begin_branch_search_online(self,time_limit,extro_constrain,current_node,assigned_task,assign_task):

        root_node=[[] for agent in self.agent_data]#(solution,assigned_task)
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
            if self.best_up_bound<530:
                s=1
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
        self.get_time_table_of_best_solution(self.solution)# remain to update

    def Begin_branch_search2(self,time_limit,up_bound_method=1,low_bound_method=1,search_method='DFS'):
        root_node=[[] for i in self.agent_data]#(solution,assigned_task)
        assigned_tasks=[]
        self.get_lower_bound(low_bound_method)
        up_bound,solution=self.get_upper_bound(root_node,assigned_tasks,up_bound_method)
        #low_bound=self.get_lower_bound_method(root_node,assigned_tasks)
        self.branch_tree=[(root_node,assigned_tasks)]
        self.search_node_list={}
        self.search_node_list[tuple(assigned_tasks)]=[root_node]
        self.best_solution=solution
        self.best_up_bound=up_bound
        self.max_low_bound=0
        start=time.time()
        while (not self.branch_tree==[]) and time.time()-start<time_limit:
            #print('check a branch')
            node,task=self.branch_tree.pop()
        #child_nodes=self.branching_routine(search_method)
            if tuple(task) in self.search_node_list.keys():
                if node not in self.search_node_list[tuple(task)]:
                    self.search_node_list[tuple(task)].append(node)
                    low_bound=self.get_lower_bound_method(node,task)
                    if low_bound<self.best_up_bound:
                        child_nodes=self.exten_child_nodes(node,task)
                        self.branch_tree.extend(child_nodes)
                        up_bound,solution=self.get_upper_bound(node,task,up_bound_method)

                        if up_bound<self.best_up_bound:

                            self.best_solution=solution
                            self.best_up_bound=up_bound
                else:
                    child_nodes=self.exten_child_nodes(node,task)
                    self.branch_tree.extend(child_nodes)
            else:
                self.search_node_list[tuple(task)]=[node]
                low_bound=self.get_lower_bound_method(node,task)
                if low_bound<self.best_up_bound:
                    child_nodes=self.exten_child_nodes(node,task)
                    self.branch_tree.extend(child_nodes)
                    up_bound,solution=self.get_upper_bound(node,task,up_bound_method)
                    if up_bound<low_bound:
                        s=1
                    #self.branch_tree.append((node,task,up_bound,low_bound))
                    if up_bound<self.best_up_bound:

                        self.best_solution=solution
                        self.best_up_bound=up_bound
            print('new branch up bound is',self.best_up_bound)

        self.print_answer()
        self.get_time_table_of_best_solution(self.best_solution)

    def Begin_branch_search1(self,time_limit,up_bound_method=1,low_bound_method=1,search_method='DFS'):
        root_node=[[] for i in self.agent_data]#(solution,assigned_task)
        assigned_tasks=[]
        self.get_lower_bound(low_bound_method)
        up_bound,solution=self.get_upper_bound(root_node,assigned_tasks,up_bound_method)
        low_bound=self.get_lower_bound_method(root_node,assigned_tasks)
        self.branch_tree=[(root_node,assigned_tasks,up_bound,low_bound)]
        self.search_node_list={}
        self.search_node_list[tuple(assigned_tasks)]=[root_node]
        self.best_solution=solution
        self.best_up_bound=up_bound
        self.max_low_bound=low_bound
        start=time.time()
        while (not self.branch_tree==[]) and time.time()-start<time_limit:
            print('check a branch')
            child_nodes=self.branching_routine(search_method)
            label_to_update_best_solution=0
            for node,task in child_nodes:
                if tuple(task) in self.search_node_list.keys():
                    if node not in self.search_node_list[tuple(task)]:
                        self.search_node_list[tuple(task)].append(node)
                        low_bound=self.get_lower_bound_method(node,task)
                        if low_bound<self.best_up_bound:
                            #self.branch_tree.append((node,task,up_bound,low_bound))
                            up_bound,solution=self.get_upper_bound(node,task,up_bound_method)
                            self.branch_tree.append((node,task,up_bound,low_bound))
                            if up_bound<self.best_up_bound:
                                label_to_update_best_solution=1
                                self.best_solution=solution
                                self.best_up_bound=up_bound
                else:
                    self.search_node_list[tuple(task)]=[node]
                    low_bound=self.get_lower_bound_method(node,task)
                    if low_bound<self.best_up_bound:
                        self.branch_tree.append((node,task,up_bound,low_bound))
                        up_bound,solution=self.get_upper_bound(node,task,up_bound_method)
                        self.branch_tree.append((node,task,up_bound,low_bound))
                        if up_bound<self.best_up_bound:
                            label_to_update_best_solution=1
                            self.best_solution=solution
                            self.best_up_bound=up_bound
            print('new branch up bound is',self.best_up_bound)
            if label_to_update_best_solution:
                self.prune_tree()
        self.print_answer()
        self.get_time_table_of_best_solution()

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
                if not len(set(self.poset_graph.pred[i])-assiged_task_set-{'root'})==0:
                    un_assig_task.remove(i)
            to_assig_task = random.sample( un_assig_task,1)
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
            for i in range(5):
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
                t,time_list_i,_=self.opt_for_partial_assigment_online(new_node,unfinished_assigned_task_list,extro_constrain)
                time_list.append(max(time_list_i))
            if len(time_list)==0:
                s=1
            l=time_list.index(min(time_list))
            init_node=node_list[l]

        #time_list=[]
        if sample_list==[]:
            return self.horizon,[]
        else:
            return min(time_list),init_node

    def get_upper_bound(self,node,assigned_tasks,up_bound_method):
        if up_bound_method=='greedy':#should be finished
            up_bound,solution=self.found_solution_greedy(node,assigned_tasks)
            #print('get up_bound',up_bound)
            return up_bound,solution
        elif up_bound_method=='sample':
            up_bound,solution=self.get_n_solution_with_sample(node,assigned_tasks)

        elif up_bound_method=='':
            1
        else:
            raise Exception('Undefined up bound method')
            return up_bound,solution

    def found_solution_greedy(self,init_node,assigned_tasks):
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
            for to_assig_task in un_assig_task:
                new_assiged_task=assiged_task |{to_assig_task}
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
        for i,j in self.poset:
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
        end_time=cp.Variable(shape=(len(self.task_data),1),name='endtime',nonneg=True)
        total_constrain=[]
        M1=[]
        B1=[[]]
        for i,j in self.poset:
            m=[0 for k in range(len(self.task_data))]
            m[self.task_data[i][0]]=1
            m[self.task_data[j][0]]=-1
            M1.append(m)
            B1[0].append(-self.task_type[self.task_data[j][1]][0])
        if not M1==[]:
            M11=self.Turn_Matrix(M1)
            constraint1=[M11 @ end_time <= B1]
            total_constrain.append(*constraint1)
        M2=[]
        B2=[[]]
        for agent_i in range(len(self.agent_data)):
            if len(solution[agent_i])>0:
                m=[0 for i in range(len(self.task_data))]
                m[solution[agent_i][0][0][0]]=1
                M2.append(m)
                B2[0].append(self.get_distance(self.agent_data[agent_i][1],solution[agent_i][0][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                    self.task_type[solution[agent_i][0][0][1]][0])
            if len(solution[agent_i])>1:
                for task in range(len(solution[agent_i])-1):
                    m=[0 for i in range(len(self.task_data))]
                    m[solution[agent_i][task][0][0]]=-1
                    m[solution[agent_i][task+1][0][0]]=1
                    b=self.get_distance(solution[agent_i][task][0][2],solution[agent_i][task+1][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                        self.task_type[solution[agent_i][task+1][0][1]][0]
                    M2.append(m)
                    B2[0].append((b))
        task_time_cost_list=[self.task_type[task[1]][0] for task in self.task_data]
        list1=[[1] for task in self.task_data]
        M21=self.Turn_Matrix(M2)
        constraint2=[M21 @ end_time >= B2]# constraint of poset
        total_constrain.append(*constraint2)
        obj = cp.Minimize(list1 @ end_time)
        #obj=cp.Minimize(end_time)
        prob=cp.Problem(obj,total_constrain)
        prob.solve(solver=cp.SCS)
        if prob.status=='optimal':
            self.task_time_table=[[i,end_time.value[i][0]-task_time_cost_list[i],end_time.value[i][0]] for i in range(len(self.task_data))]
        else:
            s=1

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

    def get_n_solution_with_sample(self,init_node,assigned_tasks,num):
        answers=[]
        solutions=[]
        for i in range(num):
            solution,no_ans_label=self.get_a_solution_with_sample(init_node,assigned_tasks)
            if no_ans_label==1:
                max_answer=self.horizon
                solution=[]
                return max_answer,solution
            answer=self.opt_function_with_cvxpy(solution)
            answers.append(answer)
            solutions.append(solution)
        max_answer=min(answers)
        best_solution=solutions[answers.index(max_answer)]
        return max_answer,best_solution

    def get_a_solution_with_sample(self,init_node,assigned_tasks):
        sequence=[(set(assigned_tasks),init_node)]
        task_set=set(range(len(self.task_data)))
        un_found=1
        sample_list=[]
        while sequence!=[] and un_found:
            root_node=sequence.pop()
            assiged_task=root_node[0]
            init_node=root_node[1]
            #print(assiged_task)
            un_assig_task=task_set-assiged_task
            to_assig_task=random.sample(un_assig_task,1)[0]
            sub_task_list=self.task_type[self.task_data[to_assig_task][1]][1]
            for sub_task,num in sub_task_list.items():
                feasible={}
                list=[]
                for agent_i in self.agent_data:
                    if sub_task in self.agent_type[agent_i[2]]['serve']:
                        list.append(agent_i[0])
                feasible[sub_task]=(list,num)
        #=====================get task distribution
            conflict=1
            round=0
            un_feasible=0
            while conflict:
                round=round+1
                if round>20:
                    un_feasible=1
                    break
                assign_list={}
                check_list=[]
                new_node=copy.deepcopy(init_node)
                for sub_task,(list,num) in feasible.items():
                    assign_list[sub_task]=random.sample(list,num)
                    check_list.extend(assign_list[sub_task])
                    repet_Num=Counter(check_list)
                    if len(repet_Num)<len(check_list):
                        break
                if len(repet_Num)<len(check_list):
                    continue
                for sub_task,samb in assign_list.items():
                    po_label=0
                    for agent_i in samb:
                        agent=init_node[agent_i]
                        if self.check_poset_in_agent(agent,to_assig_task):
                            new_node[agent_i].append((self.task_data[to_assig_task],sub_task))
                        else:
                            po_label=1
                            break
                    if po_label==1:
                        break
                if po_label==1:
                    continue
                else:
                    init_node=copy.deepcopy(new_node)
                    conflict=0
            if not un_feasible:
                assiged_task.add(to_assig_task)
                sequence.append((assiged_task,init_node))
                #print(len(assiged_task),'vs',len(task_set))
            else:
                break
            if len(assiged_task)==len(task_set):
                #print('found')
                sample_list.append(init_node)
                un_found=0
        no_ans_label=0
        if sequence==[] and un_found==0:
            no_ans_label=1
        return sample_list,no_ans_label

    def get_lower_bound(self,low_bound_method):
        if low_bound_method=='i_j_k':
            start=time.time()
            #print('error! the lower bound method is  still wrong')
            self.get_lower_bound_method=self.get_lower_bound_with_i_j_k

        if low_bound_method=='i_j_l':
            start=time.time()
            self.get_lower_bound_method=self.get_lower_bound_with_i_j_l_faster
            end=time.time()
            print(end-start)
        if low_bound_method=='i_j':
            self.get_lower_bound_method=self.get_lower_bound_with_i_j
        #low_bound1=self.get_lower_bound_with_i_j_k_faster(node,assigned_tasks)
        #return  low_bound1

    def get_lower_bound_with_i_j_k(self,node,assigned_tasks):
        if len(assigned_tasks)==len(self.task_data):
            a,_=self.opt_for_partial_assigment(node,assigned_tasks)
            return a
        unassigned_tasks=list(range(len(self.task_data)))
        for i in assigned_tasks:
            unassigned_tasks.remove(i)
        agent_number=len(self.agent_data)
        task_number=len(unassigned_tasks)
        #max_task_list=task_number
        max_task_list=task_number
        x_i_j_k=cp.Variable(shape=(agent_number*task_number*max_task_list,1),boolean=True)
        t_j=cp.Variable(shape=(len(self.task_data),1),nonneg=True)
        total_constrain=[]
        #--------------------- partlai order constraints (1)
        if not self.poset=={}:
            M=[[0 for i in self.poset] for j in self.task_data]
            b=[[]]
            line=0
            for j1,j2 in self.poset:
                M[j1][line]=1
                M[j2][line]=-1
                b[0].append(-self.task_type[self.task_data[j1][1]][0])
                line=line+1
            poset_constrain=[M @ t_j <= b]
            total_constrain.append(*poset_constrain)
        # ================provide enough serves for the task j (2)
        M2=[[0 for i in range(task_number)] for j in range(agent_number*task_number*max_task_list)]
        b2=[[0 for i in range(task_number)]]
        z=0
        for task_j in range(task_number):
            for agent_i in range(agent_number):
                for sub_task in self.task_type[self.task_data[unassigned_tasks[task_j]][1]][1].keys():
                    bil=0
                    if sub_task in self.agent_type[self.agent_data[agent_i][2]]['serve']:
                        bil=1
                for order_k in range(max_task_list):
                    num=agent_i*task_number*max_task_list+\
                        task_j*max_task_list+\
                        order_k
                    M2[num][z]=bil
            tol_num=0
            for _,num in self.task_type[self.task_data[unassigned_tasks[task_j]][1]][1].items():
                tol_num=tol_num+num
            b2[0][z]=tol_num
            z=z+1
        enough_constrain=[M2 @ x_i_j_k == b2]
        total_constrain.append(*enough_constrain)
        #===================one agent con only provide the serve it has:(3)
        M3=[[0 for i in range(agent_number*task_number*max_task_list)] for j in range(agent_number*task_number*max_task_list)]
        b3=[[0 for i in range(agent_number*task_number*max_task_list)]]
        z=0
        for agent_i in range(agent_number):
            for task_j in range(task_number):
                for order_k in range(max_task_list):
                        num=agent_i*task_number*max_task_list+\
                            task_j*max_task_list+\
                            order_k
                        M3[num][z]=1
                        for sub_task in self.task_type[self.task_data[unassigned_tasks[task_j]][1]][1].keys():
                            if sub_task in self.agent_type[self.agent_data[agent_i][2]]['serve']:
                                b3[0][z]=1
                        z=z+1
        once_constrain=[M3 @ x_i_j_k <= b3]
        total_constrain.append(*once_constrain)
        #================= one agent execute one task no more than once: (4)
        M4=[[0 for i in range(agent_number*task_number)] for j in range(agent_number*task_number*max_task_list)]
        b4=[[1 for i in range(agent_number*task_number)]]
        z=0
        for agent_i in range(agent_number):
            for task_j in range(task_number):
                for order_k in range(max_task_list):
                    num=agent_i*task_number*max_task_list+\
                        task_j*max_task_list+\
                        order_k
                    M4[num][z]=1
                z=z+1
        constrain4=[M4 @ x_i_j_k <= b4]
        total_constrain.append(*constrain4)
        #================= one agent at any time can only execute no more than one task (5)
        M5=[[0 for i in range(agent_number*max_task_list)] for j in range(agent_number*task_number*max_task_list)]
        b5=[[0 for i in range(agent_number*max_task_list)]]
        z=0
        for agent_i in range(agent_number):
            for order_k in range(max_task_list):
                for task_j in range(task_number):
                    num=agent_i*task_number*max_task_list+\
                        task_j*max_task_list+\
                        order_k
                    M5[num][z]=1
                b5[0][z]=1
                z=z+1
        one_task_constrain=[M5 @ x_i_j_k <= b5]
        total_constrain.append(*one_task_constrain)
        #=============== no jump constraint(6)
        M6=[[0 for i in range(agent_number*(max_task_list-1))] for j in range(agent_number*task_number*max_task_list)]
        B6=[[0 for i in range(agent_number*(max_task_list-1))]]
        z=0
        for agent_i in range(agent_number):
            for order_k in range(max_task_list-1):
                for task_j in range(task_number):
                    num1=agent_i*task_number*max_task_list+\
                        task_j*max_task_list+\
                        order_k
                    num2=agent_i*task_number*max_task_list+\
                        task_j*max_task_list+ \
                         (order_k+1)
                    M6[num1][z]=1
                    M6[num2][z]=-1
                z=z+1
        if not sum(M6,[])==[]:
            continue_constrain=[M6 @ x_i_j_k >= B6]
            total_constrain.append(*continue_constrain)
        #============== motion constrain (7)
        M7=[]
        T7=[]
        B7=[]
        for agent_i in range(agent_number):
            for task_j1 in range(task_number):
                for task_j2 in range(task_number):
                    if not task_j1==task_j2:
                        t=[0 for i in range(len(self.task_data))]
                        t[unassigned_tasks[task_j1]]=-1
                        t[unassigned_tasks[task_j2]]=1
                        for order_k in range(max_task_list-1):
                            m=[0 for i in range(agent_number*max_task_list*task_number)]
                            numj1=agent_i*task_number*max_task_list+\
                            task_j1*max_task_list+\
                            order_k
                            numj2=agent_i*task_number*max_task_list+\
                            task_j2*max_task_list+ \
                                  (order_k+1)
                            m[numj1]=-self.horizon
                            m[numj2]=-self.horizon
                            b=self.get_distance(self.task_data[unassigned_tasks[task_j1]][2],self.task_data[unassigned_tasks[task_j2]][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                                self.task_type[self.task_data[unassigned_tasks[task_j1]][1]][0]-\
                                2*self.horizon
                            M7.append(m)
                            T7.append(t)
                            B7.append([b])
        if not M7==[]:
            M71=self.Turn_Matrix(M7)
            T71=self.Turn_Matrix(T7)
            B71=self.Turn_Matrix(B7)
            motion_constrain=[M71 @x_i_j_k + T71 @ t_j >= B71]
            total_constrain.append(*motion_constrain)
        #========================constrain (8)
        M8=[[0 for i in range(agent_number*task_number)] for j in range(agent_number*task_number*max_task_list)]
        t8=[[0 for i in range(agent_number*task_number)] for j in range(len(self.task_data))]
        B8=[[0 for i in range(agent_number*task_number)]]
        z=0
        for agent_i in range(agent_number):
            if len(node[agent_i])==0:
                for task_j in range(task_number):
                    num=agent_i*task_number*max_task_list+\
                            task_j*max_task_list
                    M8[num][z]=-self.horizon
                    t8[task_j][z]=1
                    B8[0][z]=self.get_distance(self.agent_data[agent_i][1],self.task_data[task_j][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']-self.horizon
                    z=z+1
            else:
                for task_j in range(task_number):
                    task_in_end_agent_i=node[agent_i][-1]
                    num=agent_i*task_number*max_task_list+\
                            task_j*max_task_list
                    M8[num][z]=-self.horizon
                    t8[task_j][z]=1
                    B8[0][z]=self.get_distance(task_in_end_agent_i[0][2],self.task_data[task_j][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']-self.horizon
                    z=z+1
        motion_constrain8=[M8 @ x_i_j_k + t8 @ t_j >= B8]
        total_constrain.append(*motion_constrain8)
        #======constrain case by partial attribe node:
        M9=[]
        B9=[[]]
        for agent_i in range(len(self.agent_data)):
            if len(node[agent_i])>0:
                m=[0 for i in self.task_data]
                c=node[agent_i][0][0][0]
                m[c]=1
                b=self.get_distance(self.agent_data[agent_i][1],node[agent_i][0][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                    self.task_type[node[agent_i][0][0][1]][0]
                M9.append(m)
                B9[0].append(self.get_distance(self.agent_data[agent_i][1],node[agent_i][0][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity'])
            if len(node[agent_i])>1:
                for task in range(len(node[agent_i])-1):
                    m=[0 for i in range(len(self.task_data))]
                    c=node[agent_i][task][0][0]
                    m[c]=-1
                    c=node[agent_i][task+1][0][0]
                    m[c]=1
                    b=self.get_distance(node[agent_i][task][0][2],node[agent_i][task+1][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                        self.task_type[node[agent_i][task][0][1]][0]
                    M9.append(m)
                    B9[0].append((b))
        if not M9==[]:
            M91=self.Turn_Matrix(M9)
            constraint9=[M91 @ t_j >= B9]# constraint of poset
            total_constrain.append(*constraint9)
        M10=[]
        t10=[]
        B10=[[]]
        b121=[]
        for agent_i in range(agent_number):
            if not len(node[agent_i])==0:
                task_j0=node[agent_i][-1][0][0]
                for task_j in range(task_number):
                    m=[0 for i in range(agent_number*task_number*max_task_list)]
                    t=[0 for i in range(len(self.task_data))]
                    num=agent_i*task_number*max_task_list+\
                            task_j*max_task_list
                    m[num]=-self.horizon
                    t[unassigned_tasks[task_j]]=1
                    t[task_j0]=-1
                    B10[0].append(self.get_distance(self.task_data[task_j0][2],
                                                   self.task_data[unassigned_tasks[task_j]][2])/
                                 self.agent_type[self.agent_data[agent_i][2]]['velocity']-
                                 self.horizon+
                                  self.task_type[self.task_data[task_j0][1]][0]
                                  )
                    b121.append(self.get_distance(self.task_data[task_j0][2],
                                                   self.task_data[unassigned_tasks[task_j]][2])/
                                 self.agent_type[self.agent_data[agent_i][2]]['velocity']+
                                  self.task_type[self.task_data[task_j0][1]][0])
                    M10.append(m)
                    t10.append(t)
        self.b1221=b121
        if not M10==[]:
            M101=self.Turn_Matrix(M10)
            t101=self.Turn_Matrix(t10)
            #B101=self.Turn_Matrix(B10)
            motion_constrain10=[M101 @ x_i_j_k + t101 @ t_j >= B10]
            total_constrain.append(*motion_constrain10)
        tim=[[]]
        for i in self.task_data:
            tim[0].append(self.task_type[i[1]][0])
        obj = cp.Minimize(cp.max(t_j+tim))
        prob=cp.Problem(obj,total_constrain)
        #solver: GLPK_MI CBC SCIP
        prob.solve(solver='GLPK_MI',verbose=False)
        #print('faster value',t_j.value)
        self.new_node=copy.deepcopy(node)
        assignment=[[[] for i in range(len(self.task_data))] for j in range(len(self.agent_data))]
        z=0
        for i in x_i_j_k.value:
            if i[0]==1:
                agent_i=z//(task_number*max_task_list)
                left=np.mod(z,task_number*max_task_list)
                task_j=left//(max_task_list)
                left=np.mod(left,max_task_list)
                order_k=left
                assignment[agent_i][order_k]=self.task_data[unassigned_tasks[int(task_j)]]
            z=z+1
        for agent_i in range(len(node)):
            self.new_node[agent_i].extend(assignment[agent_i])
        if prob.status=='optimal':
            return prob.value
        else:
            return 0

    def get_lower_bound_with_i_j_l(self,node,assigned_tasks):
        self.get_horizon()
        agent_number=len(self.agent_data)
        task_number=len(self.task_data)
        sub_task_number=len(self.sub_task_type)
        x_i_j_l=cp.Variable(shape=(agent_number*task_number*sub_task_number,1),boolean=True)
        total_constrain=[]
        # ================provide enough serves for the task j (2)
        M2=[[0 for i in range(task_number*sub_task_number)] for j in range(agent_number*task_number*sub_task_number)]
        b2=[[0 for i in range(task_number*sub_task_number)]]
        z=0
        for task_j in range(task_number):
            for sub_l in range(sub_task_number):
                for agent_i in range(agent_number):
                    if self.sub_task_type[sub_l] in self.agent_type[self.agent_data[agent_i][2]]['serve']:
                        #print(self.sub_task_type[sub_l],'in')
                        bil=1
                    else:
                        bil=0
                    num=agent_i*task_number*sub_task_number+\
                            task_j*sub_task_number+\
                            sub_l
                    M2[num][z]=bil
                if self.sub_task_type[sub_l] in self.task_type[self.task_data[task_j][1]][1].keys():
                    b2[0][z]=self.task_type[self.task_data[task_j][1]][1][self.sub_task_type[sub_l]]
                else:
                    b2[0][z]=0
                z=z+1
        enough_constrain=[M2 @ x_i_j_l == b2]
        total_constrain.append(*enough_constrain)
        #===================one agent con only provide the serve it has:(3)
        M3=[[0 for i in range(agent_number*task_number*sub_task_number)] for j in range(agent_number*task_number*sub_task_number)]
        b3=[[0 for i in range(agent_number*task_number*sub_task_number)]]
        z=0
        for agent_i in range(agent_number):
            for task_j in range(task_number):
                    for sub_l in range(sub_task_number):
                        num=agent_i*task_number*sub_task_number+\
                            task_j*sub_task_number+\
                            sub_l
                        M3[num][z]=1
                        if self.sub_task_type[sub_l] in self.agent_type[self.agent_data[agent_i][2]]['serve']:
                            b3[0][z]=1
                        z=z+1
        once_constrain=[M3 @ x_i_j_l <= b3]
        total_constrain.append(*once_constrain)
        #================= one agent execute one task no more than once: (4)
        M4=[[0 for i in range(agent_number*task_number)] for j in range(agent_number*task_number*sub_task_number)]
        b4=[[1 for i in range(agent_number*task_number)]]
        z=0
        for agent_i in range(agent_number):
            for task_j in range(task_number):
                for sub_l in range(sub_task_number):
                    num=agent_i*task_number*sub_task_number+\
                        task_j*sub_task_number+\
                        sub_l
                    M4[num][z]=1
                z=z+1
        constrain4=[M4 @ x_i_j_l <= b4]
        total_constrain.append(*constrain4)
        #=============partial node constrain
        M9=[]
        B9=[]
        for agent_i in range(len(node)):
            for order_k in node[agent_i]:
                m=[0 for i in range(agent_number*task_number*sub_task_number)]
                task_j=order_k[0][0]
                sub_l=self.sub_task_type.index(order_k[1])
                num=agent_i*task_number*sub_task_number+\
                    task_j*sub_task_number+\
                    sub_l
                m[num]=1
                b=1
                M9.append(m)
                B9.append([b])
        if not M9==[]:
            M91=self.Turn_Matrix(M9)
            B91=self.Turn_Matrix(B9)
            constrain9=[M91 @ x_i_j_l==B91]
            total_constrain.append(*constrain9)
    #================= minium motion
        new_task_time_set={}
        for task_j in range(task_number):
            time_table=[]
            m=[0 for i in range(agent_number*task_number*sub_task_number)]
            for agent in self.agent_data:
                time=self.get_distance(self.task_data[task_j][2],agent[1])/self.agent_type[agent[2]]['velocity']
                time_table.append(time)
            for task in self.task_data:
                time=self.get_distance(self.task_data[task_j][2],self.task_data[task[0]][2])/2
                time_table.append(time)
            new_task_time=self.task_type[self.task_data[task_j][1]][0]+min(time_table)
            new_task_time_set[task_j]=new_task_time
        M6=[]
        for agent_i in range(len(self.agent_data)):
            m=[0 for o in range(agent_number*task_number*sub_task_number)]
            for task_j in range(task_number):
                for sub_l in range(len(self.sub_task_type)):
                    num=agent_i*task_number*sub_task_number+\
                    task_j*sub_task_number+\
                    sub_l
                    m[num]=new_task_time_set[task_j]
            M6.append(m)
        M61=self.Turn_Matrix(M6)
        total_constrain=[*enough_constrain,*once_constrain,*constrain4]
        obj = cp.Minimize(cp.max(M61 @ x_i_j_l))
        prob=cp.Problem(obj,total_constrain)
        #solver: GLPK_MI CBC SCIP
        prob.solve(solver='GLPK_MI')
        print('low bound:',prob.value)
        if prob.status=='optimal':
            return prob.value
        else:
            return 0

    def get_lower_bound_online(self,node,assigned_tasks,extro_constrain):

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
        T51=self.Turn_Matrix(T5)
        b=[[extro_constrain.begin_time[i]] for i in range(agent_number)]
        [M51 @ x_i_j]
        [T5 @ t_i]
        constrain5=[M51 @ x_i_j+T5 @ t_i >=b]
        total_constrain.append(*constrain5)
        obj_1 = cp.Minimize(cp.max(t_i))

        prob_1=cp.Problem(obj_1,total_constrain)
        #solver: GLPK_MI CBC SCIP
        prob_1.solve(solver='GLPK_MI')

        print('low bound:',prob_1.value)
        if prob_1.status=='optimal':
            return prob_1.value
        else:
            return 0

    def branching_routine(self,method='A*'):
        if method=='DFS':
            parent_node,task,_,_=self.branch_tree.pop()
            #print('child_nodes',task)
            child_nodes=self.exten_child_nodes(parent_node,task)
            return child_nodes
        if method=='BFS':
            parent_node,task,_,_=self.branch_tree.pop(0)
            child_nodes=self.exten_child_nodes(parent_node,task)
            return child_nodes
        if method=='A*':
            if self.Astar_table==[]:
                self.generate_Astar_table()
            parent_node,task,up,low=self.fetch_node_with_Astar()
            child_nodes=self.exten_child_nodes(parent_node,task)
            return child_nodes

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
            return max(time_list)
        begin_time_list=[]
        for agent in node:
            if len(agent)==0:
                begin_time_list.append(0)
            else:
                begin_time_list.append(time_list[assigned_task_dic[agent[-1][0][0]]])
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
        M_time=[[0  for i in range(agent_number)] for j in range(agent_number * task_number)]
        b_time=[[begin_time_list[j]] for j in range(agent_number)]
        T_time=[]
        for agent_i in range(agent_number):
            t=[0 for o in range(agent_number)]
            t[agent_i]=1
            for task_j in task_dic.keys():
                num=agent_i*task_number+task_dic[task_j]
                M_time[num][agent_i]=-new_task_time_set[task_j]
                self.task_data[task_j][0]
            T_time.append(t)
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

    #================= minium motion
        #M5=[]
        #T5=[]
        #for agent_i in range(len(self.agent_data)):
        #    t=[0 for o in range(agent_number)]
        #    t[agent_i]=1
        #    m=[0 for o in range(agent_number*task_number)]
        #    for task_j in task_dic.keys():
       #         num=agent_i*task_number+task_dic[task_j]
        #        m[num]=-new_task_time_set[task_dic[task_j]]
       #     M5.append(m)
        #    T5.append(t)
        #M51=self.Turn_Matrix(M5)
       # b=[[begin_time_list[i]] for i in range(agent_number)]
        #constrain5=[M51 @ x_i_j+T5 @ t_i >=b]
        #total_constrain.append(*constrain5)
        obj_1 = cp.Minimize(cp.max(t_i))

        prob_1=cp.Problem(obj_1,total_constrain)
        #solver: GLPK_MI CBC SCIP
        prob_1.solve(solver='GLPK_MI')

        print('low bound:',prob_1.value)
        if prob_1.status=='optimal':
            return prob_1.value
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

    def opt_for_partial_assigment(self,node,assign_task):
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
        for i,j in self.poset:
            if self.task_data[i][0] in assign_task and self.task_data[j][0] in assign_task:
                m=[0 for l in range(len(assign_task))]
                m[assign_task_dic[self.task_data[i][0]]]=1
                m[assign_task_dic[self.task_data[j][0]]]=-1
                b=-self.task_type[self.task_data[j][1]][0]
                M1.append(m)
                B1[0].append(-self.task_type[self.task_data[j][1]][0])
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
                #print(node[agent_i])
                c=assign_task_dic[node[agent_i][0][0][0]]
                m[c]=1
                #b=self.get_distance(self.agent_data[agent_i][1],node[agent_i][0][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                #    self.task_type[node[agent_i][0][0][1]][0]
                M2.append(m)
                B2[0].append(self.get_distance(self.agent_data[agent_i][1],node[agent_i][0][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
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
        prob.solve(solver=cp.SCS)
        if prob.status=='optimal':
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
            #print(i)
            assign_task_dic[i[0]]=t
            t=t+1

        end_time=cp.Variable(shape=(len(assign_task),1),name='endtime',nonneg=True)
        total_constrain=[]
        M1=[]
        B1=[[]]
        for i,j in self.poset:
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
        if not M1==[]:
            M11=self.Turn_Matrix(M1)
            constraint1=[M11 @ end_time <= B1]
            total_constrain.append(*constraint1)
#=======motion_constrain
        M2=[]
        B2=[[]]
        for agent_i in range(len(self.agent_data)):
            if len(node[agent_i])>0:
                m=[0 for i in range(len(assign_task))]
                if not node[agent_i][0][0][0] in  assign_task_dic.keys():
                    s=1
                c=assign_task_dic[node[agent_i][0][0][0]]
                m[c]=1
                #print(node[agent_i][0][0][2])
                x1=extro_constrain.agent_pose[agent_i]
                x2=self.position[node[agent_i][0][0][2]]
                dis=((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)**0.5
                #b=self.get_distance(extro_constrain.agent_pose[agent_i],node[agent_i][0][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                #    self.task_type[node[agent_i][0][0][1]][0]
                M2.append(m)
                B2[0].append(dis/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                    extro_constrain.task_execute_time[node[agent_i][0][0][0]]+extro_constrain.begin_time[agent_i])
            if len(node[agent_i])>1:
                for task in range(len(node[agent_i])-1):
                    m=[0 for i in range(len(assign_task))]
                    c=assign_task_dic[node[agent_i][task][0][0]]
                    m[c]=-1
                    if not node[agent_i][task+1][0][0] in  assign_task_dic.keys():
                        s=1
                    #print(assign_task_dic.keys())
                    #print(node[agent_i][task+1][0][0])
                    c=assign_task_dic[node[agent_i][task+1][0][0]]
                    m[c]=1
                    b=self.get_distance(node[agent_i][task][0][2],node[agent_i][task+1][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                        extro_constrain.task_execute_time[node[agent_i][task+1][0][0]]
                    M2.append(m)
                    B2[0].append((b))
        M21=self.Turn_Matrix(M2)
        constraint2=[M21 @ end_time >= B2]# constraint of poset
        total_constrain.append(*constraint2)
        list1=[[1] for task in assign_task]
        obj = cp.Minimize(list1 @ end_time)
        prob=cp.Problem(obj,total_constrain)
        prob.solve(solver=cp.SCS)
        if prob.status=='optimal':
            return prob.value,end_time.value,assign_task_dic
        else:
            return self.horizon,[],assign_task_dic


    def Turn_Matrix(self,M):
        r = [[] for i in M[0]]
        for i in M:
            for j in range(len(i)) :
                r[j].append(i[j])
        return  r

    def get_horizon(self):
        self.horizon=10000
        #for i in self.task_data:
        #    self.horizon=self.task_type[i[1]][0]*2+self.horizon+100

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
