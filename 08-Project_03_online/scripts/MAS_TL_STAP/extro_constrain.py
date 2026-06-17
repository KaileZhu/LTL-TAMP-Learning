class The_extro_condition:
    def __init__(self,agent_pose,finished_time_list,unfinished_task_list,begin_time,task_dic,task_execute_time,broken_agent_list):
        self.agent_pose=agent_pose
        # describe when the agent can to execute next action
        self.finished_time_list=finished_time_list
        self.unfinished_task_list=unfinished_task_list
        self.begin_time=begin_time
        self.task_dic=task_dic
        self.task_execute_time=task_execute_time
        self.broken_agent_list=broken_agent_list