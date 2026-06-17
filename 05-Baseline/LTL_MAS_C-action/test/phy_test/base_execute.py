import sys
sys.path.append('/home/LZS/LTL/git/LTL_MAS_C-action/src')
sys.path.append('/home/dell/LTL_planning/LTL_MAS_C-action/src')
sys.path.append('/home/dell/LTL_planning/LTL_MAS_C-action')
from src.ltl_mas.tools.poset_builder import Buchi_poset_builder
from src.ltl_mas.tools.nx_plot.base_plot import plot
from src.ltl_mas.tools import optimize_method
from data import input_data
import numpy as np
import time
from src.ltl_mas.experiment.phy_field_background_old import field


task1='<>(repairp1_p32 && <> ( ! repairp32_p32 && photop32_p32)) && <> checkt6_t6 && <> weedp10_p10 && <> washp15_p15'
task1='<>(repairp2_p2 && <> ( photop2_p2)) && <> checkt1_t1 && <> weedp1_p1 && <> washp5_p5 && [](repairp2_p2 -> ! photop2_p2)'
task1='<>(repairp2_p2 && <> scanp2_p2 && <> sweepp2_p2) && <> fixt1_t1 && <>   scanp1_p1 && <> washp5_p5 && [](repairp2_p2 -> ! scanp2_p2)' \
      '&& [](repairp2_p2 -> ! sweepp2_p2)'
#task='<>(blow && <> ( wash && <> weed) && <> (sweep && <> photo)) &&[](wash -> ! weed)'
#solution=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/solution.npy')

start_for_NAB=time.time()
Bu_poset=Buchi_poset_builder(task1)#
Bu_poset.main_fun_to_get_poset(20)
end_for_NBA=time.time()
poset={'||': set(), '<=': {(3, 4)}, '<': set(),'!=': {(4, 3)},'=': set(),
'action_map': [['checkt4_t4'],['weedp1_p1'],['washp5_p5'],['repairp3_p3'],['photop3_p3']]}
poset={'||': set(),
 '<=': {(3, 4), (3, 5)},
 '<': set(),
 '!=': {(4, 3), (5, 3)},
 '=': set(),
 'action_map': ['scanp1_p1',
  'fixt1_t1',
  'washp5_p5',
  'repairp2_p2',
  'scanp2_p2',
  'sweepp2_p2']}

task_data_list=[(0, 'scanp1', 'p1'),
 (1, 'fixt1', 't1'),
 (2, 'washp5', 'p5'),
 (3, 'repairp2', 'p2'),
 (4, 'scanp2', 'p2'),
 (5, 'sweepp2', 'p2')]
task=[(0, 'repairp2', 'p2'),
 (1, 'mowp1', 'p1'),
 (2, 'sweepp2', 'p2'),
 (3, 'scanp2', 'p2'),
 (4, 'washp5', 'p5'),
 (5, 'fixt1', 't1')]

task_data_list2=[(0, 'checkt4', 't4'),
 (1, 'weedp1', 'p1'),
 (2, 'washp5', 'p5'),
 (3, 'repairp3', 'p3'),
 (4, 'photop3', 'p3')]
poset={'||': set(),
 '<=': {(3, 4), (3, 5)},
 '<': set(),
 '!=': {(4, 3), (5, 3)},
 '=': set(),
 'action_map': ['scanp3_p3',
  'fixt1_t1',
  'washp5_p5',
  'repairp2_p2',
  'scanp2_p2',
  'sweepp2_p2']}

task_data_list=[(0, 'scanp3', 'p3'),
 (1, 'fixt1', 't1'),
 (2, 'washp5', 'p5'),
 (3, 'repairp2', 'p2'),
 (4, 'scanp2', 'p2'),
 (5, 'sweepp2', 'p2')]
