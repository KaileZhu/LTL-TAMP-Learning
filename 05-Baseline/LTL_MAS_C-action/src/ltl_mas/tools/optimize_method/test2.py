from data.input_data.task_data import task_type,task_data,sub_task_type
from data.input_data.agent_data import agent_type,agent_data
from data.input_data.map_data import position
import copy
import time
import cvxpy as cp
from ortools.sat.python import cp_model
import numpy as np


"""
jobs type: 'search' ',goto','formation','surround'
cost time:  '5'      '1'       '3'        '7'

interested position: a (0,0) b(0,5) c(0,10) d(5,0) e(5,5) f(10,5) g (5,10)
task=<> (search_a && <> (goto_b && <> formation_d)) && <> (goto_b &&  <> surround_g)

"""
start=time.time()
poset={(0,1)}#,(2,3)}#,(2,4),(3,4)}
agent_number=len(agent_data)
root_node=[[0,1],[2,3],[4],[5,6,7,8],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]


class neighbour(object):
    def __init__(self,node,poset,position,agent_data,task_data,task_type,sub_task_type,agent_type):
        self.node=node
        self.poset=poset
        self.position=position
        self.agent_data=agent_data
        self.task_data=task_data
        self.task_type=task_type
        self.sub_task_type=sub_task_type
        self.agent_type=agent_type

    def get_initial_node_for_local_search(self):
        '''
        using some rule to generate a initial node
        '''
        init_node=[[] for i in self.agent_data]
        sequence=[(-1,init_node)]
        un_found=1
        while un_found and not sequence==[]:
            root_node=sequence.pop()
            i=root_node[0]+1
            sub_task_list=self.task_type[self.task_data[i]][1]
            for sub_task in sub_task_list.keys():
                1

    def remove(self,i):
        removed_node=[]
        for j in self.node:
            removed_node.append([x for x in j if x!=i])
        self.removed_node=removed_node

    def plance(self,i):
        xt=len(self.removed_node)
        x=1
        y=0
        while(x<=xt):
            #print(x,y)
            #print('len:',len(self.removed_node[x-1]))
            if y>len(self.removed_node[x-1]):
                #print(x,y)
                y=0
                x=x+1
            else:
                c=copy.deepcopy(self.removed_node)
                c[x-1].insert(y,i)
                if self.check_poset(c,x,y):
                    self.neighbour_list.append(c)
                y=y+1

    def check_poset(self,c,x,y):
        label=1
        if len(c[x-1])>=2:
            for i in c[x-1][:y]:
                if (c[x-1][y],i) in self.poset:
                    label=0
            for i in c[x-1][y:]:
                if (i,c[x-1][y]) in self.poset:
                    label=0
                #print(1)
        return  label


    def find_neighbour(self):
        self.neighbour_list=[]
        for i in sum(self.node,[]):
            self.remove(i)
            self.plance(i)
        print('found neighbour:',len(self.neighbour_list))
        self.neighbour_list_valie=[]
        for node in self.neighbour_list:
            #self.neighbour_list_valie.append(self.opt_function_under_local_search_with_cp_model(node))
            self.neighbour_list_valie.append(self.opt_function_under_local_search_with_cvxpy(node))
        min_value=min(self.neighbour_list_valie)
        new_node_id=self.neighbour_list_valie.index(min_value)
        new_node=self.neighbour_list[new_node_id]
        print('new_optiaml_value is:',min_value)
        if self.node==new_node:
            print('Achieve local maximum')
            i=1
            return new_node,i
        else:
            i=0
            return new_node,i

    def local_search(self):
        j=0
        i=0
        while (j<30) and i==0:
            print('in round :',j+1)
            new_node,i=self.find_neighbour()
            self.node=new_node
            j=j+1
        print('round:',j)

    def opt_function_under_local_search_with_cp_model(self,node):
        model=cp_model.CpModel()
        self.get_horizon()
        j=0
        task_var={}
        for i in range(len(self.task_data)):
            suffix='_%i' % (j)
            end_time=model.NewIntVar(0,self.horizon,'end'+suffix)
            task_var[j]=end_time
            j=j+1
        for i,j in self.poset:
            #print(task_var[i],'+',self.task_type[self.task_data[j][1]],'<',task_var[j])
            model.Add(task_var[i]-task_var[j]<=-self.task_type[self.task_data[j][1]])
        for agent in range(len(node)):
            if len(node[agent]) >0:
                #print(task_var[node[agent][0]],'>',self.get_distance(self.task_data[node[agent][0]][2],self.agent_data[agent][1])
                #      ,'+',self.task_type[self.task_data[node[agent][0]][1]])
                model.Add(task_var[node[agent][0]]
                          >=self.get_distance(self.task_data[node[agent][0]][2],self.agent_data[agent][1])
                          +self.task_type[self.task_data[node[agent][0]][1]])
                for i in range(len(node[agent][1:])):
                #    print(task_var[node[agent][i]],'+',self.get_distance(self.task_data[node[agent][i]][2],self.task_data[node[agent][i+1]][2])
                #          ,'+',self.task_type[self.task_data[node[agent][i+1]][1]],'<=',task_var[node[agent][i+1]])
                    model.Add(task_var[node[agent][i]]
                              -task_var[node[agent][i+1]]<=-self.get_distance(self.task_data[node[agent][i]][2],self.task_data[node[agent][i+1]][2])
                              -self.task_type[self.task_data[node[agent][i+1]][1]])
        #print('one function')
        obj_var=model.NewIntVar(0,self.horizon,'makespan')
        model.AddMaxEquality(obj_var,[task_var[var] for var in task_var])
        model.Minimize(obj_var)
        solver =cp_model.CpSolver()
        status=solver.Solve(model)
        if status==4:
            #print(solver.ObjectiveValue())
            return solver.ObjectiveValue()
        else:
            return self.horizon

    def opt_function_under_local_search_with_cvxpy(self,node):
        self.get_horizon()
        end_time=cp.Variable(shape=(len(self.task_data),1),name='endtime',nonneg=True)
        M=[[0 for i in range(len(self.poset))] for j in  range(len(self.task_data)) ]
        b=[[0] for j in range(len(self.poset))]
        l=0
        for i,j in self.poset:
            M[i][l]=1
            M[i][l]=-1
            b[l][0]=-self.task_type[self.task_data[j][1]]
            l=l+1
        constraint=[M @ end_time <= b]# constraint of poset
        M1,B1,M2,B2=[],[],[],[]
        constraint0=[]
        constraint1=[]
        for agent in range(len(node)):
            if len(node[agent]) >0:
                con=[0 for i in range(len(self.task_data))]
                con[node[agent][0]]=1
                b1=self.get_distance(self.task_data[node[agent][0]][2],self.agent_data[agent][1])+self.task_type[self.task_data[node[agent][0]][1]]
                M1.append(con)
                B1.append([b1])
                for i in range(len(node[agent][1:])):
                    con=[0 for i in range(len(self.task_data))]
                    con[node[agent][i]]=1
                    con[node[agent][i+1]]=-1
                    b2=-self.get_distance(self.task_data[node[agent][i]][2],self.task_data[node[agent][i+1]][2])-self.task_type[self.task_data[node[agent][i+1]][1]]
                    M2.append(con)
                    B2.append([b2])
        M1T=self.Turn_Matrix(M1)
        M2T=self.Turn_Matrix(M2)
        constraint0=[M1T @ end_time >= B1]
        constraint1=[M2T @ end_time <= B2]
        constraints=[*constraint,*constraint0,*constraint1]
        obj = cp.Minimize(cp.max(end_time))
        prob=cp.Problem(obj,constraints)
        #print('one function')
        prob.solve(solver=cp.SCS,eps=1)#here I tried to cutdown the accurate and the system become faster as expect.
        return prob.value
        #print(prob.status)
        #print('opt:',prob.value)
        #print('var',end_time.value)

    def opt_function_for_MILP_under_cvxpy(self):
        self.get_horizon()
        agent_number=len(self.agent_data)
        task_number=len(self.task_data)
        max_task_list=int(len(self.task_data))
        sub_task_number=len(self.sub_task_type)
        self.x_i_j_k_l=cp.Variable(shape=(agent_number*task_number*max_task_list*sub_task_number,1),boolean=True)
        self.t_j=cp.Variable(shape=(task_number,1),nonneg=True)
        total_constrain=[]
        #--------------------- partlai order constraints (1)
        if not self.poset=={}:
            M=[[0 for i in self.poset] for j in self.task_data]
            b=[[0] for j in self.poset]
            line=0
            for j1,j2 in self.poset:
                M[j1][line]=1
                M[j2][line]=-1
                b[line]=[-self.task_type[self.task_data[j1][1]][0]]
                line=line+1
            poset_constrain=[M @ self.t_j <= b]
            total_constrain.append(*poset_constrain)
        # ================provide enough serves for the task j (2)
        M2=[[0 for i in range(task_number*sub_task_number)] for j in range(agent_number*task_number*max_task_list*sub_task_number)]
        b2=[[0 for i in range(task_number*sub_task_number)]]
        z=0
        for task_j in range(task_number):
            for sub_l in range(sub_task_number):
                for agent_i in range(agent_number):
                    if self.sub_task_type[sub_l] in self.agent_type[self.agent_data[agent_i][2]]:
                        #print(self.sub_task_type[sub_l],'in')
                        bil=1
                    else:
                        bil=0
                    for order_k in range(max_task_list):
                        num=agent_i*task_number*max_task_list*sub_task_number+\
                            task_j*max_task_list*sub_task_number+\
                            order_k*sub_task_number+sub_l
                        M2[num][z]=bil
                if self.sub_task_type[sub_l] in self.task_type[self.task_data[task_j][1]][1].keys():
                    b2[0][z]=self.task_type[self.task_data[task_j][1]][1][self.sub_task_type[sub_l]]
                else:
                    b2[0][z]=0
                z=z+1
        enough_constrain=[M2 @ self.x_i_j_k_l == b2]
        total_constrain.append(*enough_constrain)
        #===================one agent con only provide the serve it has:(3)
        M3=[[0 for i in range(agent_number*task_number*max_task_list*sub_task_number)] for j in range(agent_number*task_number*max_task_list*sub_task_number)]
        b3=[[0 for i in range(agent_number*task_number*max_task_list*sub_task_number)]]
        z=0
        for agent_i in range(agent_number):
            for task_j in range(task_number):
                for order_k in range(max_task_list):
                    for sub_l in range(sub_task_number):
                        num=agent_i*task_number*max_task_list*sub_task_number+\
                            task_j*max_task_list*sub_task_number+\
                            order_k*sub_task_number+sub_l
                        M3[num][z]=1
                        if self.sub_task_type[sub_l] in self.agent_type[self.agent_data[agent_i][2]]:
                            b3[0][z]=1
                        z=z+1
        once_constrain=[M3 @ self.x_i_j_k_l <= b3]
        total_constrain.append(*once_constrain)
        #================= one agent execute one task no more than once: (4)
        M4=[[0 for i in range(agent_number*task_number)] for j in range(agent_number*task_number*max_task_list*sub_task_number)]
        b4=[[1 for i in range(agent_number*task_number)]]
        z=0
        for agent_i in range(agent_number):
            for task_j in range(task_number):
                for order_k in range(max_task_list):
                    for sub_l in range(sub_task_number):
                        num=agent_i*task_number*max_task_list*sub_task_number+\
                            task_j*max_task_list*sub_task_number+\
                            order_k*sub_task_number+sub_l
                        M4[num][z]=1
                z=z+1
        constrain4=[M4 @ self.x_i_j_k_l <= b4]
        total_constrain.append(*constrain4)
        #================= one agent at any time can only execute no more than one task (5)
        M5=[[0 for i in range(agent_number*max_task_list)] for j in range(agent_number*task_number*max_task_list*sub_task_number)]
        b5=[[0 for i in range(agent_number*max_task_list)]]
        z=0
        for agent_i in range(agent_number):
            for order_k in range(max_task_list):
                for task_j in range(task_number):
                    for sub_l in range(sub_task_number):
                        num=agent_i*task_number*max_task_list*sub_task_number+\
                            task_j*max_task_list*sub_task_number+\
                            order_k*sub_task_number+sub_l
                        M5[num][z]=1
                b5[0][z]=1
                z=z+1
        one_task_constrain=[M5 @ self.x_i_j_k_l <= b5]
        total_constrain.append(*one_task_constrain)
        #=============== no jump constraint(6)
        M6=[[0 for i in range(agent_number*(max_task_list-1))] for j in range(agent_number*task_number*max_task_list*sub_task_number)]
        B6=[[0 for i in range(agent_number*(max_task_list-1))]]
        z=0
        for agent_i in range(agent_number):
            for order_k in range(max_task_list-1):
                for task_j in range(task_number):
                    for sub_l in range(sub_task_number):
                        num1=agent_i*task_number*max_task_list*sub_task_number+\
                            task_j*max_task_list*sub_task_number+\
                            order_k*sub_task_number+sub_l
                        num2=agent_i*task_number*max_task_list*sub_task_number+\
                            task_j*max_task_list*sub_task_number+ \
                             (order_k+1)*sub_task_number+sub_l
                        M6[num1][z]=1
                        M6[num2][z]=-1
                z=z+1
        continue_constrain=[M6 @ self.x_i_j_k_l >= B6]
        if not continue_constrain==[]:
            total_constrain.append(*continue_constrain)
        #============== motion constrain (7)
        M7=[]
        T7=[]
        B7=[]
        for agent_i in range(agent_number):
            for task_j1 in range(task_number):
                for task_j2 in range(task_number):
                    if not task_j1==task_j2:
                        t=[0 for i in range(task_number)]
                        t[task_j1]=-1
                        t[task_j2]=1
                        for order_k in range(max_task_list-1):
                            m=[0 for i in range(agent_number*max_task_list*task_number*sub_task_number)]
                            for sub_l in range(sub_task_number):
                                numj1=agent_i*task_number*max_task_list*sub_task_number+\
                                task_j1*max_task_list*sub_task_number+\
                                order_k*sub_task_number+sub_l
                                numj2=agent_i*task_number*max_task_list*sub_task_number+\
                                task_j2*max_task_list*sub_task_number+ \
                                      (order_k+1)*sub_task_number+sub_l
                                m[numj1]=-self.horizon
                                m[numj2]=-self.horizon
                            b=self.get_distance(self.task_data[task_j1][2],self.task_data[task_j2][2])+\
                                self.task_type[self.task_data[task_j1][1]][0]-\
                                2*self.horizon
                            M7.append(m)
                            T7.append(t)
                            B7.append([b])
        if not M7==[]:
            M71=self.Turn_Matrix(M7)
            T71=self.Turn_Matrix(T7)
            B71=self.Turn_Matrix(B7)
            motion_constrain=[M71 @ self.x_i_j_k_l + T71 @ self.t_j >= B71]
            #total_constrain.append(*motion_constrain)
        #========================constrain (8)
        M8=[[0 for i in range(agent_number*task_number)] for j in range(agent_number*task_number*max_task_list*sub_task_number)]
        t8=[[0 for i in range(agent_number*task_number)] for j in range(task_number)]
        B8=[[0 for i in range(agent_number*task_number)]]
        z=0
        for agent_i in range(agent_number):
                for task_j in range(task_number):
                    for sub_l in range(sub_task_number):
                        num=agent_i*task_number*max_task_list*sub_task_number+\
                            task_j*max_task_list*sub_task_number+sub_l
                        M8[num][z]=-self.horizon
                    t8[task_j][z]=1
                    B8[0][z]=self.get_distance(self.agent_data[agent_i][1],self.task_data[task_j][2])-self.horizon
                    #B8[0][z]=10
                    z=z+1
        motion_constrain2=[M8 @ self.x_i_j_k_l + t8 @ self.t_j >= B8]
        #total_constrain.append(*motion_constrain2)
        total_constrain=[*poset_constrain,*enough_constrain,*one_task_constrain,*constrain4,*continue_constrain,*once_constrain,*motion_constrain,*motion_constrain2]
        tim=[[]]
        for i in self.task_data:
            tim[0].append(self.task_type[i[1]][0])
        obj = cp.Minimize(cp.max(self.t_j+tim))
        prob=cp.Problem(obj,total_constrain)
        #solver: GLPK_MI CBC SCIP
        prob.solve(solver='GLPK_MI',verbose = True,eps=1)
        print('opt-value:',prob.value)
        if prob.status=='optimal':
            self.valueofx_i_j_k_l=self.x_i_j_k_l.value
            self.valueoft_j=self.t_j.value
            self.print_answer()
            z=1
            for i in self.assignment:
                print('agent',z,'task list is:',i)
                z=z+1
        return prob

    def base_MILP_of_cvxpy(self):
        self.get_horizon()
        agent_number=len(self.agent_data)
        task_number=len(self.task_data)
        max_task_list=int(len(self.task_data))
        sub_task_number=len(self.sub_task_type)
        self.x_i_j_k_l=cp.Variable(shape=(agent_number*task_number*max_task_list*sub_task_number,1),boolean=True)
        self.t_j=cp.Variable(shape=(task_number,1),nonneg=True)
        con1=self.Temporal_con_of_equation_1()
        con2=self.enough_con_of_equation_2()
        con3=self.serve_limit_con_of_equation_3()
        con4=self.once_task_con_of_equation_4()
        con5=self.one_task_a_time_con_of_equation_5()
        con6=self.equation_6()
        con7=self.equation_7()
        con8=self.equation_8()
        total_constrain=[*con1,*con2,*con3,*con4,*con5,*con6,*con7,*con8]
        tim=[[]]
        for i in self.task_data:
            tim[0].append(self.task_type[i[1]][0])
        obj = cp.Minimize(cp.max(self.t_j+tim))
        prob=cp.Problem(obj,total_constrain)
        #solver: GLPK_MI CBC SCIP
        prob.solve(solver='GLPK_MI',verbose = True,eps=1)
        print('opt-value:',prob.value)
        if prob.status=='optimal':
            self.valueofx_i_j_k_l=self.x_i_j_k_l.value
            self.valueoft_j=self.t_j.value
            self.print_answer()
            z=1
            for i in self.assignment:
                print('agent',z,'task list is:',i)
                z=z+1
        return prob

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

    def Temporal_con_of_equation_1(self):#(1)
        if not self.poset=={}:
            M=[[0 for i in self.poset] for j in self.task_data]
            b=[[0] for j in self.poset]
            line=0
            for j1,j2 in self.poset:
                M[j1][line]=1
                M[j2][line]=-1
                b[line]=[-self.task_type[self.task_data[j1][1]][0]]
                line=line+1
            return  [M @ self.t_j <= b]

    def enough_con_of_equation_2(self):#(2)
        agent_number=len(self.agent_data)
        task_number=len(self.task_data)
        max_task_list=int(len(self.task_data))
        sub_task_number=len(self.sub_task_type)
        M2=[[0 for i in range(task_number*sub_task_number)] for j in range(agent_number*task_number*max_task_list*sub_task_number)]
        b2=[[0 for i in range(task_number*sub_task_number)]]
        z=0
        for task_j in range(task_number):
            for sub_l in range(sub_task_number):
                for agent_i in range(agent_number):
                    if self.sub_task_type[sub_l] in self.agent_type[self.agent_data[agent_i][2]]:
                        bil=1
                    else:
                        bil=0
                    for order_k in range(max_task_list):
                        num=agent_i*task_number*max_task_list*sub_task_number+\
                            task_j*max_task_list*sub_task_number+\
                            order_k*sub_task_number+sub_l
                        M2[num][z]=bil
                if self.sub_task_type[sub_l] in self.task_type[self.task_data[task_j][1]][1].keys():
                    b2[0][z]=self.task_type[self.task_data[task_j][1]][1][self.sub_task_type[sub_l]]
                else:
                    b2[0][z]=0
                z=z+1
        enough_constrain=[M2 @ self.x_i_j_k_l == b2]
        return enough_constrain

    def serve_limit_con_of_equation_3(self):
        #===================one agent con only provide the serve it has:(3)
        agent_number=len(self.agent_data)
        task_number=len(self.task_data)
        max_task_list=int(len(self.task_data))
        sub_task_number=len(self.sub_task_type)
        M3=[[0 for i in range(agent_number*task_number*max_task_list*sub_task_number)] for j in range(agent_number*task_number*max_task_list*sub_task_number)]
        b3=[[0 for i in range(agent_number*task_number*max_task_list*sub_task_number)]]
        z=0
        for agent_i in range(agent_number):
            for task_j in range(task_number):
                for order_k in range(max_task_list):
                    for sub_l in range(sub_task_number):
                        num=agent_i*task_number*max_task_list*sub_task_number+\
                            task_j*max_task_list*sub_task_number+\
                            order_k*sub_task_number+sub_l
                        M3[num][z]=1
                        if self.sub_task_type[sub_l] in self.agent_type[self.agent_data[agent_i][2]]:
                            b3[0][z]=1
                        z=z+1
        once_constrain=[M3 @ self.x_i_j_k_l <= b3]
        return once_constrain

    def once_task_con_of_equation_4(self):
        agent_number=len(self.agent_data)
        task_number=len(self.task_data)
        max_task_list=int(len(self.task_data))
        sub_task_number=len(self.sub_task_type)
        M4=[[0 for i in range(agent_number*task_number)] for j in range(agent_number*task_number*max_task_list*sub_task_number)]
        b4=[[1 for i in range(agent_number*task_number)]]
        z=0
        for agent_i in range(agent_number):
            for task_j in range(task_number):
                for order_k in range(max_task_list):
                    for sub_l in range(sub_task_number):
                        num=agent_i*task_number*max_task_list*sub_task_number+\
                            task_j*max_task_list*sub_task_number+\
                            order_k*sub_task_number+sub_l
                        M4[num][z]=1
                z=z+1
        constrain4=[M4 @ self.x_i_j_k_l <= b4]
        return constrain4

    def one_task_a_time_con_of_equation_5(self):
        agent_number=len(self.agent_data)
        task_number=len(self.task_data)
        max_task_list=int(len(self.task_data))
        sub_task_number=len(self.sub_task_type)
        M5=[[0 for i in range(agent_number*max_task_list)] for j in range(agent_number*task_number*max_task_list*sub_task_number)]
        b5=[[0 for i in range(agent_number*max_task_list)]]
        z=0
        for agent_i in range(agent_number):
            for order_k in range(max_task_list):
                for task_j in range(task_number):
                    for sub_l in range(sub_task_number):
                        num=agent_i*task_number*max_task_list*sub_task_number+\
                            task_j*max_task_list*sub_task_number+\
                            order_k*sub_task_number+sub_l
                        M5[num][z]=1
                b5[0][z]=1
                z=z+1
        one_task_constrain=[M5 @ self.x_i_j_k_l <= b5]
        return  one_task_constrain

    def equation_6(self):
        agent_number=len(self.agent_data)
        task_number=len(self.task_data)
        max_task_list=int(len(self.task_data))
        sub_task_number=len(self.sub_task_type)
        M6=[[0 for i in range(agent_number*(max_task_list-1))] for j in range(agent_number*task_number*max_task_list*sub_task_number)]
        B6=[[0 for i in range(agent_number*(max_task_list-1))]]
        z=0
        for agent_i in range(agent_number):
            for order_k in range(max_task_list-1):
                for task_j in range(task_number):
                    for sub_l in range(sub_task_number):
                        num1=agent_i*task_number*max_task_list*sub_task_number+\
                            task_j*max_task_list*sub_task_number+\
                            order_k*sub_task_number+sub_l
                        num2=agent_i*task_number*max_task_list*sub_task_number+\
                            task_j*max_task_list*sub_task_number+ \
                             (order_k+1)*sub_task_number+sub_l
                        M6[num1][z]=1
                        M6[num2][z]=-1
                z=z+1
        continue_constrain=[M6 @ self.x_i_j_k_l >= B6]
        return  continue_constrain

    def equation_7(self):
        agent_number=len(self.agent_data)
        task_number=len(self.task_data)
        max_task_list=int(len(self.task_data))
        sub_task_number=len(self.sub_task_type)
        M7=[]
        T7=[]
        B7=[]
        for agent_i in range(agent_number):
            for task_j1 in range(task_number):
                for task_j2 in range(task_number):
                    if not task_j1==task_j2:
                        t=[0 for i in range(task_number)]
                        t[task_j1]=-1
                        t[task_j2]=1
                        for order_k in range(max_task_list-1):
                            m=[0 for i in range(agent_number*max_task_list*task_number*sub_task_number)]
                            for sub_l in range(sub_task_number):
                                numj1=agent_i*task_number*max_task_list*sub_task_number+\
                                task_j1*max_task_list*sub_task_number+\
                                order_k*sub_task_number+sub_l
                                numj2=agent_i*task_number*max_task_list*sub_task_number+\
                                task_j2*max_task_list*sub_task_number+ \
                                      (order_k+1)*sub_task_number+sub_l
                                m[numj1]=-self.horizon
                                m[numj2]=-self.horizon
                            b=self.get_distance(self.task_data[task_j1][2],self.task_data[task_j2][2])+\
                                self.task_type[self.task_data[task_j1][1]][0]-\
                                2*self.horizon
                            M7.append(m)
                            T7.append(t)
                            B7.append([b])
        if not M7==[]:
            M71=self.Turn_Matrix(M7)
            T71=self.Turn_Matrix(T7)
            B71=self.Turn_Matrix(B7)
            motion_constrain=[M71 @ self.x_i_j_k_l + T71 @ self.t_j >= B71]
            return  motion_constrain

    def equation_8(self):
        agent_number=len(self.agent_data)
        task_number=len(self.task_data)
        max_task_list=int(len(self.task_data))
        sub_task_number=len(self.sub_task_type)
        M8=[[0 for i in range(agent_number*task_number)] for j in range(agent_number*task_number*max_task_list*sub_task_number)]
        t8=[[0 for i in range(agent_number*task_number)] for j in range(task_number)]
        B8=[[0 for i in range(agent_number*task_number)]]
        z=0
        for agent_i in range(agent_number):
                for task_j in range(task_number):
                    for sub_l in range(sub_task_number):
                        num=agent_i*task_number*max_task_list*sub_task_number+\
                            task_j*max_task_list*sub_task_number+sub_l
                        M8[num][z]=-self.horizon
                    t8[task_j][z]=1
                    B8[0][z]=self.get_distance(self.agent_data[agent_i][1],self.task_data[task_j][2])-self.horizon
                    #B8[0][z]=10
                    z=z+1
        motion_constrain2=[M8 @ self.x_i_j_k_l + t8 @ self.t_j >= B8]
        return motion_constrain2

    def Turn_Matrix(self,M):
        r = [[] for i in M[0]]
        for i in M:
            for j in range(len(i)) :
                r[j].append(i[j])
        return  r

    def get_horizon(self):
        self.horizon=80

    def get_distance(self,i,j):
        pos1=self.position[i][0]-self.position[j][0]
        pos2=self.position[i][1]-self.position[j][1]
        lenth=(pos1**2+pos2**2)**0.5
        return int(lenth)



a=neighbour(root_node,poset,position,agent_data,task_data,task_type,sub_task_type,agent_type)
prob=a.opt_function_for_MILP_under_cvxpy()
a.base_MILP_of_cvxpy()
#a.opt_function_under_local_search_with_cvxpy(root_node)
end=time.time()
print('totally cost',end-start)
