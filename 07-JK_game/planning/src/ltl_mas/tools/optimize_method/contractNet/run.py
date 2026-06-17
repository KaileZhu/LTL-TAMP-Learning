#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Agent import Agent
from Task import Task
from Subnet import Subnet
from Groupnet import Groupnet
import experiments as ep
import time


class Simulation:
    # 初始化仿真对象
    def __init__(self, config):
        self.config = config
        self.subnet_num = config["subnet_num"]

        # 定义任务列表
        self.total_tasks = []
        for t in config["tasks"]:
            self.total_tasks.append(Task(t["id"], t["timeConsume"], t["target"], t["value"], t["threat"], t["defense"], t["priority"]))

        # 定义子网列表subnets
        self.subnets = []
        subnet_task_capacity = config["subnet_task_capacity"]
        agent_task_capacity = config["agent_task_capacity"]
        for id in range(1, self.subnet_num+1):
            name_string = "subnet_" + str(id) + "_agents"
            subnet_agents = []
            for a in config[name_string]:
                subnet_agents.append(Agent(a["id"], a["subnet_id"], a["speed"], a["initPos"], a["value"], a["attack"], a["defense"], agent_task_capacity, a["pref"]))
            # 构建一个子网
            self.subnets.append(Subnet(id, subnet_agents, subnet_task_capacity))
    
        # 定义子网集群groupnet
        self.groupnet = Groupnet(self.subnets, self.total_tasks)


    # 执行两层合同网算法
    def contractNet_algorithm(self):
        print('开始合同网两级协商算法')
        print('说明1: 本算法支持多个和多种对手目标')
        print('说明2: 本算法基于异构集群资源，可实现多约束条件(包括但不限于作战环境、威胁等）和多偏好优化（包括但不限于最短时间、最高效费比、最高成功率等）\n')
        t_start = time.time()
        print("第一阶段开始\n")
        # 进行第一层协商
        self.groupnet.first_layer_BID()
        print("———————— 合同网第一层任务分配   完成\n")

        # 进行第二层协商               这里最好用多线程方法同步进行
        for i in range(self.subnet_num):
            print("subnet ", self.subnets[i].id, " is running")
            self.subnets[i].second_layer_BID()
        print("———————— 合同网第二层任务分配   完成\n")
        print("第一阶段结束\n")

        # 展示结果1
        self.print_summary_1()
        
        # 进行重分配
        print("第二阶段开始\n")
        self.groupnet.Reallocation()
        print("———————— 任务重分配   完成\n")
        self.print_Phase_2_Reallocation_summary()

        # 进行任务交换
        self.groupnet.Exchange()
        print("\n———————— 任务交换   完成\n")
        self.print_Phase_2_Exchange_summary()
        print("\n第二阶段结束\n\n")

        t_end = time.time()
        t = t_end - t_start
        # 算法结束，输出耗时
        print('合同网两级协商算法运行完毕\n')
        print('算法运行耗时：%s seconds'%(t))
        # 展示最终结果
        self.print_Final_summary()


    # 算法结果展示：正常两层合同网协商之后的结果
    def print_summary_1(self):
        print("----------------------------   第一阶段总结   ----------------------------")

        # 1、子网接收任务的情况
        print("1、各子网接收任务情况:")
        for subnet in self.subnets:
            print("子网 ", subnet.id, " 分配到了任务: ", end="")
            for task in subnet.subnet_tasks:
                print(task.id, " ", end="")
            print()
        print("-----------------------------------------------------------------------------")

        # 2、各子网的agent任务分配的情况
        print("2、各子网内agent任务分配情况:")
        for subnet in self.subnets:
            for agent in subnet.subnet_agents:
                print("子网 ", subnet.id, " Agent ", agent.id, " 分配到了任务: ", end="")
                for task in agent.contracted_list:
                    print(task.id, " ", end="")
                print()
            print()
        print("-----------------------------------------------------------------------------")
        
        # 3、未分配的任务的情况
        print("3、未分配的任务:")
        realloc_tasks = []
        for task in self.total_tasks:
            if task.contractor == None:
                realloc_tasks.append(task)
                print("Task ", task.id)
        print("-----------------------------------------------------------------------------\n\n")

        print('由于分配存在不合理之处，开始第二阶段层间反馈\n')



    # 任务重分配后的结果
    def print_Phase_2_Reallocation_summary(self):
        print("----------------------------   第二阶段：重分配   ----------------------------")

        # 4、任务重分配的情况
        print("4、任务重分配情况:")
        for task_1 in self.groupnet.realloc_tasks:
            for task in self.groupnet.total_tasks:
                if task.id == task_1.id:
                    print("此前未分配的任务 ", task.id, " 现在被分配给了: 子网 ", task.contracted_subnet, " agent ", task.contractor)
        print("-------------------------------------------------------------------------------------------")



    # 任务交换后的总结
    def print_Phase_2_Exchange_summary(self):
        print("----------------------------   第二阶段：任务交换   ----------------------------")

        # 5、任务交换的情况
        print("5、任务交换情况:")
        for i in range(len(self.groupnet.NegativeBid_tasks)):
            task_1 = self.groupnet.NegativeBid_tasks[i]
            task_2 = self.groupnet.best_Exchange_tasks[i]
            
            if isinstance(task_2, Task):
                # 如果task_2是Task类的对象，说明是两个任务交换
                print("子网 ", task_1.contracted_subnet, " agent ", task_1.contractor, " task ", task_1.id, " 与 ", end="")
                print("子网 ", task_2.contracted_subnet, " agent ", task_2.contractor, " task ", task_2.id, " 进行交换 ")
                print("   交换后的结果为：")
                print("      ---->  子网 ", task_1.contracted_subnet, " agent ", task_1.contractor, " task ", task_2.id)
                print("      ---->  子网 ", task_2.contracted_subnet, " agent ", task_2.contractor, " task ", task_1.id, "\n")
            else:
                # 如果task_2不是Task类的对象，而是某个agent，说明是任务转移
                print("子网 ", task_1.contracted_subnet, " agent ", task_1.contractor, " task ", task_1.id, "被重新分配给了 ", end="")
                print("子网 ", task_2.subnet_id, " agent ", task_2.id)
                print("    重新分配后的结果为")
                print("      ---->  子网 ", task_1.contracted_subnet, " agent ", task_1.contractor, " task None")
                print("      ---->  子网 ", task_2.subnet_id, " agent ", task_2.id, " task ", task_1.id, "\n")

        print("--------------------------------------------------------------------------------------")
        

    # 最终总结
    def print_Final_summary(self):
        # 6、最终的任务分配情况
        print("\n\n----------------------------  最终任务分配结果   ----------------------------")
        print("A、各子网分配到的任务:")
        # 子网接收任务的情况
        for subnet in self.subnets:
            print("子网 ", subnet.id, " 分配到了任务: ", end="")
            for task in subnet.subnet_tasks:
                print(task.id, " ", end="")
            print()
        print("--------------------------------------------------------------------------")

        # 各子网的agent任务分配的情况
        print("B、子网中各agent分配到的任务:")
        for subnet in self.subnets:
            for agent in subnet.subnet_agents:
                print("子网 ", subnet.id, " Agent ", agent.id, " 分配到了任务: ", end="")
                for task in agent.contracted_list:
                    print(task.id, " ", end="")
                print()
            print()
        print("--------------------------------------------------------------------------")



# 主函数
if __name__ == '__main__':

    # 定义仿真案例，进行合同网算法仿真
    # sim = Simulation(ep.case_1)
    sim = Simulation(ep.case_2)
    sim.contractNet_algorithm()