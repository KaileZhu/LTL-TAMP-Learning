
import numpy as np
import ContractNet_pkg.experiments as ep


# 子网中执行任务的agent的类
class Agent:
    
    def __init__(self, id, pose, type, task_capacity):
        # 基础信息
        self.id = id
        self.pos = pose
                            
        self.type = type                        # agent的类型
        for key in ep.agent_type:
            if self.type == key:
                self.serve = ep.agent_type[key]['serve']       # agent可执行的任务类型
                self.vel = ep.agent_type[key]['velocity']

        # 任务相关
        self.task_capacity = task_capacity      # agent的任务容量
        self.contracted_list = []               # agent最终中标的任务列表
        
        # 投标状态与投标值
        self.states = {}                        # 投标状态与投标值都是字典类型变量，元素形式为：任务id：“state” 或 任务id：Bid
        self.currentBid = {}                    # agent对任务的当前投标值
    

    # 将agent对某任务的投标状态还原为“等待（WAITING）”
    def clean_states(self, task):
        self.states[task.id] = "WAITING"


    # 计算两点距离
    def calculate_points_distance(self, p1, p2):
        vec_p = np.array([p2[0]-p1[0], p2[1]-p1[1]])
        distance = np.linalg.norm(vec_p)
        return distance


    # 根据agent对任务的当前投标状态确定下一步的投标状态
    def determine_states(self, task):                                    
        if self.states[task.id] == "WAITING":
            self.states[task.id] = "PRE_BID"
        elif self.states[task.id] == "DEF_BID":
            task.contractor.append(self.id)
            self.states[task.id] = "CONTRACTOR"
            self.contracted_list.append(task)


    # 主体：计算投标值
    def calculate_Bid(self, task):
        # 1、计算agent与该新增任务点之间的距离dis
        if len(self.contracted_list) != 0:
            # 若此前contracted_list中已有若干待执行的任务，则agent到该新增任务点的距离是agent经过所有任务点时的距离
            dis = self.calculate_points_distance(self.pos, self.contracted_list[0].target)
            for i in range(len(self.contracted_list) - 1):
                dis += self.calculate_points_distance(self.contracted_list[i].target, self.contracted_list[i+1].target)
            dis += self.calculate_points_distance(self.contracted_list[-1].target, task.target)    
        else:
            # 若此前contracted_list中没有待执行的任务，则直接计算agent到该任务点的距离
            dis = self.calculate_points_distance(self.pos, task.target)
        
        # 2、计算执行此任务的代价cost
        k1 = 0.6
        k2 = 1.0 - k1
        cost = k1*task.ExecuteCost + k2*(dis/self.vel)

        # 3、对此任务的投标值
        self.currentBid[task.id] = - cost

        return self.currentBid[task.id]