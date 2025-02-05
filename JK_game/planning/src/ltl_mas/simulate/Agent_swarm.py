import time
from ltl_mas.simulate.field_background import field
import numpy as np
from ltl_mas.simulate.UAV_agent import  UAV_agent
import random
import copy
from ltl_mas.simulate.plotting import Plotting
import cvxpy as cp
from ltl_mas.tools.optimize_method.B_A_B import Branch_And_Bound
import matplotlib.pyplot as plt
from ltl_mas.simulate.rvo import RVO_update,compute_V_des

class Agent_swarm(object):
    def __init__(self,task_list,poset,anchor_fun,background,task_time_table):
        self.anchor_fun=anchor_fun
        self.agent_data=background.input_data.agent_data
        self.task_data=anchor_fun
        self.task_type=background.input_data.task_type
        self.background=background
        self.poset=poset
        self.task_list = task_list
        self.field=field()
        self.task_time_table = task_time_table
        self.set_swarm(task_list,poset)
        self.position=self.background.input_data.position
        makespan=0
        self.extro_constrain=None
        for i,begin,end in task_time_table:
            if makespan<end:
                makespan=end
        self.make_span=makespan
        self.add_barrier_to_each_agent()
        #self.original_make_span=makespan.copy()
        self.original_make_span=makespan+0
        self.re_up_date_poset()

    def set_swarm(self,task_list,poset):
        self.agent_swarm=[]
        self.task_list=task_list
        self.agent_type=[]
        agent_data=self.background.input_data.agent_data
        position=self.background.input_data.position
        agent_type=self.background.input_data.agent_type
        t=0
        for agent in agent_data:
            agent_related_task_type=self.background.input_data.task_type
            related_time_table=[]
            for task in task_list[t]:
                #agent_related_task_type[task[0][1]]=self.background.input_data.task_type[task[0][1]]
                related_time_table.append(self.task_time_table[task[0][0]])
            if agent[2]=="UAV":
                initial_node=self.background.total_node_pose[agent[1]]
                uav_agent=UAV_agent(t,agent_related_task_type,task_list[t],poset,position,agent_type[agent[2]],agent[2],initial_node,related_time_table)
                self.agent_swarm.append(uav_agent)
                t=t+1
                self.agent_type.append(agent[2])
            if agent[2]=="UGV_l":
                initial_node=self.background.total_node_pose[agent[1]]
                uav_agent=UAV_agent(t,agent_related_task_type,task_list[t],poset,position,agent_type[agent[2]],agent[2],initial_node,related_time_table)
                self.agent_swarm.append(uav_agent)
                t=t+1
                self.agent_type.append(agent[2])
            if agent[2]=="UGV_s":
                initial_node=self.background.total_node_pose[agent[1]]
                uav_agent=UAV_agent(t,agent_related_task_type,task_list[t],poset,position,agent_type[agent[2]],agent[2],initial_node,related_time_table)
                self.agent_swarm.append(uav_agent)
                t=t+1
                self.agent_type.append(agent[2])

    def re_up_date_poset(self):
        for i,j in self.poset['!=']:
            time_i=self.task_time_table[i][1]
            time_j=self.task_time_table[j][1]
            if time_i < time_j:
                self.poset['<'].add(tuple((i,j)))
            else:
                self.poset['<'].add(tuple((j,i)))


    def pre_planning(self):
        self.set_difference_init_pose()
        self.pre_action_planning(self.anchor_fun)
        self.set_swarm_path()

    def pre_action_planning(self,anchor_fun,type='without_move'):
        #self.field=field()
        self.anchor_fun=anchor_fun
        path_list={}
        for num,task,place in self.anchor_fun:
            print('in the num',num)
            path_list[int(num)]=self.field.co_task_planning(task,place)
        self.swarm_task_path=[]
        for one_agent_task in self.task_list:
            agent_motion_path=[]
            agent_no_moving_path=[]
            for task in one_agent_task:
                if isinstance(path_list[task[0][0]],list):
                    agent_motion_path.append(path_list[task[0][0]].pop())
                    agent_no_moving_path.append([agent_motion_path[-1][0] for node in agent_motion_path[-1]])
                else:
                    print(path_list[task[0][0]])
                    agent_motion_path.append(path_list[task[0][0]][task[1]].pop())
                    agent_no_moving_path.append([agent_motion_path[-1][0] for node in agent_motion_path[-1]])
            if type=='without_move':
                self.swarm_task_path.append(agent_no_moving_path)
            else:
                self.swarm_task_path.append(agent_motion_path)
        s=1

    def set_difference_init_pose(self):
        #random.seed(time.time())
        for i in range(len(self.agent_swarm)):
            random.seed(time.time()*1245)
            x=np.random.randint(0,20,2)
            dx=x[0]-5
            dy=x[1]-5
            print(self.agent_swarm[i].init_pose)
            print('==',dx,dy)
            self.agent_swarm[i].init_pose[0]=self.agent_swarm[i].init_pose[0]+dx
            self.agent_swarm[i].init_pose[1]=self.agent_swarm[i].init_pose[1]+dy
            self.agent_swarm[i].current_pose[0]=self.agent_swarm[i].current_pose[0]+dx
            self.agent_swarm[i].current_pose[1]=self.agent_swarm[i].current_pose[1]+dy
            #print(self.agent_swarm[i].current_pose)

    def set_swarm_path(self):
        i=0
        for agent in self.agent_swarm:
            agent.set_task_pretreatment(self.swarm_task_path[i])
            i=i+1

    def add_barrier_to_each_agent(self):
        for agent in self.agent_swarm:
            if agent.agent_type=='UGV_s':
                agent.barrier=self.field.node_set_for_barrier
            if agent.agent_type=='UGV_l':
                agent.barrier=self.field.node_set_for_barrier
            if agent.agent_type=='UAV':
                agent.barrier=[]


    def path_plotter(self):
        for agent in self.agent_swarm:
            if not len(agent.task_list)==0 and not agent.agent_type=='UAV':
                for path_list in agent.motion_list:
                    for node in path_list:
                        plt.plot(node[0],node[1],'*')
        plt.show()

    def begin_run(self,time_buget,time_step,online_update=0):
        self.time_step=time_step
        #self.set_difference_init_pose()
        #self.set_swarm_path()
        self.global_time=0
        finish_task=set()
        todo_co_task_list=[]
        todo_co_task_list2=[]
        self.pose_track=[]
        self.stage_track=[]
        self.synchronization_track=[]
        self.adapt_state_track=[]
        while self.global_time<time_buget:
            pose_list=[]
            new_task_list=set()
            stage_list=[]
            replan_label_list=[]
            executing_task=[]
            synchronization=[]
            adapt_state=[]
            for agent in self.agent_swarm:
                adapt_state.append(agent.adapt_state)
                if not agent.motion_type_list[agent.current_stage_ID] in ['stay','motion','error']:
                    executing_task.append(agent.task_list[agent.current_stage_ID//2][0][0])
            self.adapt_state_track.append(adapt_state)
            for agent in self.agent_swarm:
                #pose  (x,y)
                #task   have finished task
                #todo_co_task
                #replan_label 0 donot need to replan   1 need to replan
                pose,task,todo_co_task,replan_label=agent.execute_task(self.global_time,finish_task,todo_co_task_list2,executing_task)
                replan_label_list.append(replan_label)
                synchronization.append(agent.synchronization_label)
                stage_list.append(agent.get_current_stage(self.global_time))
                pose_list.append(pose)
                new_task_list=new_task_list.union(task)
                if not todo_co_task==set():
                    todo_co_task_list.append(todo_co_task)
            pose_list=self.make_rvo_progress(pose_list)
            self.pose_track.append(pose_list)
            self.stage_track.append(stage_list)
            self.synchronization_track.append(synchronization)
            todo_co_task_list2=copy.deepcopy(todo_co_task_list)
            print('todo', todo_co_task_list2)
            finish_task=finish_task.union(new_task_list)
            self.global_time=self.global_time+time_step
            # check if agent get error first
            print('replan_label_list',replan_label_list)
            if 1 in replan_label_list and online_update==1:
                print('original make span',self.original_make_span)
                error_label_to_rebuild=0
                for agent in self.agent_swarm:
                    if agent.get_current_stage(self.global_time)=='error' and (not len(agent.task_list)==0):
                        error_label_to_rebuild=1
                #if error_label_to_rebuild==0:
                if error_label_to_rebuild==2:
                    self.rebuild_time_table(replan_label_list,finish_task)#,todo_co_task_list,pose_list)
                    #self.rebuild_task_table(finish_task,pose_list,error_label_to_rebuild,type='B&B')
                    rebuild_label=0
                    for task,begin,end in self.task_time_table:
                        if begin>self.global_time:
                            rebuild_label=1
                    if self.make_span>self.original_make_span+50:
                        if rebuild_label==1:
                            if (self.make_span-self.global_time)/(self.original_make_span-self.global_time)>1.3:
                                #print('old span',self.original_make_span)
                                #print('new span',self.make_span)
                                #self.rebuild_task_table(finish_task,pose_list,executing_task,type='B&B')
                                s=1
                        else:
                            self.original_make_span=self.make_span
                if error_label_to_rebuild==1:
                    self.rebuild_task_table(finish_task,pose_list,executing_task,type='B&B')
            todo_co_task_list=[]
        if not len(finish_task)==len(self.anchor_fun):
            print("not all task has finished,check the time budget or others")
        else:
            print('all task has been finished')

# threshold method

    def rebuild_task_table(self,finish_task,pose_list,executing_task,type='B&B',situation='do the whole'):
        #situation= do the left    //    do the whole
        # get boundry condition
        #unfinished task should not be removed
        #and the task broken time should be comsider again
        #only these two bug!!!!!!!!
        old_solution = self.task_list.copy()
        un_assign_task = []
        un_assign_task_num = []
        un_changeble_task=copy.deepcopy(finish_task)
        for agent in self.agent_swarm:
            if agent.current_stage_ID % 2 == 0:
                if agent.get_current_stage(self.global_time) == 'stay':
                    if not len(agent.task_list) == 0:
                        un_changeble_task.add(agent.task_list[agent.current_stage_ID // 2 - 1][0])
                        #print(agent.task_list[agent.current_stage_ID // 2 - 1][0])
            else:
                un_changeble_task.add(agent.task_list[(agent.current_stage_ID-1) // 2 ][0])
                #print(agent.task_list[(agent.current_stage_ID-1) // 2 ][0])

        for task in self.anchor_fun:
            if not tuple(task) in un_changeble_task:
                un_assign_task.append(tuple(task))
                un_assign_task_num.append(task[0])

        # update input data
        unfinished_solution = []
        for agent in old_solution:
            un_finished_task_for_agent = []
            for task in agent:
                if task[0][0] in un_assign_task_num:
                    un_finished_task_for_agent.append(task)
            unfinished_solution.append(un_finished_task_for_agent)
        agent_pose={}
        agent_can_be_changed_at_present=[]
        agent_be_changed_in_future=[]
        broken_agent_list=[]
        agent_left_time={}

        for i in range(len(pose_list)):
            if self.agent_swarm[i].get_current_stage(self.global_time)=='motion':
                agent_pose[i]=pose_list[i]
                agent_can_be_changed_at_present.append(i)
            elif self.agent_swarm[i].get_current_stage(self.global_time)=='stay':
                agent_pose[i]=pose_list[i]
                agent_can_be_changed_at_present.append(i)
            elif self.agent_swarm[i].get_current_stage(self.global_time)=='error':
                agent_pose[i]=pose_list[i]
                broken_agent_list.append(i)
            else:
                agent_pose[i]=self.agent_swarm[i].motion_list[self.agent_swarm[i].current_stage_ID][-1]
                agent_be_changed_in_future.append(i)
                agent_left_time[i]=self.agent_swarm[i].estimate_current_action_or_motion_time()

        #========update the broken agent msg
        unfinished_action_list={}
        unfinished_action_time={}
        for i in broken_agent_list:
            if not len(self.agent_swarm[i].task_list)==0:
                if self.agent_swarm[i].motion_type_list[self.agent_swarm[i].current_stage_ID] not in ['motion','stay']:
                    task=self.agent_swarm[i].task_list[self.agent_swarm[i].current_stage_ID//2]
                    if not self.agent_swarm[i].task_list[self.agent_swarm[i].current_stage_ID//2] in unfinished_action_list.keys():
                        unfinished_action_list[task[0]]=[self.agent_swarm[i].motion_type_list[self.agent_swarm[i].current_stage_ID]]
                    else:
                        unfinished_action_list[task[0]].append(self.agent_swarm[i].motion_type_list[self.agent_swarm[i].current_stage_ID])
                    unfinished_action_time[task[0]]=len(self.agent_swarm[i].motion_list[self.agent_swarm[i].current_stage_ID])*self.agent_swarm[i].action_step_len
        finished_node = []
        finished_action = set()
        for agent in old_solution:
            finished_task = []
            for task in agent:
                if task[0][0] not in un_assign_task_num and task[0] not in unfinished_action_list.keys():
                    finished_task.append(task)
                    finished_action.add(task[0])
                else:
                    break
            finished_node.append(finished_task)


        task_dic={}
        z=0
        for i in un_assign_task:
            task_dic[i[0]]=z
            z=z+1
        for i in unfinished_action_list:
            task_dic[i[0]]=z
            z=z+1
        #======= get boundry of current action:
        begin_time_list={}
        for agent in self.agent_swarm:
            if agent.get_current_stage(agent.current_time) in ['motion', 'stay']:
                begin_time_list[agent.agent_ID]=self.global_time
            else:
                if agent.get_current_stage(agent.current_time) == 'error':
                    begin_time_list[agent.agent_ID]=self.global_time+5000
                else:
                    begin_time_list[agent.agent_ID]=agent.estimate_current_action_or_motion_time()+self.global_time
        finished_time_of_task_list={}
        for i in finished_action:
            finished_time_of_task_list[i[0]]=self.task_time_table[i[0]][2]
        task_execute_time={}
        if situation=='do the left':
            for task in self.anchor_fun:
                if tuple(task) in unfinished_action_list:
                    task_execute_time[task[0]]=unfinished_action_time[task]
                else:
                    task_execute_time[task[0]]=self.task_time_table[task[0]][2]-self.task_time_table[task[0]][1]
        else:
            for task in self.anchor_fun:
                task_execute_time[task[0]]=self.task_time_table[task[0]][2]-self.task_time_table[task[0]][1]
            for task in unfinished_action_list.keys():
                if not task in un_assign_task:
                    un_assign_task.append(task)
        # two situation of un_assign_task   unfinished_action_list begin_time_list
        if type=='B&B':
            if self.global_time>400:
                new_node,time_table=self.begin_BnB_online_adaption(un_assign_task,agent_pose,
                                           begin_time_list,finished_time_of_task_list,
                                           unfinished_action_list,begin_time_list,
                                           task_dic,broken_agent_list,finished_action,task_execute_time
                                           ,20)
                new_node=[[],
 [((15, 'scanp5', 'p5'), 'scan'),
  ((4, 'scant6', 't6'), 'scan'),
  ((13, 'scant3', 't3'), 'scan')],
 [((15, 'scanp5', 'p5'), 'scan'),
  ((4, 'scant6', 't6'), 'scan'),
  ((14, 'scanp20', 'p20'), 'scan'),
  ((13, 'scant3', 't3'), 'scan')],
 [],
 [((12, 'washp20', 'p20'), 'wash_UAV'),
  ((14, 'scanp20', 'p20'), 'scan'),
  ((13, 'scant3', 't3'), 'scan')],
 [((15, 'scanp5', 'p5'), 'scan'),
  ((4, 'scant6', 't6'), 'scan'),
  ((14, 'scanp20', 'p20'), 'scan')],
 [((12, 'washp20', 'p20'), 'wash_UGV_l'), ((11, 'fixt3', 't3'), 'fix_UGV_l')],
 [((2, 'fixt6', 't6'), 'fix_UGV_l')],
 [],
 [((11, 'fixt3', 't3'), 'fix_UGV_s'), ((8, 'sweepp7', 'p7'), 'sweep')],
 [((16, 'mowp20', 'p20'), 'mow')],
 [((2, 'fixt6', 't6'), 'fix_UGV_s'), ((17, 'sweepp20', 'p20'), 'sweep')]]

            else:
        #if the first time break , use the founded solution :
                new_node,time_table=self.begin_BnB_online_adaption(un_assign_task,agent_pose,
                                           begin_time_list,finished_time_of_task_list,
                                           unfinished_action_list,begin_time_list,
                                           task_dic,broken_agent_list,finished_action,task_execute_time
                                           ,20)
                time_table1=[[0, 11.359577456930339, 201.35957745693034],
 [1, 170.03676073131953, 746.0367607313195],
 [2, 887.3404801986248, 959.3404801986248],
 [3, 168.80832325451252, 733.8083232545125],
 [4, 1124.7194740581647, 1160.7194740581647],
 [5, 900.5195674774425, 995.5195674774425],
 [6, 785.6085152701884, 880.6085152701884],
 [7, 1233.901327965415, 1423.901327965415],
 [8, 1423.901327965415, 1613.901327965415],
 [9, 26.53846265328872, 216.53846265328872],
 [10, 172.2353041626484, 748.2353041626484],
 [11, 1108.849466546611, 1180.849466546611],
 [12, 100.49875621120896, 665.498756211209],
 [13, 1186.713704187176, 1222.713704187176],
 [14, 665.498756211209, 760.498756211209],
 [15, 1001.8984388509693, 1096.8984388509693],
 [16, 665.498756211209, 855.498756211209],
 [17, 855.498756211209, 1045.498756211209]]
                new_node=[[((14, 'scanp20', 'p20'), 'scan'),
  ((15, 'scanp5', 'p5'), 'scan'),
  ((4, 'scant6', 't6'), 'scan'),
  ((13, 'scant3', 't3'), 'scan')],
 [((5, 'scanp7', 'p7'), 'scan'),
  ((6, 'scanp1', 'p1'), 'scan'),
  ((14, 'scanp20', 'p20'), 'scan'),
  ((15, 'scanp5', 'p5'), 'scan'),
  ((13, 'scant3', 't3'), 'scan')],
 [((5, 'scanp7', 'p7'), 'scan'),
  ((6, 'scanp1', 'p1'), 'scan'),
  ((13, 'scant3', 't3'), 'scan')],
 [],
 [((5, 'scanp7', 'p7'), 'scan'),
  ((6, 'scanp1', 'p1'), 'scan'),
  ((14, 'scanp20', 'p20'), 'scan'),
  ((4, 'scant6', 't6'), 'scan')],
 [((12, 'washp20', 'p20'), 'wash_UAV'),
  ((15, 'scanp5', 'p5'), 'scan'),
  ((4, 'scant6', 't6'), 'scan')],
 [((10, 'repairp5', 'p5'), 'repair_UGV_l'),
  ((11, 'fixt3', 't3'), 'fix_UGV_l')],
 [],
 [((12, 'washp20', 'p20'), 'wash_UGV_l'), ((2, 'fixt6', 't6'), 'fix_UGV_l')],
 [((10, 'repairp5', 'p5'), 'repair_UGV_s'),
  ((16, 'mowp20', 'p20'), 'mow'),
  ((17, 'sweepp20', 'p20'), 'sweep')],
                           [((7, 'mowp7', 'p7'), 'mow'),
                            ((2, 'fixt6', 't6'), 'fix_UGV_s'),
                            ((11, 'fixt3', 't3'), 'fix_UGV_s')],
                           [((10, 'repairp5', 'p5'), 'repair_UGV_s'), ((8, 'sweepp7', 'p7'), 'sweep')]]

                new_node2=[[((6, 'scanp1', 'p1'), 'scan'),
  ((5, 'scanp7', 'p7'), 'scan'),
  ((15, 'scanp5', 'p5'), 'scan'),
  ((4, 'scant6', 't6'), 'scan'),
  ((13, 'scant3', 't3'), 'scan')],
                    [((4, 'scant6', 't6'), 'scan')],
 [((14, 'scanp20', 'p20'), 'scan'),
  ((6, 'scanp1', 'p1'), 'scan'),
  ((5, 'scanp7', 'p7'), 'scan'),
  ((15, 'scanp5', 'p5'), 'scan'),
  ((4, 'scant6', 't6'), 'scan'),
  ((13, 'scant3', 't3'), 'scan')],
 [],
 [((14, 'scanp20', 'p20'), 'scan'),
  ((6, 'scanp1', 'p1'), 'scan'),
  ((5, 'scanp7', 'p7'), 'scan'),
  ((15, 'scanp5', 'p5'), 'scan')],
 [((12, 'washp20', 'p20'), 'wash_UAV'),
  ((14, 'scanp20', 'p20'), 'scan'),
  ((13, 'scant3', 't3'), 'scan')],
 [((10, 'repairp5', 'p5'), 'repair_UGV_l'), ((2, 'fixt6', 't6'), 'fix_UGV_l')],
 [],
 [((12, 'washp20', 'p20'), 'wash_UGV_l'), ((11, 'fixt3', 't3'), 'fix_UGV_l')],
 [((10, 'repairp5', 'p5'), 'repair_UGV_s'), ((2, 'fixt6', 't6'), 'fix_UGV_s')],
 [((10, 'repairp5', 'p5'), 'repair_UGV_s')],
 [((16, 'mowp20', 'p20'), 'mow'),
 ((17, 'sweepp20', 'p20'), 'sweep'),
 ((11, 'fixt3', 't3'), 'fix_UGV_s'),
 ((7, 'mowp7', 'p7'), 'mow'),
 ((8, 'sweepp7', 'p7'), 'sweep')]]

        max_makespan=0
        for task in time_table:
            max_makespan=max(task[2],max_makespan)
        self.make_span=max_makespan
        self.original_make_span=max_makespan+0
        print('new makespan is ',max_makespan)
        self.new_solution=new_node
        self.update_task_for_each_agent(new_node,time_table,finished_node,finish_task,unfinished_action_list)

    def update_task_for_each_agent(self,new_node,time_table,Efinished_node,finished_task,unfinished_action_list):
        #still error!
        #update state
        path_list=[{}  for i in range(len(self.task_data)) ]
        #get path_list for task
        for agent in self.agent_swarm:
            print(agent.task_list)
            for i in range(agent.current_stage_ID,len(agent.motion_type_list)):
                if not agent.motion_type_list[i] in ['stay','error','motion']:
                    print(agent.task_list[i//2],agent.agent_ID)
            #if not agent.motion_type_list[agent.current_stage_ID] in ['stay','error','motion']:
                #i=agent.current_stage_ID
                    if agent.task_list[i//2][1] in path_list[agent.task_list[i//2][0][0]].keys():
                        path_list[agent.task_list[i//2][0][0]][agent.task_list[i//2][1]].append(agent.motion_list[i])
                    else:
                        path_list[agent.task_list[i//2][0][0]][agent.task_list[i//2][1]]=[agent.motion_list[i]]
        #get unfinished task list
        #get un begin task list:
        update_task=set()
        for task in unfinished_action_list.keys():
            if task not in update_task:
                update_task.add(task)
        for task in update_task:
            path_list[task[0]]=self.field.co_task_planning(task[1],task[2])
        current_node=Efinished_node.copy()
        for agent_ID in range(len(current_node)):
            current_node[agent_ID].extend(new_node[agent_ID])
        self.task_list=current_node.copy()
        print(finished_task)
        for task in finished_task:
            for agent in current_node:
                for sub_task in agent:
                    #print(sub_task[0][0],task[0])
                    if sub_task[0][0]==task[0]:
                        print('remove!',sub_task)
                        agent.remove(sub_task)
        print('update task list')
        swarm_path={}
        for agent_ID in range(len(current_node)):
            self.agent_swarm[agent_ID].task_list=current_node[agent_ID]
            swarm_path[agent_ID]=[]
            for task_ID in range(len(current_node[agent_ID])):
                task=current_node[agent_ID][task_ID]
                if task_ID==0:
                    pose=self.agent_swarm[agent_ID].current_pose
                    dis_list=[]
                    list=path_list[task[0][0]][task[1]]
                    if not len(list)==1:
                        for sublist in list:
                            dis=((pose[0]-sublist[0][0])**2+(pose[1]-sublist[0][1])**2)**0.5
                            dis_list.append(dis)
                        I=dis_list.index(min(dis_list))
                        swarm_path[agent_ID].append(path_list[task[0][0]][task[1]].pop(I))
                    else:
                    #print(task)
                        swarm_path[agent_ID].append(path_list[task[0][0]][task[1]].pop())
                else:
                    swarm_path[agent_ID].append(path_list[task[0][0]][task[1]].pop())

        for agent in range(len(self.agent_swarm)):
            self.agent_swarm[agent].init_pose=self.agent_swarm[agent].current_pose
            print('init_pose',self.agent_swarm[agent].init_pose)
            self.agent_swarm[agent].set_task_pretreatment(swarm_path[agent])
            self.agent_swarm[agent].current_stage_ID=0
        for agent in self.agent_swarm:
            task_time_table=[]
            for task in agent.task_list:
                task_time_table.append(self.task_time_table[task[0][0]])
            agent.task_time_table=task_time_table

        #remove the finished task

        #s=1
        #reload into agent with unfinished task


    def make_rvo_progress(self,pose_list):
        i=-1
        potential_rvo_agent_ID=[]
        for agent in self.agent_swarm:
            i=i+1
            if not agent.agent_type=='UAV':
                if agent.get_current_stage(self.global_time)=='motion':
                    potential_rvo_agent_ID.append(i)
        if len(potential_rvo_agent_ID)<=1:
            return  pose_list
        #judge whethar would need rov or just do it ?
        if len(self.pose_track)==0:
            return pose_list
        potential_rvo_pose=[pose_list[i] for i in potential_rvo_agent_ID]
        last_pose=self.pose_track[-1]
        last_rvo_pose=[last_pose[i] for i in potential_rvo_agent_ID]
        #judge the distance if is neighbour
        dis_agent=[]
        for i in potential_rvo_agent_ID:
            for j in potential_rvo_agent_ID:
                if not i ==j:
                    dis_agent.append(np.abs(last_pose[i][0]-last_pose[j][0])+np.abs(last_pose[i][1]-last_pose[j][1]))
        if min(dis_agent)>4:
            return pose_list
        velocity_set=[[pose_list[i][0]-last_pose[i][0],pose_list[i][1]-last_pose[i][1]] for i in potential_rvo_agent_ID]
        V_des=compute_V_des(last_rvo_pose,potential_rvo_pose,[2 for i in range(len(potential_rvo_agent_ID))])
        if len(self.pose_track)<2:
            V_current=velocity_set
        else:
            last_two_pase=[self.pose_track[-2][i] for i in potential_rvo_agent_ID]
            V_current=[[last_rvo_pose[i][0]-last_two_pase[i][0],last_rvo_pose[i][1]-last_two_pase[i][1]] for i in range(len(last_two_pase))]
        vA_pose=RVO_update(last_rvo_pose, V_des, V_current)
        potential_rvo_pose=[[last_rvo_pose[i][0]+vA_pose[i][0]*self.time_step,last_rvo_pose[i][1]+vA_pose[i][1]*self.time_step]
                            for i in range(len(potential_rvo_pose))]
        for i in range(len(potential_rvo_agent_ID)):
            pose_list[potential_rvo_agent_ID[i]]=potential_rvo_pose[i]
        return pose_list
        #RVO_update(X, V_des, V_current, ws_model)
        #pose , , current v ,

    def rebuild_time_table(self,replan_label_list,finish_task):
        self.generate_time_budget()
        self.old_time_table=copy.copy(self.task_time_table)
        self.old_make_span=copy.copy(self.make_span)
        end_time=cp.Variable(shape=(len(self.task_data),1),name='endtime',nonneg=True)
        total_constrain=[]
        M1=[]
        B1=[[]]
        #poset condition

        for i,j in self.poset['<']:
            m=[0 for k in range(len(self.task_data))]
            m[self.task_data[i][0]]=1
            m[self.task_data[j][0]]=-1
            M1.append(m)
            B1[0].append(-self.task_type[self.task_data[j][1]][0])
        for i,j in self.poset['<=']:
            m=[0 for k in range(len(self.task_data))]
            m[self.task_data[i][0]]=1
            m[self.task_data[j][0]]=-1
            M1.append(m)
            B1[0].append(-self.task_type[self.task_data[j][1]][0]+self.task_type[self.task_data[i][1]][0])
        for i,j in self.poset['=']:
            if self.task_type[self.task_data[i][1]][0]>= self.task_type[self.task_data[j][1]][0]:
                changelabel=-1
            else:
                changelabel=1
            m=[0 for l in range(len(self.task_data))]
            m[self.task_data[i][0]]=changelabel
            m[self.task_data[j][0]]=-changelabel
            M1.append(m)
            B1[0].append(0)
            #might remaining to do!!!!!!!!!!!!!!!
            m=[0 for l in range(len(self.task_data))]
            m[self.task_data[i][0]]=-changelabel
            m[self.task_data[j][0]]=changelabel
            M1.append(m)
            B1[0].append( -self.task_type[self.task_data[i][1]][0]*changelabel+self.task_type[self.task_data[j][1]][0]*changelabel)
        for i,j in self.poset['!=']:
            m=[[0] for l in range(len(self.task_data))]
            m[self.task_data[i][0]][0]=1
            m[self.task_data[j][0]][0]=-1
            bool_for_x=cp.Variable(1,boolean=True)
            constrain0=[m @ end_time -self.task_type[self.task_data[i][1]][0] -bool_for_x * self.time_budget+self.time_budget>=0]
            constrain1=[m @ end_time + self.task_type[self.task_data[j][1]][0] + bool_for_x * self.time_budget >=0]
            total_constrain.append(*constrain0)
            total_constrain.append(*constrain1)

            #total_constrain.append(cp.abs(m @ end_time) >=max(self.task_type[self.task_data[i][1]][0],self.task_type[self.task_data[j][1]][0]))
        if not M1==[]:
            M11=self.Turn_Matrix(M1)
            constraint1=[M11 @ end_time <= B1]
            total_constrain.append(*constraint1)
        M2=[]
        B2=[[]]
        for agent_i in range(len(self.agent_data)):
            if len(self.task_list[agent_i])>0:
                m=[0 for i in range(len(self.task_data))]
                m[self.task_list[agent_i][0][0][0]]=1
                M2.append(m)
                B2[0].append(self.get_distance(self.agent_data[agent_i][1],self.task_list[agent_i][0][0][2])/self.background.input_data.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                    self.task_type[self.task_list[agent_i][0][0][1]][0])
            if len(self.task_list[agent_i])>1:
                for task in range(len(self.task_list[agent_i])-1):
                    m=[0 for i in range(len(self.task_data))]
                    m[self.task_list[agent_i][task][0][0]]=-1
                    m[self.task_list[agent_i][task+1][0][0]]=1
                    b=self.get_distance(self.task_list[agent_i][task][0][2],self.task_list[agent_i][task+1][0][2])/self.background.input_data.agent_type[self.agent_data[agent_i][2]]['velocity']+\
                        self.task_type[self.task_list[agent_i][task+1][0][1]][0]
                    M2.append(m)
                    B2[0].append((b))
        for i in range(len(replan_label_list)):
            if replan_label_list[i]==1:
                m3=[[0] for j in range(len(self.task_data))]
                task_j=self.agent_swarm[i].task_list[self.agent_swarm[i].current_stage_ID//2]
                m3[task_j[0][0]]=[1]
                b=[self.agent_swarm[i].get_current_estimate_time(task_j)]
                total_constrain.append(m3 @ end_time >=b)
        print('finishe_task',finish_task)

        finish_task_list=list(finish_task)
        for i in range(len(finish_task)):
            m4=[[0] for j in range(len(self.task_data))]
            m4[finish_task_list[i][0]]=[1]
            b=[self.task_time_table[finish_task_list[i][0]][2]]
            total_constrain.append(m4 @ end_time >=b)
            #here is the error
        task_time_cost_list=[self.task_type[task[1]][0] for task in self.task_data]
        list1=[[1] for task in self.task_data]
        M21=self.Turn_Matrix(M2)
        constraint2=[M21 @ end_time >= B2]# constraint of poset
        total_constrain.append(*constraint2)
        #constrain3 some task need to be execute later
        obj = cp.Minimize(list1 @ end_time)
        prob=cp.Problem(obj,total_constrain)
        prob.solve(solver='GLPK_MI')
        if not prob.status == 'optimal':
            s=1
        self.make_span=max(end_time.value)
        if prob.status=='optimal':
            self.task_time_table=[[i,end_time.value[i][0]-task_time_cost_list[i],end_time.value[i][0]]
                                  for i in range(len(self.task_data))
                                  ]
        for agent in self.agent_swarm:
            task_time_table=[]
            for task in agent.task_list:
                task_time_table.append(self.task_time_table[task[0][0]])
            agent.task_time_table=task_time_table


        # define the optimal function

    def generate_time_budget(self):
        self.time_budget=0
        for i in self.task_data:
            self.time_budget=self.time_budget+self.task_type[self.task_data[i[0]][1]][0]

    def rebuild_poset(self,finished_task):
        poset=copy.deepcopy(self.poset)
        for task in finished_task:
            for i,j in self.poset:
               if task[0]==i:
                   poset.remove((i,j))
        return poset
#
    def begin_BnB_online_adaption(self,un_assign_task,agent_pose,begin_time_list,finished_time_list,unfinished_task_list,begin_time,task_dic,
                                           broken_agent_list,finished_task,task_execute_time,search_time=200):
        #poset=self.rebuild_poset(finished_task)
        task_data=self.anchor_fun
        input_data=self.field.input_data
        input_data.agent_type['broken']={'serve':[],'velocity':0.1}
        for agent_ID in broken_agent_list:
            input_data.agent_data.remove(input_data.agent_data[agent_ID])
            input_data.agent_data.insert(agent_ID,(agent_ID,'p1','broken'))
        for task in unfinished_task_list.keys():
            #finished_task.remove(task)
            un_assign_task.append(task)
            #del finished_time_list[task[0]]
        #rebuild the task type
        #task data showed be rebuild
        #add old task into new task
        if self.extro_constrain==None:

            self.extro_constrain=The_extro_condition(agent_pose,finished_time_list,unfinished_task_list,begin_time,
                                            task_dic,task_execute_time,broken_agent_list)
        else:
            #this situation occurs when the agent break more than one time,so that the task need add the old task
            for task,time in self.extro_constrain.finished_time_list.items():
                if task not in finished_time_list.keys():
                    finished_time_list[task]=time
            num=0
            task_dic={}
            for i in range(len(self.task_data)):
                if not i in finished_time_list.keys():
                    task_dic[i]=num
                    num=num+1
            for i in finished_time_list.keys():
                if not self.task_data[i] in finished_task:
                    finished_task.add(self.task_data[i])
            self.extro_constrain=The_extro_condition(agent_pose,finished_time_list,unfinished_task_list,begin_time,
                                            task_dic,task_execute_time,broken_agent_list)

        bnb=Branch_And_Bound(self.poset,task_data,input_data)

        bnb.Begin_branch_search_online(search_time,self.extro_constrain,finished_task)
        new_solution=bnb.best_solution
        new_time_table=bnb.task_time_table
        return new_solution,new_time_table

    def get_real_execution_time_table(self):
        self.estimate_task_time_table=[[] for i in range(len(self.agent_data))]
        count=0
        for task_list in self.stage_track:
            count=count+1
            for i in range(len(self.agent_data)):
                if task_list[i] not in ['motion','stay']:
                    if not len(self.estimate_task_time_table[i])==0:
                        if task_list[i] == self.estimate_task_time_table[i][-1][0]:
                            if self.estimate_task_time_table[i][-1][2]+1==count:
                                self.estimate_task_time_table[i][-1][2]=count
                            else:
                                self.estimate_task_time_table[i].append([task_list[i],count,count])
                        else:
                            self.estimate_task_time_table[i].append([task_list[i],count,count])
                    else:
                        self.estimate_task_time_table[i].append([task_list[i],count,count])
        self.adapt_time_table=[[] for i in range(len(self.agent_data))]
        self.adapt_state_track.pop(0)
        count=0
        for task_list in self.adapt_state_track:
            count=count+1
            for i in range(len(self.agent_swarm)):
                print(i)
                if not len(self.adapt_time_table[i])==0:
                    if task_list[i] == self.adapt_time_table[i][-1][0]:
                        if self.adapt_time_table[i][-1][2]+1==count:
                            self.adapt_time_table[i][-1][2]=count
                        else:
                            self.adapt_time_table[i].append([task_list[i],count,count])
                    else:
                        self.adapt_time_table[i].append([task_list[i],count,count])
                else:
                    self.adapt_time_table[i].append([task_list[i],count,count])

# =========================

    def Turn_Matrix(self,M):
        r = [[] for i in M[0]]
        for i in M:
            for j in range(len(i)) :
                r[j].append(i[j])
        return  r

    def plot(self,num):
        self.field.plot_back_ground(self.agent_type,self.pose_track,self.stage_track,num)

    def plot_static(self,time,color_table,pre_name):
        self.field.plot_back_ground_with_time(self.agent_type,self.pose_track,self.stage_track,time,color_table,pre_name)


    def get_distance(self,i,j):
        #return self.position[(i,j)]
        pos1=self.position[i][0]-self.position[j][0]
        pos2=self.position[i][1]-self.position[j][1]
        lenth=(pos1**2+pos2**2)**0.5
        return lenth

class The_extro_condition:
    def __init__(self,agent_pose,finished_time_list,unfinished_task_list,begin_time,task_dic,task_execute_time,broken_agent_list):
        self.agent_pose=agent_pose
        # describe when the agent can to execute next action
        self.finished_time_list=finished_time_list
        self.unfinished_task_list=unfinished_task_list
        self.begin_time=begin_time
        self.task_dic=task_dic
        self.task_execute_time=task_execute_time
        self.broken_agent_list=broken_agent_list