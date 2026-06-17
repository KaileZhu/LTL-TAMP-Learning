# -*-coding:utf-8-*-
import time
import zmq
import sys
import json
sys.path.append('C:/Users/MSI1/Documents/LTL/Collaborative_project')
sys.path.append('C:/Users/MSI1/Documents/LTL/Collaborative_project/test')
sys.path.append('C:/Users/MSI1/Documents/LTL/Collaborative_project/src')
from main_function2 import determine_task_assignment
from data.input_data.first_data import software_input_data


message=software_input_data
message_from_beihang={}
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:9999")
initialize=0
print('label1')
while True:
    #  Wait for next request from client
    print('label2')
    #message = socket.recv_string()
    #print('label3',message)
    #c2 = eval(message)
    #print(type(c2))
    if initialize:
        command=planner.online_manager(message,message_from_beihang)
        print('label4')
    else:
        print('label5')
        planner=determine_task_assignment()
        command = planner.online_manager(message,message_from_beihang)
        initialize=1
    print(command)
    # print("Received request: %s" % message)

    # Do some 'work'
    time.sleep(1)

    #  Send reply back to client
    command = dict()
    command = {"moveactions":[{"agentname":"Red.RedForce_RedCommander#0.RedSUAV#0","longitude":78.32120839849014,"latitude":30.48194871300596,"altitude":1}]}
    command_json = json.dumps(command)
    socket.send_string(command_json)