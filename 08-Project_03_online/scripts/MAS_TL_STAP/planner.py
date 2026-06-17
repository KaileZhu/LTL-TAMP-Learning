#！/usr/bin/env python3
'''
@Date   : 2023/11 -->  
@Authors: Junjie Wang, Yunyi Zhang
@Contact: pkuwjj1998@163.com
@Version: 1.0
@Descrip: the module contains the class for planner, which is used to solve
        the simultaneous task allocation and planning for multi-agent system.
@Log:
        - 2023/11/20: the first version that contains the class for BnB Search
'''

import time
import copy

# import cvxpy as cp
import networkx as nx

# from B_A_B2 import Branch_And_Bound

class BnBSearch:
    """
    Class for the branch and bound algorithm.
    """
    def __init__(self, poset, task_data, input_data, ):
        """
        Args:
            poset: the poset list
            task: 
            input: 
        """
        self.poset = poset
        self.position = input_data.position
        self.agent_data = input_data.agent_data
        self.task_data = task_data
        self.task_type = input_data.task_type
        self.sub_task_type = input_data.sub_task_type
        self.agent_type = input_data.agent_type
        self.Astar_table = []
        self.get_horizon()
        self.explored_node_dic = {}
        self.generate_poset_graph()


    def Begin_branch_search2(self, ):
        pass






class MILP:
    """
    Class for the mixed integer linear programming algorithm.
    """
    pass