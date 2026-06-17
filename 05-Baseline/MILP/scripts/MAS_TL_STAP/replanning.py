

class Replanning:
    def __init__(self, assignment, task, scene):
        self.assignment = assignment
        self.task = task
        self.scene = scene


    def task_update(self, ):
        # 根据当前执行情况，更新Task的状态
        task = self.task
        assignment = self.assignment

        # 检测self.assignment中是否有触发式任务，若有则更新task
        for agent in assignment:
            pass


        return task


    def scene_update(self, ):
        # 根据当前执行情况，更新scene中的Agent的状态(主要是位置)
        for agent in self.scene.agent_data:
            agent['reg'] = "???"  # 赋予智能体执行完任务后的位置
        return self.scene


    def finish(self, ):
        # 判断任务是否执行完成，若完成则返回True
        is_finish = True
        return is_finish