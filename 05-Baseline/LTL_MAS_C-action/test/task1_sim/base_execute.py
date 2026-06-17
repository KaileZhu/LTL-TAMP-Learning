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


task1='<>(repairp31_p31 && <> ( ! repairp31_p31 && photop31_p31)) && <> checkt6_t6 && <> weedp10_p10 && <> washp15_p15'

task1='<>(repairp31_p31 && <> scanp31_p31) && [] (repairp31_p31 -> ! scanp31_p31) && <>(fixt6_t6 && <> scant6_t6)' \
      '&& [] (fixt6_t6 -> ! scant6_t6) && <> washp15_p15 && <> mowp8_p8'
#task1='<> (p1 && <> p2 ) && <> (p2 && <> p3) '
#task1='<> (p2 && <> (p1 && p2)) '
#task1='<>(repairp3_p3 && <> ( photop3_p3)) && <> checkt4_t4 && <> weedp1_p1 && <> washp5_p5 && [](repairp3_p3 -> ! photop3_p3)'
#32-3
#6->4
#10->1
#15-5
#task='<>(blow && <> ( wash && <> weed) && <> (sweep && <> photo)) &&[](wash -> ! weed)'
#solution=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/solution.npy')
start_for_NAB=time.time()
Bu_poset=Buchi_poset_builder(task1)#
Bu_poset.main_fun_to_get_poset(1)
end_for_NBA=time.time()
#print('execute time', end_for_NBA-start_for_NAB)
#print('pruning_time',Bu_poset.pruning_step_time)
#print('poset time',Bu_poset.poset_ana_time)
#break3
poset={'||': set(),
  '<=': {(0, 1), (2, 3)},
  '<': set(),
  '!=': {(1, 0),(3,2)},
  '=': set(),
  'action_map': ['fixt6_t6',
   'scant6_t6',
   'repairp31_p31',
   'scanp31_p31',
   'washp15_p15',
   'mowp8_p8']}


task_data_list=[(0, 'fixt6', 't6'),
  (1, 'scant6', 't6'),
  (2, 'repairp31', 'p31'),
  (3, 'scanp31', 'p31'),
  (4, 'washp15', 'p15'),
  (5, 'mowp8', 'p8')]

#print("use time",end_for_NBA-start_for_NAB,"for NBA analysis")
field_env=field()
field_env.init_background()
#a=optimize_method.Branch_And_Bound(Bu_poset.poset_list[0]['less-than'],Bu_poset.task_data_list[0],field_env.input_data)
a=optimize_method.Branch_And_Bound2(poset,task_data_list,field_env.input_data)
#a.generate_time_budget()
#root_node=[[] for i in a.agent_data]#(solution,assigned_task)
#assigned_tasks=[]
#self.get_lower_bound(low_bound_method)
#up_bound,solution=self.get_upper_bound(root_node,assigned_tasks,up_bound_method)
begin=time.time()
a.Begin_branch_search2(1,up_bound_method='greedy',low_bound_method='i+j',search_method='DFS')
end1=time.time()
print(end1-begin)

a.plot_bnb_graph_phi1(load='1')
#a.Begin_branch_search2(2000,up_bound_method='greedy',low_bound_method='i_j',search_method='DFS')
exit()
end2=time.time()
print('totally time cost',end2-end1)#
#start=time.time()
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/solution.npy',a.best_solution)
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/anchorfunction.npy',Bu_poset.task_data_list[0])
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/poset.npy',Bu_poset.poset_list[0])
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/time_table.npy',a.task_time_table)
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task1/solution_s0.npy', a.best_solution)
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task1/time_table_s0.npy', a.task_time_table)
#solution=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task1/solution_s0.npy')
solution=[[((3, 'scanp31', 'p31'), 'scan')],
 [((1, 'scant6', 't6'), 'scan')],
 [((3, 'scanp31', 'p31'), 'scan')],
 [((3, 'scanp31', 'p31'), 'scan')],
 [((1, 'scant6', 't6'), 'scan')],
 [((4, 'washp15', 'p15'), 'wash_UAV'), ((1, 'scant6', 't6'), 'scan')],
 [((0, 'fixt6', 't6'), 'fix_UGV_l')],
 [((2, 'repairp31', 'p31'), 'repair_UGV_l')],
 [((4, 'washp15', 'p15'), 'wash_UGV_l')],
 [((2, 'repairp31', 'p31'), 'repair_UGV_s')],
 [((2, 'repairp31', 'p31'), 'repair_UGV_s')],
 [((5, 'mowp8', 'p8'), 'mow'), ((0, 'fixt6', 't6'), 'fix_UGV_s')]]




task_time_table=[[0, 340.7390722338504, 412.7390722338504],
 [1, 694.7520575366232, 730.7520575366232],
 [2, 60.14149981501953, 636.1414998150195],
 [3, 636.1414998150195, 731.1414998150195],
 [4, 119.8540779448075, 684.8540779448075],
 [5, 70.12889917858399, 260.128899178584]]

a=Agent_swarm(solution,poset,task_data_list,field_env,task_time_table)
a.pre_planning()
a.begin_run(1000,1,0)
#a.plot(1000)
color_varide0=['Greys','Purples','Blues','Greens','Oranges','Reds','YlOrBr','YlOrRd','OrRd','PuRd','RdPu','GnBu']
color_table=['#006400', 'c', 'k', '#6A5ACD', 'y','m', 'g', 'aqua', 'brown', '#FF0000','#FFDEAD','k']
a.plot_static(900,color_table,'task1/task1_motion_fig_at_time_323')
#import matplotlib.pyplot as plt
#for node in a.field.node_set_for_barrier:
#    plt.plot(node[0],node[1],'*')
#a.plot_static(800,color_table,'task1/task1_motion_fig_at_time_323')

s=1
#for i in [520,530,540,550]:

#for i in range(100,1000,100):
    #a.plot_static(i,color_table,'task1/task1_motion_fig_at_time_')


