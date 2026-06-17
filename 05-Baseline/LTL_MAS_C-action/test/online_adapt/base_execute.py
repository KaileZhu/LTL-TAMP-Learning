import sys
sys.path.append('/home/LZS/LTL/git/LTL_MAS_C-action/src')
from src.ltl_mas.tools.poset_builder import Buchi_poset_builder
from src.ltl_mas.tools.nx_plot.base_plot import plot
from src.ltl_mas.tools import optimize_method
from data import input_data
import numpy as np
import time
from src.ltl_mas.simulate.field_background import field
from src.ltl_mas.simulate.Agent_swarm import Agent_swarm
from Gantt_platter_task3_by_execution import gantt_plotter
import matplotlib.pyplot as plt



task3='<>(repairp1_p1 && <> scanp1_p1) && [] (repairp1_p1 -> ! scanp1_p1) &&' \
      ' <>(fixt6_t6 && <> scant6_t6)  && [] (fixt6_t6 -> ! scant6_t6)&& ' \
      '<>(washp7_p7 && <> (mowp7_p7 && <> sweepp7_p7) && <> scanp7_p7) && []((washp7_p7 || mowp7_p7) -> ! sweepp7_p7)' \
      '&&[](washp7_p7 -> ! mowp7_p7)&& [](washp7_p7 ->!scanp7_p7) && ' \
      '<> scanp24_p24'
start_for_NAB=time.time()
end_for_NBA=time.time()

poset={'||': set(),
 '<=': {(1, 6), (2, 4), (3, 5), (3, 7), (7, 8)},
 '<': set(),
 '!=': {(4, 2), (5, 3), (6, 1), (7, 3), (8, 3), (8, 7)},
 '=': set(),
 'action_map': ['scanp24_p24',
  'repairp1_p1',
  'fixt6_t6',
  'washp7_p7',
  'scant6_t6',
  'scanp7_p7',
  'scanp1_p1',
  'mowp7_p7',
  'sweepp7_p7']}


task_data_list=  [(0, 'scanp24', 'p24'),
  (1, 'repairp1', 'p1'),
  (2, 'fixt6', 't6'),
  (3, 'washp7', 'p7'),
  (4, 'scant6', 't6'),
  (5, 'scanp7', 'p7'),
  (6, 'scanp1', 'p1'),
  (7, 'mowp7', 'p7'),
  (8, 'sweepp7', 'p7')]

print("use time",end_for_NBA-start_for_NAB,"for NBA analysis")
field_env=field()
field_env.init_background()
a=optimize_method.Branch_And_Bound2(poset,task_data_list,field_env.input_data)


end1=time.time()
#a.Begin_branch_search2(20,up_bound_method='greedy',low_bound_method='i_j',search_method='DFS')

end2=time.time()
print('totally time cost',end2-end1)#
#start=time.time()
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task3/solution_s0.npy',solution)
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task3/time_table_s0.npy',task_time_table)
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task3/time_table_s3.npy',a.task_time_table)

solution=[[((4, 'scant6', 't6'), 'scan')],
 [((6, 'scanp1', 'p1'), 'scan'), ((0, 'scanp24', 'p24'), 'scan')],
 [((6, 'scanp1', 'p1'), 'scan'), ((0, 'scanp24', 'p24'), 'scan')],
 [((5, 'scanp7', 'p7'), 'scan'),
  ((6, 'scanp1', 'p1'), 'scan'),
  ((0, 'scanp24', 'p24'), 'scan')],
 [((5, 'scanp7', 'p7'), 'scan'), ((4, 'scant6', 't6'), 'scan')],
 [((3, 'washp7', 'p7'), 'wash_UAV'),
  ((5, 'scanp7', 'p7'), 'scan'),
  ((4, 'scant6', 't6'), 'scan')],
 [((1, 'repairp1', 'p1'), 'repair_UGV_l')],
 [],
 [((3, 'washp7', 'p7'), 'wash_UGV_l'), ((2, 'fixt6', 't6'), 'fix_UGV_l')],
 [((1, 'repairp1', 'p1'), 'repair_UGV_s')],
 [((1, 'repairp1', 'p1'), 'repair_UGV_s'),
  ((2, 'fixt6', 't6'), 'fix_UGV_s')],
 [((7, 'mowp7', 'p7'), 'mow'),
  ((8, 'sweepp7', 'p7'), 'sweep')]]


task_time_table=[[0, 966.964590023048, 1061.964590023048],
 [1, 170.03676073131953, 746.0367607313195],
 [2, 893.1397388636133, 965.1397388636133],
 [3, 168.80832325451252, 733.8083232545125],
 [4, 965.1397388636133, 1001.1397388636133],
 [5, 733.8083232545125, 828.8083232545125],
 [6, 848.7193754617666, 943.7193754617666],
 [7, 733.8083232545125, 923.8083232545125],
 [8, 923.8083232545125, 1113.8083232545125]]




a=Agent_swarm(solution,poset,task_data_list,field_env,task_time_table)
a.pre_planning()
#for node in a.field.node_set_for_barrier:
    #plt.plot(node[0],node[1],'^')
#a.path_plotter()
a.begin_run(1500,1,1)

a.get_real_execution_time_table()
#a.plot(1000)
color_table=['#006400', 'c', 'k', '#6A5ACD', 'y','m', 'g', 'aqua', 'brown', '#FF0000','#FFDEAD','k']
gantt_plotter('3',a.estimate_task_time_table)
np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/onlineadapt/estimate_task_time_table_s3.npy',a.estimate_task_time_table)

a.plot_static(1450,color_table,'onlineadapt/task3_motion_fig_at_time_online_s3')
s=1


