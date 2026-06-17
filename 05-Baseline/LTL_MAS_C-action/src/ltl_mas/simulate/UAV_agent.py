from src.ltl_mas.simulate.arastar import AraStar
from src.ltl_mas.simulate.astar import AStar
from data import input_data
from src.ltl_mas.simulate.field_background import photovoltaic_Env
import copy
import random

class UAV_agent:
    def __init__(self,ID,input_task_type,task_list,related_poset,interested_map,agent_msg,agent_type,initial_node,local_task_time_table):
        self.agent_ID=ID
        self.input_task_type=input_task_type
        self.init_pose=initial_node.copy()
        self.current_pose=initial_node.copy()
        self.task_list=task_list
        self.agent_type=agent_type
        self.sub_serve=agent_msg["serve"]
        self.velocity=agent_msg["velocity"]
        self.interested_map=interested_map
        self.related_poset=related_poset
        #self.next_stage_time=0
        self.current_time=0
        self.action_step_len=1
        self.task_time_table=local_task_time_table
        self.synchronization_label=0
        self.adapt_state=0# here is four state motion | wait for co-operate  |wait for pre-requirement   |task|stay
        self.error_time=100000


    def set_task_pretreatment(self,action_path):
        self.action_path=action_path
        if not len(self.task_list)==0:
            if not len(self.action_path)==0:
                self.task_pretreatment()
            else:
                s=1
        else:
            self.motion_type_list=['stay']
            self.current_stage_ID=0

    def task_pretreatment(self,presuf="pre"):
        #print(self.task_list)
        if presuf=="pre":
            self.motion_list=[]
            self.motion_type_list=[]
            #print(self.interested_map)
            #print(self.task_list[0][0])
            if len(self.action_path[0])==0:
                goal_position=self.current_pose
                self.action_path[0]=[self.current_pose]
            else:
                goal_position=self.action_path[0][0]
            #goal_position=self.interested_map[self.task_list[0][0][2]]
            self.motion_list.append(self.find_path(self.init_pose,goal_position))
            #print(self.motion_list)
            self.motion_type_list.append("motion")
            if self.agent_ID==7:
                i=0
            if not len(self.task_list)==len(self.action_path):
                s=1
            for i in range(len(self.task_list)-1):
                self.motion_list.append(self.action_path[i])
                self.motion_type_list.append(self.task_list[i][0][1])
                print(self.action_path[i][-1])
                print(len(self.action_path))
                print(i)
                print(self.action_path[i+1][0])
                change_path=self.find_path(#
                self.action_path[i][-1],self.action_path[i+1][0]
#                    self.interested_map[self.task_list[i][0][2]],self.interested_map[self.task_list[i+1][0][2]]
                )
                self.motion_list.append(change_path)
                self.motion_type_list.append("motion")
            self.motion_type_list.append(self.task_list[-1][0][1])
            self.motion_list.append(self.action_path[-1])
            self.motion_type_list.append("stay")
            self.current_stage_ID=0
        if presuf=="suf":
            self.motion_list=[]
            self.motion_type_list=[]
            i=0
            goal_position=self.interested_map[self.task_list[0][0][2]]
            self.motion_list.append(self.find_path(self.init_pose,goal_position))
            self.motion_type_list.append("motion")
            for i in range(len(self.task_list)-1):
                self.motion_list.append(self.task_list[i])
                self.motion_type_list.append("action")
                change_path=self.find_path(
                    self.interested_map[self.task_list[i][2]],self.interested_map[self.task_list[i+1][2]]
                )
                self.motion_list.append(change_path)
                self.motion_type_list.append("action")

            change_path=self.find_path(self.interested_map(self.task_list[i+1][2]),self.init_pose)
            self.motion_list.append(change_path)
            self.motion_type_list.append("motion")
            self.current_stage_ID=0

    def task_pretreatment_online(self,presuf="pre"):
        #print(self.task_list)
        self.init_pose=self.current_pose
        if presuf=="pre":
            self.motion_list=[]
            self.motion_type_list=[]
            if len(self.action_path[0])==0:
                goal_position=self.current_pose
                self.action_path[0]=[self.current_pose]
            else:
                goal_position=self.action_path[0][0]
            self.motion_list.append(self.find_path(self.init_pose,goal_position))
            self.motion_type_list.append("motion")
            i=0
            for i in range(len(self.task_list)-1):
                self.motion_list.append(self.action_path[i])
                self.motion_type_list.append(self.task_list[i][0][1])
                print(self.action_path[i][-1])
                print(self.action_path[i+1][0])
                change_path=self.find_path(#
                self.action_path[i][-1],self.action_path[i+1][0]
#                    self.interested_map[self.task_list[i][0][2]],self.interested_map[self.task_list[i+1][0][2]]
                )
                self.motion_list.append(change_path)
                self.motion_type_list.append("motion")
            self.motion_type_list.append(self.task_list[-1][0][1])
            self.motion_list.append(self.action_path[-1])
            self.motion_type_list.append("stay")
            self.current_stage_ID=0


    def find_path(self,start,end,type='Astar'):
        if type=='Astar':
            path,_=self.find_path_Astar(start,end,"manhattan")
        if type=='Arastar':
            path, _ = self.find_path_Arastar(start, end, "manhattan")
        return path

    def execute_task(self,global_time,finished_task,co_task_todo,executing_Task):
        '''
        return pose, doing task ,todotask, whether_need_replan
        '''
        self.synchronization_label=0
        if len(self.task_list)==0:
            self.current_time=global_time
            self.adapt_state='stay'
            return self.current_pose,set(),set(),0
        if self.get_current_stage(global_time)=='error':
            self.adapt_state='error'
            return  self.current_pose,set(),set(),1
        self.execute_error(2)
        if self.motion_type_list[self.current_stage_ID]=="motion":
            #if self.current_stage_ID==2:
            #    z=1
            self.current_pose,todo_co_task=self.get_next_pose(global_time,finished_task,co_task_todo,executing_Task)
            replan_label=self.diagnose_ignorable_event()
            if not replan_label in [0,1]:
                z=1
            return self.current_pose,set(),todo_co_task,replan_label
        elif self.motion_type_list[self.current_stage_ID]=="stay":
            self.adapt_state='stay'
            self.current_time=global_time
            return self.current_pose,set(),set(),0
        else:
            self.adapt_state='task'
            self.current_time=global_time
            print(len(self.action_path))
            print('ID',self.current_stage_ID)
            if len(self.action_path)==0:
                s=1
            if len(self.action_path[self.current_stage_ID//2])>0:
                self.current_pose=self.action_path[self.current_stage_ID//2].pop(0)
                replan_label=self.diagnose_ignorable_event()
                return self.current_pose,set(),set(),replan_label
            else:
                if self.motion_type_list[self.current_stage_ID+1]=="stay":#finished
                    self.current_stage_ID= self.current_stage_ID+1
                    #return self.current_pose,{self.motion_type_list[self.current_stage_ID-1]},set(),0
                    return self.current_pose,{self.task_list[self.current_stage_ID//2-1][0]},set(),0
                else:#working
                    #print('after that1',self.current_time)
                    print('agent_',self.agent_ID,'finished',self.motion_type_list[self.current_stage_ID])
                    #print('after that',self.current_time)
                    self.current_stage_ID=self.current_stage_ID+1
                    #self.motion_begin_time=self.next_stage_time
                    self.current_pose, todo_co_task=self.get_next_pose(global_time,finished_task,co_task_todo,executing_Task)
                    replan_label=self.diagnose_ignorable_event()
                    if not replan_label in [0,1]:
                        z=1
                    #return self.current_pose,{self.motion_type_list[self.current_stage_ID-1]},todo_co_task,replan_label
                    return self.current_pose,{self.task_list[self.current_stage_ID//2-1][0]},todo_co_task,replan_label

    def find_next_stage_time(self,global_time):
        if self.motion_type_list[self.current_stage_ID]=="motion":
            dis=0
            node=self.motion_list[self.current_stage_ID][0]
            for next_node in self.motion_list[self.current_stage_ID]:
                dis=dis+self.get_distance(node,next_node)
                node=next_node
            return  dis/self.velocity
        if self.motion_type_list[self.current_stage_ID]=="action":
            task_time= self.input_task_type[self.motion_list[self.current_stage_ID][0][1]][0]
            return global_time+task_time

    def execute_error(self,situation=1):
        if situation==1:
            if self.agent_ID in [3]:
                if self.current_time>300:
                    self.error_time=0
        if situation==2:
            if self.agent_ID in [3]:
                if self.current_time>250:
                    self.error_time=0
            if self.agent_ID in [6,11]:
                if self.current_time>600:
                    self.error_time=0


    def get_next_pose(self,global_time,finished_task,co_task_todo,executing_Task):
        dis=(global_time-self.current_time)*self.velocity
        finished_dis=0
        #print(self.motion_list[self.current_stage_ID])
        next_node=self.current_pose

        while finished_dis< dis:
            current_node=copy.deepcopy(next_node)
            if len(self.motion_list[self.current_stage_ID])<=0:
                if self.lead_requirement(finished_task,executing_Task):#pre task is finished

                    self.synchronization_label=1
                    if self.cooperater_agent_satisfied(co_task_todo): #coperate
                        self.current_time=global_time
                        self.current_stage_ID=self.current_stage_ID+1
                        print('agent begin execute task',self.motion_type_list[self.current_stage_ID],
                              'at time',self.current_time)
                        #self.next_stage_time=self.current_time+ \
                                             #self.input_task_type[self.motion_list[self.current_stage_ID][0][1]][0]
                        self.adapt_state='cooperate'
                        return current_node,set()
                    else:
                        self.current_time=global_time
                        self.adapt_state='cooperate'
                        return current_node,(self.motion_type_list[self.current_stage_ID+1],self.task_list[self.current_stage_ID//2][1])
                else:
                    self.adapt_state='pretask'
                    self.current_time=global_time
                    return current_node,set()
            next_node=self.motion_list[self.current_stage_ID].pop()
            if self.agent_ID == 7:
                if self.get_distance(self.current_pose,next_node)>9:
                    s=1
            if dis-finished_dis<self.get_distance(current_node,next_node):
                self.current_time=global_time
                self.motion_list[self.current_stage_ID].append(next_node)
                x=next_node[0]*(dis-finished_dis)/self.get_distance(current_node,next_node)+\
                  current_node[0]*(1-(dis-finished_dis)/self.get_distance(current_node,next_node))
                y=next_node[1]*(dis-finished_dis)/self.get_distance(current_node,next_node)+\
                  current_node[1]*(1-(dis-finished_dis)/self.get_distance(current_node,next_node))
                self.adapt_state='motion'
                #if not self.motion_list[self.current_stage_ID][-1]==next_node:
                #    self.motion_list[self.current_stage_ID].append(next_node)
                return (x,y),set()
            if dis-finished_dis==self.get_distance(current_node,next_node):
                self.current_time=global_time
                self.adapt_state='motion'

                return next_node,set()
            finished_dis=finished_dis+self.get_distance(current_node,next_node)
        if (finished_dis-dis)==0:
            new_node=self.current_pose
        self.current_time=global_time
        self.adapt_state='motion'
        return new_node,set()

    def cooperater_agent_satisfied(self,co_task_todo):
        next_task=self.motion_type_list[self.current_stage_ID+1]
        subtask_list={}
        if len(co_task_todo)==0:
            return 0
        #print('co_task_todo',co_task_todo)
        for task,subtask in co_task_todo:
            if task==next_task:
                if subtask in subtask_list.keys():
                    subtask_list[subtask]=subtask_list[subtask]+1
                else:
                    subtask_list[subtask]=1
        #print('plan to do the subtask of ',next_task,'is',subtask_list)
        #print(next_task)

        check_task_list= self.input_task_type[next_task][1]
        for subtask,num in check_task_list.items():
            if subtask in subtask_list.keys():
                if not num==subtask_list[subtask]:
                    return 0
            else:
                return 0
        print('task ',next_task,' satisfied')
        return 1

    def get_distance(self,current_node,next_node):
        x=current_node[0]-next_node[0]
        y=current_node[1]-next_node[1]
        return (x**2+y**2)**0.5

    def lead_requirement(self,finished_task,executing_Task):
        feasible_label=1
        pre_task=[]
        pre_equ_task=[]
        equ_task=[]
        noequ_task=[]
        for a,b in self.related_poset['<']:
            if b==self.task_list[self.current_stage_ID//2][0][0]:
                pre_task.append(a)
        for a,b in self.related_poset['<=']:
            if b==self.task_list[self.current_stage_ID//2][0][0]:
                pre_equ_task.append(a)
        for a,b in self.related_poset['=']:
            if b==self.task_list[self.current_stage_ID//2][0][0]:
                if self.input_task_type.task_data[a][1]>self.input_task_type.task_data[b][1]:
                    equ_task.append(a)
            if a ==self.task_list[self.current_stage_ID//2][0][0]:
                if not self.input_task_type.task_data[a][1]>self.input_task_type.task_data[b][1]:
                    equ_task.append(b)
        for a,b in self.related_poset['!=']:
            if b==self.task_list[self.current_stage_ID//2][0][0]:
                noequ_task.append(a)
            if a ==self.task_list[self.current_stage_ID//2][0][0]:
                noequ_task.append(b)
        finished_task_num=[]
        for task in finished_task:
            finished_task_num.append(task[0])
        for i in pre_task:
            if not i in finished_task_num:
                print('still need task<',i)
                #print(finished_task)
                return 0
        for i in pre_equ_task:
            if not i in executing_Task and not i in finished_task_num:
                print('still need task<=',i)
                #print(finished_task)
                return 0
        for i in equ_task:
            if not i in executing_Task:
                print('still need task=',i)
                return 0
        for i in noequ_task:
            if not i in noequ_task:
                print('still need task!=',i)
                return 0
        #print('OKK')
        return feasible_label

#================
# these function is used for calculate the time




    def estimate_current_action_or_motion_time(self):
        '''
        consider the time quantum from the begin of these action
        to the begin of next action
        first three part in the following
        as |action | motion| wait | action|
           ================================
        '''
        if self.motion_type_list[self.current_stage_ID]=='motion':
            #calculate the left time for current motion
            #print(self.motion_list[self.current_stage_ID])
            #print(self.agent_ID)
            #print(self.current_stage_ID)
            if len(self.motion_list[self.current_stage_ID])==0:
                return 0
            dis=0
            node=self.motion_list[self.current_stage_ID][0]
            for next_node in self.motion_list[self.current_stage_ID]:
                dis=dis+self.get_distance(node,next_node)
                node=next_node
            estimate_time=dis/self.velocity
            return estimate_time
        elif self.motion_type_list[self.current_stage_ID]=='stay':
            return 0
        else:
            estimate_time=len(self.motion_list[self.current_stage_ID])*self.action_step_len
            return estimate_time

    def diagnose_ignorable_event(self):
        '''
        if the event do not change the time of action ,this will not take into
        consider
        '''
        estimate_time=self.estimate_current_action_or_motion_time()
        if self.motion_type_list[self.current_stage_ID]=='motion':
            #get next station begin time
            #print((self.current_stage_ID+1)//2)
            #print(self.task_time_table)
            current_plan_ddl=self.task_time_table[(self.current_stage_ID+1)//2][1]
            #get
            if current_plan_ddl-self.current_time-estimate_time<0:
                return  1
            else:
                return  0
        elif self.motion_type_list[self.current_stage_ID]=='stay':
            return 0
        else:
            current_plan_ddl=self.task_time_table[self.current_stage_ID//2][2]
            if not abs(current_plan_ddl-estimate_time)<2:# over the threshold
                return 1
            else:
                return 0
        s=1

    def generate_boundry_condition(self,boundry_condition):
        self.bounry_condition=boundry_condition+self.current_time

    def get_current_estimate_time(self,task_j):

        estimate=self.estimate_current_action_or_motion_time()+self.current_time
        return estimate


# =============
    def get_current_stage(self,time,num=0):
        if time<self.error_time:
            return self.motion_type_list[self.current_stage_ID-num]
        else:
            return 'error'


    def find_path_Astar(self,start, end, type="manhattan"):
        #zanshi d chuli
        new_env=photovoltaic_Env(5)
        new_env.add_barrier(self.barrier)
        #print(start)
        #print(end)
        #print(start[0]//5)
        astar=AStar((start[0]//5*5,start[1]//5*5), (end[0]//5*5,end[1]//5*5), type, new_env)
        path,node=astar.searching()
        return path,node
    @staticmethod
    def find_path_Arastar(start, end, type="manhattan"):
        arastar=AraStar(tuple(start),tuple(end), type)
        path,node=arastar.searching()
        return path,node