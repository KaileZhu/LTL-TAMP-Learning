from flask import Flask, render_template, session, request
import json
import numpy as np
import time
from planning.src.http import dec_data
from planning.src.central_master import central_master
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
ServerAPP = Flask(__name__)
Central_master=central_master()
#Central_master.get_initial_data()


red = ['Red.RedForce_RedCommander#0', 'Red.RedForce_RedCommander#0_RedCommanderMiddle#0',
                'Red.RedForce_RedCommander#0_RedAirArtillery#0', 'Red.RedForce_RedCommander#0_RedAirArtillery#1',
                   'Red.RedForce_RedCommander#0_RedAirArtillery#2', 'Red.RedForce_RedCommander#0_RedAirArtillery#3',
                   'Red.RedForce_RedCommander#0_RedRocketGun#0', 'Red.RedForce_RedCommander#0_RedRocketGun#1',
                'Red.RedForce_RedCommander#0_RedRocketGun#2', 'Red.RedForce_RedCommander#0_RedRocketGun#3',
                'Red.RedForce_RedCommander#0_RedRocketGun#4', 'Red.RedForce_RedCommander#0_RedSAUGV#0', 'Red.RedForce_RedCommander#0_RedSAUGV#1',
            'Red.RedForce_RedCommander#0_RedSAUGV#2', 'Red.RedForce_RedCommander#0_RedSAUGV#3',
            'Red.RedForce_RedCommander#0_RedRSUAVehicle#0', 'Red.RedForce_RedCommander#0_RedRSUAVehicle#1',
                  'Red.RedForce_RedCommander#0_RedRSUAVehicle#2', 'Red.RedForce_RedCommander#0_RedRSUAVehicle#0.RedRSUAV#0',
            'Red.RedForce_RedCommander#0_RedRSUAVehicle#1.RedRSUAV#0','Red.RedForce_RedCommander#0_RedRSUAVehicle#2.RedRSUAV#0',
            'Red.RedForce_RedCommander#0_RedFSUAVehicle#0', 'Red.RedForce_RedCommander#0_RedFSUAVehicle#1',
                  'Red.RedForce_RedCommander#0_RedFSUAVehicle#2', 'Red.RedForce_RedCommander#0_RedFSUAVehicle#0.RedFSUAV#0', 'Red.RedForce_RedCommander#0_RedFSUAVehicle#1.RedFSUAV#0',
            'Red.RedForce_RedCommander#0_RedFSUAVehicle#2.RedFSUAV#0', 'Red.RedForce_RedCommander#0_RedArCMUGV#0',
            'Red.RedForce_RedCommander#0_RedArCMUGV#1', 'Red.RedForce_RedCommander#0_RedInCMUGV#0', 'Red.RedForce_RedCommander#0_RedAJUGV#0',
              'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#0', 'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#1',
                'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#2', 'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#3',
                'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#4', 'Red.RedForce_RedCommander#0_RedArCMUGV#0.RedArCMissile#5',
                'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#0', 'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#1',
                'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#2', 'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#3',
                'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#4', 'Red.RedForce_RedCommander#0_RedArCMUGV#1.RedArCMissile#5',
                'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#0', 'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#1',
                'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#2', 'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#3',
                'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#4', 'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#5',
                'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#6', 'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#7',
                'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#8', 'Red.RedForce_RedCommander#0_RedInCMUGV#0.RedInCMissile#9']

blue= ['Blue.BlueForce_BlueCommander#0', 'Blue.BlueForce_BlueCommander#0_BlueUAVehicle#0',
                 'Blue.BlueForce_BlueCommander#0_BlueCommandMiddle#0', 'Blue.BlueForce_BlueCommander#0_BlueCommandMiddle#1',
                     'Blue.BlueForce_BlueCommander#0_BlueCommandMiddle#2', 'Blue.BlueForce_BlueCommander#0_BlueCommandMiddle#3',
                     'Blue.BlueForce_BlueCommander#0_BlueInfantry#0', 'Blue.BlueForce_BlueCommander#0_BlueInfantry#1',
                'Blue.BlueForce_BlueCommander#0_BlueInfantry#2', 'Blue.BlueForce_BlueCommander#0_BlueInfantry#3',
                'Blue.BlueForce_BlueCommander#0_BlueArtillery#0', 'Blue.BlueForce_BlueCommander#0_BlueArtillery#1',
                 'Blue.BlueForce_BlueCommander#0_BlueArtillery#2',
                 'Blue.BlueForce_BlueCommander#0_BlueArchibald#0', 'Blue.BlueForce_BlueCommander#0_BlueArchibald#1', 'Blue.BlueForce_BlueCommander#0_BlueADLanucher#0', 'Blue.BlueForce_BlueCommander#0_BlueADLanucher#1',
                  'Blue.BlueForce_BlueCommander#0_BlueADLanucher#2', 'Blue.BlueForce_BlueCommander#0_BlueCommNode#0',
                'Blue.BlueForce_BlueCommander#0_BlueRadar#0', 'Blue.BlueForce_BlueCommander#0_BlueRadar#1'
        ,'Blue.BlueForce_BlueCommander#0_BlueUAV#0']

