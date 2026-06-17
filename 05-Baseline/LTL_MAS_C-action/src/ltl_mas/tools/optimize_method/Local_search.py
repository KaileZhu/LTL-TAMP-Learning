import copy
import cvxpy as cp
import numpy as np
import random
from collections import Counter
from itertools import product as iter_product
from itertools import combinations as iter_com
import time as time_fun
import scipy.optimize as sco

class Local_Search(object):
    def __init__(self,poset,task_data,input_data):#position,agent_data,task_data,task_type,sub_task_type,agent_type):
        self.poset=poset
        self.position=input_data.position
        self.agent_data=input_data.agent_data
        self.task_data=task_data
        self.task_type=input_data.task_type
        self.sub_task_type=input_data.sub_task_type
        self.agent_type=input_data.agent_type
        self.get_horizon()

    def get_initial_node_for_local_search(self):
        '''
        using some rule to generate a initial node
        '''
        init_node=[[] for i in self.agent_data]
        sequence=[(set(),init_node)]
        task_set=set(range(len(self.task_data)))
        un_found=1
        while sequence!=[] and un_found:
            root_node=sequence.pop()
            assiged_task=root_node[0]
            init_node=root_node[1]
            #print(assiged_task)
            un_assig_task=task_set-assiged_task
            to_assig_task=random.sample(un_assig_task,1)[0]
            sub_task_list=self.task_type[self.task_data[to_assig_task][1]][1]
            feasible={}
            for sub_task,num in sub_task_list.items():
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
                un_found=0
        self.node=init_node

    def remove1(self,task):
        '''
        task type as :(0,'goto','b')
        '''
        removed_nodeset=[]
        for agent in range(len(self.node)):
            #print(range(len(self.node[agent])))
            for i in range(len(self.node[agent])):
                #print(i)
                if self.node[agent][i][0]==task:
                    removed_node=copy.deepcopy(self.node)
                    subtask=removed_node[agent].pop(i)
                    removed_nodeset.append((removed_node,subtask))
                    break
        return removed_nodeset

    def remove2(self,task):
        '''
        task type as :(0,'goto','b')
        '''
        removed_node=copy.deepcopy(self.node)
        for agent in range(len(self.node)):
            #print(range(len(self.node[agent])))
            for i in range(len(self.node[agent])):
                #print(i)
                if self.node[agent][i][0]==task:
                    removed_node[agent].pop(i)
                    continue
        return removed_node

    def place1(self,removed_nodeset):
        placed_set=[]
        for removed_node,subtask in removed_nodeset:
            for agent_i in range(len(removed_node)):
                if not subtask[1] in self.agent_type[self.agent_data[agent_i][2]]['serve']:
                    continue
                label=0
                for oldsub in removed_node[agent_i]:
                    if oldsub[0][0]==subtask[0][0]:
                        label=1
                        break
                if label:
                    continue
                for i in range(len(removed_node[agent_i])+1):
                    if self.check_poset(removed_node[agent_i],i,subtask):
                        new_placed_node=copy.deepcopy(removed_node)
                        new_placed_node[agent_i].insert(i,subtask)
                        placed_set.append(new_placed_node)
        return placed_set

    def place_agent(self,removed_nodeset,task):
        #find the feasible set
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
        agent_list=iter_product(*pot_agent_list)
        return self.place_order(removed_nodeset,agent_list,sub_task_list,agent_num,task)

    def place_order(self,removed_node,agent_list,sub_task_list,agent_num,task):
        new_neighbours=[]
        for assig_list in agent_list:
            t=[]
            for i in assig_list:
                t.extend(list(i))
            if len(Counter(t))<agent_num:
                continue
            order_list=[]
            sub_task_list2=[]
            agent_list2=[]
            for agent_i in range(len(assig_list)):
                for i in assig_list[agent_i]:
                    agent_list2.append(i)
                    sub_list=[]
                    for order_k in range(len(removed_node[i])+1):
                        if self.check_poset(removed_node[i],order_k,[task]):
                            sub_list.append(order_k)
                    sub_task_list2.append(sub_task_list[agent_i])
                    order_list.append(sub_list)
            final_assigs=iter_product(*order_list)
            for assig in final_assigs:
                new_node=copy.deepcopy(removed_node)
                for i in range(len(assig)):
                    #print(assig[i])
                    #print(sub_task_list[i])
                    new_sub_task=(task,sub_task_list2[i])
                    new_node[agent_list2[i]].insert(assig[i],new_sub_task)
                new_neighbours.append(new_node)
        print('find',len(new_neighbours),'in task',task)
        return  new_neighbours

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

    def find_neighbour(self,type=1):
        self.neighbour_list=[]
        if type==1:
            for i in self.task_data:
                removed_nodeset=self.remove1(i)
                self.neighbour_list.extend(self.place1(removed_nodeset))
        if type==2:
            for i in self.task_data:
                removed_nodeset=self.remove2(i)
                self.neighbour_list.extend(self.place_agent(removed_nodeset,i))
        print('found neighbour:',len(self.neighbour_list))
        self.neighbour_list_valie=[]
        self.neighbour_list_x=[]
        ass=range(len(self.task_data))
        for node in self.neighbour_list:
            #self.neighbour_list_valie.append(self.opt_function_under_local_search_with_cp_model(node))
            val,time=self.opt_function_under_local_search_with_cvxpy(node)
            #val,time=self.opt_for_partial_assigment(node,ass)
            self.neighbour_list_valie.append(val)
            self.neighbour_list_x.append(time)
        min_value=min(self.neighbour_list_valie)
        new_node_id=self.neighbour_list_valie.index(min_value)
        new_node=self.neighbour_list[new_node_id]
        print('new_optiaml_value is:',min_value)
        if self.node==new_node:
            print('Achieve local maximum')
            i=1
            return new_node,i,min_value
        else:
            i=0
            return new_node,i,min_value

    def local_search(self,type=1):
        j=0
        i=0
        self.get_initial_node_for_local_search()
        while (j<30) and i==0:
            print('in round :',j+1)
            new_node,i,opt=self.find_neighbour(type)
            self.node=new_node
            #if i==1:
                #print('opt:',opt)
                #print(new_node)
            j=j+1
        self.print_answer()

    def opt_function_under_local_search_with_cvxpy(self,node):
        self.get_horizon()
        end_time=cp.Variable(shape=(len(self.task_data),1),name='endtime',nonneg=True)
        M1=[]
        B1=[[]]
        for i,j in self.poset:
            m=[0 for i in range(len(self.task_data))]
            m[i]=1
            m[j]=-1
            b=-self.task_type[self.task_data[j][1]][0]
            M1.append(m)
            B1[0].append(b)
        M11=self.Turn_Matrix(M1)
        constraint1=[M11 @ end_time <= B1]
        M2=[]
        B2=[[]]
        for agent_i in range(len(self.agent_data)):
            if len(node[agent_i])>0:
                m=[0 for i in range(len(self.task_data))]
                m[node[agent_i][0][0][0]]=1
                b=self.get_distance(self.agent_data[agent_i][1],node[agent_i][0][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                    self.task_type[node[agent_i][0][0][1]][0]
                M2.append(m)
                B2[0].append(b)
            if len(node[agent_i])>1:
                for task in range(len(node[agent_i])-1):
                    m=[0 for i in range(len(self.task_data))]
                    m[node[agent_i][task][0][0]]=-1
                    m[node[agent_i][task+1][0][0]]=1
                    b=self.get_distance(node[agent_i][task][0][2],node[agent_i][task+1][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                        self.task_type[node[agent_i][task+1][0][1]][0]
                    M2.append(m)
                    B2[0].append((b))
        M21=self.Turn_Matrix(M2)
        constraint2=[M21 @ end_time >= B2]# constraint of poset
        constraints=[*constraint1,*constraint2]
        obj = cp.Minimize(cp.max(end_time))
        prob=cp.Problem(obj,constraints)
        prob.solve(solver=cp.SCS)
        if prob.status=='optimal':
            #print('opt:',prob.value)
            #print('t:',end_time.value)
            return prob.value,end_time.value
        else:
            return self.horizon,[]

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
                m=[0 for i in range(len(assign_task))]
                m[assign_task_dic[self.task_data[i][0]]]=1
                m[assign_task_dic[self.task_data[j][0]]]=-1
                b=-self.task_type[self.task_data[j][1]][0]
                M1.append(m)
                B1[0].append(-self.task_type[self.task_data[j][1]][0])
        if not M1==[]:
            M11=self.Turn_Matrix(M1)
            constraint1=[M11 @ end_time <= B1]
            total_constrain.append(*constraint1)
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
                b=self.get_distance(self.agent_data[agent_i][1],node[agent_i][0][0][2])/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                    self.task_type[node[agent_i][0][0][1]][0]
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
        obj = cp.Minimize(cp.max(end_time))
        prob=cp.Problem(obj,total_constrain)
        prob.solve(solver=cp.SCS)
        if prob.status=='optimal':
            return prob.value,end_time.value
        else:
            return self.horizon,[]


    def print_answer(self):
        task_number=len(self.task_data)
        max_task_list=int(len(self.task_data))
        sub_task_number=len(self.sub_task_type)
        self.assignment=[[[] for i in range(len(self.task_data))] for j in range(len(self.agent_data))]
        z=0
        for i in self.valueofx_i_j_k_l:
            if i[0]==1:
                agent_i=z//(task_number*max_task_list*sub_task_number)
                left=np.mod(z,task_number*max_task_list*sub_task_number)
                task_j=left//(max_task_list*sub_task_number)
                left=np.mod(left,max_task_list*sub_task_number)
                order_k=left//(sub_task_number)
                sub_l=np.mod(left,sub_task_number)
                sub=(self.task_data[int(task_j)],self.sub_task_type[int(sub_l)])
                self.assignment[agent_i][order_k]=[sub]
            z=z+1

    def Turn_Matrix(self,M):
        r = [[] for i in M[0]]
        for i in M:
            for j in range(len(i)) :
                r[j].append(i[j])
        return  r

    def get_horizon(self):
        self.horizon=0
        for i in self.task_data:
            self.horizon=self.task_type[i[1]][0]*2+self.horizon

    def get_distance(self,i,j):
        pos1=self.position[i][0]-self.position[j][0]
        pos2=self.position[i][1]-self.position[j][1]
        lenth=(pos1**2+pos2**2)**0.5
        return lenth

    def print_answer(self):
        for i in range(len(self.node)):
            print('agent ',i,'task list is:',self.node[i])


