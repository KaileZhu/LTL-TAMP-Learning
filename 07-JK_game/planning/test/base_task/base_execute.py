import sys
sys.path.append('C:/Users/MACDLab/Documents/GitHub/Collaborative_project/src')
sys.path.append('C:/Users/MACDLab/Documents/GitHub/Collaborative_project')
from ltl_mas.tools.poset_builder import Buchi_poset_builder
from ltl_mas.tools import optimize_method
import numpy as np
import time
from ltl_mas.simulate.Agent_swarm import Agent_swarm
from ltl_mas.formula_generater.Pre_LTL_formula import LTL_generater
from ltl_mas.tools.Data_pre_treatment import Data_pretreat
from ltl_mas.tools.poset_product import  Poset_producter

import zmq
from data.input_data.first_data import software_input_data
from ltl_mas.tools.online_detection import Online_detection

goal_subject_pair=[('redall','d','uav')]
task=LTL_generater()
task.create_one_LTL_formula(goal_subject_pair,'Spy_Scout')
goal_subject_pair=[('redall','f','ugv')]
task.create_one_LTL_formula(goal_subject_pair,'Spy_Scout')
task.check_current_LTL_formula()
task.create_final_formula()
task1=task.final_formula
# this step is to meneage the list
#context=zmq.Context()
#socket=context.socket(zmq.REQ)
#socket.connect("tcp://127.0.0.1:9999")
#message=socket.recv()
# get data and pre trent the message

Poset_product=Poset_producter(task1)
Poset_product.generate_poset()
Poset_product.prodocter()
#output data
# this step is to meneage the input and out put data into a proper structure
# this step is to meneage the list
#context=zmq.Context()
#socket=context.socket(zmq.REQ)
#socket.connect("tcp://127.0.0.1:9999")
#message=socket.recv()
# get data and pre trent the message


Data_manager=Data_pretreat()
Data_manager.manage_software_data(software_input_data)
#Data_manager.load_priori_knowledge()
Data_manager.estimate_cost_of_tasks(Poset_product)
input_data=Data_manager.input_data

# next step can use the data for bnb search

#a=optimize_method.Branch_And_Bound(Bu_poset.poset_list[0]['less-than'],Bu_poset.task_data_list[0],field_env.input_data)


'''
here we should get the message of tasks in the simulater.
'''

#bnb should change the 1 check if agetn alive in step online
# change the
a=optimize_method.Branch_And_Bound(Poset_product.final_poset,Poset_product.final_task_data_list,input_data)
a.Begin_branch_search(30,up_bound_method='greedy',low_bound_method='i+j',search_method='DFS')
# give a simulation of execution and rebuild online adaptation
#Data_manager.manage_output_data(Poset_product.final_poset,a.best_solution,10,a.task_time_table)
data_from_script={'1':{'finished_task':{0},'executing_task':set()}}
solution=[[],
 [((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((1, 'redall', 'follow', 'c', 'uav'), 'follow'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack'),
  ((3, 'redall', 'follow', 'c', 'ugv'), 'follow')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack')],
 [((0, 'redall', 'attack', 'c', 'uav'), 'attack'),
  ((2, 'redall', 'attack', 'c', 'ugv'), 'attack')]]
task_time_table=[[0, 0.14596244784813717, 6.854166380347507],
 [1, 6.8541663803475075, 11.326302335347087],
 [2, 11.326302335347084, 18.034506267846453],
 [3, 18.034506267846453, 22.506642222846033]]
poset={'||': set(),
 '<=': {(0, 1), (2, 3)},
 '<': set(),
 '!=': set(),
 '=': set(),
 'action_map': [(0, 'redall', 'attack', 'c', 'uav'),
  (1, 'redall', 'follow', 'c', 'uav'),
  (2, 'redall', 'attack', 'c', 'ugv'),
  (3, 'redall', 'follow', 'c', 'ugv')]}

Data_manager.manage_output_data(poset,solution,10,task_time_table)
#b=Online_detection(poset,task_time_table,solution,input_data)
#b.online_adaptation(Poset_product,software_input_data,data_from_script)


print(a.task_time_table)
exit()



