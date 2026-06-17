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
from src.baseline.sampling_based.agent import Agent
from src.baseline.sampling_based.system import MultiAgentSystem
from src.baseline.sampling_based.planner import ltl_planner
from src.ltl_mas.simulate.field_background import field
#=================generate wts
begin_time=time.time()
f=field()


#agent1:single agent without action model
agent_swarm=[]
agent_type=['UAV','UAV','UGV','UGV','UGV','UAV','UGV','UGV','UGV','UAV','UGV','UGV','UGV','UAV','UGV','UGV','UGV']
for i in range(6):
    agent=Agent('agent_'+str(i))
    agent.build_motion_fts(f)
    agent.add_action_model(f)
    agent.compute_motact_model()
    agent_swarm.append(agent)
#--------------------

# to test the planning of a team
task='<>(repairp31 && <> scanp31)  && <>fixt6 && <> scanp6 && <> washp15 '
task3='<>(repairp31 && <> scanp31)&& <> washp15 && <>fixt6'
task3='<> (repairp31 && <> scanp31) && <> washp15  && <>fixt6'
task3='<>(washp11 && <> (mowp11 && <> sweepp11) && <> scanp11)'
task1='<>(washp11 && <> (mowp11 && <> sweepp11) && <> scanp11)' \
'&& <>(washp20 && <> (mowp20 && <> sweepp20)&& <> scanp20)&& <> tempt4 '
task3='<>(washp11 && <> (mowp11 && <> sweepp11) && <> scanp11) && <>(washp20 && <> (mowp20 && <> sweepp20)&& <> scanp20) && <> tempt4'
task2='<>(washp11 && <> (mowp11 && <> sweepp11) && <> scanp11) && []((washp1 || mowp11) -> ! sweepp11)' \
      '&&[](washp11 -> ! mowp11)&& [](washp11 ->!scanp11) ' \
'&& <>(washp20 && <> (mowp20 && <> sweepp20)&& <> scanp20) && []((washp20 || mowp20) -> ! sweepp20) ' \
     '&&[](washp20 -> ! mowp20)&& [](washp20 ->!scanp20)'\
    '&& <> tempt4'
task='<>washp11'
for agent in agent_swarm:
    removed_nodes=[]
    for node in agent.motact_model.nodes:
        label=0
        for subset in agent.motact_model.nodes[node]['label']:
            if  subset in task2:
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
team.add_team_task(task2)
team.compute_buchi()
team.buchi.graph['accept']={'accept_S26'}
#step 1
team.construct_product_ts_buchi()
team_planner=ltl_planner(team.PBA)
#begin search
#line_pre,line_list,prefix=team_planner.optimal_star(search_round=2000)
line_pre,line_list,prefix=team_planner.optimal_fast2(task2,search_round=80)
#team_planner.optimal_improve(search_round=80)
#team_planner.optimal(search_round=2000)
end_time=time.time()
print(end_time-begin_time)
cost=0
for node in  prefix:
    cost=team_planner.search_graph
# now you can search over team.prod_marco_ts_buchi
def calculate_synchronization(prefix):
    syn_num=0
    syn_num2=0
    for node in prefix:
        for sub_node in node[0]:
            if not sub_node[1]=='None':
                syn_num2=syn_num2+1
                for _,i in f.input_data.task_type[sub_node[1]][1].items():
                    syn_num=syn_num+i
        syn_num=syn_num+1
            #syn_num=syn_num+f.input_data.task_type[node[1][1]][1]
    print('need synchronization ',syn_num)
    print('need synchronization2 ',syn_num2)
calculate_synchronization(prefix)
prefix=[((((358, 15), 'None'), ((358, 15), 'None'), ((358, 15), 'None')), 'T0_init'),
        ((((133, 270), 'None'), ((100, 256), 'None'), ((133, 270), 'None')), 'T3_S1'),
        ((((133, 270), 'None'), ((378, 215), 'None'), ((146, 96), 'None')), 'T3_S1'),
        ((((133, 270), 'sweepp1'), ((378, 215), 'repairp20'), ((146, 96), 'washp11')), 'T3_S1'),
        ((((133, 270), 'None'), ((378, 215), 'None'), ((146, 96), 'None')), 'T7_S70'),
        ((((133, 270), 'scanp1'), ((378, 215), 'None'), ((146, 96), 'scanp11')), 'T7_S70'),
        ((((133, 270), 'None'), ((378, 215), 'None'), ((146, 96), 'None')), 'T7_S84'),
        ((((146, 96), 'None'), ((378, 215), 'None'), ((146, 96), 'mowp11')), 'T7_S84'),
        ((((100, 256), 'None'), ((477, 218), 'None'), ((146, 96), 'None')), 'T7_S56'),
        ((((100, 256), 'None'), ((477, 218), 'tempt4'), ((146, 96), 'scanp11')), 'T7_S56'),
        ((((100, 256), 'None'), ((477, 218), 'None'), ((146, 96), 'None')), 'T7_S57'),
        ((((100, 256), 'None'), ((378, 215), 'None'), ((100, 256), 'None')), 'T7_S57'),
        ((((133, 270), 'None'), ((378, 215), 'washp20'), ((100, 256), 'tempp2')), 'T7_S57'),
        ((((100, 256), 'None'), ((378, 215), 'None'), ((100, 256), 'None')), 'T0_S67'),
        ((((133, 270), 'None'), ((378, 215), 'None'), ((146, 96), 'None')), 'T0_S67'),
        ((((100, 256), 'None'), ((378, 215), 'None'), ((146, 96), 'sweepp11')), 'T0_S67'),
        ((((133, 270), 'None'), ((378, 215), 'None'), ((146, 96), 'None')), 'T5_S39'),
        ((((100, 256), 'None'), ((378, 215), 'mowp20'), ((378, 215), 'None')), 'T5_S39'),
        ((((378, 215), 'None'), ((378, 215), 'None'), ((378, 215), 'sweepp20')), 'T6_S35'),
        ((((378, 215), 'scanp20'), ((378, 215), 'sweepp20'), ((378, 215), 'None')), 'T6_S35'),
        ((((378, 215), 'scanp20'), ((378, 215), 'sweepp20'), ((378, 215), 'None')), 'accept_all')]
