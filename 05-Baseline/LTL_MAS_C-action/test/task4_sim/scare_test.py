import sys
sys.path.append('/home/LZS/LTL/git/LTL_MAS_C-action/src')
from ltl_mas.tools.poset_builder import Buchi_poset_builder
from ltl_mas.tools.nx_plot.base_plot import plot
from ltl_mas.tools import optimize_method
from data import input_data
import numpy as np
import time
from ltl_mas.simulate.field_background import field
from itertools import chain,combinations
from ltl_mas.simulate.Agent_swarm import Agent_swarm
from Gantt_platter_task3_by_execution import gantt_plotter
from  Gantt_platter_task3 import  gantt_plotter as gantt_plotter2
import matplotlib.pyplot as plt
#task: repairp1_p1  scanp1_p1  fixt6_t6 scant6_t6 p4 p5 washp7  mowp7  sweepp7  tempp24 tempp17 washp20_20 mowp20_p20 sweepp20_p20
# 1 prefix  <>(repairp1_p1 && <> scanp1_p1)  <>(washp7_p7 && <>  mowp7_p7 &&  && <> scanp7_p7  <> (mowp7_p7 && <> sweepp7_p7)
#            <> tempp24_p24   <> (tempp14_p14 && ! l)
#           ! p24_p24 p25 p26 U b fixt3_t3
# 2 suffix [] <> (sweepp20_p20 && mowp20_20) && [] <> (mowp20_20 && washp20_p20) && [] ! p5 && [] ! p10 &&
#
#  prefix part
start_time=time.time()
#\varphi2
task31='<>(repairp3_p3 && <> scanp3_p3)  && ' \
      '<>(washp21_p21 && <>  mowp21_p21  && <> scanp21_p21 ) &&  <> (sweepp21_p21 && ! washp21_p21 && <> mowp21_p21 )&&' \
      '<> (fixt5_t5 && ! p18_p18 ) '\
      ' && [] <> washp34_p34 &&   ! p28_p28  U sweepp27_p27 && ' \
      '[] <> tempt7_t7  && [] <> (tempp17_p17 && X fixt6_t6) && [](repairp3_p3 -> ! scanp3_p3)'
#\varphi 1
task3='<>(washp11_p11 && <> (mowp11_p11 && <> sweepp11_p11) && <> scanp11_p11) && []((washp11_p11 || mowp11_p11) -> ! sweepp11_p11)' \
      '&&[](washp11_p11 -> ! mowp11_p11)&& [](washp11_p11 ->!scanp11_p11) ' \
'&& <>(washp20_p20 && <> (mowp20_p20 && <> sweepp20_p20)&& <> scanp20_p20) && []((washp20_p20 || mowp20_p20) -> ! sweepp20_p20) ' \
     '&&[](washp20_p20 -> ! mowp20_p20)&& [](washp20_p20 ->!scanp20_p20)'\
    '&& <> tempt4_t4'
#\varphi 3
task31='<>(washp11_p11 && <> (mowp11_p11 && <> sweepp11_p11) && <> scanp11_p11) && []((washp11_p11 || mowp11_p11) -> ! sweepp11_p11)' \
      '&&[](washp11_p11 -> ! mowp11_p11)&& [](washp11_p11 ->!scanp11_p11) && <>(sweepp8_p8 && <>  washp8_p8 ) &&  <> (sweepp8_p8 && ! washp8_p8 && <> mowp8_p8 )&&' \
      '   ! p28_p28  U fixt2_t2  ' \

poset={'||': set(),
 '<=': {(0, 2), (0, 4), (2, 3), (5, 6), (5, 7), (7, 8)},
 '<': set(),
 '!=': {(0, 2), (0, 3), (0, 4), (2, 3), (5, 6), (5, 7), (5, 8), (7, 8)},
 '=': set(),
 'action_map': [['washp11_p11'],
  ['tempt4_t4'],
  ['mowp11_p11'],
  ['sweepp11_p11'],
  ['scanp11_p11'],
  ['washp20_p20'],
  ['scanp20_p20'],
  ['mowp20_p20'],
  ['sweepp20_p20']]}
