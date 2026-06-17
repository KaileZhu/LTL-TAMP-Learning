import copy
import sys
sys.path.append('/home/LZS/LTL/git/LTL_MAS_C-action/src')
from ltl_mas.simulate.field_background import field
import matplotlib.pyplot as plt
import numpy as np
from ltl_mas.simulate.UAV_agent import  UAV_swarm
from data.input_data.agent_data import agent_type,agent_data
from data.input_data import map_data
from ltl_mas.simulate.plotting import Plotting
solution=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/solution.npy')
#task='<> (search_a && <> (goto_b && <> formation_d)) && <> (goto_c)'
#Bu_poset=Buchi_poset_builder(task)
#Bu_poset.main_fun_to_get_poset()



related_poset={(2,3)}
agent_list=[]
time_step=0.5
interested_map=map_data.position
t=0
for i in range(len(solution)):
    agent_list.append(UAV_swarm(t,agent_data[i],solution[i],related_poset,interested_map,time_step))
    t=t+1
for i in range(len(agent_list)):

    agent_list[i].init_pose[0]=agent_list[i].init_pose[0]+i/20
    agent_list[i].init_pose[1]=agent_list[i].init_pose[1]+i/20

    agent_list[i].current_pose[0]=agent_list[i].current_pose[0]+i/20
    agent_list[i].current_pose[1]=agent_list[i].current_pose[1]+i/20

global_time=0
finish_task=set()
todo_co_task_list=[]
todo_co_task_list2=[]
pose_track=[]
stage_track=[]
for i in range(250):
    pose_list=[]
    new_task_list=set()
    stage_list=[]
    for agent in agent_list:
        pose,task,todo_co_task=agent.execute_task(global_time,finish_task,todo_co_task_list2)
        stage_list.append(agent.motion_type_list[agent.current_stage_ID])
        pose_list.append(pose)
        new_task_list=new_task_list.union(task)
        if not todo_co_task==set():
            todo_co_task_list.append(todo_co_task)
        #print('at time:',global_time,'   ',end='')
    pose_track.append(pose_list)
    stage_track.append(stage_list)
    todo_co_task_list2=copy.deepcopy(todo_co_task_list)
    todo_co_task_list=[]
    #print('todo', todo_co_task_list2)
    finish_task=finish_task.union(new_task_list)
    global_time=global_time+time_step

plot = Plotting((0,0), (1,1))#,task_list)
plot.plot_trajectory(pose_track,stage_track)
plt.show()