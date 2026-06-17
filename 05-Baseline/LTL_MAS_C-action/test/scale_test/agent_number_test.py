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
import  matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

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
#start_for_NAB=time.time()
#Bu_poset=Buchi_poset_builder(task2)#
#Bu_poset.main_fun_to_get_poset(30)
#end_for_NBA=time.time()
#print('execute time', end_for_NBA-start_for_NAB)
#print('pruning_time',Bu_poset.pruning_step_time)
#print('poset time',Bu_poset.poset_ana_time)
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

#print("use time",end_for_NBA-start_for_NAB,"for NBA analysis")
field_env=field()
field_env.init_background()
first_solution=[]
ten_percent_solution=[]
best_solution=[]
for i in range(5):
    field_env.choose_agent_number(i)
    a=optimize_method.Branch_And_Bound2(poset,task_data_list,field_env.input_data)
    if i<=1:
        a.Begin_branch_search2(80,up_bound_method='greedy',low_bound_method='i+j',search_method='DFS')
    else:
        a.Begin_branch_search2(40,up_bound_method='greedy',low_bound_method='i+j',search_method='DFS')
    first_solution.append(a.upper_bound_list[1])
    ten_percent_solution.append(a.best_up_bound_list)
    best_solution.append(a.best_up_bound_list)
#a.get_time_table_of_best_solution(solution)
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/time_table.npy',a.task_time_table)
  #.position,input_data.agent_data,input_data.task_data,
#                            input_data.task_type,input_data.sub_task_type,input_data.agent_type)

for best_up_bound_list in best_solution:
    percent_list_x=[]
    percent_list_y=[]
    optimal_value=list(best_up_bound_list.items())[-1][1][0]
    for value,time in best_up_bound_list.items():
        percent_list_y.append(time[0]/optimal_value)
        percent_list_x.append(time[1])
    plt.plot(percent_list_x,percent_list_y)
    print(percent_list_y)
plt.ylim(1,4)


#======legend
plt.legend(labels=['(4,2,2)','(8,4,4)','(12,6,6)','(16,6,6)','(20,10,10)'],loc='upper right')
plt.show()
print(a.best_up_bound_list)
print(a.upper_bound_list)
end1=time.time()
plt.show()

