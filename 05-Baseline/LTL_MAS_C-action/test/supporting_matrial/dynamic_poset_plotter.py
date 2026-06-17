import sys
from support_plotter import  Support_Plotter
import matplotlib.pyplot as plt

sys.path.append('/home/LZS/LTL/git/LTL_MAS_C-action/src')
sys.path.append('/home/dell/LTL_planning/LTL_MAS_C-action/src')
sys.path.append('/home/dell/LTL_planning/LTL_MAS_C-action')
from src.ltl_mas.experiment.phy_field_background_old import field



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

task_data_list=[(0, 'scanp3', 'p1'),
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


field_env=field()
field_env.init_background()
#a=optimize_method.Branch_And_Bound(Bu_poset.poset_list[0]['less-than'],Bu_poset.task_data_list[0],field_env.input_data)
solution=[[((2, 'washp5', 'p5'), 'wash_UAV'), ((0, 'scanp3', 'p3'), 'scan')],
 [((0, 'scanp3', 'p3'), 'scan'), ((4, 'scanp2', 'p2'), 'scan')],
 [((0, 'scanp3', 'p3'), 'scan'), ((4, 'scanp2', 'p2'), 'scan')],
 [((4, 'scanp2', 'p2'), 'scan')],
 [((3, 'repairp2', 'p2'), 'repair_UGV_s'),((5, 'sweepp2', 'p2'), 'sweep'),((1, 'fixt1', 't1'), 'fix_UGV_s')],
 [((2, 'washp5', 'p5'), 'wash_UGV_l'),  ((3, 'repairp2', 'p2'), 'repair_UGV_l'),((1, 'fixt1', 't1'), 'fix_UGV_l')]]

solution2=[[((2, 'washp5', 'p5'), 'wash_UAV'),((0, 'scanp3', 'p1'), 'scan'),((4, 'scanp2', 'p2'), 'scan') ],
 [((0, 'scanp3', 'p1'), 'scan'), ((4, 'scanp2', 'p2'), 'scan')],
 [((0, 'scanp3', 'p1'), 'scan'), ((4, 'scanp2', 'p2'), 'scan')],
 [],
 [((3, 'repairp2', 'p2'), 'repair_UGV_s'),
  ((5, 'sweepp2', 'p2'), 'sweep'),
  ((1, 'fixt1', 't1'), 'fix_UGV_s')],
 [((2, 'washp5', 'p5'), 'wash_UGV_l'),
  ((3, 'repairp2', 'p2'), 'repair_UGV_l'),
  ((1, 'fixt1', 't1'), 'fix_UGV_l')]]
task_time_table=[[0, 65.66753854700104, 79.66753854700104],
 [1, 115.08679631863114, 123.08679631863114],
 [2, 13.752272539475065, 55.752272539475065],
 [3, 71.30862172557912, 79.30862172557912],
 [4, 82.41753854700104, 96.41753854700104],
 [5, 79.30862172557912, 107.30862172557912]]
task_time_table2=[[0, 80.66753854700104, 94.66753854700104],
 [1, 132.08679631863114, 141.08679631863114],
 [2, 13.752272539475065, 55.752272539475065],
 [3, 89.30862172557912, 97.30862172557912],
 [4, 82.41753854700104, 96.41753854700104],
 [5, 97.30862172557912, 125.30862172557912]]

#data_name='/home/LZS/LTL/git/LTL_MAS_C-action/data/input_data/experiment_data/pathdata/pose_trajectory_of_normal_exam2.npy'
data_name='/home/LZS/LTL/git/LTL_MAS_C-action/data/input_data/experiment_data/pathdata/pose_trajectory_of_adapt_exam2.npy'
SP=Support_Plotter(data_name,task_data_list,solution,task_time_table)
SP.pre_treat_poset(poset)
SP.animate_plotter_poset(end=230)
color_varide0=['Greys','Purples','Blues','Greens','Oranges','Reds','YlOrBr','YlOrRd','OrRd','PuRd','RdPu','GnBu']
color_table=['#006400', 'c', 'k', '#6A5ACD', 'y','m', 'g', 'aqua', 'brown', '#FF0000','#FFDEAD','k']