final_location = [[], [], [], [], [], []]
final_flag = [0, 0, 0, 0, 0, 0]
detect_index = [18, 19, 20, 24, 25, 26]
al_task = []
reward_list = []

@ServerAPP.route('/', methods=['POST'])
def mainentry():
    data = request.json
    print(data)
    return data


@ServerAPP.route('/decision', methods=['POST'])
def getSituation():  # situation，次级接口，接受command数据
    command= request.json  # 读取command数据
    #command = json.dumps(situationDataDict)  # 将数据修改，这里实际上是最后一步，
    #这里读取输入的数据， 然后进行一个对command 的分析
    #function1
    print('这里是输入的参数',command)
    if 'calculate_content' in command.keys():
        #{'场景选择': '进攻场景', '算法选择': '两级合同网', '算法路径':
        # 'planning\\src\\ltl_mas\\tools\\Ct_N.py', '偏好选择': '执行速度优先', '战法选择': '占场扫描', '条例选择': ['禁止攻击']}
        input=command['calculate_content']

        print(input)
        background=input['场景选择']
        calculate_type=input['算法选择']
        path_calculate=input['算法路径']
        prefer_type=input['偏好选择']
        war_type=input['战法选择']
        stick=input['条例选择']
        begin_time=time.time()
        #初始化背景参数
        output=Central_master.pre_design_the_subtask_structure(background,calculate_type,path_calculate,prefer_type,war_type,stick)
        #输入算法，偏好，战法，条例
        Central_master.first_level_calculate_time=time.time()-begin_time
        print('output',output)
        print('--------------------------')
        print('完成中枢决策层计算！')
        print('中枢决策层计算时间为：',Central_master.first_level_calculate_time*100)
        return  json.dumps(output)

    if 'calculate_subtask' in command.keys():
        input = command['calculate_subtask']
        print('first_error',input)
        input,prefer=Central_master.change_goal_task_pair(input)
        print('input',input)
        output_data=Central_master.calculate_subtask_value(input,Central_master.task.stick,Central_master.task.war_type)
        f = open('subtask_data1.txt', 'w')#路径改到gui里面吧
        f.write(str(output_data))
        f.close()
        print('final',output_data)
        #理论上这部分是直接保存在 subtask_data.py文件里？
        #为啥这部分会自动刷新？？
        return json.dumps(output_data)

    if 'calculate_execute' in command.keys():
        input = command['calculate_execute']
        Central_master.alg_param=int(input['算法参数'])
        print('input_task_type',input)
        Central_master.determine_step()
        f = open(input['战法选择']+'.txt', 'w')
        f.write(str(Central_master.current_solution))
        f.close()
        #现在这里的问题是，运行之后 应该到不了1了
        #但是决策的过程已经完成了
        return json.dumps(1)

    if 'ZF_choose_function' in command.keys():
        #输出智能体信息
        Central_master.Data_manager.agent_data
        #print(Data_manager.agent_data)
        return json.dumps(Central_master.Data_manager.agent_data)
    #function2
    if 'ZF_combination' in command.keys():
        #这部分战法属于预先完成的内容，所以可以直接查表
        print('dsaffad')
        return json.dumps(dec_data.zanfa_data[command['ZF_combination']])
    #function3
    if 'ZF_detail' in command.keys():
        #这里需要输入战法的内容，进行对于的计算，最终返回子任务序列，
        print('dsaffad')
        Central_master.get_input_data(command['ZF_detail'])
        subtask_list=Central_master.out_put_subtask_data()
        #Centrol_master.get_input_data(command['ZF_detail'])
        #return json.dumps(Centrol_master.poset['action_map'])
        #这里返回的是子任务，以及子任务对于的4个维度的参数

        return json.dumps(subtask_list)
    if 'ZF_calculate' in command.keys():
        time_limit=15
        Central_master.determine_step(time_limit)
        f = open('全面进攻.txt', 'w')
        f.write(str(Central_master.current_solution))
        f.close()

        return
    #function4-5


    if 'Gantt_graph' in command.keys():
        if 'first' == command['Gantt_graph']:
            gantt_data=Central_master.get_off_line_gantt_graph()

            return json.dumps(gantt_data)
        if 'final' == command['Gantt_graph']:
            #这里需要获取来着北航的message_data
            message_data = []
            with open('subtask.txt', 'r') as f:
                content = f.readlines()
                for idx, cur in enumerate(content):
                    if idx == len(content) - 1:
                        message_data.append(eval(cur))
                    else:
                        message_data.append(eval(cur)[0])
            gantt_data_dic=Central_master.online_gantt_graph(message_data)
            return json.dumps(gantt_data_dic)