[((((358, 15), 'None'), ((358, 15), 'None'), ((358, 15), 'None')), 'T0_init'),
 ((((146, 96), 'None'), ((100, 256), 'None'), ((133, 270), 'None')), 'T3_S1'),
 ((((146, 96), 'washp11'), ((100, 256), 'None'), ((133, 270), 'washp1')), 'T3_S1'),
 ((((146, 96), 'None'), ((100, 256), 'None'), ((133, 270), 'None')), 'T7_S70'),
 ((((146, 96), 'mowp11'), ((100, 256), 'None'), ((133, 270), 'None')), 'T7_S70'),
 ((((146, 96), 'None'), ((146, 96), 'None'), ((477, 218), 'None')), 'T7_S42'),
 ((((133, 270), 'None'), ((146, 96), 'sweepp11'), ((477, 218), 'None')), 'T7_S42'),
 ((((146, 96), 'None'), ((146, 96), 'None'), ((477, 218), 'None')), 'T7_S15'),
 ((((146, 96), 'scanp11'), ((378, 215), 'None'), ((477, 218), 'tempt4')), 'T7_S15'),
 ((((146, 96), 'None'), ((146, 96), 'None'), ((477, 218), 'None')), 'T7_S30'),
 ((((133, 270), 'None'), ((378, 215), 'None'), ((378, 215), 'None')), 'T7_S30'),
 ((((133, 270), 'None'), ((378, 215), 'mowp20'), ((378, 215), 'washp20')), 'T7_S30'),
 ((((378, 215), 'None'), ((378, 215), 'None'), ((378, 215), 'None')), 'T4_S35'),
 ((((378, 215), 'scanp20'), ((378, 215), 'tempp20'), ((378, 215), 'sweepp20')), 'T4_S35'),
 ((((378, 215), 'scanp20'), ((378, 215), 'tempp20'), ((378, 215), 'sweepp20')), 'accept_all')]
[((((358, 15), 'None'), ((358, 15), 'None'), ((358, 15), 'None'), ((358, 15), 'None'), ((358, 15), 'None'), ((358, 15), 'None')), 'T0_init'),
 ((((378, 215), 'None'), ((378, 215), 'None'), ((477, 218), 'None'), ((477, 218), 'None'), ((477, 218), 'None'), ((378, 215), 'None')), 'T3_S1'),
 ((((146, 96), 'None'), ((378, 215), 'mowp20'), ((477, 218), 'None'), ((378, 215), 'None'), ((146, 96), 'None'), ((146, 96), 'None')), 'T3_S1'),
 ((((146, 96), 'washp11'), ((378, 215), 'None'), ((477, 218), 'tempt4'), ((378, 215), 'washp20'), ((146, 96), 'tempp11'), ((477, 218), 'None')), 'T3_S1'),
 ((((146, 96), 'None'), ((378, 215), 'mowp20'), ((477, 218), 'None'), ((378, 215), 'None'), ((146, 96), 'None'), ((146, 96), 'None')), 'T5_S7'),
 ((((378, 215), 'None'), ((378, 215), 'None'), ((146, 96), 'None'), ((378, 215), 'scanp20'), ((378, 215), 'None'), ((146, 96), 'scanp11')), 'T6_S45'),
 ((((378, 215), 'scanp20'), ((477, 218), 'None'), ((378, 215), 'None'), ((378, 215), 'None'), ((146, 96), 'None'), ((146, 96), 'None')), 'T8_S46'),
 ((((378, 215), 'None'), ((146, 96), 'None'), ((378, 215), 'tempp20'), ((378, 215), 'None'), ((146, 96), 'mowp11'), ((378, 215), 'None')), 'T8_S46'),
 ((((378, 215), 'scanp20'), ((477, 218), 'None'), ((378, 215), 'None'), ((378, 215), 'None'), ((146, 96), 'None'), ((146, 96), 'None')), 'T8_S54'),
 ((((378, 215), 'scanp20'), ((477, 218), 'tempt4'), ((378, 215), 'scanp20'), ((378, 215), 'None'), ((146, 96), 'scanp11'), ((146, 96), 'None')), 'T8_S54'),
 ((((378, 215), 'scanp20'), ((477, 218), 'None'), ((378, 215), 'None'), ((378, 215), 'None'), ((146, 96), 'None'), ((146, 96), 'None')), 'T0_S19'),
 ((((378, 215), 'None'), ((146, 96), 'None'), ((378, 215), 'None'), ((378, 215), 'None'), ((378, 215), 'None'), ((146, 96), 'sweepp11')), 'T0_S19'),
 ((((477, 218), 'None'), ((146, 96), 'scanp11'), ((378, 215), 'sweepp20'), ((146, 96), 'None'), ((378, 215), 'scanp20'), ((146, 96), 'None')), 'T2_S33'),
 ((((477, 218), 'None'), ((146, 96), 'scanp11'), ((378, 215), 'sweepp20'), ((146, 96), 'None'), ((378, 215), 'scanp20'), ((146, 96), 'None')), 'accept_S26')]
