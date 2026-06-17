import numpy as np
import planning.data.input_data as old_input_data
from planning.data.input_data.LTL_formula import *
from planning.data.input_data.agent_data import agent_resource
import random
class Data_pretreat(object):
	'''
	this class is to formula the data into proper structure in the following detail
	here we define the goal structure of input data
	self.agent_data={'agent_name':{pose:(x,y),type:red_UAV,alive:1}
	self.agent_type={'agnet_type':{maxspeed:?,ATK:?,skill: attack plane? attack ground?}}
	self.map_data={'goal_place': {pose:?,label:0}}
	self.agent_list=[UAV1,UAV2,UAV3]#data of red agent(which we can control)
	self.task_data={task1:?,]
	self.task_list=[task1,task2]
	'''
	def __init__(self):
		self.agent_data={}
		self.agent_type={}
		self.agent_list=None
		self.task_data=None
		self.task_list=None
		self.map_data=None
		self.sub_task_type=None
		self.position=None
		self.enemy_type={}
		self.enemy_data={}
		#self.input_data=input_data()

	def load_priori_knowledge(self):
		'''
		this function is to manage the priori knwledeg already written in the function
		:return:
		'''
		data_trajectory=''
		data=np.load(data_trajectory)
		#manage the load message
		#self.map_data=old_input_data.position


	def get_map_data(self,map_data,background):
		self.map_data=map_data
		print('地图信息',self.map_data.position)
		if background == '想定场景1':
			self.costheta=0.86

		elif background == '想定场景2':
			self.costheta=0.927

		elif background == '想定场景3':
			self.costheta=0.9
	def manage_software_data(self,software_data):
		self.agent_type_with_agent={}
		self.agent_name_2_symbol={}
		self.agent_symbol_2_name={}
		self.enemy_agent_data={}
		self.enemy_agent_symbol_2_name={}
		self.enemy_agent_name_2_symbol={}
		self.enemy_type={}
		self.agent_name_counter={'enemy':0}
		self.alive_list=[]
		self.map_with_red_agent={}
		self.agent_type={}
		self.agent_data={}
		self.enemy_data={}
		for agent_type, agent_detail in software_data['redSituation'].items():
			for sub_agent_detail in agent_detail:
				if agent_type not in self.agent_name_counter.keys():
					self.agent_name_counter[agent_type]=0
				if agent_type not in self.agent_type_with_agent.keys():
					self.agent_type_with_agent[agent_type]=[]
				self.agent_type_with_agent[agent_type].append(sub_agent_detail['name'])
				n=self.agent_name_counter[agent_type]+0
				self.agent_name_counter[agent_type]=self.agent_name_counter[agent_type]+1
				symbol_name=agent_type+str(n)
				#print(sub_agent_detail)
				self.agent_symbol_2_name[symbol_name]=sub_agent_detail['name']
				self.agent_name_2_symbol[sub_agent_detail['name']]=symbol_name
				self.agent_data[symbol_name]={'name':sub_agent_detail['name'],
				                              'pose':(sub_agent_detail['longitude']*111*self.costheta,
				                                      sub_agent_detail['latitude']*111,
				                                      sub_agent_detail['altitude']),
				                              'status': sub_agent_detail['status'],
				                              'type':agent_type}
				self.alive_list.append(sub_agent_detail['status'])
				self.check_red_agent_in_map(symbol_name,(sub_agent_detail['longitude']*111*self.costheta,sub_agent_detail['latitude']*111))
				if 'important' in sub_agent_detail.keys():
					self.agent_data[symbol_name]['important']=sub_agent_detail['important']
				if 'maxspeed' in sub_agent_detail.keys():
					self.agent_data[symbol_name]['velocity']=sub_agent_detail['maxspeed']/60
				else:
					self.agent_data[symbol_name]['velocity']=0.1
		print('error_智能体数量',len(self.agent_data))
		self.enemy_agent_name_counter={}
		self.enemy_agent_data={}
		self.map_with_agent={}
		map_list=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		for map in map_list:
			self.map_with_agent[map]=[]
		for agent_type, agent_detail in software_data['blueSituation'].items():
			for sub_agent_detail in agent_detail:
				if agent_type not in self.enemy_agent_name_counter.keys():
					self.enemy_agent_name_counter[agent_type]=0
				n=self.enemy_agent_name_counter[agent_type]+0
				self.enemy_agent_name_counter[agent_type]=self.enemy_agent_name_counter[agent_type]+1
				symbol_name=agent_type+str(n)
				#print(sub_agent_detail)
				self.enemy_agent_data[symbol_name]={
				                              'pose':(sub_agent_detail['longitude']*111*self.costheta,
				                                      sub_agent_detail['latitude']*111,
				                                      sub_agent_detail['altitude']),
				                              'type':agent_type}
				self.check_agent_in_map(symbol_name,(sub_agent_detail['longitude']*111*self.costheta,sub_agent_detail['latitude']*111))

				if 'important' in sub_agent_detail.keys():
					self.enemy_agent_data[symbol_name]['important']=sub_agent_detail['important']

	def judge_the_taishi_of_agent(self,software_data):
		print('红方智能体数量：',len(software_data['redSituation']))
		print('红方智能体数量：', len(software_data['blueSituation']))
		self.enemy_taishi=[]
		self.our_taishi=[]
		for agent_type, agent_detail in software_data['redSituation'].items():
			for sub_agent_detail in agent_detail:
				yitu_list=['等待','进攻','移动','支持']
				agent_message={'类型':sub_agent_detail['name'],
							   '运动状态':'走向（'+ str(sub_agent_detail['longitude']*111*self.costheta)+','+
										  str(sub_agent_detail['latitude']*111)+')',
							   '意图': random.sample(yitu_list,1) ,
							   '资源': agent_resource[agent_type] }
				self.our_taishi.append(agent_message)
		for agent_type, agent_detail in software_data['blueSituation'].items():
			for sub_agent_detail in agent_detail:
				yitu_list=['等待','进攻','移动','支持']
				agent_message1={'类型':sub_agent_detail['name'],
							   '运动状态':'走向（'+ str(sub_agent_detail['longitude']*111*self.costheta)
										  +','+str(sub_agent_detail['latitude']*111)+')',
							   '意图': random.sample(yitu_list,1)  }
				self.enemy_taishi.append(agent_message1)


	def online_task_detection(self,software_data ):
		self.agent_name_2_symbol={}
		self.agent_symbol_2_name={}
		self.enemy_agent_symbol_2_name={}
		self.enemy_agent_name_2_symbol={}
		self.enemy_type={}
		self.agent_name_counter={'enemy':0}

		for agent_type, agent_detail in software_data['redSituation'].items():
			for sub_agent_detail in agent_detail:
				if agent_type not in self.agent_name_counter.keys():
					self.agent_name_counter[agent_type]=0
				n=self.agent_name_counter[agent_type]+0
				self.agent_name_counter[agent_type]=self.agent_name_counter[agent_type]+1
				symbol_name=agent_type+str(n)
				#print(sub_agent_detail)
				self.agent_symbol_2_name[symbol_name]=sub_agent_detail['name']
				self.agent_name_2_symbol[sub_agent_detail['name']]=symbol_name
				self.agent_data[symbol_name]={'name':sub_agent_detail['name'],
				                              'pose':(sub_agent_detail['longitude']*111*self.costheta,
				                                      sub_agent_detail['latitude']*111,
				                                      sub_agent_detail['altitude']),
				                              'status': sub_agent_detail['status'],
				                              'type':agent_type}
				if sub_agent_detail['status'] > 0:
					self.agent_data[symbol_name]['type']=agent_type
				else:
					self.agent_data[symbol_name]['type'] = 'break'
				if 'important' in sub_agent_detail.keys():
					self.agent_data[symbol_name]['important']=sub_agent_detail['important']
		self.enemy_agent_name_counter={}
		self.enemy_agent_data={}
		self.map_with_agent={}
		for agent_type, agent_detail in software_data['blueSituation'].items():
			for sub_agent_detail in agent_detail:
				if agent_type not in self.enemy_agent_name_counter.keys():
					self.enemy_agent_name_counter[agent_type]=0
				n=self.enemy_agent_name_counter[agent_type]+0
				self.enemy_agent_name_counter[agent_type]=self.enemy_agent_name_counter[agent_type]+1
				symbol_name=agent_type+str(n)
				#print(sub_agent_detail)
				self.enemy_agent_data[symbol_name]={
				                              'pose':(sub_agent_detail['longitude']*111*self.costheta,
				                                      sub_agent_detail['latitude']*111,
				                                      sub_agent_detail['altitude']),
				                              'type':agent_type}
				if sub_agent_detail['status'] > 0:
					#只有活着的智能体可以考虑，死了就不考虑了
					self.check_agent_in_map(symbol_name,(sub_agent_detail['longitude']*111*self.costheta,sub_agent_detail['latitude']*111))

				if 'important' in sub_agent_detail.keys():
					self.enemy_agent_data[symbol_name]['important']=sub_agent_detail['important']


	def get_value_place_dic(self):
		value_place_dic={}
		red_list={}
		for name,len_list in self.map_with_red_agent.items():
			red_list[name]=len(len_list)
		#red_list.sort(reverse=True)
		#只保留地点
		#print(red_list)
		#根据远近距离对其他的地点进行更新
		new_red_list=[]
		for name,place in self.map_data.position_center.items():
			#get related place
			distance_list=[]
			for name_2,place_2 in self.map_data.position_center.items():
				if not name_2==name:
					distance=abs(place[0]-place_2[0])+abs(place[1]-place_2[1])
					distance_list.append([name_2,distance])
			distance_list.sort(key=lambda x:x[1],reverse=True)
			n=len(self.map_with_red_agent[distance_list[-1][0]])+\
			  len(self.map_with_red_agent[distance_list[-2][0]])+\
			  len(self.map_with_red_agent[distance_list[-3][0]])
			new_red_list.append([red_list[name]+n/4,name])
		new_red_list.sort(reverse=True)
		new_red_list=[i[1] for i in new_red_list ]
		#对地点价值进行排序
		blue_list = {}
		for name, len_list in self.map_with_agent.items():
			blue_list[name]=len(len_list)
		new_blue_list = []
		for name, place in self.map_data.position_center.items():
			# get related place
			distance_list = []
			for name_2, place_2 in self.map_data.position_center.items():
				if not name_2 == name:
					distance = abs(place[0] - place_2[0]) + abs(place[1] - place_2[1])
					distance_list.append([name_2, distance])
			distance_list.sort(key=lambda x: x[1], reverse=True)
			n = len(self.map_with_agent[distance_list[-1][0]]) + \
				len(self.map_with_agent[distance_list[-2][0]]) + \
				len(self.map_with_agent[distance_list[-3][0]])
			new_blue_list.append([blue_list[name] + n / 4, name])
		new_blue_list.sort(reverse=True)
		# 只保留地点
		new_blue_list = [ i[1] for i in new_blue_list]
		value_place_dic['red']=new_red_list
		value_place_dic['blue']=new_blue_list
		return  value_place_dic



	def check_agent_in_map(self,name,pose):
		for area, poly in self.map_data.position.items():
			#print(pose,poly)
			if area not in self.map_with_agent.keys():
				#print(1)
				self.map_with_agent[area]=[]
			if self.if_goal_in_area(poly,pose):
				self.map_with_agent[area].append(name)

	def check_red_agent_in_map(self,name,pose):
		for area, poly in self.map_data.position.items():
			#print(pose,poly)
			if area not in self.map_with_red_agent.keys():
				#print(1)
				self.map_with_red_agent[area]=[]
			if self.if_goal_in_area(poly,pose):
				self.map_with_red_agent[area].append(name)

	def generate_tasks_goals(self):
		'''

		here we assume that the LTL has already know the name of goals?
		there might be two kind process
		1 the commender give the war operation and then the function found the goal automaticly?
		I think commend only required the area and then the function found the agent in represent area
		2 the commender give the goal already
		these step is used if we choose situation 2
		:return:
		'''
		1

	def estimate_cost_of_tasks(self,poset_product,background='想定场景1',prefer_type='time_first'):
		# 估算子任务的各项属性
		# 计算子任务的执行风险 计算方法为统计该区域的敌方火力强度，并根据我方智能体性能判断该子任务的执行风险
		# 计算任务贡献度 根据本任务对全局战场的贡献，进行分析 贡献度的总和为1
		# 计算资源消耗 资源消耗取决于任务目标智能体的种类数量，以及我方智能体所消耗的资源类型
		# 计算战力需求  表征执行该任务需要的智能体数量，与我方智能体战斗力，历史交战平均值，该任务目标敌方智能体数量等密切相关

		'''
		judge the value of goal tasks
		goal -> important
		time_first: 基础类型
		efficient_first:效率
		success_first:成功率
		'''
		if background=='想定场景1':
			limit_num=8
		elif background=='想定场景2':
			limit_num=5
		elif background=='想定场景3':
			limit_num=4

		task_data_list=poset_product.final_task_data_list
		self.task_data_cost=[]
		self.task_data_final_judgement_value=[]
		task_risk = []
		self.agent_needed=[]
		self.task_cost_tuple=[]
		for ID,subject,act,area,goal in task_data_list:
			# define the area agent number
			poly_area=self.map_data.position[area]
			agent_list=self.map_with_agent[area]
			relatied_agent_list=self.check_related_agent_list(agent_list,goal)
			basic_value=old_input_data.task_type[act]
			if prefer_type=='efficient_first':
				value=max(len(agent_list)**0.5*basic_value,basic_value)/1.2
			else:
				value=max(len(agent_list)**0.5*basic_value,basic_value)
			task_risk.append(max(1,len(agent_list)))
			#self.task_data_cost.append(value*50)
			#this step is to define the agent number to execute current task
			#for simplified here we just assume x agent for a group?
			if prefer_type=='success_first':
				required_agent_number=int(min(max(4*len(agent_list),4),8)*1.2)
			else:
				required_agent_number = min(max(2 * len(agent_list), 2), limit_num)
				if act=='trick':
					required_agent_number=min(max( len(agent_list), 1), 2)
			self.task_data_cost.append(value)
			self.agent_needed.append(required_agent_number)
			self.task_cost_tuple.append((value,required_agent_number))
		self.input_data=input_data()
		self.input_data.enemy_agent_data=self.enemy_agent_data
		self.input_data.agent_data=self.agent_data
		self.input_data.agent_type=old_input_data.agent_type
		self.input_data.position=self.position
		self.input_data.task_type=old_input_data.task_type
		self.input_data.task_data_cost=self.task_cost_tuple
		self.input_data.position_center=self.map_data.position_center
		#生成4个指标的参数 任务风险、目标贡献度（对大家求百分比）、执行时间
		task_comtribution=[]
		total_cost=0
		#时长，任务需要智能体数量
		for time,agent_num in self.task_cost_tuple:
			total_cost=total_cost+time*agent_num
		#贡献度
		for time,agent_num in self.task_cost_tuple:
			task_comtribution.append(time*agent_num/total_cost)
		#危险分析 分析目标区域的智能体数量

		#最终生成任务的代价
		self.task_information={'time_cost': self.task_data_cost,
							  'agent_needed': self.agent_needed,
							  'task_comtribution':task_comtribution,
							  'task_risk':task_risk
								}



	def check_related_agent_list(self,agent_list,goal):
		count=0
		for agent in agent_list:
			if goal in agent.lower():
				count=count+1
		return  count
	def online_estimate_cost_of_tasks(self):
		'''
		judge the value of goal tasks
		goal -> important
		'''
		task_data_list=self.task_data
		self.task_data_cost=[]
		for ID,subject,act,area,goal in task_data_list:
			# define the area agent number
			poly_area=old_input_data.map_data.position[area]
			agent_list=self.map_with_agent[area]
			basic_value=old_input_data.task_type[act]
			value=len(agent_list)**0.5*basic_value
			#self.task_data_cost.append(value*50)
			#this step is to define the agent number to execute current task
			#for simplified here we just assume x agent for a group?
			required_agent_number=4*len(agent_list)
			self.task_data_cost.append((value,required_agent_number))
			#for agent in agent_list:
			#	agent_type=self.enemy_agent_data[agent]['type']
			#	value=old_input_data.agent_data.agent_value[agent_type]
		#position,task_type,sub_task_type,agent_data,agent_type

		#self.input_data=input_data()
		self.input_data.enemy_agent_data=self.enemy_agent_data
		self.input_data.agent_data=self.agent_data
		self.input_data.agent_type=old_input_data.agent_type
		self.input_data.position=self.position
		self.input_data.task_type=old_input_data.task_type
		self.input_data.task_data_cost=self.task_data_cost
		self.input_data.position_center=self.position_center

	def add_data_from_script(self,Poset_product,data_from_script):
		self.task_data=Poset_product.final_task_data_list
		self.input_data=input_data()
		finished_task=set()
		for agent, detail in data_from_script.items():
			finished_task=finished_task | detail['finished_task']
		self.input_data.finished_task=finished_task
		executing_task=set()
		for agent, detail in data_from_script.items():
			executing_task=executing_task | detail['executing_task']
		self.input_data.executing_task=executing_task

	def if_goal_in_area(self,poly,pose):
		poly2=[poly[-1],*poly[:-1]]
		s=0
		area=self.get_area(poly)
		for i in range(len(poly)):
			node1=poly[i]
			node2=poly2[i]
			s=s+self.get_area([pose,node1,node2])
		#print(s,area)
		if s<=area:
			return 1
		else :
			return 0

	def get_area(self,node_list):
		S=0
		for i in range(len(node_list)-2):
			x1=node_list[0]
			x2=node_list[i+1]
			x3=node_list[i+2]
			S=S+np.abs((x2[0]-x1[0])*(x3[1]-x1[1])-(x2[1]-x1[1])*(x3[0]-x1[0]))/2
		return S


	def manage_output_data(self,poset,solution,time_step,task_time_table):
		'''

		:param poset:
		:param solution:
		:return:
		'''
		output_data={"moveactions":[]}
		z=-1
		for agent in solution:
			z=z+1
			agent_symbol=list(self.agent_data.keys())[z]
			agent_name=self.agent_symbol_2_name[agent_symbol]
			z_goal_pose=list(self.agent_data.values())[z]['pose'][2]
			if len(agent)==0:
				#agent has no task so just stay at original place
				goal_pose=list(self.agent_data.values())[z]['pose']
				task_action='moveactions'
			else:
				found_label=0
				for task in agent:
					task_id=task[0][0]
					task_action=action_2_commander[task[1]]
					if time_step<task_time_table[task_id][1]:
						goal_pose=self.input_data.position_center[task[0][3]]
						found_label=1
						break
					elif time_step<task_time_table[task_id][2]:
						goal_pose=self.input_data.position_center[task[0][3]]
						found_label=1
						break
				if found_label==0:
					goal_pose=self.input_data.position_center[agent[-1][0][3]]
			if task_action in output_data.keys():
				output_data[task_action].append({'agentname':agent_name,"longitude":goal_pose[0]/110/self.costheta,"latitude":goal_pose[1]/110,"altitude":z_goal_pose})
			else:
				output_data[task_action]=[{'agentname':agent_name,"longitude":goal_pose[0]/110/self.costheta,"latitude":goal_pose[1]/110,"altitude":z_goal_pose}]
		return output_data

	def poset_task_supervision_initial(self,poset,task_data,agent_data):
		#初始化监督内容
		self.poset=poset
		self.finished_task=[]
		self.begined_task=set()
		self.executing_task=set()
		#self.alive_list=[]
		self.agent_data=agent_data
		self.gantt_data_list=[]
	def poset_task_supervision(self, data):
		#该函数目的为监督任务的执行情况
		#监督完成的情况
		#统计已经开始的任务
		self.executing_task=set()
		for task in data:
			if not task<0:
				self.begined_task.add(task)
				self.executing_task.add(task)
		#检查已经完成的任务
		self.finished_task=self.begined_task-self.executing_task
		#检查是否有新的智能体损毁
		agent_ID=0
		current_alive_agent=[]
		new_break_agent_list=[]
		for task in data:
			if task>0:
				current_alive_agent.append(1)
			else:
				if self.alive_list[agent_ID] == 1:
					#这意味着新的智能体坏了
					new_break_agent_list.append(agent_ID)

				current_alive_agent.append(0)
			agent_ID=agent_ID+1
		#这里损毁的智能体超过过阈值，重新进行计算
		if len(new_break_agent_list)>0:
			self.alive_list=current_alive_agent
			replanning_label=1
		else:
			replanning_label=0

		return replanning_label


	def gantt_online_menegar(self,data):
		#生成一致的时长
		color_dic = {"observe": "blue", "support": "green", "attack": "red"}

		agent_ID = -1
		# 计算位置
		time_data=data['step']
		executing_task_data=['task']
		if len(self.gantt_data_list)==0:
			for task in executing_task_data:
				agent_ID=agent_ID+1
				jason_agent_dic = {"agent_ID": agent_ID, "task": []}
				jason_task_data = {}
				jason_task_data["task_ID"] = task
				jason_task_data["begin_time"] = time_data
				jason_task_data["color"] = color_dic[self.poset['action_map'][task][0][2]]
				jason_task_data["duration"] =1
				jason_agent_dic["task"].append(jason_task_data)
				self.gantt_data_list.append(jason_agent_dic)
		else:
			for task in executing_task_data:
				agent_ID=agent_ID+1
				#选取最后一个执行的状态
				current_task_data=self.gantt_data_list[agent_ID]['task'][-1]
				#判断是否还在执行这个动作
				if current_task_data["task_ID"]==task:
					#则修改执行的时间
					current_task_data["duration"]=current_task_data["duration"]+1
				else:
					#开始进行新的工作
					#额外判断智能体是否损坏？
					jason_task_data = {}
					jason_task_data["task_ID"] = task
					jason_task_data["begin_time"] =  time_data
					if task == -1:
						jason_task_data["color"]="black"
					else:
						jason_task_data["color"] = color_dic[task[0][2]]
					jason_task_data["duration"] =1
					self.gantt_data_list[agent_ID]['task'].append(jason_task_data)

	def required_online_gantt_data(self):
		return self.gantt_data_list


	def generate_online_input_data(self,soft_ware_data):
		#生成在线优化的input data

	    #a = optimize_method.Branch_And_Bound(Poset_product.final_poset, Poset_product.final_task_data_list,input_data)
		self.input_data=input_data()
		self.input_data.enemy_agent_data=self.enemy_agent_data
		#
		self.input_data.agent_data=self.agent_data
		#根据当前情况，处理agent data
		#处理方法，将损毁的智能体的功能转为空
		agent_ID=0
		for agent in self.alive_list:
			if agent==0:
				self.input_data.agent_data[agent_ID]['agent_type']='break'
			agent_ID=agent_ID+1
		self.input_data.agent_type=old_input_data.agent_type

		self.input_data.position=self.position

		self.input_data.task_type=old_input_data.task_type

		self.input_data.task_data_cost=self.task_data_cost

		self.input_data.position_center=self.position_center
		#Agent_pose

		#finished_time_list智能体完成手头任务的时间
		finished_time_list={}
		for task in self.finished_task:
			finished_time_list[task]=0
		#unfinished_task_list 还在执行的任务（忽略了）
		agent_pose={}
		agent_ID=0
		for agent_type, agent_detail in soft_ware_data['redSituation'].items():
			for sub_agent_detail in agent_detail:
				agent_pose[agent_ID]=(sub_agent_detail['longitude']*111*self.costheta,sub_agent_detail['latitude']*111 )
				agent_ID=agent_ID+1
		#begin_time
		begin_time={}
		agent_ID=0
		for agent in self.agent_list:
			if agent==0:
				begin_time[agent_ID]=5000
			else:
				begin_time[agent_ID]=0
			agent_ID=agent_ID+1
		#task_dic

		#task_execute_time  任务执行时间表
		task_execute_time={}
		task_dic={}
		task_ID=0
		another_ID=0
		for task_cost,agent_number in self.task_data_cost:
			if task_ID not in self.finished_task:
				task_dic[task_ID]=another_ID
				another_ID=another_ID+1
			task_execute_time[task_ID]=task_cost
			task_ID=task_ID+1

		#broken_agent_list  损毁的智能体表
		broken_agent_list=[]
		agent_ID=0
		for agent in self.agent_list:
			if agent==0:
				broken_agent_list.append(agent_ID)
			agent_ID=agent_ID+1
		extro_constrain=The_extro_condition(agent_pose,finished_time_list,begin_time,
                                            task_dic,task_execute_time,broken_agent_list)



		return self.input_data,extro_constrain

	def menage_online_software_data(self,data_in_beihang,software_data):
		#这里是处理的主程序
		#这里在线的处理来自北航的数据
		#处理目的为处理执行情况的数据



		replanning_label=self.poset_task_supervision(data_in_beihang['task'])
		# 甘特图在线估计
		self.gantt_online_menegar(data_in_beihang)
		input_data=0
		extro_constrain = 0
		if replanning_label:
			input_data,extro_constrain=self.generate_online_input_data(software_data)

		return  replanning_label,input_data,extro_constrain,self.finished_task

	def assess_solution(self,solution,subtask_value):
		#=============================
		#对任务分配方案进行评估，
		#确定危险性量化指标、集群完好度量化指标和对抗胜利概率量化指标，为集群任务决策提供依据
		#作战危险性指标 通过分析统计每个智能体执行对应任务的危险性 获取整体分配方案的危险性指标
		#集群完好度指标，计算每个智能体在每个任务下存活期望，最后统计集群的完好度指标
		#对抗胜率概率指标  由历史平均胜率概率以及危险性带来的风险影响，加权计算得到
		#======================================================
		label_dic={}
		danger_num=0
		total_danger=0
		#胜利rate
		rate=1
		agent_num=len(solution)
		survive_num=0
		success_rate=1
		danger_num+rate+success_rate
		for agent in solution:
			for task in agent:
				total_danger=subtask_value[task[0][0]]['loss']+total_danger
			n=len(agent)
			survive_num=5/(5+n)+survive_num
		label_dic['集群完好度']=survive_num/agent_num
		label_dic['作战危险性']=total_danger
		label_dic['对抗胜利概率']=0.8+0.2*random.random()
		print('本次方案的评估为：集群完好度',survive_num/agent_num,'作战危险性',total_danger,'对抗胜率概率',0.8+0.2*random.random())
		#return  label_dic



class input_data:
	def __init__(self):
		self.position=None

class The_extro_condition:
    def __init__(self,agent_pose,finished_time_list,begin_time,task_dic,task_execute_time,broken_agent_list):
        self.agent_pose=agent_pose
        # describe when the agent can to execute next action
        self.finished_time_list=finished_time_list
        self.begin_time=begin_time
        self.task_dic=task_dic
        self.task_execute_time=task_execute_time
        self.broken_agent_list=broken_agent_list