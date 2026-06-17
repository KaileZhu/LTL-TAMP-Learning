from data.input_data.gantt_test_data import message_data,message_date_2
import sys
sys.path.append('C:/Users/MSI1/Documents/LTL/Collaborative_project')
sys.path.append('C:/Users/MSI1/Documents/LTL/Collaborative_project/test')
sys.path.append('C:/Users/MSI1/Documents/LTL/Collaborative_project/src')
from src.ltl_mas.tools import optimize_method
import time
from src.ltl_mas.formula_generater.LTL_formula_generater import LTL_generater
from src.ltl_mas.tools.Data_pre_treatment import Data_pretreat
from src.ltl_mas.tools.poset_product import  Poset_producter
from data.input_data.first_data import software_input_data
poset={'||': set(),
 '<=': {(0, 3),
  (0, 4),
  (0, 5),
  (1, 3),
  (1, 4),
  (1, 5),
  (2, 3),
  (2, 4),
  (2, 5),
  (3, 5),
  (4, 5)},
 '<': set(),
 '!=': {(0, 3),
  (0, 4),
  (0, 5),
  (1, 3),
  (1, 4),
  (1, 5),
  (2, 3),
  (2, 4),
  (2, 5),
  (3, 5),
  (4, 5)},
 '=': set(),
 'action_map': [(0, 'redall', 'observe', 'g', 'all'),
  (1, 'redall', 'observe', 'm', 'all'),
  (2, 'redall', 'observe', 'l', 'all'),
  (3, 'redall', 'attack', 'l', 'infantry'),
  (4, 'redall', 'attack', 'l', 'artillery'),
  (5, 'redall', 'attack', 'l', 'all')]}


solution=[[],
 [],
 [],
 [],
 [],
 [],
 [],
 [],
 [],
 [],
 [],
 [((2, 'redall', 'observe', 'l', 'all'), 'observe'),
  ((3, 'redall', 'attack', 'l', 'infantry'), 'attack')],
 [((2, 'redall', 'observe', 'l', 'all'), 'observe'),
  ((0, 'redall', 'observe', 'g', 'all'), 'observe'),
  ((3, 'redall', 'attack', 'l', 'infantry'), 'attack'),
  ((5, 'redall', 'attack', 'l', 'all'), 'attack')],
 [((1, 'redall', 'observe', 'm', 'all'), 'observe')],
 [((2, 'redall', 'observe', 'l', 'all'), 'observe'),
  ((1, 'redall', 'observe', 'm', 'all'), 'observe'),
  ((5, 'redall', 'attack', 'l', 'all'), 'attack')],
 [],
 [],
 [],
 [((1, 'redall', 'observe', 'm', 'all'), 'observe')],
 [((2, 'redall', 'observe', 'l', 'all'), 'observe'),
  ((0, 'redall', 'observe', 'g', 'all'), 'observe')],
 [((2, 'redall', 'observe', 'l', 'all'), 'observe')],
 [],
 [],
 [],
 [((2, 'redall', 'observe', 'l', 'all'), 'observe'),
  ((1, 'redall', 'observe', 'm', 'all'), 'observe')],
 [],
 [((2, 'redall', 'observe', 'l', 'all'), 'observe')],
 [((5, 'redall', 'attack', 'l', 'all'), 'attack')],
 [((3, 'redall', 'attack', 'l', 'infantry'), 'attack')],
 [((3, 'redall', 'attack', 'l', 'infantry'), 'attack')],
 [((2, 'redall', 'observe', 'l', 'all'), 'observe')],
 [((5, 'redall', 'attack', 'l', 'all'), 'attack')],
 [((3, 'redall', 'attack', 'l', 'infantry'), 'attack'),
  ((5, 'redall', 'attack', 'l', 'all'), 'attack')],
 [],
 [((5, 'redall', 'attack', 'l', 'all'), 'attack')],
 [((3, 'redall', 'attack', 'l', 'infantry'), 'attack'),
  ((5, 'redall', 'attack', 'l', 'all'), 'attack')],
 [],
 [],
 [],
 [((3, 'redall', 'attack', 'l', 'infantry'), 'attack')],
 [((4, 'redall', 'attack', 'l', 'artillery'), 'attack'),
  ((5, 'redall', 'attack', 'l', 'all'), 'attack')],
 [((4, 'redall', 'attack', 'l', 'artillery'), 'attack')],
 [((4, 'redall', 'attack', 'l', 'artillery'), 'attack')],
 [((4, 'redall', 'attack', 'l', 'artillery'), 'attack')],
 [],
 [],
 [((4, 'redall', 'attack', 'l', 'artillery'), 'attack')],
 [],
 [((3, 'redall', 'attack', 'l', 'infantry'), 'attack')],
 [((4, 'redall', 'attack', 'l', 'artillery'), 'attack')],
 [],
 [((4, 'redall', 'attack', 'l', 'artillery'), 'attack')],
 [((4, 'redall', 'attack', 'l', 'artillery'), 'attack')]]



#Data_manager = Data_pretreat()
#Data_manager.manage_software_data(software_input_data)
#Data_manager.estimate_cost_of_tasks(poset)
Poset_product = Poset_producter('task1')
Poset_product.poset=poset
Gantt_data=Poset_product.gantt_graph_generate( solution ,poset)
for data_step in message_date_2:
    Poset_product.gantt_online_menegar(data_step,poset)
s=1
#online generate gantt_data

a = optimize_method.Branch_And_Bound(poset, poset['action_map'],)
