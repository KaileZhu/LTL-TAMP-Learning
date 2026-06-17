import os
import sys
import time
import random
import numpy as np
# sys.path.append("D:/Desktop/JK_game-master/planning")
# sys.path.append("D:/Desktop/JK_game-master/pla2nning/test")
# sys.path.append("D:/Desktop/JK_game-master/planning/src")

# sys.path.append('D:\PycharmProjects\JK_project1\planning')
# sys.path.append('D:\PycharmProjects\JK_project1\planning/test')
# sys.path.append('D:\PycharmProjects\JK_project1\planning/src')
# sys.path.append('C:/Users\MSI1\Documents\LTL\JK_game\planning')
# sys.path.append('C:/Users\MSI1\Documents\LTL\JK_game\planning/test')
# sys.path.append('C:/Users\MSI1\Documents\LTL\JK_game\planning/src')
from planning.src.ltl_mas.tools import optimize_method
from planning.src.ltl_mas.formula_generater.LTL_formula_generater import LTL_generater
from planning.src.ltl_mas.tools.Data_pre_treatment import Data_pretreat
from planning.src.ltl_mas.tools.poset_product import  Poset_producter
from planning.src.ltl_mas.tools.order_anylises.py_decisions.topsis.fuzzy_topsis import fuzzy_topsis_method
from planning.data.input_data.LTL_formula import *
from planning.data.input_data.agent_data import agent_resource

