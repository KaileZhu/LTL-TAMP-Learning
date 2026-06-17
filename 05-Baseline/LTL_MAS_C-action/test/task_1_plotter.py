import sys
sys.path.append('/home/LZS/LTL/git/LTL_MAS_C-action/src')
from ltl_mas.tools.poset_builder import Buchi_poset_builder
from ltl_mas.tools.nx_plot.base_plot import plot
from ltl_mas.tools import optimize_method
from data import input_data
import numpy as np
import time
import matplotlib.pyplot as plt
from ltl_mas.simulate.field_background import field
from ltl_mas.simulate.Agent_swarm import Agent_swarm
from ltl_mas.tools.nx_plot.bezier_method import smoothing_base_bezier

task1='<>(repairp32_p32 && <> ( ! repairp32_p32 && photop32_p32)) && <> checkt6_t6 && <> weedp10_p10 && <> washp15_p15'

field_env=field()
#start=time.time()

#a=Agent_swarm(a.best_solution,Bu_poset.poset_list[0],Bu_poset.task_data_list[0],field_env,a.task_time_table)
poset_list=[[0, 'repairp32', 'p32'],
       [1, 'photop32', 'p32'],
       [2, 'weedp10', 'p10'],
       [3, 'checkt6', 't6'],
       [4, 'washp15', 'p15']]
time_table=[[  0.        , 442.30668948, 632.30668948],
       [  1.        , 632.30671853, 727.30671853],
       [  2.        , 727.30669413, 917.30669413],
       [  3.        , 332.02888856, 427.02888856],
       [  4.        , 332.02888392, 522.02888392],
       [  5.        ,  33.76165635, 223.76165635],
       [  6.        , 223.76164191, 318.76164191],
       [  7.        , 318.76160698, 883.76160698]]
poset={'||': {(1, 2), (1, 3), (1, 4), (2, 4), (2, 3), (0, 4), (0, 3), (3, 4), (0, 2)},
       '<=': set(), '<': {(0, 1)}, '!=': set(), '=': set(),
       'action_map': [['repairp32_p32'], ['photop32_p32'], ['weedp10_p10'], ['checkt6_t6'], ['washp15_p15']]}
solution=[[],
       [((4, 'washp15', 'p15'), 'wash_UAV'), ((1, 'photop32', 'p32'), 'photo')],
       [], [((1, 'photop32', 'p32'), 'photo')],
       [((1, 'photop32', 'p32'), 'photo')],
       [((0, 'repairp32', 'p32'), 'repair_UGV_l')],
       [((3, 'checkt6', 't6'), 'check_UGV_l')],
       [((4, 'washp15', 'p15'), 'wash_UGV_l')],
       [((3, 'checkt6', 't6'), 'check_UGV_s'), ((0, 'repairp32', 'p32'), 'repair_UGV_s')],
       [((2, 'weedp10', 'p10'), 'weed'), ((0, 'repairp32', 'p32'), 'repair_UGV_s')]]


a=Agent_swarm(solution,poset,poset_list,field_env,time_table)
a.pre_planning()
a.begin_run(1300,1,0)
#a.plot(1000)
color_table=['#006400', 'c', 'k', '#6A5ACD', 'y','m', 'g', 'aqua', 'brown', '#FF0000','#FFDEAD','B8860B']
agent_path=a.pose_track
path_agent=[[] for i in range(len(agent_path[0]))]
for agent_time in agent_path:
    for i in range(len(agent_path[0])):
           path_agent[i].append(agent_time[i])
#x_curve, y_curve =smoothing_base_bezier([path_agent[1][i*2][0] for i in range(len(path_agent[0])//2-1)], [path_agent[1][i*2][1] for i in range(len(path_agent[0])//2-1)],0.6)
#plt.plot(x_curve, y_curve, label='$k=0.3$')
#plt.show()
a.plot_static(200,color_table)
plt.savefig('gantte_task1_s3.eps',format='eps',dpi=100)

