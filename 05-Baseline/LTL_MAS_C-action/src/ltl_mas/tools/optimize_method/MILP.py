import cvxpy as cp
import numpy as np
from collections import Counter

class MILP_CVXPY(object):
    def __init__(self,poset,task_data,input_data):#,position,agent_data,task_data,task_type,sub_task_type,agent_type):
        self.poset=poset
        self.position=input_data.position
        self.agent_data=input_data.agent_data
        self.task_data=task_data
        self.task_type=input_data.task_type
        self.sub_task_type=input_data.sub_task_type
        self.agent_type=input_data.agent_type

    def Base_OPT_MILP_of_cvxpy(self):
        self.get_horizon()
        agent_number=len(self.agent_data)
        task_number=len(self.task_data)
        max_task_list=int(len(self.task_data))
        sub_task_number=len(self.sub_task_type)
        self.x_i_j_k_l=cp.Variable(shape=(agent_number*task_number*max_task_list*sub_task_number,1),boolean=True)
        self.t_j=cp.Variable(shape=(task_number,1),nonneg=True)
        con1=self.Temporal_con_of_equation_1()
        con15=self.Neq_con_of_equation_2()
        con2=self.enough_con_of_equation_2()
        con3=self.serve_limit_con_of_equation_3()
        con4=self.once_task_con_of_equation_4()
        con5=self.one_task_a_time_con_of_equation_5()
        con6=self.equation_6()
        con7=self.equation_7()
        con8=self.equation_8()
        total_constrain=[*con1,*con2,*con3,*con4,*con5,*con6,*con7,*con8,*con15]
        tim=[[]]
        for i in self.task_data:
            tim[0].append(self.task_type[i[1]][0])
        obj = cp.Minimize(cp.max(self.t_j+tim))
        prob=cp.Problem(obj,total_constrain)
        #solver: GLPK_MI CBC SCIP
        prob.solve(solver='GLPK_MI',verbose=True)
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
                self.assignment[agent_i][order_k]=sub
            z=z+1
        for agent_i in self.assignment:
            remove_list=[]
            for i in range(len(agent_i)):
                if agent_i[i]==[]:
                    remove_list.append(i)
            for i in reversed(remove_list):
                agent_i.remove([])

    def Temporal_con_of_equation_1(self):#(1)
        if not self.poset=={}:
            M=[[0 for i in self.poset['<=']] for j in self.task_data]
            b=[[]]
            line=0
            for j1,j2 in self.poset['<=']:
                M[j1][line]=1
                M[j2][line]=-1
                #b[0].append(-self.task_type[self.task_data[j1][1]][0])
                b[0].append(0)
                line=line+1
            return  [M @ self.t_j <= b]

    def Neq_con_of_equation_2(self):
        self.time_budget=10000
        if not self.poset=={}:
            M=[]
            count=0
            for i,j in self.poset['!=']:
                count=count+1
                #if count>5:
                #    break
                m=[[0] for l in range(len(self.task_data))]
                m[self.task_data[i][0]][0]=1
                m[self.task_data[j][0]][0]=-1
                bool_for_x=cp.Variable(1,boolean=True)
                constrain0=[m @ self.t_j - self.task_type[self.task_data[j][1]][0]  -bool_for_x * self.time_budget+self.time_budget>=0]
                constrain1=[m @ self.t_j + self.task_type[self.task_data[i][1]][0] - bool_for_x * self.time_budget <=0]
                M.append(*constrain0)
                M.append(*constrain1)
            return M
        if not self.poset=={}:
            M=[[0 for i in self.poset['!=']] for j in self.task_data]
            b=[[]]
            line=0
            for j1,j2 in self.poset['!=']:
                M[j1][line]=1
                M[j2][line]=-1
                b[0].append(-self.task_type[self.task_data[j1][1]][0])
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
                    if self.sub_task_type[sub_l] in self.agent_type[self.agent_data[agent_i][2]]['serve']:
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
                        if self.sub_task_type[sub_l] in self.agent_type[self.agent_data[agent_i][2]]['serve']:
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
        max_task_list=len(self.task_data)
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
                            b=self.get_distance(self.task_data[task_j1][2],
                                                self.task_data[task_j2][2]
                                                )/self.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                              self.task_type[self.task_data[task_j1][1]][0]-2*self.horizon
                            M7.append(m)
                            T7.append(t)
                            B7.append([b])
        self.M7=M7
        self.T7=T7
        self.B7=B7
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
                    B8[0][z]=self.get_distance(self.agent_data[agent_i][1],self.task_data[task_j][2])/\
                             self.agent_type[self.agent_data[agent_i][2]]['velocity']-self.horizon
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
        self.horizon=0
        for i in self.task_data:
            self.horizon=self.task_type[i[1]][0]*2+self.horizon+100

    def get_distance(self,i,j):
        #lenth=self.position[(i,j)]
        #return lenth
        pos1=self.position[i][0]-self.position[j][0]
        pos2=self.position[i][1]-self.position[j][1]
        lenth=(pos1**2+pos2**2)**0.5
        return lenth

    def check_the_value(self,node):
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
        M9=[]
        B9=[]
        for agent_i in range(len(node)):
            for order_k in range(len(node[agent_i])):
                sub_l=self.sub_task_type.index(node[agent_i][order_k][1])
                task_j=node[agent_i][order_k][0][0]
                #print('i',agent_i,'j',task_j,'k',order_k,'l',sub_l)
                m=[0 for i in range(agent_number*task_number*max_task_list*sub_task_number)]
                num=(agent_i)*task_number*max_task_list*sub_task_number+ \
                    (task_j)*max_task_list*sub_task_number+ \
                    (order_k)*sub_task_number +sub_l
                m[num]=1
                #print('num',num)
                b=1
                M9.append(m)
                B9.append([b])
        M91=self.Turn_Matrix(M9)
        B91=self.Turn_Matrix(B9)
        cons9=[M91 @ self.x_i_j_k_l==B91]
        total_constrain.append(*cons9)
        tim=[[]]
        for i in self.task_data:
            tim[0].append(self.task_type[i[1]][0])
        obj = cp.Minimize(cp.max(self.t_j+tim))
        prob=cp.Problem(obj,total_constrain)
        #solver: GLPK_MI CBC SCIP
        prob.solve(solver='GLPK_MI',eps=0.1)
        #print('opt-value:',prob.value)
        print(prob.value)
        print(self.t_j.value)
        if prob.status=='optimal':
            self.valueofx_i_j_k_l=self.x_i_j_k_l.value
            self.valueoft_j=self.t_j.value
            self.print_answer()
            z=1
            for i in self.assignment:
                #print('agent',z,'task list is:',i)
                z=z+1
        print(prob.value)
        #print(node)
        #print(self.valueoft_j)
        return prob