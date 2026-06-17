import sys
sys.path.append('C:/Users/MSI1/Documents/LTL/Collaborative_project/src')
sys.path.append('C:/Users/MSI1/Documents/LTL/Collaborative_project')
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


#output data
# this step is to meneage the input and out put data into a proper structure
# this step is to meneage the list
#context=zmq.Context()
#socket=context.socket(zmq.REQ)
#socket.connect("tcp://127.0.0.1:9999")
#message=socket.recv()
# get data and pre trent the message

class determine_task_assignment():
    def __init__(self):
        self.Data_manager=Data_pretreat()
        self.Data_manager.manage_software_data(software_input_data)
        goal_subject_pair = [('redall', 'd', 'uav'),('redall', 'd', 'radar'),('redall', 'd', 'commander')]
        task = LTL_generater(self.Data_manager)
        #task.create_one_LTL_formula2(goal_subject_pair, 'Spy_Scout')
        task.create_one_LTL_formula2(goal_subject_pair, 'Spy_obs')
        goal_subject_pair = [('redall', 'f', 'ugv'), ('redall', 'f', 'radar'),('redall', 'f', 'commander')]
        task.create_one_LTL_formula2(goal_subject_pair, 'Spy_obs')
        #task.create_one_LTL_formula(goal_subject_pair, 'Spy_Scout')
        task.check_current_LTL_formula()
        task.create_final_formula()
        task1 = task.final_formula
        # this step is to meneage the list
        # context=zmq.Context()
        # socket=context.socket(zmq.REQ)
        # socket.connect("tcp://127.0.0.1:9999")
        # message=socket.recv()
        # get data and pre trent the message

        Poset_product = Poset_producter(task1)
        Poset_product.generate_poset()
        Poset_product.prodocter()

        #Data_manager.load_priori_knowledge()
        self.Data_manager.estimate_cost_of_tasks(Poset_product)
        input_data=self.Data_manager.input_data
        print(input_data)
        # next step can use the data for bnb search
        a=optimize_method.Branch_And_Bound(Poset_product.final_poset,Poset_product.final_task_data_list,input_data)
        a.Begin_branch_search(30,up_bound_method='greedy',low_bound_method='i+j',search_method='DFS')
        # give a simulation of execution and rebuild online adaptation
        #Data_manager.manage_output_data(Poset_product.final_poset,a.best_solution,10,a.task_time_table)
        self.current_solution=a.best_solution
        self.task_time_table=a.task_time_table
        self.poset=Poset_product.final_poset
        print(self.poset)

    def online_manager(self,message,message_beihang,alpha=10):
        time_step=message['step']/alpha

        output_data=self.Data_manager.manage_output_data(self.poset,self.current_solution,time_step,self.task_time_table)
        return output_data