def change_poset(poset):
  task_map=poset['action_map']
  task_data=[]
  double_label=0
  name_dict=[]
  zero_list=[]
  for task_i in range(len(task_map)):
      if len(task_map[task_i]) > 1:
          double_label=1
      if len(task_map[task_i])==0:
          zero_list.append(task_i)
  new_dic_list={}
  t=0
  for i in range(len(task_map)):
      if not i in zero_list:
          new_dic_list[i]=t
          t=t+1
  new_leq=set()
  for i,j in poset['<=']:
      if not i in zero_list and not j in zero_list:
          new_leq.add(tuple((new_dic_list[i],new_dic_list[j])))
  poset['<=']=new_leq
  new_neq=set()
  for i,j in poset['!=']:
      if not i in zero_list and not j in zero_list:
          new_neq.add(tuple((new_dic_list[i],new_dic_list[j])))
  poset['!=']=new_neq
  if [] in task_map:
      task_map.remove([])
  if not double_label:
      for i in range(len(task_map)):
          num=task_map[i][0].find('_')
          task_name=task_map[i][0][0:num]
          task_place=task_map[i][0][num+1:]
          task=(i,task_name,task_place)
          task_data.append(task)
      new_action_map=[]
      for act in poset['action_map']:
          new_action_map.append(act[0])
      poset['action_map']=task_data
      return poset
  else:
      #to rebuild the number list
      num_dict={}
      z=0
      for i in range(len(task_map)):
          num_dict[i]=list(range(z,z+len(task_map[i])))
          z=z+len(task_map[i])
      for old_num,new_num_list in num_dict.items():
          for j in range(len(new_num_list)):
              num_=task_map[old_num][j].find('_')
              task_name=task_map[old_num][j][0:num_]
              task_place=task_map[old_num][j][num_+1:]
              task=(new_num_list[j],task_name,task_place)
              name_dict.append(task_map[old_num][j])
              task_data.append(task)
      #rebuild poset
      new_poset={}
      for key,sub_dict in poset.items():
          if not key =='action_map':
              new_poset[key]=set()
              for i,j in poset[key]:
                  for new_i in num_dict[i]:
                      for new_j in num_dict[j]:
                          new_poset[key].add((new_i,new_j))
          if key == '=':
              for old_num,new_num in num_dict.items():
                  if len(new_num)>1:
                      new_poset[key]=set(combinations(new_num,2))
      new_poset['action_map']=name_dict
      return new_poset
#poset1=change_poset(poset)
#add the or relation
#task='<>(blow && <> ( wash && <> weed) && <> (sweep && <> photo)) &&[](wash -> ! weed)'
#solution=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/solution.npy')
# start_for_NAB=time.time()
#Bu_poset=Buchi_poset_builder(task3)#
#Bu_poset.main_fun_to_get_poset(30)
#print('the old state number is ',len(Bu_poset.buchi.nodes),'edges is',len(Bu_poset.buchi.edges))
#print(Bu_poset.poset_list[0],Bu_poset.poset_list[1])
#print('first calculate time is',start_time-Bu_poset.poset_calculate_time[0])
#print('best calculate time is',start_time-Bu_poset.poset_calculate_time[Bu_poset.evaluater_sorter[0]])
#print('the new state number is ',len(Bu_poset.new_buchi.nodes),'edges is',len(Bu_poset.new_buchi.edges))
#print('pruning step is ',Bu_poset.pruning_step_time)



# end_for_NBA=time.time()
# print('execute time', end_for_NBA-start_for_NAB)
# print('pruning_time',Bu_poset.pruning_step_time)
# print('poset time',Bu_poset.poset_ana_time)
# break3
poset={'||': set(),
 '<=': {(0, 2), (0, 4), (2, 3), (5, 6), (5, 7), (7, 8)},
 '<': set(),
 '!=': {(0, 2), (0, 4), (2, 3), (5, 6), (5, 7), (7, 8)},
 '=': set(),
 'action_map': [(0, 'washp11', 'p11'),
  (1, 'tempt4', 't4'),
  (2, 'mowp11', 'p11'),
  (3, 'sweepp11', 'p11'),
  (4, 'scanp11', 'p11'),
  (5, 'washp20', 'p20'),
  (6, 'scanp20', 'p20'),
  (7, 'mowp20', 'p20'),
  (8, 'sweepp20', 'p20')]}

field_env=field()
field_env.init_background()
a=optimize_method.Branch_And_Bound2(poset,poset['action_map'],field_env.input_data)

#end1=time.time()
a.Begin_branch_search2(10,up_bound_method='greedy',low_bound_method='i+j',search_method='DFS')
print(a.low_bound_list)
print(a.upper_bound_list)
print(a.best_up_bound_list)


