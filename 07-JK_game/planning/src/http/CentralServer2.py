from flask import Flask, request
import json
import dec_data,gam_data
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
from src.central_master import central_master

#这里大致是服务器的主程序，接口访问后
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
        #输出智能体信息
        Centrol_master.Data_manager.agent_data
        #print(Data_manager.agent_data)
        return json.dumps(Centrol_master.Data_manager.agent_data)
    #function2
    if 'ZF_combination' in command.keys():
        #这部分战法属于预先完成的内容，所以可以直接查表
        return json.dumps(dec_data.zanfa_data[command['ZF_combination']])
    #function3
    if 'ZF_detail' in command.keys():
        Centrol_master.get_input_data(command['ZF_detail'])
        return json.dumps(Centrol_master.poset['action_map'])
    #function4-5
    if 'Gantt_graph' in command.keys():
        if 'first' == command['Gantt_graph']:
            gantt_data=Centrol_master.get_off_line_gantt_graph()

            return json.dumps(gantt_data)
        if 'final' == command['Gantt_graph']:
            #这里需要获取来着北航的message_data

            gantt_data_dic=Centrol_master.online_gantt_graph(message_data)
            return json.dumps(gantt_data_dic)


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
    #设定初始化程序都在这里调用，然后通过之上的程序进行返回？
    #设计原则，尽量减少交互次数，数据整体打包，然后整体的分解，这样子更为合理
    #对应的逻辑上可以更为困难，
    Data_manager = Data_pretreat()
    Data_manager.manage_software_data(software_input_data)
    print('run to here')
    #或者
    Centrol_master=central_master()
    ServerAPP.run(host='localhost', port=9999)
    # 这个程序是一直run的，无法运行后面的程序



