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

task2='<>(washp11_p11 && <> (mowp11_p11 && <> sweepp11_p11) && <> scanp11_p11) && []((washp11_p11 || mowp11_p11) -> ! sweepp11_p11)' \
      '&&[](washp11_p11 -> ! mowp11_p11)&& [](washp11_p11 ->!scanp11_p11) ' \
'&& <>(washp20_p20 && <> (mowp20_p20 && <> sweepp20_p20)&& <> scanp20_p20) && []((washp20_p20 || mowp20_p20) -> ! sweepp20_p20) ' \
     '&&[](washp20_p20 -> ! mowp20_p20)&& [](washp20_p20 ->!scanp20_p20)'\
    '&& <> tempt4_t4'


task21='<>(blowp17_p17 && <> ( washp17_p17 && <> mowp17_p17) &&' \
      '<> sweepp17_p17 &&  <> photop17_p17 ) && ' \
      '[](washp17_p17 -> ! mowp17_p17) &&'\
      '[](blowp17_p17 -> (! washp17_p17 && ! sweepp17_p17 && ! photop17_p17)) &&'\
      '[](photop17_p17 -> ! sweepp17_p17)'# task conflict

#task='<>(blow && <> ( wash && <> weed) && <> (sweep && <> photo)) &&[](wash -> ! weed)'
#solution=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/solution.npy')
start_for_NAB=time.time()
Bu_poset=Buchi_poset_builder(task2)#
#Bu_poset.main_fun_to_get_poset(200)
end_for_NBA=time.time()
poset={'||': set(),
  '<=': {(1, 2), (1, 3), (3, 4), (5, 6), (5, 7), (6, 8)},
  '<': set(),
  '!=': {(2, 1), (3, 1), (4, 1), (4, 3), (6, 5), (7, 5), (8, 5), (8, 6)},
  '=': set(),
  'action_map': ['tempt4_t4',
   'washp11_p11',
   'scanp11_p11',
   'mowp11_p11',
   'sweepp11_p11',
   'washp20_p20',
   'mowp20_p20',
   'scanp20_p20',
   'sweepp20_p20']}


task_data_list=[(0, 'tempt4', 't4'),
  (1, 'washp11', 'p11'),
  (2, 'scanp11', 'p11'),
  (3, 'mowp11', 'p11'),
  (4, 'sweepp11', 'p11'),
  (5, 'washp20', 'p20'),
  (6, 'mowp20', 'p20'),
  (7, 'scanp20', 'p20'),
  (8, 'sweepp20', 'p20')]

print("use time",end_for_NBA-start_for_NAB,"for NBA analysis")
field_env=field()
field_env.init_background()
field_env.choose_agent_number(0)
begin_time=time.time()
a=optimize_method.MILP_CVXPY(poset,task_data_list,field_env.input_data)
a.Base_OPT_MILP_of_cvxpy()
#a.get_time_table_of_best_solution(solution)
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/time_table.npy',a.task_time_table)
  #.position,input_data.agent_data,input_data.task_data,
#                            input_data.task_type,input_data.sub_task_type,input_data.agent_type)
end1=time.time()
print(end1-begin_time)
print(end1-start_for_NAB)
exit()
a.Begin_branch_search2(100,up_bound_method='greedy',low_bound_method='i_j',search_method='DFS')
a.plt_bnb_graph()
end2=time.time()
print('totally time cost',end2-end1)#
start=time.time()
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task2/solution_s0.npy', solution)
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task2/solution_s3.npy',a.best_solution)
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task2/time_table_s3.npy',a.task_time_table)
solution=[[((2, 'scanp11', 'p11'), 'scan')],
 [((1, 'washp11', 'p11'), 'wash_UAV'),
  ((2, 'scanp11', 'p11'), 'scan')],
 [((0, 'tempt4', 't4'), 'temp'), ((2, 'scanp11', 'p11'), 'scan')],
 [((7, 'scanp20', 'p20'), 'scan')],
 [((7, 'scanp20', 'p20'), 'scan')],
 [((5, 'washp20', 'p20'), 'wash_UAV'),
  ((7, 'scanp20', 'p20'), 'scan')],
 [],
 [ ((1, 'washp11', 'p11'), 'wash_UGV_l')],
 [((5, 'washp20', 'p20'), 'wash_UGV_l')],
 [((8, 'sweepp20', 'p20'), 'sweep')],
 [((3, 'mowp11', 'p11'), 'mow'),((4, 'sweepp11', 'p11'), 'sweep')],
 [((6, 'mowp20', 'p20'), 'mow')]]

task_time_table=[[0, 23.530830839560252, 33.53083083956025],
 [1, 113.47356520353105, 678.473565203531],
 [2, 678.473565203531, 773.473565203531],
 [3, 678.473565203531, 868.473565203531],
 [4, 868.473565203531, 1058.473565203531],
 [5, 100.49875621120896, 665.498756211209],
 [6, 665.498756211209, 855.498756211209],
 [7, 665.498756211209, 760.498756211209],
 [8, 855.498756211209, 1045.498756211209]]



a=Agent_swarm(solution,poset,task_data_list,field_env,task_time_table)
a.pre_planning()
a.begin_run(2000,1,0)
#a.plot(1000)
color_table=['#006400', 'c', 'k', '#6A5ACD', 'y','m', 'g', 'aqua', 'brown', '#FF0000','#FFDEAD','k']
#for i in range(100,1000,100):
#     a.plot_static(i,color_table)
a.plot_static(1300,color_table,'task2/task2_motion_fig_at_time_')


