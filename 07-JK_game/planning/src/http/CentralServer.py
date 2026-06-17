from flask import Flask, request
import json
import dec_data,gam_data

ServerAPP = Flask(__name__)
#在客户端中，通过端口激活对应的程序，激活后，运行该程序的代码，然后代码会反会一系列的值，最终，客户端能获得到对应的数据。
@ServerAPP.route('/', methods=['POST'])
def mainentry():  # 主接口
    data = request.json#读取从端口发来的信息。
    data['moveactions']=3# 读取请求数据
    #json.dumps() 将python数据类型列表进行json格式的编码,理论上这一步应该是必须的
    print(json.dumps(data))
    return data  # 返回请求数据

@ServerAPP.route('/decision', methods=['POST'])
def getSituation():  # situation，次级接口，接受command数据
    command= request.json  # 读取command数据
    #command = json.dumps(situationDataDict)  # 将数据修改，这里实际上是最后一步，
    #这里读取输入的数据， 然后进行一个对command 的分析
    #function1
    print(command)
    if 'ZF_choose_function' in command.keys():
        return json.dumps(dec_data.zanfa_data_list)
    #function2
    if 'ZF_combination' in command.keys():
        return json.dumps(dec_data.zanfa_data[command['ZF_combination']])
    #function3
    if 'ZF_detail' in command.keys():
        return json.dumps(dec_data.subtask_list)
    #function4-5
    if 'Gantt_graph' in command.keys():
        if 'first' == command['Gantt_graph']:

            return json.dumps(dec_data.first_gantt_garph)
        if 'final' == command['Gantt_graph']:
            return json.dumps(dec_data.final_gantt_graph)


@ServerAPP.route('/gaming', methods=['POST'])
def getSituation2():  # situation，次级接口，接受command数据
    command = request.json  # 读取command数据
    #command = json.dumps(situationDataDict)  # 将数据修改，
    #这里读取输入的数据， 然后进行一个调用，然后返回
    # function1
    if 'red_war_infor' ==command:
        return json.dumps(gam_data.red_war_infor)

    if 'blue_war_infor' == command:
        return json.dumps(gam_data.blue_war_infor)

    if 'red_search_infor' == command:
        return json.dumps(gam_data.red_search_infor)

    if 'red_blue_ability' == command:
        return json.dumps(gam_data.red_blue_ability)

    if 'red_blue_value'== command:
        return json.dumps(gam_data.red_blue_value)

    if 'red_executing_subtask'== command:
        return json.dumps(gam_data.red_executing_subtask)

    if 'red_reward' == command:
        return json.dumps(gam_data.red_reward)


if __name__ == '__main__':
    ServerAPP.run(host='localhost', port=9999)

