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
import matplotlib.pyplot as plt



task2='<>(washp11_p11 && <> (mowp11_p11 && <> sweepp11_p11) && <> scanp11_p11) && []((washp11_p11 || mowp11_p11) -> ! sweepp11_p11)' \
      '&&[](washp11_p11 -> ! mowp11_p11)&& [](washp11_p11 ->!scanp11_p11) ' \
'&& <>(washp20_p20 && <> (mowp20_p20 && <> sweepp20_p20)&& <> scanp20_p20) && []((washp20_p20 || mowp20_p20) -> ! sweepp20_p20) ' \
     '&&[](washp20_p20 -> ! mowp20_p20)&& [](washp20_p20 ->!scanp20_p20)'\
    '&& <> tempt4_t4'


def task_repair_pi(pi_number):
    task='<>(repair'+pi_number+' && <> scan'+pi_number+') && [] (repair'+pi_number+' -> ! scanp'+pi_number+') '
    return task

def fix_scan_ti(ti_number):
    task= '<>(fix'+ti_number+' && <> scan'+ti_number+')' \
      '&& [] (fix'+ti_number+' -> ! scan'+ti_number+') '
    return task

def generate_task_formula(task_number):
    task=task_repair_pi('p1_p1')
    for i in range(task_number-1):
        i=i+2
        num='p'+str(i)+'_p'+str(i)
        task=task+'&&'+task_repair_pi(num)
    for j in range(task_number):
        j=j+1
        num='t'+str(j)+'_t'+str(j)
        task=task+'&&'+fix_scan_ti(num)
    return task
def generate_poset_strictly(num_ti,num_pi):
    poset={'||':set(),'<=':set(),'<':set(),'!=':set(),'=':set(),'action_map':[]}
    task_data_list=[]
    #=================generate action list
    task_num=0
    for i in range(num_ti):
        i=i+1
        task_data_list.append((task_num,'fixt'+str(i),'t'+str(i)))
        poset['action_map'].append('fixt'+str(i)+'_t'+str(i))
        poset['<='].add((task_num,task_num+1))
        poset['!='].add((task_num,task_num+1))
        task_num=task_num+1
        task_data_list.append((task_num,'scant'+str(i),'t'+str(i)))
        task_num=task_num+1
        poset['action_map'].append('scant'+str(i)+'_t'+str(i))
    for i in range(num_pi):
        i=i+1
        task_data_list.append((task_num,'repairp'+str(i),'p'+str(i)))
        poset['action_map'].append('repairp'+str(i)+'_p'+str(i))
        poset['<='].add((task_num,task_num+1))
        poset['!='].add((task_num,task_num+1))
        task_num=task_num+1
        task_data_list.append((task_num,'scanp'+str(i),'p'+str(i)))
        poset['action_map'].append('scanp'+str(i)+'_p'+str(i))
        task_num=task_num+1
    return  poset,task_data_list



phi1=generate_task_formula(1)
start_for_NAB=time.time()
Bu_poset=Buchi_poset_builder(phi1)
Bu_poset.main_fun_to_get_poset(20)
end_for_NBA=time.time()
print('execute time', end_for_NBA-start_for_NAB)
print('pruning_time',Bu_poset.pruning_step_time)
print('poset time',Bu_poset.poset_ana_time)
print('poset time list',Bu_poset.poset_start_time_list)
print('poset language',Bu_poset.language_list)
#break3
best_solution=[]
#print("use time",end_for_NBA-start_for_NAB,"for NBA analysis")
for i in range(1,5):
    field_env=field()
    field_env.init_background()
    #a=optimize_method.Branch_And_Bound2(Bu_poset.poset_list[0],Bu_poset.task_data_list[0],field_env.input_data)
    poset_list,task_data_list=generate_poset_strictly(i,i)
    a=optimize_method.Branch_And_Bound2(poset_list,task_data_list,field_env.input_data)
    begin=time.time()
    a.Begin_branch_search2(60,up_bound_method='greedy',low_bound_method='i+j',search_method='DFS')
    end1=time.time()
    print('execute time', end_for_NBA-start_for_NAB)
    print('pruning_time',Bu_poset.pruning_step_time)
    print('poset time',Bu_poset.poset_ana_time)
    print('poset time list',Bu_poset.poset_start_time_list)
    print('poset language',Bu_poset.language_list)
    print('search time',end1-begin)
    #print(a.best_up_bound_list)
    best_solution.append(a.best_up_bound_list)
for best_up_bound_list in best_solution:
    percent_list_x=[]
    percent_list_y=[]
    optimal_value=list(best_up_bound_list.items())[-1][1][0]
    for value,time in best_up_bound_list.items():
        percent_list_y.append(time[0]/optimal_value)
        percent_list_x.append(time[1])
    plt.plot(percent_list_x,percent_list_y)
    print(percent_list_y)
plt.ylim(1,2)
plt.show()