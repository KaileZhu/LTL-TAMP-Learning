from data.input_data.task_data import task_type,task_data,sub_task_type
from data.input_data.agent_data import agent_type,agent_data
from data.input_data.map_data import position
from src.ltl_mas.tools.optimize_method.MILP import MILP_CVXPY
from src.ltl_mas.tools.optimize_method.Local_search import Local_Search
from src.ltl_mas.tools.optimize_method.B_A_B import Branch_And_Bound
import time



start=time.time()
poset={(0,1),(2,3),(1,3)}
#a=Branch_And_Bound(poset,position,agent_data,task_data,task_type,sub_task_type,agent_type)
#a.Begin_branch_search(120,up_bound_method='greedy',low_bound_method='i_j_k',search_method='DFS')
end1=time.time()
#a.Begin_branch_search(120,up_bound_method='greedy',low_bound_method='i_j_l',search_method='DFS')
end2=time.time()
print('totally time cost',end1-start)#
#start=time.time()

#b=MILP_CVXPY(poset,position,agent_data,task_data,task_type,sub_task_type,agent_type)
#pp=b.Base_OPT_MILP_of_cvxpy()
end3=time.time()
d=Local_Search(poset,position,agent_data,task_data,task_type,sub_task_type,agent_type)
d.local_search()
end4=time.time()
#a.opt_for_partial_assigment(b.assignment,[0,1,2,3])
print('B&B time cost with ijk',end1-start)#
print('B&B time cost with ijl',end2-end1)
print('MILP time cost',end3-end2)
print('Local time cost',end4-end3)

file=open('data.txt','w')
file.write(str(b.valueoft_j))
s=1
#a=MILP_CVXPY(poset,position,agent_data,task_data,task_type,sub_task_type,agent_type)
#prob=a.Base_OPT_MILP_of_cvxpy()
#end=time.time()
#print('totally time cost',end-start)