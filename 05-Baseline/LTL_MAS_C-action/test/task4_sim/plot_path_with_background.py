import sys
sys.path.append('/home/LZS/LTL/git/LTL_MAS_C-action/src')
from ltl_mas.tools.poset_builder import Buchi_poset_builder
from ltl_mas.tools.nx_plot.base_plot import plot
from ltl_mas.tools import optimize_method
from data import input_data
import numpy as np
import time
from ltl_mas.simulate.field_background import field
from ltl_mas.simulate.Agent_swarm import Agent_swarm
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
#a=optimize_method.Branch_And_Bound2(poset,task_data_list,field_env.input_data)


end1=time.time()
#a.Begin_branch_search2(1,up_bound_method='greedy',low_bound_method='i+j',search_method='DFS')
#a.plot_bnb_graph_phi3(load='3')

end2=time.time()
print('totally time cost',end2-end1)#
#start=time.time()
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task3/solution_s0.npy',solution)
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task3/time_table_s0.npy',task_time_table)
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task3/time_table_s3.npy',a.task_time_table)

solution=[[((0, 'tempp24', 'p24'), 'temp'),
  ((5, 'scanp7', 'p7'), 'scan'),
  ((13, 'scant3', 't3'), 'scan'),
  ((15, 'scanp5', 'p5'), 'scan')],
 [((14, 'scanp20', 'p20'), 'scan'),
  ((6, 'scanp1', 'p1'), 'scan'),
  ((13, 'scant3', 't3'), 'scan'),
  ((15, 'scanp5', 'p5'), 'scan')],
 [((9, 'tempp17', 'p17'), 'temp'),
  ((6, 'scanp1', 'p1'), 'scan'),
  ((4, 'scant6', 't6'), 'scan'),
  ((13, 'scant3', 't3'), 'scan')],
 [((12, 'washp20', 'p20'), 'wash_UAV'),
  ((14, 'scanp20', 'p20'), 'scan'),
  ((5, 'scanp7', 'p7'), 'scan'),
  ((4, 'scant6', 't6'), 'scan')],
 [((14, 'scanp20', 'p20'), 'scan'),
  ((6, 'scanp1', 'p1'), 'scan'),
  ((15, 'scanp5', 'p5'), 'scan')],
 [((3, 'washp7', 'p7'), 'wash_UAV'),
  ((5, 'scanp7', 'p7'), 'scan'),
  ((4, 'scant6', 't6'), 'scan')],
 [((1, 'repairp1', 'p1'), 'repair_UGV_l'), ((11, 'fixt3', 't3'), 'fix_UGV_l')],
 [((12, 'washp20', 'p20'), 'wash_UGV_l'), ((2, 'fixt6', 't6'), 'fix_UGV_l')],
 [((3, 'washp7', 'p7'), 'wash_UGV_l'),
  ((10, 'repairp5', 'p5'), 'repair_UGV_l')],
 [((1, 'repairp1', 'p1'), 'repair_UGV_s'),
  ((2, 'fixt6', 't6'), 'fix_UGV_s'),
  ((10, 'repairp5', 'p5'), 'repair_UGV_s')],
 [((1, 'repairp1', 'p1'), 'repair_UGV_s'),
  ((11, 'fixt3', 't3'), 'fix_UGV_s'),
  ((10, 'repairp5', 'p5'), 'repair_UGV_s')],
 [((16, 'mowp20', 'p20'), 'mow'),
  ((17, 'sweepp20', 'p20'), 'sweep'),
  ((7, 'mowp7', 'p7'), 'mow'),
  ((8, 'sweepp7', 'p7'), 'sweep')]]



task_time_table=[[0, 11.359577456930339, 201.35957745693034],
 [1, 170.03676073131953, 746.0367607313195],
 [2, 789.3589548124138, 861.3589548124138],
 [3, 168.80832325451252, 733.8083232545125],
 [4, 923.9526055270246, 959.9526055270246],
 [5, 797.0863224052044, 892.0863224052044],
 [6, 785.6085152701884, 880.6085152701884],
 [7, 1136.9676716961976, 1326.9676716961976],
 [8, 1326.9676716961976, 1516.9676716961976],
 [9, 26.53846265328872, 216.53846265328872],
 [10, 1012.5872652967348, 1588.5872652967348],
 [11, 882.5221079302039, 954.5221079302039],
 [12, 100.49875621120896, 665.498756211209],
 [13, 985.9468356560359, 1021.9468356560359],
 [14, 665.498756211209, 760.498756211209],
 [15, 1588.5872652967348, 1683.5872652967348],
 [16, 665.498756211209, 855.498756211209],
 [17, 855.498756211209, 1045.498756211209]]




a=Agent_swarm(solution,poset,task_data_list,field_env,task_time_table)
a.pre_planning()
#for node in a.field.node_set_for_barrier:
    #plt.plot(node[0],node[1],'^')
#a.path_plotter()
a.begin_run(1600,1,1)

a.get_real_execution_time_table()
#a.plot(1000)
color_table=['#006400', 'c', 'k', '#6A5ACD', 'y','m', 'g', 'aqua', 'brown', '#FF0000','#FFDEAD','k']
#gantt_plotter('3','0',a.estimate_task_time_table,a.adapt_time_table)
#a.plot_static(i,color_table,'task3/task3_motion_fig_at_time_')
#for i in [40,200,240,340,450,632,727]:
#     a.plot_static(i,color_table,'task3/task3_motion_fig_at_time_')
#==== add the back ground graph

a.plot_static(1450,color_table,'task3/task3_motion_fig_at_time_online')
s=1


