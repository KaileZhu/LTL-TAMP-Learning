# -*-coding:utf-8-*-
import time
import zmq
import sys
import json
sys.path.append('C:/Users/MACDLab/Documents/GitHub/Collaborative_project/src')
sys.path.append('C:/Users/MACDLab/Documents/GitHub/Collaborative_project')
sys.path.append('C:/Users/MACDLab/Documents/GitHub/Collaborative_project/base_task')
from main_function import determine_task_assignment
from data.input_data.first_data import software_input_data

import time
import zmq
import sys
import json
from main_function2 import determine_task_assignment
from data.input_data.first_data import software_input_data


message=software_input_data
message_from_beihang={}
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:9999")
initialize=0
while True:
    if initialize:
        #这里自己设定时间步长，单位是分钟
        command=planner.online_manager(message,message_from_beihang,time_step)
    else:
        planner=determine_task_assignment()
        command = planner.online_manager(message,message_from_beihang,time_step)
        initialize=1
    print(command)
    time.sleep(10)