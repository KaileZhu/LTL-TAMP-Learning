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
from Gantt_platter_task3_by_execution import gantt_plotter,gantt_plotter_communication
from  Gantt_platter_task3 import  gantt_plotter as gantt_plotter2
import matplotlib.pyplot as plt
#task: repairp1_p1  scanp1_p1  fixt6_t6 scant6_t6 p4 p5 washp7  mowp7  sweepp7  tempp24 tempp17 washp20_20 mowp20_p20 sweepp20_p20
# 1 prefix  <>(repairp1_p1 && <> scanp1_p1)  <>(washp7_p7 && <>  mowp7_p7 &&  && <> scanp7_p7  <> (mowp7_p7 && <> sweepp7_p7)
#            <> tempp24_p24   <> (tempp14_p14 && ! l)
#           ! p24_p24 p25 p26 U b fixt3_t3
# 2 suffix [] <> (sweepp20_p20 && mowp20_20) && [] <> (mowp20_20 && washp20_p20) && [] ! p5 && [] ! p10 &&
#
#  prefix part
#这个是之前实验的最终版本 base_execute suffix 不是
task3='<>(repairp3_p3 && <> ( scanp3_p3  && <> fixt1_t1))  && ' \
      '<>(washp21_p21 && <>  mowp21_p21  && <> scanp21_p21 ) &&  <> (sweepp21_p21 && ! washp21_p21 && <> mowp21_p21 )&&' \
      '<> (fixt5_t5 && ! p18_p18 ) '\
      '  &&   ! p24_p24  U sweepp27_p27   &&   <> adssa21_p21 X scanp22_p22 '
task3='<>(repairp3_p3 && !scanp3_p3 && <>  scanp3_p3  )  && ' \
      '<>(washp21_p21 && <>  mowp21_p21  && <> scanp21_p21 ) &&  <> (sweepp21_p21 && ! washp21_p21 && <> mowp21_p21 )&&' \
      '<> (fixt5_t5 && ! p18_p18 ) '\
      '  &&   ! p24_p24  U sweepp27_p27   &&   <> (washp34_p34 && X  scanp34_p34) '

#add the or relation
#task='<>(blow && <> ( wash && <> weed) && <> (sweep && <> photo)) &&[](wash -> ! weed)'
#solution=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/solution.npy')
#start_for_NAB=time.time()
#Bu_poset=Buchi_poset_builder(task3)#
#Bu_poset.main_fun_to_get_path()

#Bu_poset.main_fun_to_get_poset(50)
#print('the old state number is ',len(Bu_poset.buchi.nodes),'edges is',len(Bu_poset.buchi.edges))

#print('the new state number is ',len(Bu_poset.new_buchi.nodes),'edges is',len(Bu_poset.new_buchi.edges))
#print('pruning step is ',Bu_poset.pruning_step_time)


poset={'||': set(),
 '<=': {(0, 7),
  (1, 2),
  (2, 7),
  (3, 4),
  (3, 6),
  (4, 7),
  (5, 6),
  (6, 7),
  (7, 8),(8,9)},
 '<': set(),
 '!=': {(5, 3),(1,2)},
 '=': set(),
 'action_map': [(0, 'fixt5', 't5'),
 (1, 'repairp3', 'p3'),
 (2, 'scanp3', 'p3'),
 (3, 'washp21', 'p21'),
 (4, 'scanp21', 'p21'),
 (5, 'sweepp21', 'p21'),
 (6, 'mowp21', 'p21'),
 (7, 'sweepp27', 'p27'),
 (8, 'washp34', 'p34'),
                (9,'scanp34','p34')],
 'self_loop': [[' '],
  ['(!p24_p24)'],
  ['(!p24_p24)'],
  ['(!p24_p24)'],
  ['(!p24_p24)'],
  ['(!p24_p24)'],
  ['(!p24_p24)'],
  ['(!p24_p24)'],
  [' '],
  [' ']]}

end_for_NBA=time.time()
# # print('execute time', Bu_poset.pruning_step_time-start_for_NAB)
#print('pruning_time',Bu_poset.pruning_step_time)
#print('poset time',Bu_poset.poset_ana_time)
#print('first calculate time is',Bu_poset.pruning_step_time-Bu_poset.poset_calculate_time[0])
#print('best calculate time is',Bu_poset.pruning_step_time-Bu_poset.poset_calculate_time[-1])
#print('language 1',Bu_poset.language_list[0])
#print(end_for_NBA-start_for_NAB)
#exit()

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
      poset['action_map']=new_action_map
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

