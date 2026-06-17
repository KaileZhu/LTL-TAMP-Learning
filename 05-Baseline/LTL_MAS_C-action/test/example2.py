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

# ((carry)&<> default))'
#task='<>(blowp1_p1 && (<> shootp3_p3 && <> washp1_p1)) && <> weedp12_p12 && <>(blowp7_p7 && (<> shootp15_p15 && <> washp13_p13))'
#task='<>(blowp1_p1 && <> ( sweepp1_p1 && ! blowp1_p1)) && <> (shootp12 && <> (sweepp12_p12 && ! shootp12))' \'&& <>(blowp7_p7 && <> (washp7_p7 && ! blowp7_p7)) && [](blowp1_p1 -> <>( shootp1_p1 && ! blowp1_p1)) &&' \'[](blowp7_p7 -> <> (shootp7_p7 && ! blowp7_p7))'
#task='<>(blowp1_p1 && <> ( shootp1_p1 && <> sweepp1_p1)) && <>(blowp7_p7 && <>( shootp7_p7 && <> washp7_p7))'
#task='<> (b1 && <> s1) && <>(b12 && <> w12) && <> (b7 && <> ( w7 && <> s7)) && [](b1 -> <> (s1 && NOT b1))' \
    # ' && [](b7 -> <> (s7 && NOT b7)) && [](b12 -> <> (s12 && NOT b12))'
#task='<> (m1 && photo) && <> (m4 && photo) && <> (m6 && photo) && [](! meeting -> !camera) && <> (d5 && carry U ( d3 && X! carry)) && [] (carry -> ! public) && <> (d11 && guide U ( m6 && X! guide))'
task1='<> a && <> b && <> c && <> d && <> f&& <> g '
task1='<>(repairp3_p3 && !scanp3_p3 && <>  scanp3_p3  )  && ' \
      '<>(washp21_p21 && <>  mowp21_p21  && <> scanp21_p21 ) &&  <> (sweepp21_p21 && ! washp21_p21 && <> mowp21_p21 )&&' \
      '<> (fixt5_t5 && ! p18_p18 ) '\
      '  &&   ! p24_p24  U sweepp27_p27   &&   <> (washp34_p34 && X  scanp34_p34) '
#task='<>(blow && <> ( wash && <> weed) && <> (sweep && <> photo)) &&[](wash -> ! weed)'
#solution=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/solution.npy')
start_for_NAB=time.time()
Bu_poset=Buchi_poset_builder(task1)
Bu_poset.main_fun_to_get_poset(20)
end_for_NBA=time.time()

print("use time",end_for_NBA-start_for_NAB,"for NBA analysis")
#Bu_poset=Buchi_poset_builder(task3)#
#Bu_poset.main_fun_to_get_path()
print('essential time',Bu_poset.self_loop_time)
#Bu_poset.main_fun_to_get_poset(50)
print('the old state number is ',len(Bu_poset.buchi.nodes),'edges is',len(Bu_poset.buchi.edges))
print('one poset time',Bu_poset.each_poset_time_list)
print('the new state number is ',len(Bu_poset.new_buchi.nodes),'edges is',len(Bu_poset.new_buchi.edges))
print('pruning step is ',Bu_poset.pruning_step_time)
print('len', Bu_poset.language_list)

exit()
field_env=field()
field_env.init_background()
#a=optimize_method.Branch_And_Bound(Bu_poset.poset_list[0]['less-than'],Bu_poset.task_data_list[0],field_env.input_data)
a=optimize_method.Branch_And_Bound2(Bu_poset.poset_list[0],Bu_poset.task_data_list[0],field_env.input_data)
#a.get_time_table_of_best_solution(solution)
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/time_table.npy',a.task_time_table)
  #.position,input_data.agent_data,input_data.task_data,
#                            input_data.task_type,input_data.sub_task_type,input_data.agent_type)
#a.Begin_branch_search(120,up_bound_method='greedy',low_bound_method='i_j_k',search_method='DFS')
end1=time.time()
a.Begin_branch_search2(30,up_bound_method='greedy',low_bound_method='i_j',search_method='DFS')

end2=time.time()
print('totally time cost',end2-end1)#
#start=time.time()
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/solution.npy',a.best_solution)
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/anchorfunction.npy',Bu_poset.task_data_list[0])
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/poset.npy',Bu_poset.poset_list[0])
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/time_table.npy',a.task_time_table)
a=Agent_swarm(a.best_solution,Bu_poset.poset_list[0],Bu_poset.task_data_list[0],field_env,a.task_time_table)
a.pre_planning()
a.begin_run(1300,1,0)
#a.plot(1000)
color_table=['#006400', 'c', 'k', '#6A5ACD', 'y','m', 'g', 'aqua', 'brown', '#FF0000','#FFDEAD','B8860B']
for i in range(100,1000,100):
     a.plot_static(i,color_table)
#b=optimize_method.MILP_CVXPY(Bu_poset.poset_list[0]['less-than'],Bu_poset.task_data_list[0],field_env.input_data)
# #(poset,position,agent_data,task_data,task_type,sub_task_type,agent_type)
#pp=b.Base_OPT_MILP_of_cvxpy()
#b.check_the_value(a.best_solution)
#end3=time.time()
#print('totally time cost',end3-end2)
#d=optimize_method.Local_Search(Bu_poset.poset_list[0]['less-than'],Bu_poset.task_data_list[0],input_data)
	#(poset,position,agent_data,task_data,task_type,sub_task_type,agent_type)
#d.local_search()
#end4=time.time()
#a.opt_for_partial_assigment(b.assignment,[0,1,2,3])
#a=MILP_CVXPY(poset,position,agent_data,task_data,task_type,sub_task_type,agent_type)
#prob=a.Base_OPT_MILP_of_cvxpy()
#end=time.time()
#print('totally time cost',end-start)
#plot(1,Bu_poset.new_buchi)


