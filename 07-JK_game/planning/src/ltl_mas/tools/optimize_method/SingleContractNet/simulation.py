#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ContractNet_pkg.Agent import Agent
from ContractNet_pkg.Task import Task
import math


class Simulation:
    # 初始化仿真对象
    def __init__(self, config):
        self.config = config

        # 定义任务列表
        self.total_tasks = []
        for t in config["tasks"]:
            self.total_tasks.append(Task(t["id"], t["ExecuteCost"], t["Req_AgentNum"], t["Req_AgentType"], t["target_No"]))

        # 定义agent列表
        self.agents = []
        for a in config["agents"]:
            self.agents.append(Agent(a["id"], a["pose"], a["type"], config["agent_task_capacity"]))

    
    # 合同网协商
    def ContratNet_BID(self):
        for task in self.total_tasks:
            BID_agents_dic = {}
            # A、确定参与投标的agent
            for agent in self.agents:
                agent.states[task.id] = "WAITING"
                # 判断：如果agent任务容量已满，则退出投标
                if len(agent.contracted_list) == agent.task_capacity:
                    agent.states[task.id] == "DEF_REJ"
                    agent.currentBid[task.id] = -(math.inf)
                    continue
                # 符合条件的待投标agent，进入投标环节
                else:
                    # 每个agent进行一次判断，更改投标状态
                    agent.determine_states(task)
                    # 如果该agent的状态是“预投标（PRE_BID）”，则将其加入投标列表BID_agents
                    if agent.states[task.id] == "PRE_BID": 
                        # 计算投标值，并将agent的id与投标值以字典元素的形式加入字典BID_agents_dic
                        BID_agents_dic[str(agent.id)] = agent.calculate_Bid(task)
            
            # B、按BID_agents中每个agent的投标值从大到小对字典进行排序(键名为agent的id，键值为投标值)
            BID_agents_dic_sorted = dict(sorted(BID_agents_dic.items(), key=lambda x: x[1], reverse=True))
  
            # C、为任务分配agent，直到满足任务的agent数量要求
            for key in BID_agents_dic_sorted :                       # key代表agent的投标值
                if len(task.contractor) < task.Req_AgentNum :
                    task.contractor.append(int(key))
                else :
                    break
                            
            # D、修改被选中的agent的最终投标状态
            for agent in self.agents:
                if agent.id in task.contractor:                       
                    agent.states[task.id] = "DEF_BID"                
                else:
                    agent.states[task.id] = "DEF_REJ"                
            # E、最后更新一次所有agent的状态，如果状态是DEF_BID，则确定为contractor
                agent.determine_states(task)


    # 最终总结
    def print_Final_summary(self):
        # 6、最终的任务分配情况
        print("----------------------------  Final summary  ----------------------------")
        print("Final tasks allocation:")

        # 各agent任务分配的情况
        for agent in self.agents:
            if agent.contracted_list == [] :
                continue
            else:
                print(" Agent ", agent.id, " is contracted with tasks: ", end="")
                for task in agent.contracted_list:
                    print(task.id, " ", end="")
                print()
        print()
        print("------------------------------     end     -------------------------------")


    # 执行合同网算法
    def contractNet_algorithm(self):
        self.ContratNet_BID()
        # 展示最终结果
        self.print_Final_summary()


    # 获取任务分配结果作为返回值
    def return_solution(self):
        solution = []
        for agent in self.agents:
            contracted_tasks = []
            for task in agent.contracted_list:
                contracted_tasks.append(task.id)
            solution.append(contracted_tasks)
            
        return solution