import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from visual_env.crazyswarm.scripts.pycrazyswarm import *
'''
目前已经完成的功能：
    啥也没有 嘿嘿
目前想完成的功能：
1 对网格世界进行画图
2 对最终路径进行绘图
3 
'''
class Grid_world_plotter():#不继承MotionFts的属性 而是作为数据直接 在使用上可以直接调用 但是代价是耗内存？
    def __init__(self,MotionFts):#初始化函数 输入状态，标签，区域类型（这个好像不重要
        self.MotionFts=MotionFts#简简单单来一个初始化

    def Motionfit_Area_plotter(self,label='label',Dimensionality=2,cmap=None,node_color='blue',node_size=2000,plotshow=1):# 画出初始区域的图像 默认维度是2维的
        '''
        设想输入区域信息，
        画图思路
        1 确定节点的坐标，画出点和边的图
        2 画出网格图形
        '''
        node_colors=[]
        position={}
        labels={}
        i=0
        for node in self.MotionFts.nodes:
            position[node]=node[0:Dimensionality]
            labels[node]=self.MotionFts.nodes[node][label]
            if node==list(self.MotionFts.graph['initial'])[0]:
                node_colors.append('red')
            else:
                node_colors.append(node_color)
        #print(node_colors)
        #node_colors[list(self.MotionFts.graph['initial'])[0]]='red'
        plt.figure()
        plt.ylabel('y')
        plt.xlabel('x')
        nx.draw(self.MotionFts,  pos=position ,node_color=node_colors, node_size=node_size,cmap=cmap)
        nx.draw_networkx_labels(self.MotionFts,pos=position,labels=labels)
        #第一步对节点画图完成
        #第二步画网格
        #这里网格暂时还没有合适的想法
        if plotshow==1:
            plt.show()

    def path_plotter(self,prefix,suffix):
        #self.Motionfit_Area_plotter(node_size=800,plotshow=0)
        i=1
        for nodes in prefix:
            x=[]
            y=[]
            for node in nodes[0]:
                x.append(node[0][0]+i/10)
                y.append(node[0][1]+i/10)
                if node[1]=='c1':
                    plt.scatter(node[0][0]+i/10,node[0][1]+i/10)
            plt.plot(x,y)
            i+1
        plt.show()
        #self.Motionfit_Area_plotter(node_size=800,plotshow=0)
        i=1
        for nodes in suffix:
            x=[]
            y=[]
            for node in nodes[0]:
                x.append(node[0][0]+i/10)
                y.append(node[0][1]+i/10)
                if node[1]=='c1':
                    plt.scatter(node[0][0]+i/10,node[0][1]+i/10)
            plt.plot(x,y)
            i+1
        plt.show()

class Agent_plotter():
    '''
    1 发布命令
    2 检查位置
    3 生成控制律
    4 根据截至条件，返回时间
    5 输出轨迹
    6 生成动画
    '''
    def __init__(self,LTL_planner,number,name='robot'):
        #处理任务形式
        self.run=LTL_planner.run
        robot_line_path={}
        robot_loop_path={}
        self.name=name
        self.state={}#设置一个简单的小车模型，这里放的是状态
        self.pre_state=LTL_planner
        for j in np.arange(number):
            robot_line_path[name+str(j+1)]=[]
            robot_loop_path[name + str(j + 1)] = []
            self.state[name+str(j+1)]=[0,0,0]#x,y,theta
        self.pre_plan=LTL_planner.run.pre_plan
        self.suf_plan=LTL_planner.run.suf_plan
        for nodes in LTL_planner.run.line:
            self.task_issue(nodes)
        for nodes in LTL_planner.run.loop:
            self.task_issue(nodes)

    #def task_issue(self,nodes)


    def motion_calculate(self,nodes):
        i=1
        for node in nodes:
            self.state[self.name+str(i)]

    def robot_motion_planner(self):
        x=(0,0)

    def Single_agent_kinematic_model(position,goal,deltat=0.01):

        position

