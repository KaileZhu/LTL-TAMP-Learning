from src.ltl_mas.models.ts import MotionFts,ActionModel,MotActModel,Product_MotActFts
from src.ltl_mas.visualization.LTL_plotter import Grid_world_plotter
import numpy as np
from src.ltl_mas.models.planner import ltl_planner
from src.ltl_mas.models.buchi import mission_to_buchi
from src.ltl_mas.models.product import ProdAut
from src.ltl_mas.tools.discrete_plan import dijkstra_plan_networkX
##############################
# motion FTS
ap = {'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r', 'b'}
# +-----+-----+-----+
# | r4,r| r5,b| r6,b|
# +-----+-----+-----+
# | r1,r| r2,b| r3,r|
# +-----+-----+-----+
regions_list={}

for i in np.arange(1,3):
    regions_list['regions'+str(i)] = {   (0, 0, 1): set(['r'+str(i)+'1', 'r']),
              (1, 0, 1): set(['r'+str(i)+'2', 'b']),
              (2, 0, 1): set(['r'+str(i)+'3', 'r']),
              (0, 1, 1): set(['r'+str(i)+'4', 'r']),
              (1, 1, 1): set(['r'+str(i)+'5', 'b']),
              (2, 1, 1): set(['r'+str(i)+'6', 'b']),
                }

edges = [((0, 0, 1), (1, 0, 1)),
         ((1, 0, 1), (2, 0, 1)),
         ((0, 1, 1), (1, 1, 1)),
         ((1, 1, 1), (2, 1, 1)),
         ((0, 0, 1), (0, 1, 1)),
         ((1, 0, 1), (1, 1, 1)),
         ((2, 0, 1), (2, 1, 1)),
        ]

##############################
# action FTS
############# no action model
#action = dict()
############# with action
action = { 'pick': (100, 'r', set(['pick'])),
           'drop': (50, 'b', set(['drop']))
}
#{act_name: (cost, guard_formula, label)}

robot_action = ActionModel(action)

Tsdic={}
for i in np.arange(1,3):
    Fts=MotionFts(regions_list['regions' + str(i)], ap, 'office')
    Fts.set_initial((0,0,1))
    Fts.add_un_edges(edges, unit_cost = 0.1)
    Tsdic['robot_motion'+str(i)] = MotActModel(Fts,robot_action)
print(Tsdic)
#Tsset=[robot_motion,robot_motion,robot_motion]
product_robot_motion= Product_MotActFts(Tsdic,type='MotActModel')
#add the macro-action
#first defined macro-action
macro_action={'C'  : ( 500,(0,1),0)  }#(cost,(agents),
product_robot_motion.add_macro_action(macro_action)

##############################
# complete robot model
hard_task = '<>(r11 && <> (r12 && <> r16)) && ([]<> r16) && ([]<> r11) && [] <>(r11 -> X r15)'
#hard_task = '<>(r1 && <> (r2 && <> r6)) '
soft_task = None
#robot_planner = ltl_planner(product_robot_motion, hard_task, soft_task)
buchi = mission_to_buchi(hard_task, soft_task)#判断是否有为none的约束 转换为buchi
product = ProdAut(product_robot_motion, buchi)
for buchi_init in product.graph['buchi'].graph['initial']:
    init_prod_node = product.composition(product.graph['ts'].graph['initial'][0], buchi_init)
    print(init_prod_node)
product.build_full()




run, plantime = dijkstra_plan_networkX(product, 10,True)
print('run',run)
# synthesis
#start = time.time()