@ServerAPP.route('/situation', methods=['POST'])
def getSituation_rl():
    situationDataDict = request.json
    # print(situationDataDict)
    global task, task_context, task_now, task_num, task_num_now, task_num_list0

    if situationDataDict['step'] == 30 or situationDataDict['step'] == 70:
        # 得到已完成任务列表
        remain_task_list = []
        for i in range(53):
            for j in range(len(task[i])):
                if j < task_num_now[i]:
                    continue
                if task[i][j] not in remain_task_list and task[i][j] !=100 and task[i][j] != -1:
                    remain_task_list.append(task[i][j])
        finish_task_list = []
        for task_n in task_num_list0:
            if task_n in remain_task_list:
                continue
            finish_task_list.append(task_n)

        # 重规划
        print(finish_task_list)
        new_task_list = Central_master.online_replanning(situationDataDict, finish_task_list, is_beihang=True)
        task, task_context, task_now, task_num, task_num_now = get_txt_from_replan(new_task_list)
        print('--重规划已完成--')


    # 任务预处理
    index = 0
    life = [1 for _ in range(53)]
    for id, entities in situationDataDict['redSituation'].items():
        for entity in entities:
            if entity['life'] <= 0:
                life[index] = 0
            index += 1

    for i in range(53):
        if life[i] == 0:
            task_now[i] = -1

    for i in range(53):
        if task_now[i] == 100 or task_now[i] == -1:
            pass
        else:
            if is_task_done(situationDataDict, task_context[i][task_num_now[i]], red[i]) or task_now[i] in al_task:
                task_num_now[i] += 1
                al_task.append(task_now[i])
                if task_num_now[i] == task_num[i]:
                    task_now[i] = 100
                else:
                    task_now[i] = task[i][task_num_now[i]]

    task_now_constrain = get_task_constrain(task_now)
    task_set = list(set(task_now_constrain))
    if 100 in task_set:
        task_set.remove(100)
    if -1 in task_set:
        task_set.remove(-1)

    logger(situationDataDict, task_set, reward_list)

    command = decision_process(situationDataDict, task_now_constrain)
    command = blue_action(situationDataDict, command)

    for id, entities in situationDataDict['redSituation'].items():
        for entity in entities:
            if entity['name'] in red[2:6]:
                action = {}
                action['agentname'] = entity['name']
                action['targetname'] = ['Blue.BlueForce_BlueCommander#0_BlueUAV#0']
                command['fireactions'].append(action)

    return command


@ServerAPP.route('/gaming', methods=['POST'])
def getSituation2():  # situation，次级接口，接受command数据
    command = request.json  # 读取command数据
    #command = json.dumps(situationDataDict)  # 将数据修改，
    #这里读取输入的数据， 然后进行一个调用，然后返回
    # function1
    if 'red_war_infor' ==command:
        dict_list = []
        with open('red_damage.txt', 'r') as f:
            content = f.readlines()
            for idx, cur in enumerate(content):
                if idx == len(content) - 1:
                    dict_list.append(eval(cur))
                else:
                    dict_list.append(eval(cur)[0])
        return json.dumps(dict_list)

    if 'blue_war_infor' == command:
        dict_list = []
        with open('blue_damage.txt', 'r') as f:
            content = f.readlines()
            for idx, cur in enumerate(content):
                if idx == len(content) - 1:
                    dict_list.append(eval(cur))
                else:
                    dict_list.append(eval(cur)[0])
        return json.dumps(dict_list)

    if 'red_search_infor' == command:
        dict_list = []
        with open('detect', 'r') as f:
            content = f.readlines()
            for idx, cur in enumerate(content):
                if idx == len(content) - 1:
                    dict_list.append(eval(cur))
                else:
                    dict_list.append(eval(cur)[0])
        return json.dumps(dict_list)

    if 'red_blue_ability' == command:
        dict_list = []
        with open('strength.txt', 'r') as f:
            content = f.readlines()
            for idx, cur in enumerate(content):
                if idx == len(content) - 1:
                    dict_list.append(eval(cur))
                else:
                    dict_list.append(eval(cur)[0])
        return json.dumps(dict_list)

    if 'red_blue_value'== command:
        dict_list = []
        with open('value.txt', 'r') as f:
            content = f.readlines()
            for idx, cur in enumerate(content):
                if idx == len(content) - 1:
                    dict_list.append(eval(cur))
                else:
                    dict_list.append(eval(cur)[0])
        return json.dumps(dict_list)

    if 'red_executing_subtask'== command:
        dict_list = []
        with open('subtask.txt', 'r') as f:
            content = f.readlines()
            for idx, cur in enumerate(content):
                if idx == len(content) - 1:
                    dict_list.append(eval(cur))
                else:
                    dict_list.append(eval(cur)[0])
        return json.dumps(dict_list)

    if 'red_reward' == command:
        dict_list = []
        with open('reward.txt', 'r') as f:
            content = f.readlines()
            for idx, cur in enumerate(content):
                if idx == len(content) - 1:
                    dict_list.append(eval(cur))
                else:
                    dict_list.append(eval(cur)[0])
        return json.dumps(dict_list)

def decision_process(situation, task_now):
    command = net(situation, task_now, task_context, task_num_now)
    return command


if __name__ == '__main__':
    ServerAPP.run(host='127.0.0.1', port=9999,debug=True )