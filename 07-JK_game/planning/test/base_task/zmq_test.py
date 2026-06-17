# -*-coding:utf-8-*-
import time
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:9999")

while True:
    #  Wait for next request from client

    message = socket.recv_string()
    print(message)
    c2 = eval(message)
    print(type(c2))

    # print("Received request: %s" % message)

    # Do some 'work'
    # time.sleep(5)

    #  Send reply back to client
    command = dict()
    command = {"moveactions": [{"agentname": "Red.RedForce_RedCommander#0.RedSUAV#0", "longitude": 78.32120839849014,
                                "latitude": 30.48194871300596, "altitude": 1}]}
    command_json = json.dumps(command)
    socket.send_string(command_json)
    print(command)