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

task31='<>(repairp1_p1 && <> scanp1_p1) && [] (repairp1_p1 -> ! scanp1_p1) &&' \
      ' <>(fixt6_t6 && <> scant6_t6)  && [] (fixt6_t6 -> ! scant6_t6)&& ' \
      '<>(washp7_p7 && <> (mowp7_p7 && <> sweepp7_p7) && <> scanp7_p7) && []((washp7_p7 || mowp7_p7) -> ! sweepp7_p7)' \
      '&&[](washp7_p7 -> ! mowp7_p7)&& [](washp7_p7 ->!scanp7_p7) && ' \
      '<> tempp24_p24 && <> tempp17_p17 &&' \
       ' <>(repairp5_p5 && <> scanp5_p5) && [] (repairp5_p5 -> ! scanp5_p5) &&'\
       ' <>(fixt3_t3 && <> scant3_t3)  && [] (fixt3_t3 -> ! scant3_t3)&&' \
       '<>(washp20_p20 && <> (mowp20_p20 && <> sweepp20_p20) && <> scanp20_p20) && []((washp20_p20 || mowp20_p20) -> ! sweepp20_p20)'

task3='<>(repairp1_p1 && <> scanp1_p1) && [] (repairp1_p1 -> ! scanp1_p1) &&' \
      ' <>(fixt6_t6 && <> scant6_t6)  && [] (fixt6_t6 -> ! scant6_t6)&& ' \
      '<>(washp7_p7 && <> (mowp7_p7 && <> sweepp7_p7) && <> scanp7_p7) && []((washp7_p7 || mowp7_p7) -> ! sweepp7_p7)' \
      '&&[](washp7_p7 -> ! mowp7_p7)&& [](washp7_p7 ->!scanp7_p7) && ' \
      '<> tempp24_p24 '
#task31='<>(washp11_p11 && <> (mowp11_p11 && <> sweepp11_p11) && <> scanp11_p11) && []((washp11_p11 || mowp11_p11) -> ! sweepp11_p11)' \
 #     '&&[](washp11_p11 -> ! mowp11_p11)&& [](washp11_p11 ->!scanp11_p11) &&' \
  #    ' <>(fixt6_t6 && <> scant6_t6) && [] (fixt6_t6 -> ! scant6_t6) && ' \
   #   '<>(repairp31_p31 && <> scanp31_p31) && [] (repairp31_p31 -> ! scanp31_p31) && <> scanp6_p6 && ' \
    #  '<>repairp33_p33 '
#1-2  7 - 17
#add the or relation
#task='<>(blow && <> ( wash && <> weed) && <> (sweep && <> photo)) &&[](wash -> ! weed)'
#solution=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/solution.npy')
# start_for_NAB=time.time()
#Bu_poset=Buchi_poset_builder(task3)#
#Bu_poset.main_fun_to_get_poset(50)
# end_for_NBA=time.time()
# print('execute time', end_for_NBA-start_for_NAB)
# print('pruning_time',Bu_poset.pruning_step_time)
# print('poset time',Bu_poset.poset_ana_time)
# break3

poset={'||': set(),
 '<=': {(1, 6), (2, 4), (3, 5), (3, 7), (7, 8),
        (10, 15), (11, 13), (12, 14), (12, 16), (16, 17)},
 '<': set(),
 '!=': {(4, 2), (5, 3), (6, 1), (7, 3), (8, 3), (8, 7),
        (13, 11), (14, 12), (15, 10), (16, 12), (17, 12), (17, 16)},
 '=': set(),
 'action_map': ['tempp24_p24',
  'repairp1_p1',
  'fixt6_t6',
  'washp7_p7',
  'scant6_t6',
  'scanp7_p7',
  'scanp1_p1',
  'mowp7_p7',
  'sweepp7_p7',
  'tempp17_p17',
  'repairp5_p5',
  'fixt3_t3',
  'washp20_p20',
  'scant3_t3',
  'scanp20_p20',
  'scanp5_p5',
  'mowp20_p20',
  'sweepp20_p20']}