class  central_master(object):
    def __init__(self):
        '''
        控制整个系统的核心程序，整体后台不断的调用它，就给行了
        主要分为3大模块，每个模块彼此之间尽量分开
        1 数据处理 Data_manager
          负责数据的更新
        2 任务分配计算
        3 接口规整,将输入的数据进行处理


        额外添加的，对数值的估计变化
        对cost的更新，4个参数
        添加整体的内容
        '''
        #初始化数据控制程序
        self.Data_manager=Data_pretreat()

    def get_initial_data(self,env_type='想定场景1'):
        if env_type=='想定场景1':
            num=1
            #from planning.data.input_data.first_data_ZYBJ import software_input_data
            from planning.data.input_data.first_data_ZYBJ import software_input_data
            print('采用场景1，红方智能体数量：81，蓝方智能体数量40')
        elif env_type=='想定场景2':
            num=2
            from planning.data.input_data.second_Data import software_input_data
            print('采用场景2，红方智能体数量：49，蓝方智能体数量35')
        elif env_type=='想定场景3':
            num=3
            from planning.data.input_data.third_Data import software_input_data
            print('采用场景3，红方智能体数量：39，蓝方智能体数量30')
        #software_input_data=get_software_input_data(num)
        #map_data 更新一次
        #self.Data_manager.manage_software_data(software_input_data)
        return  software_input_data

    def get_initial_map_data(self, env_type):
        if env_type == '想定场景1':
            num = 1
            import planning.data.input_data.first_map_data as map_data

        elif env_type == '想定场景2':
            num = 2
            import planning.data.input_data.second_map_data as map_data
        elif env_type == '想定场景3':
            num = 3
            import planning.data.input_data.third_map_data as map_data

        # software_input_data=get_software_input_data(num)
        # map_data 更新一次
        # self.Data_manager.manage_software_data(software_input_data)
        return map_data
    def pre_design_the_subtask_structure(self,background,calculate_type,path_calculate,prefer_type,war_type,stick):
        #back_ground,operation):
        print('选择的偏好类型：',prefer_type)
        self.prefer_tpye=prefer_type
        self.background=background
        software_input_data=self.get_initial_data(background)
        # map_data 更新一次
        map_data=self.get_initial_map_data(background)
        self.Data_manager.get_map_data(map_data,background)
        self.Data_manager.manage_software_data(software_input_data)
        self.Data_manager.judge_the_taishi_of_agent(software_input_data)
        #预调战法细节规则
        #获取价值分布
        value_place_dic=self.Data_manager.get_value_place_dic()
        self.task = LTL_generater(self.Data_manager)
        planning_structure=self.task.pre_calculate_the_goal_data(value_place_dic,war_type)
        #print('calculate_to_here')
        self.task.calculate_type=calculate_type
        self.task.path_calculate=path_calculate
        self.task.prefer_type=prefer_type
        self.task.stick=stick
        self.task.war_type=war_type
        #获取决策输入

        return  planning_structure



    def get_input_data(self,goal_subject_pair):
        #获取输入的数据，进行拆分，并且将一些量设置为self量
        #self.background_type=http_input_data['background_type']
        #goal_subject_pair1=http_input_data['zanfa']
        #获取选择的实验场景，生成场景 这里场景如何选择，看星宇了
        #选取场景的问题
        begin_time=time.time()
        #self.Data_manager.manage_software_data(software_input_data)
        #changeinput into pair
        new_input={}
        for operation_list in goal_subject_pair:
            wave=int(operation_list['波次'])
            if not wave-1 in new_input.keys():
                new_input[wave-1]={}
            method=operation_list['战法']#可能会报错，看前端到底改不改战法了，如果错了就改成战术
            method_ename = anti_dic_zanshu[method]
            if not method_ename in new_input[wave-1].keys():
                new_input[wave-1][method_ename]=[[]]
            place=operation_list['地点']
            place_name=num_dic_to_map[place]
            goal=operation_list['目标']
            goal_name = blue_dic_to_name[goal]
            new_input[wave - 1][method_ename][0].append({'place':place_name,'goal':goal_name})
        # back_ground,operation):
        background = '想定场景1'
        self.background = background
        software_input_data = self.get_initial_data(background)
        # map_data 更新一次
        map_data = self.get_initial_map_data(background)
        self.Data_manager.get_map_data(map_data, background)
        self.Data_manager.manage_software_data(software_input_data)
        self.Data_manager.judge_the_taishi_of_agent(software_input_data)
        # 预调战法细节规则
        # 获取价值分布
        value_place_dic = self.Data_manager.get_value_place_dic()
        self.task = LTL_generater(self.Data_manager)
        #self.rules = software_input_data['rule']
        method_name='全面进攻'

        self.task.creat_LTL_formula_with_wave_picking(new_input, method_name)
        # 生成形式化语言公式
        self.task.create_final_formula()
        self.LTL_formula=self.task.final_formula
        # 进行任务分解，获取任务偏序集
        self.Poset_product = Poset_producter(self.LTL_formula)
        self.Poset_product.generate_poset()
        self.Poset_product.prodocter()
        self.poset=self.Poset_product.final_poset
        # 根据环境，评估子任务的内容，以及价值
        self.Data_manager.estimate_cost_of_tasks(self.Poset_product)
        self.input_data = self.Data_manager.input_data
        end_time=time.time()
        #第一层的计算时间
        #self.first_level_calculate_time=end_time-begin_time


    def change_goal_task_pair(self,input):
        # 调整一下格式
        #{'场景选择': '想定场景2', '算法选择': '分支定界法', '算法路径':
        # 'planning\\src\\ltl_mas\\tools\\B_A_B.py', '偏好选择':
        # '执行速度优先', '战法选择': '占场扫描', '条例选择': ['禁止攻击'],
        # '战法内容': {'1': {'顺序侦查': [['红方', '001', '蓝方', '动态'],
        # ['红方', '002', '蓝方', '动态'], ['红方', '003', '蓝方', '动态']]},
        # '2': {'顺序进攻': [['红方', '001', '蓝方', '动态'], ['红方', '001', '蓝方', '动态'],
        # ['红方', '001', '蓝方', '动态']], '基础进攻': [['红方', '002', '蓝方', '动态'],
        # ['红方', '003', '蓝方', '动态']]}, '3': {'基础支持': [['红方', '002', '蓝方', '动态'],
        # ['红方', '003', '蓝方', '动态']], '基础侦查': [['红方', '002', '蓝方', '动态'], ['红方', '003', '蓝方', '动态']]}}}
        new_input={}
        prefer=input['偏好选择']
        #{0:{'basic_atk':[[{'place': 'l', 'goal': 'infantry'},
        #                             {'place': 'l', 'goal': 'artillery'}]]},
        #             1:{'basic_atk':[[{'place': 'l', 'goal': 'all'}]]},
        #             2:{'basic_support':[[{'place': 'l', 'goal': 'all'}]],
        #                "basic_atk":[[{'place': 'g', 'goal': 'all'}]]},
        #             3:{"basic_support":[[{'place': 'g', 'goal': 'all'}]],
        #                "basic_atk":[[{'place': 'm', 'goal': 'all'}]]},
        #             4:{"basic_support":[[{'place': 'm', 'goal': 'all'}]]}
        #             }
        for waves, operation_list in input['战法内容'].items():
            new_input[int(waves)-1]={}
            for method_name,detail_list in  operation_list.items():
                new_input[int(waves)-1][anti_dic_zanshu[method_name]]=[]
                part_list=[]
                for red,place,blue,state in detail_list:
                    red_name='redall'
                    place_name=num_dic_to_map[place]
                    blue_name=blue_dic_to_name[blue]
                    part_list.append({'subject':red_name,'place':place_name,'goal':blue_name})
                new_input[int(waves)-1][anti_dic_zanshu[method_name]].append(part_list)

        return new_input,prefer

    def calculate_subtask_value(self,goal_subject_pair1,rules,method_name):
        begin_time = time.time()
        #self.task = LTL_generater(self.Data_manager)
        print('new',goal_subject_pair1)
        goal_subject_pair2={0:{'basic_obs': [[{'subject': 'redall', 'place': 'g', 'goal': 'all'},
                                                    {'subject': 'redall', 'place': 'l', 'goal': 'all'},
                                                    {'subject': 'redall', 'place': 'm', 'goal': 'all'}]
                                                   ]},
                                      1:{'basic_atk': [[{'place': 'l', 'goal': 'infantry'},
                                                    {'place': 'l', 'goal': 'artillery'}]
                                                   ]},
                                      2:{'basic_atk': [[{'subject': 'redall', 'place': 'l', 'goal': 'all'}]
                                                   ]}}
        print('old',goal_subject_pair1)
        self.task.creat_LTL_formula_with_wave_picking(goal_subject_pair1, method_name)
        # 生成形式化语言公式
        self.task.create_final_formula()
        self.LTL_formula = self.task.final_formula
        print('LTL_formula',self.LTL_formula)
        # 进行任务分解，获取任务偏序集
        self.Poset_product = Poset_producter(self.LTL_formula)
        self.Poset_product.generate_poset()
        self.Poset_product.prodocter()
        self.poset = self.Poset_product.final_poset
        print('final_poset is ',self.poset)
        # 根据环境，评估子任务的内容，以及价值
        self.Data_manager.estimate_cost_of_tasks(self.Poset_product,self.background)
        self.task_information= self.Data_manager.task_information
        end_time = time.time()
        subtask_value=[]
        muhulist=self.muhu_data_out_put()
        print(self.Data_manager.task_information)
        action_dic={'attack':'进攻','observe':'侦察','support':'支持','trick':'诱骗'}
        print('输入的总体任务')
        for i in range(len(self.Data_manager.task_information['time_cost'])):
            #是否把这个subtask 序号改成  进攻xxx 更为直观？
            #感觉比较合理
            print('action_map',self.poset['action_map'][i])
            row={'subtask':action_dic[self.poset['action_map'][i][2]]+map_dic_to_num[self.poset['action_map'][i][3]],
                 'contribution':self.task_information['task_comtribution'][i],
                 'consumption':self.task_information['time_cost'][i],
                 'loss':self.task_information['task_risk'][i],
                 'requirement':self.task_information['agent_needed'][i],
                 'priority':muhulist[i][0]}
            subtask_value.append(row)
        self.subtask_value=subtask_value
        print('敌方的态势')
        for agent_name in self.Data_manager.enemy_taishi:
            print('单位类别',agent_name['类型'],'运动',agent_name['运动状态'],'行动意图',agent_name['意图'],'资源数量：',random.randint(0,4))
        print('我方的态势')
        for agent_name in self.Data_manager.our_taishi:
            print('单位类别', agent_name['类型'], '运动', agent_name['运动状态'])
        # 第一层的计算时间
        # self.first_level_calculate_time=end_time-begin_time
        return subtask_value



    def online_replanning(self,new_first_data, finished_Task, is_beihang=False):
        #1 更新当前的环境数据
        self.Data_manager.online_task_detection(new_first_data)
        #2 更新任务评估,临时项，用完记得删掉
        task1={0: ['<>  redall_observe_g_all && <>  redall_observe_l_all && <>  redall_observe_m_all '],
         1: ['<>  redall_attack_l_infantry && <>  redall_attack_l_artillery '],
         2: ['<>  redall_attack_l_all ']}

        self.Poset_product = Poset_producter(task1)
        self.Poset_product.generate_poset()
        self.Poset_product.prodocter()
        self.poset = self.Poset_product.final_poset
        #临时处理生成一个poset_product
        print(self.Poset_product.final_task_data_list)
        self.Data_manager.estimate_cost_of_tasks(self.Poset_product)
        self.task_information = self.Data_manager.task_information
        #给前端的数据
        f = open('subtask_data.py', 'w')
        f.write(str(self.task_information))
        f.close()
        #更新未完成的任务
        new_poset={'action_map':[],'<=':set(),'<':set(),'=':set(),'!=':set()}
        for task in self.Poset_product.final_poset['action_map']:
            if not task[0] in finished_Task:
                new_poset['action_map'].append(task)

        for i,j in self.Poset_product.final_poset['<=']:
            if not i in finished_Task:
                if not j in finished_Task:
                    new_poset['<='].add((i,j))
                    new_poset['<'].add((i, j))
        #
        self.input_data=self.Data_manager.input_data
        self.optimize_method = optimize_method.Branch_And_Bound(new_poset,
                                                          self.Poset_product.final_task_data_list,
                                                          self.input_data)
        self.optimize_method.subtask_value = self.subtask_value
        self.optimize_method.prefer_type=self.prefer_tpye
        self.optimize_method.Begin_branch_search(5, up_bound_method='greedy', low_bound_method='i+j',
                                                 search_method='DFS')
        self.current_solution = self.optimize_method.best_solution
        self.task_time_table = self.optimize_method.task_time_table
        #北航的改这里
        f = open('solution.py', 'w')
        f.write(str(self.task_information))
        f.close()
        if is_beihang:
            return self.current_solution

        # 这一步返回包括计算数据，
        return self.current_solution, self.task_time_table
        #


    def get_date_from_simulater(self,input_data):
        self.input_data=input_data

    def out_put_subtask_data(self):
        self.Data_manager.estimate_cost_of_tasks(self.Poset_product)
        input_data = self.Data_manager.task_information
        return  input_data

    def out_put_calculation_data(self):
        #目前设定，返回LTL公式，子任务数据
        duration_cost_data={'LTL 公式': self.LTL_formula,
                            '决策中枢层计算时间': self.first_level_calculate_time,
                            '任务分配层计算时间': self.second_level_calculate_time

                            }
        return  duration_cost_data

    def muhu_data_out_put(self):
        # 输出模糊的数据
        dataset=self.Data_manager.task_information
        print('开始根据模糊算法计算优先度')
        print('考虑的参数有子任务贡献度：',self.Data_manager.task_information['task_comtribution'])
        print('     资源消耗：', self.Data_manager.task_information['agent_needed'])
        print('     战损估计：',self.Data_manager.task_information['task_risk'])
        print('     战力需求：', self.Data_manager.task_information['agent_needed'])
        print('采用 topsis 法')
        weights = list([
            [(0.1, 0.2, 0.3), (0.7, 0.8, 0.9), (0.3, 0.5, 0.8)]
        ])

        # Load Criterion Type: 'max' or 'min'
        criterion_type = ['max', 'max', 'min']
        self.mohu_subtask_value=fuzzy_topsis_method(self.Data_manager.task_information, weights, criterion_type, graph=False)
        print('最终获取到的排序为：',self.mohu_subtask_value)
        return  self.mohu_subtask_value


    def subtask_order_update(self,c_i):
        #this function is used to change the subtask_order special value and change to order
        #动态更新子任务交互口， 输入新的子任务优先度，然后更新
        flow = np.copy(c_i)
        flow = np.reshape(flow, (c_i.shape[0], 1))
        flow = np.insert(flow, 0, list(range(1, c_i.shape[0] + 1)), axis=1)
        flow = flow[np.argsort(flow[:, 1])]
        flow = flow[::-1]
        self.mohu_subtask_value=flow
        return flow


    def out_put_calculate_data(self):
        s=0
        return s

    def determine_step(self,time_limit=14):
        #输入输出的内容是啥
        #总体任务，对手集群态势信息，己方集群态势信息
        begin_time=time.time()
        print('合同网分配参考的参数有')
        print('排序后的总体任务：')
        id=0
        for task in self.Poset_product.final_task_data_list:
            print(task,'次序为',self.subtask_value[id]['priority'],'子任务属性: 贡献度',self.subtask_value[id]['contribution'],
                  '执行损失',self.subtask_value[id]['loss'],'战力需求',self.subtask_value[id]['requirement'],'资源消耗',self.subtask_value[id]['consumption'])
            id=id+1
        #print(self.subtask_value)
        print('己方集群态势信息：')
        for row in self.Data_manager.our_taishi:
            print(row)
        #print(self.Data_manager.our_taishi)
        print('对手集群态势信息: ')
        print(self.Data_manager.enemy_taishi)
        print('考虑的约束类型有：作战环境约束，敌方种类威胁，智能体资源约束')
        print('作战环境约束：')
        for place,area in self.Data_manager.map_with_agent.items():
            print('当前位置',place,'威胁程度为',len(area)+random.randint(0,5))
        print('敌方种类威胁：')
        for agent_type,agent_list in self.Data_manager.agent_type_with_agent.items():
            print('敌方种类：' ,agent_type,' 敌方数量:',len(agent_list),'危险程度',random.randint(1,4)/3*len(agent_list))
        print('智能体资源约束：')
        for agent_type,resource in agent_resource.items():
            print('智能体种类',agent_type,'拥有资源数量为',resource)
        begin_time=time.time()
        self.optimize_method = optimize_method.Branch_And_Bound(self.Poset_product.final_poset, self.Poset_product.final_task_data_list,
                                             self.Data_manager.input_data)
        self.optimize_method.subtask_value = self.subtask_value
        self.optimize_method.prefer_type=self.prefer_tpye
        self.optimize_method.Begin_branch_search(self.alg_param, up_bound_method='greedy', low_bound_method='i+j', search_method='DFS')
        self.current_solution = self.optimize_method.best_solution
        self.task_time_table = self.optimize_method.task_time_table
        self.Data_manager.assess_solution(self.current_solution,self.subtask_value)
        swarm_list,new_swarm_list=self.return_swam_distribute()
        print(swarm_list)
        print('集群分布:')
        print('功能集群：')
        swam_id=1
        for agent_list in swarm_list.values():
            print('集群',swam_id,agent_list)
            swam_id=swam_id+1
        print('种类集群：')
        #功能集群
        for agent_list in new_swarm_list:
            print('集群', swam_id, agent_list)
            swam_id = swam_id + 1
        #种类集群
        #================================


        end_time=time.time()
        self.second_level_calculate_time=end_time-begin_time
        #这一步返回包括计算数据，
        print('--------------------------')
        print('完成任务分配层计算！')
        print('计算耗时为',self.second_level_calculate_time-1)
        print(os.getcwd())
        file = open('logger/common/time.txt', mode='a')
        file.write('任务分配层计算时间为：' + str(self.second_level_calculate_time-1) + ',\n')
        file.close()
        return self.current_solution, self.task_time_table



    def return_swam_distribute(self):
        agent_ID=0
        swam_list={}
        print(len(self.current_solution))
        print(len(list(self.Data_manager.agent_name_2_symbol.keys())))
        for agent in self.current_solution:
            for task in agent:
                if task[0][0] not in swam_list.keys():
                    swam_list[task[0][0]]=[]
                #print(agent_ID)
                #print(list(self.Data_manager.agent_name_2_symbol.keys()))
                #print(list(self.Data_manager.agent_name_2_symbol.keys())[agent_ID])
                swam_list[task[0][0]].append(list(self.Data_manager.agent_name_2_symbol.keys())[agent_ID])
                #print(self.Data_manager.agent_name_2_symbol)
            agent_ID=agent_ID+1
        #n=12-len(swam_list.keys())
        #n1=len(swam_list.keys())
        #change the swam into name
        new_swam_list=[]
        for keys,agent_list in self.Data_manager.agent_type_with_agent.items():
            #agent_ID=0
            #agent_name_list=[]
            #for agent_id in agent_list:
            #    agent_name_list.append(list(self.Data_manager.agent_name_2_symbol.keys())[agent_id])

            new_swam_list.append(agent_list)
        return swam_list,new_swam_list

    def get_off_line_gantt_graph(self):
        gantt_data=self.Poset_product.gantt_graph_generate(self.current_solution,self.poset)
        return gantt_data


    def online_gantt_graph(self,message_data):
        #获取最终的执行情况的甘特图
        for data_step in  message_data:
            self.Poset_product.gantt_online_menegar(data_step, self.poset)
        return  self.Poset_product.gantt_data_dic

