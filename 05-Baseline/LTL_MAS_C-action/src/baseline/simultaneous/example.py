# An example to set up the system
import sys
import time

sys.path.append('/home/LZS/LTL/git/LTL_MAS_C-action/src')
import os
path0 = os.path.dirname(os.getcwd())
path1=os.path.join( path0 , 'src')
sys.path.append(path1)
#from ltl_mas.models.agent import Agent
#from ltl_mas.models.system import MultiAgentSystem
#from ltl_mas.models.planner import ltl_planner
from src.baseline.simultaneous.agent import Agent
from src.baseline.simultaneous.system import MultiAgentSystem
from src.baseline.simultaneous.planner import ltl_planner
from src.baseline.simultaneous.Deco_set_Buchi import Deco_set_Buchi
from src.ltl_mas.simulate.field_background import field
#=================generate wts
begin_time=time.time()
f=field()


#agent1:single agent without action model
agent_swarm=[]
agent_type=['UAV','UAV','UGV','UGV','UGV','UAV','UGV','UGV','UGV','UAV','UGV',
            'UGV','UGV','UAV','UGV','UGV','UGV','UAV','UGV','UGV','UGV','UAV',
            'UGV','UGV','UGV','UAV','UGV','UGV','UGV','UAV','UGV','UGV','UGV']
for i in range(24):
    agent=Agent('agent_'+str(i))
    agent.build_motion_fts(f)
    agent.add_action_model(f)
    agent.compute_motact_model()
    agent_swarm.append(agent)
#--------------------

# to test the planning of a team
task1='<>(repairp31 && <> scanp31) && [] (repairp31 -> ! scanp31) && <>(fixt6 && <> scant6)' \
      '&& [] (fixt6 -> ! scant6) && <> washp15 && <> mowp8'
task='<>(washp11 && <> (mowp11_p11 && <> sweepp11_p11) && <> scanp11_p11) && []((washp11_p11 || mowp11_p11) -> ! sweepp11_p11)' \
      '&&[](washp11_p11 -> ! mowp11_p11)&& [](washp11_p11 ->!scanp11_p11) ' \
'&& <>(washp20_p20 && <> (mowp20_p20 && <> sweepp20_p20)&& <> scanp20_p20) && []((washp20_p20 || mowp20_p20) -> ! sweepp20_p20) ' \
     '&&[](washp20_p20 -> ! mowp20_p20)&& [](washp20_p20 ->!scanp20_p20)'\
    '&& <> tempt4'
task1='<>(repairp31 && <> scanp31)'
task4='<>(washp11 && <> (mowp11 && <> sweepp11) && <> scanp11) && []((washp11 || mowp11) -> ! sweepp11)' \
      '&&[](washp11 -> ! mowp11)&& [](washp11 ->!scanp11) ' \
'&& <>(washp20 && <> (mowp20 && <> sweepp20)&& <> scanp20) && []((washp20 || mowp20) -> ! sweepp20) ' \
     '&&[](washp20-> ! mowp20)&& [](washp20 ->!scanp20)'\
    '&& <> tempt4'

for agent in agent_swarm:
    removed_nodes=[]
    for node in agent.motact_model.nodes:
        label=0
        for subset in agent.motact_model.nodes[node]['label']:
            if  subset in task:
                label=1
        if node[0]==(133,270):
            label=0
        if node[0]==(100,256):
            label=0
        if 't4' in node[1]:
            if not node[1]=='tempt4':
                label=0
        if not node==((358,15),'None'):
            if label==0:
                removed_nodes.append(node)

    for node in removed_nodes:
        agent.motact_model.remove_node(node)
team = MultiAgentSystem(agent_swarm)
team.add_team_task(task)
team.compute_buchi()
team.compute_product_ts_buchi()
team.compute_product_fianl_ts_buchi()
#1 add initial place for the agent
#2 begin a search as dij to find path.
print('begin optimal')
pre_prepare_time=time.time()
print('already prepare for ',pre_prepare_time-begin_time)
team_planner=ltl_planner(team.prod_marco_ts_buchi)
prefix,max_cost=team_planner.optimal()
end_time=time.time()
print('search_time',end_time- begin_time)
print('max_cost',max_cost)
# now you can search over team.prod_marco_ts_buchi
def calculate_synchronization(prefix):
    syn_num=0
    for node in prefix:
        if not node[1][1]=='None':
            for _,i in f.input_data.task_type[node[1][1]][1].items():
                syn_num=syn_num+i
            #syn_num=syn_num+f.input_data.task_type[node[1][1]][1]
    print(syn_num)
calculate_synchronization(prefix)

prefix=[(0, ((358, 15), 'None'), 'T0_init'), (0, ((133, 270), 'None'), 'T3_S1'),
 (1, ((358, 15), 'None'), 'T3_S1'), (2, ((358, 15), 'None'), 'T3_S1'),
 (3, ((358, 15), 'None'), 'T3_S1'), (4, ((358, 15), 'None'), 'T3_S1'),
 (5, ((358, 15), 'None'), 'T3_S1'), (6, ((358, 15), 'None'), 'T3_S1'),
 (6, ((477, 218), 'None'), 'T3_S1'), (6, ((477, 218), 'tempt4'), 'T3_S1'),
 (6, ((477, 218), 'None'), 'T3_S2'), (7, ((358, 15), 'None'), 'T3_S2'),
 (7, ((146, 96), 'None'), 'T3_S2'), (7, ((146, 96), 'washp11'), 'T3_S2'),
 (7, ((146, 96), 'None'), 'T7_S6'), (7, ((146, 96), 'scanp11'), 'T7_S6'), (7, ((146, 96), 'None'), 'T7_S79'),
 (7, ((146, 96), 'mowp11'), 'T7_S79'), (7, ((146, 96), 'None'), 'T7_S81'), (7, ((146, 96), 'sweepp11'), 'T7_S81'),
(7, ((146, 96), 'None'), 'T7_S82'), (8, ((358, 15), 'None'), 'T7_S82'), (8, ((378, 215), 'None'), 'T7_S82'),
(8, ((378, 215), 'washp20'), 'T7_S82'), (8, ((378, 215), 'None'), 'accept_S31'), (8, ((378, 215), 'scanp20'), 'T5_S31'),
(8, ((378, 215), 'None'), 'T5_S30'), (8, ((378, 215), 'mowp20'), 'T5_S30'),  (8, ((378, 215), 'None'), 'T4_S25'),
(8, ((378, 215), 'sweepp20'), 'T4_S25'), (8, ((378, 215), 'None'), 'accept_S26'), (9, ((358, 15), 'None'), 'accept_S26'),
        (9, ((474, 187), 'None'), 'accept_S26')]

search_time =581.294457912445
max_cost=1266.987130407062
15