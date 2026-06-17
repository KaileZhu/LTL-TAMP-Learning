import numpy as np
from src.ltl_mas.models.planner import ltl_planner
from src.ltl_mas.models.system import Tsset_builder,System
from src.ltl_mas.visualization.LTL_plotter import Agent_based_cf_ploter
##############################
# motion FTS
ap = {'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r', 'b'}
# +-----+-----+-----+
# | r4,r| r5,b| r6,b|
# +-----+-----+-----+
# | r1,r| r2,b| r3,r|
# +-----+-----+-----+
regions_list={}
regions={(0, 0): '1',(1, 0): '2',(0, 1): '3' ,(1, 1): '4'}
for i in np.arange(1,4):
    regions_list['robot'+str(i)] = {
              (0, 0): set(['r'+str(i)+'1']),
              (1, 0): set(['r'+str(i)+'2']),
              (0, 1): set(['r'+str(i)+'3']),
              (1, 1): set(['r'+str(i)+'4']),
                }

edges = [((0, 0), (1, 0)),
         ((1, 0), (1, 1)),
         ((0, 0), (0, 1)),
         ((0, 1), (1, 1)),
         ((0 ,0), (1, 1))
        ]

##############################
# action FTS
############# no action model

#{act_name: (cost, guard_formula, label)}
#'pick': (100, 'r', set(['pick'])),
action = { 'robot1':{'F_leader': (60, None, set(['lead']))},
           'robot2':{'F_follower': (60, None, set(['follow']))},
           'robot3':{'F_follower': (60, None, set(['follow']))}
}
#def Homogeny_Tsset_builder(n,regins_list,ap,edges,robot_action,name,initial,unit_cost=0.1)
Tsdic=Tsset_builder(3,regions_list,ap,edges,action,name='robot',initial=(0,0),unit_cost=0.1)

#product_robot_model= Product_of_TS(Tsdic,name='robot',type='MotActModel')
#add the macro-action
#first defined macro-action  (0,1,1,0)
#'pick': (100, 'r', set(['pick'])),
macro_actions={'c1'  : (200,set((('F_leader',1),('F_follower',2))),set(['formation']))  , #(cost,(agents),labeling function)
              'c2':    (400,set((('F_leader',1),('F_follower',1))),set(['search']))}
product_robot_model=System(Tsdic,macro_actions,regions,robot_name='robot',type='MotActModel')

##############################
# complete robot model
# agent_tpye + number
# agent_skill :numer
hard_task = '<>(r11 && <> (r14 && <> c13)) && <>(r31 && <> r34) && ([]<> r12) && ([]<> r11) && [] <>(r11 -> X r12)'
soft_task = None

##############################
# set planner
robot_planner = ltl_planner(product_robot_model, hard_task, soft_task)
# synthesis
#start = time.time()
robot_planner.optimal(10,'centralize')
np.save('output_data/suffix.npy',robot_planner.run.suffix)
np.save('output_data/prefix.npy',robot_planner.run.prefix)

#agent_plotter=Agent_based_cf_ploter(3)
