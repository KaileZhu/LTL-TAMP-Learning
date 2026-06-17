import time
from PyQt5 import QtWidgets,QtCore
import sys
sys.path.append('C:/Users/MSI1/Documents/LTL/JK_game/planning')
sys.path.append('C:/Users/MSI1/Documents/LTL/JK_game/planning/test')
sys.path.append('C:/Users/MSI1/Documents/LTL/JK_game/planning/src')
from src.ltl_mas.tools import optimize_method
import time
from src.ltl_mas.formula_generater.LTL_formula_generater import LTL_generater
from src.ltl_mas.tools.Data_pre_treatment import Data_pretreat
from src.ltl_mas.tools.poset_product import  Poset_producter
from data.input_data.first_data import software_input_data


Data_manager = Data_pretreat()
Data_manager.manage_software_data(software_input_data)
#步步为营
# 进攻区域，占据区域
goal_subject_pair2= {0:{'basic_atk':[[{'place': 'l', 'goal': 'infantry'},
                                     {'place': 'l', 'goal': 'artillery'}]]},
                     1:{'basic_atk':[[{'place': 'l', 'goal': 'all'}]]},
                     2:{'basic_support':[[{'place': 'l', 'goal': 'all'}]],
                        "basic_atk":[[{'place': 'g', 'goal': 'all'}]]},
                     3:{"basic_support":[[{'place': 'g', 'goal': 'all'}]],
                        "basic_atk":[[{'place': 'm', 'goal': 'all'}]]},
                     4:{"basic_support":[[{'place': 'm', 'goal': 'all'}]]}
                     }
#围点打援
#

task = LTL_generater(Data_manager)
rules = {'order_obs': [['cannonry']]}
rules2 = {0:{},1:{},2:{},3:{},4:{} }
task.creat_LTL_formula_with_wave_picking(goal_subject_pair2, 'Bubuweiying')
task.check_current_LTL_formula()
#生成形式化语言公式
task.create_final_formula()

task1 = task.final_formula
#进行任务分解，获取任务偏序集
Poset_product = Poset_producter(task1)
Poset_product.generate_poset()
Poset_product.prodocter()
#根据环境，评估子任务的内容，以及价值
Data_manager.estimate_cost_of_tasks(Poset_product)
input_data = Data_manager.input_data
print(input_data)
#根据价值，进行分支定界法的任务分配
a = optimize_method.Branch_And_Bound(Poset_product.final_poset, Poset_product.final_task_data_list,
                                  input_data)
a.Begin_branch_search(100, up_bound_method='greedy', low_bound_method='i+j', search_method='DFS')
current_solution = a.best_solution
task_time_table = a.task_time_table