task_data_list=  [(0, 'tempp24', 'p24'),
  (1, 'repairp1', 'p1'),
  (2, 'fixt6', 't6'),
  (3, 'washp7', 'p7'),
  (4, 'scant6', 't6'),
  (5, 'scanp7', 'p7'),
  (6, 'scanp1', 'p1'),
  (7, 'mowp7', 'p7'),
  (8, 'sweepp7', 'p7'),
  (9, 'tempp17', 'p17'),
  (10, 'repairp5', 'p5'),
  (11, 'fixt3', 't3'),
  (12, 'washp20', 'p20'),
  (13, 'scant3', 't3'),
  (14, 'scanp20', 'p20'),
  (15, 'scanp5', 'p5'),
  (16, 'mowp20', 'p20'),
  (17, 'sweepp20', 'p20')]

# print("use time",end_for_NBA-start_for_NAB,"for NBA analysis")
field_env=field()
field_env.init_background()
a=optimize_method.Branch_And_Bound2(poset,task_data_list,field_env.input_data)


end1=time.time()
a.Begin_branch_search2(1,up_bound_method='greedy',low_bound_method='i+j',search_method='DFS')
#print(a.low_bound_list)
#print(a.upper_bound_list)
print(a.best_up_bound_list)
cut_node_count=0
nu0_list = []
nu1_list = []
for n,nu in a.low_bound_list.items():
    if nu[2]=='cut':
        cut_node_count=cut_node_count+1
print(cut_node_count/len(a.low_bound_list))

a.plot_bnb_graph_phi3(load='1')
exit()
#
# [((13, 'scant3', 't3'), 'scan'), ((5, 'scanp7', 'p7'), 'scan'), ((6, 'scanp1', 'p1'), 'scan'), ((15, 'scanp5', 'p5'), 'scan')]
# [((5, 'scanp7', 'p7'), 'scan'), ((4, 'scant6', 't6'), 'scan'), ((14, 'scanp20', 'p20'), 'scan'), ((15, 'scanp5', 'p5'), 'scan')]
#  [((3, 'washp7', 'p7'), 'wash_UAV'), ((15, 'scanp5', 'p5'), 'scan')]
#  [((9, 'tempp17', 'p17'), 'temp'), ((13, 'scant3', 't3'), 'scan'), ((5, 'scanp7', 'p7'), 'scan'), ((6, 'scanp1', 'p1'), 'scan'), ((4, 'scant6', 't6'), 'scan')]
# [((12, 'washp20', 'p20'), 'wash_UAV'), ((4, 'scant6', 't6'), 'scan'), ((14, 'scanp20', 'p20'), 'scan')]
#  [((0, 'tempp24', 'p24'), 'temp'), ((13, 'scant3', 't3'), 'scan'), ((6, 'scanp1', 'p1'), 'scan'), ((14, 'scanp20', 'p20'), 'scan')]
#  [((1, 'repairp1', 'p1'), 'repair_UGV_l')]
# [((3, 'washp7', 'p7'), 'wash_UGV_l'), ((10, 'repairp5', 'p5'), 'repair_UGV_l')]
#  [((11, 'fixt3', 't3'), 'fix_UGV_l'), ((2, 'fixt6', 't6'), 'fix_UGV_l'), ((12, 'washp20', 'p20'), 'wash_UGV_l')]
# [((1, 'repairp1', 'p1'), 'repair_UGV_s'), ((10, 'repairp5', 'p5'), 'repair_UGV_s'), ((8, 'sweepp7', 'p7'), 'sweep')]
#  [((1, 'repairp1', 'p1'), 'repair_UGV_s'), ((7, 'mowp7', 'p7'), 'mow'), ((16, 'mowp20', 'p20'), 'mow'), ((17, 'sweepp20', 'p20'), 'sweep')]
#  [((11, 'fixt3', 't3'), 'fix_UGV_s'), ((2, 'fixt6', 't6'), 'fix_UGV_s'), ((10, 'repairp5', 'p5'), 'repair_UGV_s')]