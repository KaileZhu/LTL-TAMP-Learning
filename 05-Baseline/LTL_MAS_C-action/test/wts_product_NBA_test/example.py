# An example to set up the system
import sys
sys.path.append('/home/LZS/LTL/git/LTL_MAS_C-action/src')
import os
path0 = os.path.dirname(os.getcwd())
path1=os.path.join( path0 , 'src')
sys.path.append(path1)
#from ltl_mas.models.agent import Agent
#from ltl_mas.models.system import MultiAgentSystem
#from ltl_mas.models.planner import ltl_planner
from src.baseline.product_based.agent import Agent
from src.baseline.product_based.system import MultiAgentSystem
from src.baseline.product_based.planner import ltl_planner


nodes, symbols, edges, actions = None, None, None, None
nodes= {   (0, 0): set(['r1', 'r']),
              (1, 0): set(['r2', 'b']),
              (2, 0): set(['r3', 'r']),
              (0, 1): set(['r4', 'r']),
              (1, 1): set(['r5', 'b']),
              (2, 1): set(['r6', 'b']),
}
edges= [((0, 0), (1, 0)),
         ((1, 0), (2, 0)),
         ((0, 1), (1, 1)),
         ((1, 1), (2, 1)),
         ((0, 0), (0, 1)),
         ((1, 0), (1, 1)),
         ((2, 0), (2, 1)),
]

actions = { 'F_leader': (100, 'r', set(['pick'])),
           'F_follower': (50, 'b', set(['drop']))
}
#agent1:single agent without action model
agent_1 = Agent('agent_1')
agent_1.build_motion_fts(nodes, symbols, edges)
agent_1.motion_fts.set_initial((0,1))
agent_1.add_action_model(actions)
agent_1.compute_motact_model()
#agent2:single agent with action model
agent_2 = Agent('agent_2')
agent_2.build_motion_fts(nodes, symbols, edges)
agent_2.motion_fts.set_initial((1,1))
agent_2.add_action_model(actions)
agent_2.compute_motact_model()

agent_3 = Agent('agent_3')
agent_3.build_motion_fts(nodes, symbols, edges)
agent_3.motion_fts.set_initial((1,2))
agent_3.add_action_model(actions)
agent_3.compute_motact_model()

#--------------------
# to test planning of a single agent
local_task_1 = '<>(r1 && <> (r2 && <> r6))'
#local_task='<> photo_p3'
agent_1.add_local_task(local_task_1)
agent_1.compute_buchi()
agent_1.compute_product_motact_buchi()
agent_1_planner=ltl_planner(agent_1.prod_motact_buchi)
# now you can search over agent_1.prod_motact_buchi
#--------------------
#agent_1_planner.optimal()
#--------------------
# to test the planning of a team
team = MultiAgentSystem([agent_1, agent_2, agent_3])
team.compute_team_product_ts()
marco_actions ={'c1'  : (200,set((('F_leader',1),('F_follower',2))),set(['formation']))  , #(cost,(agents),labeling function)
              'c2':    (400,set((('F_leader',1),('F_follower',1))),set(['search']))}
team.add_marco_actions(marco_actions)

#get the massge of regions
team_task = 'g f r1 && g f r2'
regions={(0, 0): '1',(1, 0): '2',(2,0): '3' ,(0,1): '4',(1,1):'5',(2,1):'6'}#using for build special label of macro_action
#get add team task?
#
team.add_team_task(team_task)
#here we can calculate the
team.compute_buchi()

#1 add initial place for the agent
#2 begin a search as dij to find path.
team.compute_product_ts_buchi()
# now you can search over team.prod_ts_buchi
# OR
team.add_regions_for_marco_action(regions)
team.compute_product_marco_ts()
team.compute_product_marco_ts_buchi()
print('begin optimal')
team_planner=ltl_planner(team.prod_marco_ts_buchi)
team_planner.optimal()
a=3
s=1


# now you can search over team.prod_marco_ts_buchi