print("use time",end_for_NBA-start_for_NAB,"for NBA analysis")
field_env=field()
field_env.init_background()
field_env.plot_static_back_ground()
#a=optimize_method.Branch_And_Bound(Bu_poset.poset_list[0]['less-than'],Bu_poset.task_data_list[0],field_env.input_data)
end_time=time.time()
a=optimize_method.Branch_And_Bound2(poset,task_data_list,field_env.input_data)
a.Begin_branch_search2(1,up_bound_method='greedy',low_bound_method='i+j',search_method='DFS')
print(a.best_up_bound_list)
end_time=time.time()
print(end_time-start_for_NAB)
solution=[[((2, 'washp5', 'p5'), 'wash_UAV'), ((0, 'scanp1', 'p1'), 'scan')],
 [((0, 'scanp1', 'p1'), 'scan'), ((4, 'scanp2', 'p2'), 'scan')],
 [((0, 'scanp1', 'p1'), 'scan'), ((4, 'scanp2', 'p2'), 'scan')],
 [((4, 'scanp2', 'p2'), 'scan')],
 [((3, 'repairp2', 'p2'), 'repair_UGV_s'),
  ((5, 'sweepp2', 'p2'), 'sweep'),
  ((1, 'fixt1', 't1'), 'fix_UGV_s')],
 [((2, 'washp5', 'p5'), 'wash_UGV_l'),
  ((3, 'repairp2', 'p2'), 'repair_UGV_l'),
  ((1, 'fixt1', 't1'), 'fix_UGV_l')]]
a.get_time_table_of_best_solution(solution)
print(a.task_time_table)
exit()
solution1=[[((2, 'washp5', 'p5'), 'wash_UAV'), 'break'],
 [((0, 'scanp1', 'p1'), 'scan'), ((4, 'scanp2', 'p2'), 'scan')],
 [((0, 'scanp1', 'p1'), 'scan'), ((4, 'scanp2', 'p2'), 'scan')],
 [((0, 'scanp1', 'p1'), 'scan'),((4, 'scanp2', 'p2'), 'scan')],
 [((3, 'repairp2', 'p2'), 'repair_UGV_s'),
  ((5, 'sweepp2', 'p2'), 'sweep'),
  ((1, 'fixt1', 't1'), 'fix_UGV_s')],
 [((2, 'washp5', 'p5'), 'wash_UGV_l'),
  ((3, 'repairp2', 'p2'), 'repair_UGV_l'),
  ((1, 'fixt1', 't1'), 'fix_UGV_l')]]
solution2=[[((2, 'washp5', 'p5'), 'wash_UAV'),((0, 'scanp1', 'p1'), 'scan'),((4, 'scanp2', 'p2'), 'scan') ],
 [((0, 'scanp1', 'p1'), 'scan'), ((4, 'scanp2', 'p2'), 'scan')],
 [((0, 'scanp1', 'p1'), 'scan'), ((4, 'scanp2', 'p2'), 'scan')],
 [],
 [((3, 'repairp2', 'p2'), 'repair_UGV_s'),
  ((5, 'sweepp2', 'p2'), 'sweep'),
  ((1, 'fixt1', 't1'), 'fix_UGV_s')],
 [((2, 'washp5', 'p5'), 'wash_UGV_l'),
  ((3, 'repairp2', 'p2'), 'repair_UGV_l'),
  ((1, 'fixt1', 't1'), 'fix_UGV_l')]]
#first broken agent 0 break after at 60s
#second broken agent 3 break at 60s
#becaues the car has no redundancy, so we just test the broken of the agent.
task_time_table=[[0, 65.66753854700104, 79.66753854700104],
 [1, 115.08679631863114, 123.08679631863114],
 [2, 13.752272539475065, 55.752272539475065],
 [3, 71.30862172557912, 79.30862172557912],
 [4, 82.41753854700104, 96.41753854700104],
 [5, 79.30862172557912, 107.30862172557912]]


a=Agent_swarm(solution,poset,task_data_list,field_env,task_time_table)
a.pre_planning()
a.path_plotter()
a.begin_run(200,1,1)
# output the points to the ROS system
#a.begin_run(1300,1,0)
#a.plot(1000)
color_varide0=['Greys','Purples','Blues','Greens','Oranges','Reds','YlOrBr','YlOrRd','OrRd','PuRd','RdPu','GnBu']
color_table=['#006400', 'c', 'k', '#6A5ACD', 'y','m', 'g', 'aqua', 'brown', '#FF0000','#FFDEAD','k']

