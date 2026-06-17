
import ContractNet_pkg.experiments as ep

class Task:
    
    def __init__(self, id, ExecuteCost, Req_AgentNum, Req_AgentType, target_No):
        
        # 基础信息
        self.id = id
        self.ExecuteCost = ExecuteCost
        self.Req_AgentNum = Req_AgentNum
        self.Req_AgentType = Req_AgentType
        self.target_No = target_No
        for key in ep.task_target_position:     # 使用key遍历字典，获取字典的每一个键名
            if target_No == key:
                self.target = ep.task_target_position[key]      # 索引字典获取key对应的键值，即任务目标位置


        # 投标相关
        self.contractor = []                    # 承接该任务的agent
    
        