class cf_based_plotter(object):
    '''

    '''
    def __init__(self,agent_number):
        self.prefix_plan=np.load('output_data/prefix.npy')
        self.suffix_plan=np.load('output_data/suffix.npy')
        self.initial=self.prefix_plan[0][0]
        self.TS=1.0
        self.agent_number=agent_number
        self.set_initial()
        self.take_off()
        self.fly_the_plan()


    def set_initial(self):
        crazyflies_yaml = "visual_env/crazyswarm/launch/crazyflies.yaml"
        fo=open(crazyflies_yaml,'w+')
        fo.write('crazyflies:')
        fo.write('\r\n')
        for i in np.arange(self.agent_number):
            fo.write('- channel: 100')
            fo.write('\r\n')
            fo.write('  id: '+str(i))
            #fo.write(i)
            fo.write('\r\n')
            pos=list(self.initial[i][0])
            pos.append(0)
            pos=np.add(pos,[0.5*np.sin(np.pi*i/self.agent_number),0.2*np.cos(np.pi*i/self.agent_number),0])
            pos=np.round(pos,2)
            fo.write('  initialPosition: ['+str(pos[0])+', '+str(pos[1])+', '+str(pos[2])+' ]')
            #fo.write(pos)
            fo.write('\r\n')
            fo.write('  type: medium')
            fo.write('\r\n')
        fo.close()

    def take_off(self):
        swarm = Crazyswarm()
        self.timeHelper = swarm.timeHelper
        self.allcfs = swarm.allcfs
        self.timeHelper.sleep(5)
        light_set=[(1,0,0),(0,1,0),(0,0,1)]
        i=0
        for cf in self.allcfs.crazyflies:
            cf.setLEDColor(*light_set[i])
            i=i+1
        self.allcfs.takeoff(targetHeight=0.5, duration=1.0 + 1)
        self.timeHelper.sleep(5)

    def fly_the_plan(self):
        z=1
        for plan in self.prefix_plan:
            i=0
            co_cf_Set={}
            macro_action=False
            for cf in self.allcfs.crazyflies:
                if not plan[0][i][1]=='None':
                    if plan[0][i][1] in co_cf_Set.keys():#here is actual not corrent because the set did't consider the region
                        co_cf_Set[plan[0][i][1]].append((cf,plan[0][i][0]))
                    else:
                        co_cf_Set[plan[0][i][1]]=[(cf,plan[0][i][0])]
                    macro_action=True
                else:
                    one_cf_plan=list(plan[0][i][0])
                    one_cf_plan.append(1)
                    cf.goTo(one_cf_plan,0,8)
                    self.timeHelper.sleep(2)
                i=i+1
            if macro_action:
                self.go_circle(co_cf_Set,15,0.5,10,0.1)

    def go_circle(self,co_cf_Set,totalTime,radius,round,kPosition):
        for cf,pos in co_cf_Set['F_leader']:#leader plan it's own path with only the message of itself
            center=list(pos)
            center.append(1)
            leader_startPos=np.add(center,np.array([radius,0,0]))
            cf.goTo(leader_startPos,0,3)
        for cf,pos in co_cf_Set['F_follower']:
            three_pos=list(pos)
            three_pos.append(1)
            follow_startPos=np.add(three_pos,-np.array([radius,0,0]))
            cf.goTo(follow_startPos,0,3)
        self.timeHelper.sleep(3)
        startTime = self.timeHelper.time()
        endTime=startTime+totalTime
        while self.timeHelper.time()<endTime :
            time = self.timeHelper.time() - startTime
            omega = 2 * np.pi*round / totalTime
            leader_Pos=np.add(center,[radius*np.cos(omega*time),radius*np.sin(omega*time),0])
            for cf,pos in co_cf_Set['F_leader']:
                cf.goTo(leader_Pos, 0,0.1)
            i=1
            for cf,pos in co_cf_Set['F_follower']:
                follow_Pos=np.add(center,[-radius*np.cos(omega*time+np.pi/6*i),-radius*np.sin(omega*time+np.pi/6*i),0])
                i=i+1
                cf.goTo(follow_Pos,0,0.5)
            self.timeHelper.sleepForRate(10)
        self.timeHelper.sleep(5)


