import sys
sys.path.append('C:/Users/MSI1/Documents/LTL/Collaborative_project/src')
sys.path.append('C:/Users/MSI1/Documents/LTL/Collaborative_project')
from ltl_mas.tools.poset_builder import Buchi_poset_builder
from ltl_mas.tools import optimize_method
import numpy as np
import time
from ltl_mas.simulate.Agent_swarm import Agent_swarm
from ltl_mas.formula_generater.LTL_formula_generater import LTL_generater
from ltl_mas.tools.Data_pre_treatment import Data_pretreat
from ltl_mas.tools.poset_product import  Poset_producter

import zmq
from data.input_data.first_data import software_input_data
from ltl_mas.tools.online_detection import Online_detection



class determine_task_assignment():
    def __init__(self):
        self.Data_manager=Data_pretreat()
        self.Data_manager.manage_software_data(software_input_data)
        goal_subject_pair1 = {'order_obs':[[{'subject':'redall','place': 'g', 'goal':'uav'},
                             {'subject':'redall','place':  'g', 'goal':'radar'},
                             {'subject':'redall', 'place': 'g', 'goal':'command'}],[{'place': 'l', 'goal':'uav'},
                             {'place':  'l', 'goal':'radar'},
                             {'subject':'redall', 'place': 'l', 'goal':'command'}],
        [{'place': 'm', 'goal': 'uav'},
         {'place': 'm', 'goal': 'radar'},
         {'subject': 'redall', 'place': 'm', 'goal': 'commander'}]
        ]}
        goal_subject_pair1 = {'order_atk': [[{'subject': 'redall', 'place': 'g', 'goal': 'command'},
                                            {'subject': 'redall', 'place': 'g', 'goal': 'radar'},
                                            {'subject': 'redall', 'place': 'g', 'goal': 'all'},
                                            {'subject': 'redall', 'place': 'g', 'goal': 'uav'}],
                                           [{'place': 'l', 'goal': 'command'},
                                            {'place': 'l', 'goal': 'radar'},
                                            {'subject': 'redall', 'place': 'l', 'goal': 'all'},
                                            {'subject': 'redall', 'place': 'l', 'goal': 'uav'}],
                                           [{'place': 'm', 'goal': 'command'},
                                            {'place': 'm', 'goal': 'radar'},
                                            {'subject': 'redall', 'place': 'm', 'goal': 'all'},
                                            {'subject': 'redall', 'place': 'm', 'goal': 'uav'}]
                                           ]}
        goal_subject_pair = {'order_atk': [[{'place': 'l', 'goal': 'artillery'},
                                             {'place': 'l', 'goal': 'infantry'},
                                             {'subject': 'redall', 'place': 'l', 'goal': 'all'},
                                             {'subject': 'redall', 'place': 'l', 'goal': 'uav'}]
                                            ]}
        goal_subject_pair1 = {'order_obs': [[{'subject': 'redall', 'place': 'l', 'goal': 'uav'},
                                             {'subject': 'redall', 'place': 'l', 'goal': 'radar'},
                                             {'subject': 'redall', 'place': 'l', 'goal': 'command'}]
                                            ]}
        task = LTL_generater(self.Data_manager)
        #rules={'order_obs':[[]]}
        rules={'order_atk':[['cannonry']]}
        #task.create_one_LTL_formula2(goal_subject_pair, 'Spy_Scout')
        task.create_one_LTL_formula_with_default(goal_subject_pair, 'Global_attack',rules)
        #task.create_one_LTL_formula_with_default(goal_subject_pair, 'Global_scan', rules)
        #goal_subject_pair = [{'subject':'redall','place': 'f', 'goal':'uav'},
        #                     {'subject':'redall','place':  'f', 'goal':'radar'},
        #                     {'subject':'redall', 'place': 'f', 'goal':'commander'}]
        #task.create_one_LTL_formula_with_default(goal_subject_pair, 'WeiDianDaYuan',rules)
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
        a.Begin_branch_search(50,up_bound_method='greedy',low_bound_method='i+j',search_method='DFS')
        # give a simulation of execution and rebuild online adaptation
        #Data_manager.manage_output_data(Poset_product.final_poset,a.best_solution,10,a.task_time_table)

        self.current_solution=a.best_solution
        self.task_time_table=a.task_time_table
        self.poset=Poset_product.final_poset
        self.finished_task=[]
        self.executing_task=[]
        print(self.poset)

    def online_manager(self,message,message_beihang,time_step,alpha=1):
        #time_step=message['step']/alpha
        output_data=self.Data_manager.manage_output_data(self.poset,self.current_solution,time_step,self.task_time_table)
        return output_data

    def online_data_mannager(self,agent_message,agent_message_beihang,time_step):
        '''supervise the current data
        this function is used to update the data message and for the online update
        '''
        for task in agent_message_beihang['finished_task']:
            if not task in self.finished_task:
                self.finished_task.append(task)
        # 判断是否有智能体损毁，如果有就重新规划
        if not agent_message_beihang['replanning_label']==1:
            #agent_pose 当前智能体的位子，或者智能体完成该任务后的位置
            # finished_time_list 完成任务的时间表
            # unfinished_task_list 未完成的任务
            # begin_time 允许出现分配智能体任务的时间
            # task_dic 任务表
            # task_execute_time 新的任务执行时间
            # broken_agent_list
            self.extro_constrain = The_extro_condition(agent_pose, finished_time_list, unfinished_task_list,
                                                           begin_time,
                                                           task_dic, task_execute_time, broken_agent_list)

            bnb = optimize_method.Branch_And_Bound(self.poset, task_data, input_data)
            bnb.Begin_branch_search_online(search_time, self.extro_constrain, finished_task)
            self.new_solution=bnb.best_solution



