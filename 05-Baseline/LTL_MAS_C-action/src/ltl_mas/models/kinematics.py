import numpy as np

class monocycle_model(object):
    def __init__(self):
        i=1

class quadrotor_model(object):
    def __init__(self,initial_pos=[0.0,0.0,0.0,0.0],initial_velocity=[0.0,0.0,0.0,0.0],time_step=0.05,V_max=10,A_max=10,Omega_max=1,fai_max=3,controller_type='PID',FPS=15):
        '''
        因为4旋翼无人机在不考虑滚转，俯仰的情况下，是完全解耦的，四输入四输出，可以完全解耦
        这里不考虑动力学，建立在运动学上的模型将会很简单
        x1=dxdt+x0
        y1=dydt+y0
        z1=dzdt+z0
        theta1=dtehtadt+theta0
        '''

        self.initial_pos=initial_pos# x y z yaw
        self.initial_velocity=initial_velocity
        self.time_step=time_step
        self.pos=self.initial_pos
        self.velocity=self.initial_velocity
        self.V_max=V_max
        self.A_max=A_max
        self.Omega_max=Omega_max
        self.fai_max=fai_max
        self.controller_type=controller_type
        self.global_time=0
        self.recorder_time=0
        self.trajectory=[]
        self.defined_the_FPS_of_trajectory(FPS)

    def defined_the_FPS_of_trajectory(self,FPS=15):
        self.FPS=FPS

    def discrete_kinematics(self,control_input):
        self.pos=self.pos+np.multiply(self.velocity,self.time_step)
        self.velocity=control_input*self.time_step+self.velocity
        if np.linalg.norm(self.velocity)>self.V_max:#设置速度上限
            self.velocity=self.velocity/np.linalg.norm(self.velocity)*self.V_max
        self.global_time = self.global_time + self.time_step

    def PID_controller_initial(self,kP=10,kI=0.1,kD=0.02):
        self.kP=kP
        self.kI=kI
        self.kD=kD
        self.I=0
        self.I_limit=10

    def PID_controller(self,yaw=0):#拼多多版本
        #这里都用np.array
        P=self.Goal-self.pos
        self.I=self.I+P*self.time_step
        if np.linalg.norm(self.I)>self.I_limit:
            self.I=self.I/np.linalg.norm(self.I)*self.I_limit#设置积分饱和
        D=self.velocity
        Pos_control=P*self.kP+self.kI*self.I+np.multiply(self.kD,D)
        return Pos_control

    def Check_arrival(self,error=0.2):
        e=self.pos-self.Goal
        Er=np.abs(e[0])+np.abs(e[1])+np.abs(e[2])+5*np.abs(e[3])
        if Er<error:
            return True
        return False

    def message_recorder(self):#信息记录
        if self.recorder_time<= self.global_time:
            self.trajectory.append((self.pos,self.global_time))
            self.recorder_time=self.recorder_time+1/self.FPS

    #def message_publisher(self):#未来信息交流的接口

    def goto(self,Goal,yaw=0):
        self.Goal=Goal
        self.Goal=np.append(self.Goal,yaw)
        if self.controller_type=='PID':
            self.PID_controller_initial()  # 这里设置是为了避免过去积分I的影响
            while not self.Check_arrival():
                control_input=self.PID_controller(yaw)
                self.discrete_kinematics(control_input)
                self.message_recorder()




if __name__=='__main__':
    a=quadrotor_model()
    a.goto(np.array([1,2,3]),0)