class ProdAut_Run(object):#这是将算完的部分和可视化连接起来
	# prefix, suffix in product run
	# prefix: init --> accept, suffix accept --> accept
	# line, loop in ts
	def __init__(self, product, prefix, precost, suffix, sufcost, totalcost,Multy):
		self.prefix = prefix
		self.precost = precost
		self.suffix = suffix
		self.sufcost = sufcost
		self.totalcost = totalcost
		#self.prod_run_to_prod_edges(product)
		#self.plan_output(product,Multy=Multy)
		#self.plan = chain(self.line, cycle(self.loop))
		#self.plan = chain(self.loop)

	def prod_run_to_prod_edges(self, product):
		self.pre_prod_edges = zip(self.prefix[0:-2], self.prefix[1:-1])
		self.suf_prod_edges = zip(self.suffix[0:-2], self.suffix[1:-1])

	def plan_output(self, product, Multy=None):
		self.line = [product.nodes[node]['ts'] for node in self.prefix]
		self.loop = [product.nodes[node]['ts'] for node in self.suffix]
		if len(self.line) == 2:
			self.pre_ts_edges = [(self.line[0], self.line[1])]
		else:
			self.pre_ts_edges = list(zip(self.line[0:-1], self.line[1:]))
		if len(self.loop) == 2:
			self.suf_ts_edges = [(self.loop[0], self.loop[1])]
		else:
			self.suf_ts_edges = list(zip(self.loop[0:-1], self.loop[1:]))
			self.suf_ts_edges.append((self.loop[-1],self.loop[0]))
		# output plan

		if Multy==None:
			self.pre_plan = []
			self.pre_plan.append(self.line[0][0])
			for ts_edge in self.pre_ts_edges:
				if product.graph['ts'][ts_edge[0]][ts_edge[1]]['label'] == 'goto':
					self.pre_plan.append(ts_edge[1][0])  # motion
				else:
					self.pre_plan.append(ts_edge[1][1])  # action
			bridge = (self.line[-1], self.loop[0])
			if product.graph['ts'][bridge[0]][bridge[1]]['label'] == 'goto':
				self.pre_plan.append(bridge[1][0])  # motion
			else:
				self.pre_plan.append(bridge[1][1])  # action
			self.suf_plan = []
			for ts_edge in self.suf_ts_edges:
				if product.graph['ts'][ts_edge[0]][ts_edge[1]]['label'] == 'goto':
					self.suf_plan.append(ts_edge[1][0])  # motion
				else:
					self.suf_plan.append(ts_edge[1][1])  # action
		else:
			self.pre_plan = {}
			i=0
			for (key, WTS) in product.graph['ts'].graph['Tsdic'].items():
				self.pre_plan[key]=[self.line[0][i][0]]
				i=i+1
			for ts_edge in self.pre_ts_edges:
					#選取智能體的序號
				i=0
				for (key,WTS) in product.graph['ts'].graph['Tsdic'].items():

					if WTS[ts_edge[0][i]][ts_edge[1][i]]['label']=='goto':
						self.pre_plan[key].append(ts_edge[1][i][0])#motion
					else:
						self.pre_plan[key].append(ts_edge[1][i][1])#action
					i=i+1
			bridge=(self.line[-1],self.loop[0])
			i=0
			for (key,WTS) in product.graph['ts'].graph['Tsdic'].items():
				if WTS[bridge[0][i]][bridge[1][i]]['label']=='goto':
					self.pre_plan[key].append(bridge[1][i][0])
				else:
					self.pre_plan[key].append(bridge[1][i][1])
				i=i+1
			self.suf_plan = {}
			for key in product.graph['ts'].graph['Tsdic']:
				self.suf_plan[key]=[]
			for ts_edge in self.suf_ts_edges:
				i=0
				for (key, WTS) in product.graph['ts'].graph['Tsdic'].items():
					if WTS[ts_edge[0][i]][ts_edge[1][i]]['label']=='goto':
						self.suf_plan[key].append(ts_edge[1][i][0])
					else:
						self.suf_plan[key].append(ts_edge[1][i][1])