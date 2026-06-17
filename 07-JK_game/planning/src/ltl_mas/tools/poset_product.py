import numpy as np
from planning.src.ltl_mas.tools.poset_builder import Buchi_poset_builder
import cvxpy as cp
from planning.data.input_data.LTL_formula import *
class Poset_producter(object):
	def __init__(self,ltl_formula_list):
		'''
		这部分为偏序处理部分，用于优化偏序结构，处理一些参数细节等等。

		'''
		self.poset_list=ltl_formula_list
		self.gantt_data_dic={}


	def generate_poset(self):
		self.ltl2poset={}
		for round,formula_list in self.poset_list.items():
			self.ltl2poset[round]=[]
			for formula in formula_list:
				buchi=Buchi_poset_builder(formula)
				buchi.main_fun_to_get_poset(20)
				self.ltl2poset[round].append(buchi)



	def prodocter(self):
		self.final_poset={'||': set(),
			 '<=': set(),
			 '<': set(),
			 '!=': set(),
			 '=': set(),
			 'action_map': []}
		self.final_task_data_list=[]
		final_round_poset = {}
		for round,ltl2poset in self.ltl2poset.items():

			for poset in ltl2poset:
				sub_poset=poset.poset_list[0]
				sub_task_data_list=poset.task_data_list[0]
				#judge the task list
				if len(self.final_poset['action_map'])==0:
					self.final_poset['action_map']=poset.task_data_list[0]
					self.final_poset['<=']=sub_poset['<=']
					self.final_poset['!=']=sub_poset['!=']
					self.final_task_data_list.extend(sub_task_data_list)
				else:
					n=len(self.final_poset['action_map'])
					new_sub_task_data_list=[]
					if len(np.shape(poset.task_data_list))==3:
						for task in poset.task_data_list[0] :
							new_sub_task_data_list.append((task[0]+n,task[1],task[2],task[3],task[4]))
					else:
						for task in poset.task_data_list :
							new_sub_task_data_list.append((task[0]+n,task[1],task[2],task[3],task[4]))
					self.final_poset['action_map'].extend(new_sub_task_data_list)
					self.final_task_data_list.extend(new_sub_task_data_list)
					for i,j in sub_poset['<=']:
						self.final_poset['<='].add((i+n,j+n))
					for i,j in sub_poset['!=']:
						self.final_poset['!='].add((i+n,j+n))
			if len(final_round_poset)==0:
				final_round_poset=range(len(self.final_task_data_list))
			else:
				for i in range(len(self.final_task_data_list)):
					for j in final_round_poset:
						if not i in final_round_poset:
							self.final_poset['<='].add((j,i))
							self.final_poset['!='].add((j,i))
				final_round_poset=range(len(self.final_task_data_list))

			#实际上只需要在添加一组考虑波次的order的即可


	def gantt_graph_generate(self,current_solution ,poset):
		#将任务生成对颜色的映射
		color_dic={"observe":"blue","support":"green","attack":"red"}
		action_dic = {'attack': '进攻', 'observe': '侦查', 'support': '支持'}
		jason_data={}
		#agent_ID=-1
		#计算位置
		task_time_table=self.found_the_gantt_time(current_solution,poset)
		#生成基于gantt的计算方法

		for i in range(len(task_time_table)):
			jason_task_data={"task_name":action_dic[poset['action_map'][i][2]]+map_dic_to_num[poset['action_map'][i][3]],
							 "begin_time":task_time_table[i][0],
							 "duration":1}
			jason_data[i]=jason_task_data
		return  jason_data

	def gantt_online_menegar(self,data,poset):
		#生成一致的时长
		color_dic = {"observe": "blue", "support": "green", "attack": "red","trick":"purple"}
		action_dic = {'attack': '进攻', 'observe': '侦查', 'support': '支持',"trick":"诱骗"}
		agent_ID = -1
		# 计算位置
		time_data=data['step']
		executing_task_data=data['task']
		for task in executing_task_data:
			if task not in [100,-1]:
				if task in self.gantt_data_dic.keys():
					#已经存在的 只修改duration
					self.gantt_data_dic[task]['duration']=time_data-self.gantt_data_dic[task]['begin_time']
				else:
					print(poset['action_map'][task][2])
					self.gantt_data_dic[task]={'task_name': action_dic[poset['action_map'][task][2]]+map_dic_to_num[poset['action_map'][task][3]], 'begin_time': time_data, 'duration': 1}


	def  gantt_online_menegar2(self,data):
		#生成一致的时长
		color_dic = {"observe": "blue", "support": "green", "attack": "red"}

		agent_ID = -1
		# 计算位置
		time_data=data['step']
		executing_task_data=data['task']
		if len(self.gantt_data_list)==0:
			for task in executing_task_data:
				if task not in [100,-1]:

					jason_task_dic = {'task_name': 'attack', 'begin_time': 3.0, 'duration': 1, 'task_ID': 5}
					jason_task_data = {}
					jason_task_data["task_ID"] = task
					jason_task_data["begin_time"] = time_data
					jason_task_data["color"] = "white"
					jason_task_data["duration"] = 1
					jason_task_data["task_type"]='no_task'
					jason_agent_dic["task"].append(jason_task_data)
					self.gantt_data_list.append(jason_agent_dic)
					continue
				if task==-1:
					#agent 挂了
					agent_ID = agent_ID + 1
					jason_agent_dic = {"agent_ID": agent_ID, "task": []}
					jason_task_data = {}
					jason_task_data["task_ID"] = task
					jason_task_data["begin_time"] = time_data
					jason_task_data["color"] = "black"
					jason_task_data["duration"] = 1
					jason_task_data["task_type"] = 'broken'
					jason_agent_dic["task"].append(jason_task_data)
					self.gantt_data_list.append(jason_agent_dic)
				agent_ID=agent_ID+1
				jason_agent_dic = {"agent_ID": agent_ID, "task": []}
				jason_task_data = {}
				jason_task_data["task_ID"] = task
				jason_task_data["begin_time"] = time_data
				jason_task_data["color"] = color_dic[self.poset['action_map'][task][2]]
				jason_task_data["task_type"] =  self.poset['action_map'][task][2]
				jason_task_data["duration"] =1
				jason_agent_dic["task"].append(jason_task_data)
				self.gantt_data_list.append(jason_agent_dic)
		else:
			for task in executing_task_data:

				agent_ID=agent_ID+1
				#选取最后一个执行的状态
				print(self.gantt_data_list )
				current_task_data=self.gantt_data_list[agent_ID]['task'][-1]
				#判断是否还在执行这个动作
				if current_task_data["task_ID"]==task:
					#则修改执行的时间
					current_task_data["duration"]=current_task_data["duration"]+1
				else:
					#开始进行新的工作
					jason_task_data = {}
					jason_task_data["task_ID"] = task
					jason_task_data["begin_time"] =  time_data

					if task == -1:
						jason_task_data["color"]="black"
						jason_task_data["task_type"]="broken"
					else:
						if task == 100:
							jason_task_data["color"] = "white"
							jason_task_data["duration"] = 1
							jason_task_data["task_type"] = 'no_task'

						else:
							jason_task_data["task_type"] = self.poset['action_map'][task][2]

							jason_task_data["color"] = color_dic[self.poset['action_map'][task][2]]
					jason_task_data["duration"] =1
					self.gantt_data_list[agent_ID]['task'].append(jason_task_data)
	def found_the_gantt_time(self,solution,poset):
		begin_time=cp.Variable(shape=(len(poset['action_map']), 1), name='begin_time', nonneg=True)
		solution_M=[]
		total_constrain=[]
		task_number=len(poset['action_map'])
		M2=[]
		B2=[[]]
		for agent in solution:
			round=0
			for task in agent:
				if round>0:
					m=[0 for l in range(task_number)]
					j=task[0][0]
					i=agent[round-1][0][0]
					m[i] =1
					m[j] = -1
					M2.append(m)
					B2[0].append(-1)
				round = round + 1
		if not M2==[]:
			M22=self.Turn_Matrix(M2)
			costraint2=[M22 @ begin_time <= B2]
			total_constrain.append(*costraint2)
		M1=[]
		B1=[[]]
		for i, j in poset['<=']:
			m = [0 for l in range(task_number)]
			m[i] = 1
			m[j] = -1
			M1.append(m)
			B1[0].append(-1)
		if not M1==[]:
			M11 = self.Turn_Matrix(M1)
			constraint1 = [M11 @ begin_time <= B1]
			total_constrain.append(*constraint1)
		list1 = [[1] for i in range(task_number)]
		obj = cp.Minimize(list1 @ begin_time)
		prob = cp.Problem(obj, total_constrain)
		# prob.solve(solver=cp.SCS)
		prob.solve(solver='GLPK_MI')
		if prob.status == 'optimal':
			time_table={}
			j=0
			for value in begin_time.value:
				time_table[j]=value
				j=j+1
			#目前来看，分配方案还不算太好
			return  time_table

	def Turn_Matrix(self, M):
		r = [[] for i in M[0]]
		for i in M:
			for j in range(len(i)):
				r[j].append(i[j])
		return r