task_data_list=[(0, 'fixt5', 't5'),
 (1, 'repairp3', 'p3'),
 (2, 'scanp3', 'p3'),
 (3, 'washp21', 'p21'),
 (4, 'scanp21', 'p21'),
 (5, 'sweepp21', 'p21'),
 (6, 'mowp21', 'p21'),
 (7, 'sweepp27', 'p27'),
 (8, 'washp34', 'p34'),
 (9,'scanp34','p34')]
# print("use time",end_for_NBA-start_for_NAB,"for NBA analysis")
field_env=field()
field_env.init_background()
#a=optimize_method.Branch_And_Bound2(poset,task_data_list,field_env.input_data)
#a=optimize_method.Branch_And_Bound3(poset,task_data_list,field_env.input_data)
end1=time.time()
#a.Begin_branch_search2(1,up_bound_method='greedy',low_bound_method='i+j',search_method='DFS')
#print(a.best_solution)

#print(a.low_bound_list)
#print(a.upper_bound_list)
#print(a.best_up_bound_list)

#a.plot_bnb_graph_phi4(save='0',load='1')

#end2=time.time()
#print('totally time cost',end2-end1)#
#start=time.time()
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task3/solution_s0.npy',solution)
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task3/time_table_s0.npy',task_time_table)
#np.save('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task3/time_table_s3.npy',a.task_time_table)
solution=[[((4, 'scanp21', 'p21'), 'scan'), ((2, 'scanp3', 'p3'), 'scan')]
,[((4, 'scanp21', 'p21'), 'scan'), ((9, 'scanp34', 'p34'), 'scan')]
,[((8, 'washp34', 'p34'), 'wash')]
,[((3, 'washp21', 'p21'), 'wash'), ((9, 'scanp34', 'p34'), 'scan')]
,[((3, 'washp21', 'p21'), 'wash'), ((2, 'scanp3', 'p3'), 'scan')]
,[((4, 'scanp21', 'p21'), 'scan'), ((2, 'scanp3', 'p3'), 'scan'), ((9, 'scanp34', 'p34'), 'scan')]
,[((1, 'repairp3', 'p3'), 'repair_UGV_l')]
,[]
,[((0, 'fixt5', 't5'), 'fix'), ((8, 'washp34', 'p34'), 'wash')]
,[((1, 'repairp3', 'p3'), 'repair_UGV_s'), ((7, 'sweepp27', 'p27'), 'sweep')]
,[((1, 'repairp3', 'p3'), 'repair_UGV_s')]
,[((0, 'fixt5', 't5'), 'fix'), ((5, 'sweepp21', 'p21'), 'sweep'), ((6, 'mowp21', 'p21'), 'mow')]]





task_time_table=[[0, 135.27934062524108, 207.27934062524108],
 [1, 172.57244855422323, 748.5724485542232],
 [2, 748.5724485542232, 845.5724485542232],
 [3, 17.60113632695345, 596.6011363269535],
 [4, 17.601136326953437, 114.60113632695344],
 [5, 596.6011363269535, 789.6011363269535],
 [6, 789.6011363269535, 982.6011363269535],
 [7, 809.4668243207914, 1002.4668243207914],
 [8, 809.4668243207914, 1388.4668243207914],
 [9, 885.4639263408383, 982.4639263408383]]


#gantt_plotter2(solution,task_time_table,task_data_list,15)
#gantt_plotter('0','2',solution,task_time_table,task_data_list,a.adapt_time_table)


a=Agent_swarm(solution,poset,task_data_list,field_env,task_time_table)
a.pre_planning()
#for node in a.field.node_set_for_barrier:
    #plt.plot(node[0],node[1],'^')
#a.path_plotter()
a.begin_run(2400,1,1)

a.get_real_execution_time_table()
#a.plot(1000)
color_table=['#006400', 'c', 'k', '#6A5ACD', 'y','m', 'g', 'aqua', 'brown', '#FF0000','#FFDEAD','k']
#gantt_plotter(solution,task_data_list,a.estimate_task_time_table,a.adapt_time_table,26)
gantt_plotter_communication(solution,task_data_list,a.estimate_task_time_table,a.adapt_time_table,26,a.adapt_state_track,a.current_leader_track)
#a.plot_static(i,color_table,'task3/task3_motion_fig_at_time_')
#for i in [40,200,240,340,450,632,727]:
#     a.plot_static(i,color_table,'task3/task3_motion_fig_at_time_')
#a.plot_static(2200,color_table,'task3/task3_motion_fig_at_time_online')
s=1
