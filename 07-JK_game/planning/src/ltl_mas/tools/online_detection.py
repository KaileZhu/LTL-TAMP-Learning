import  networkx as nx
import  numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
from matplotlib import rc
import time
from collections import Counter
from itertools import product as iter_product
from itertools import combinations as iter_com
import copy
import random
from ltl_mas.tools.Data_pre_treatment import Data_pretreat

class Online_detection(object):
	def __init__(self,poset,task_time_table,solution,input_data):
		self.poset=poset
		self.task_data=input_data.task_data_cost
		self.task_time_table=task_time_table
		self.generate_poset_graph()
		self.agent_alive_list=[i['isAlive'] for i in input_data.agent_data.values()]
		self.solution=solution
		self.re_up_date_poset()


	def re_up_date_poset(self):
		for i,j in self.poset['!=']:
			time_i=self.task_time_table[i][1]
			time_j=self.task_time_table[j][1]
			if time_i < time_j:
				self.poset['<'].add(tuple((i,j)))
			else:
				self.poset['<'].add(tuple((j,i)))


	def generate_poset_graph(self):
		poset_graph=nx.DiGraph()
		for i,j in self.poset['<']:
			poset_graph.add_edge(i,j)
		for i,j in self.poset['<=']:
			poset_graph.add_edge(i,j)
		for i in range(len(self.task_data)):
			if not poset_graph.has_node(i):
				poset_graph.add_node(i)
		new_poset_graph=copy.deepcopy(poset_graph)
		self.poset_graph=poset_graph
		remove_list=[]
		for i,j in poset_graph.edges:
			removable_label=self.find_path(i,j)
			if removable_label:
				remove_list.append((i,j))
		for i,j in remove_list:
			self.poset_graph.remove_edge(i,j)
		node_set=[]
		for i in self.poset_graph.nodes:
			if len(self.poset_graph.pred[i])==0:
				node_set.append(i)
		for i in node_set:
			self.poset_graph.add_edge('root',i)

	def online_adaptation(self,Poset_product,software_input_data,data_from_script):
		input_data=self.data_pretretment(Poset_product,software_input_data,data_from_script)
		#passive update the data list
		self.passive_updata_data_list(input_data)
		self.rebuild_task_table(input_data)
		# if there is some changes , rebuild the task table

	def passive_updata_data_list(self,input_data):
		#if no task is feasible
		self.need_replan_task=0
		if not self.agent_alive_list==input_data.Alive_list:
			agent_ID=0
			for agent in self.solution:
				if input_data.agent_alive_list[agent_ID]==1:
					agent_ID=agent_ID+1
					continue
				agent_ID=agent_ID+1
				for task in agent:
					if task[0][0] not in input_data.finished_task:
						if task[0][0] in input_data.executing_task:
							#need to rebuild the task
							self.need_replan_task=1
							return input_data
		return input_data

		# the following should manage whether the task should be delay or others?

	def update_task_for_each_agent(self,new_node,time_table,Efinished_node,finished_task,unfinished_action_list):
		#still error!
		#update state
		path_list=[{}  for i in range(len(self.task_data)) ]
		#get path_list for task
		for agent in self.agent_swarm:
			print(agent.task_list)
			for i in range(agent.current_stage_ID,len(agent.motion_type_list)):
				if not agent.motion_type_list[i] in ['stay','error','motion']:
					print(agent.task_list[i//2],agent.agent_ID)
				#if not agent.motion_type_list[agent.current_stage_ID] in ['stay','error','motion']:
				#i=agent.current_stage_ID
					if agent.task_list[i//2][1] in path_list[agent.task_list[i//2][0][0]].keys():
						path_list[agent.task_list[i//2][0][0]][agent.task_list[i//2][1]].append(agent.motion_list[i])
					else:
						path_list[agent.task_list[i//2][0][0]][agent.task_list[i//2][1]]=[agent.motion_list[i]]
		#get unfinished task list
		#get un begin task list:
		update_task=set()
		for task in unfinished_action_list.keys():
			if task not in update_task:
				update_task.add(task)
		for task in update_task:
			path_list[task[0]]=self.field.co_task_planning(task[1],task[2])
		current_node=Efinished_node.copy()
		for agent_ID in range(len(current_node)):
			current_node[agent_ID].extend(new_node[agent_ID])
		self.task_list=current_node.copy()
		for agent in current_node:
			for sub_task in agent:
				#print(sub_task[0][0],task[0])
				if sub_task[0][0]==task[0]:
					print('remove!',sub_task)
					agent.remove(sub_task)
		print('update task list')

		for agent in range(len(self.agent_swarm)):
			self.agent_swarm[agent].init_pose=self.agent_swarm[agent].current_pose
			print('init_pose',self.agent_swarm[agent].init_pose)
			self.agent_swarm[agent].set_task_pretreatment(swarm_path[agent])
			self.agent_swarm[agent].current_stage_ID=0
		for agent in self.agent_swarm:
			task_time_table=[]
			for task in agent.task_list:
				task_time_table.append(self.task_time_table[task[0][0]])
			agent.task_time_table=task_time_table


	def rebuild_task_table(self,input_data):
		#situation= do the left    //    do the whole
		# get boundry condition
		#unfinished task should not be removed
		#and the task broken time should be comsider again
		#only these two bug!!!!!!!!
		old_solution = self.solution.copy()
		un_assign_task = []
		un_assign_task_num = []
		un_changeble_task=copy.deepcopy(input_data.finished_task)
		un_changeble_task=un_changeble_task| input_data.executing_task
		un_assign_task_num= set(range(len(self.task_data)))-un_changeble_task
		#un_finished_task=task-un_changeble_task
		# update input data
		unfinished_solution = []
		for agent in old_solution:
			un_finished_task_for_agent = []
			for task in agent:
				if task[0][0] in un_assign_task_num:
					un_finished_task_for_agent.append(task)
			unfinished_solution.append(un_finished_task_for_agent)
		agent_pose=[detail['pose'] for detail in input_data.agent_data.values()]
		broken_agent_list=[]
		z=0
		for agent in input_data.Alive_list:
			if agent==0:
				broken_agent_list.append(z)
			z=z+1
		unfinished_action_time={}
		z=0
		for i in input_data.task_data_cost:
			unfinished_action_time[1]=i[0]
			z=z+1
		#------------------------

		#========update the broken agent msg
		unfinished_action_list={}
		unfinished_action_time={}
		for i in broken_agent_list:
			if not len(self.agent_swarm[i].task_list)==0:
				if self.agent_swarm[i].motion_type_list[self.agent_swarm[i].current_stage_ID] not in ['motion','stay']:
					task=self.agent_swarm[i].task_list[self.agent_swarm[i].current_stage_ID//2]
					if not self.agent_swarm[i].task_list[self.agent_swarm[i].current_stage_ID//2] in unfinished_action_list.keys():
						unfinished_action_list[task[0]]=[self.agent_swarm[i].motion_type_list[self.agent_swarm[i].current_stage_ID]]
					else:
						unfinished_action_list[task[0]].append(self.agent_swarm[i].motion_type_list[self.agent_swarm[i].current_stage_ID])
					unfinished_action_time[task[0]]=len(self.agent_swarm[i].motion_list[self.agent_swarm[i].current_stage_ID])*self.agent_swarm[i].action_step_len
		finished_node = []
		finished_action = set()
		for agent in old_solution:
			finished_task = []
			for task in agent:
				if task[0][0] not in un_assign_task_num and task[0] not in executing_tasks:
					finished_task.append(task)
					finished_action.add(task[0])
				else:
					break
			finished_node.append(finished_task)
		task_dic={}
		z=0
		for i in un_assign_task:
			task_dic[i[0]]=z
			z=z+1
		for i in executing_tasks:
			task_dic[i[0]]=z
			z=z+1
		#======= get boundry of current action:
		begin_time_list={}
		for agent in self.agent_swarm:
			if agent.get_current_stage(agent.current_time) in ['motion', 'stay']:
				begin_time_list[agent.agent_ID]=self.global_time
			else:
				if agent.get_current_stage(agent.current_time) == 'error':
					begin_time_list[agent.agent_ID]=self.global_time+5000
				else:
					begin_time_list[agent.agent_ID]=agent.estimate_current_action_or_motion_time()+self.global_time

		task_execute_time={}
		for task in self.anchor_fun:
			if tuple(task) in unfinished_action_list:
				task_execute_time[task[0]]=unfinished_action_time[task]
			else:
				task_execute_time[task[0]]=self.task_time_table[task[0]][2]-self.task_time_table[task[0]][1]
		task_data=self.anchor_fun
		input_data=self.field.input_data
		input_data.agent_type['broken']={'serve':[],'velocity':0.1}
		for agent_ID in broken_agent_list:
			1
			#input_data.agent_data.remove(input_data.agent_data[agent_ID])
			#input_data.agent_data.insert(agent_ID,(agent_ID,'p1','broken')) should be changed
		for task in executing_tasks:
			#finished_task.remove(task)
			un_assign_task.append(task)
			#del finished_time_list[task[0]]
		#rebuild the task type
		#task data showed be rebuild
		#add old task into new task
		if self.extro_constrain==None:
			self.extro_constrain=The_extro_condition(agent_pose,finished_time_list,unfinished_task_list,begin_time,
                                            task_dic,task_execute_time,broken_agent_list)
		else:
			#this situation occurs when the agent break more than one time,so that the task need add the old task
			for task,time in self.extro_constrain.finished_time_list.items():
				if task not in finished_time_list.keys():
					finished_time_list[task]=time
			num=0
			task_dic={}
			for i in range(len(self.task_data)):
				if not i in finished_time_list.keys():
					task_dic[i]=num
					num=num+1
			for i in finished_time_list.keys():
				if not self.task_data[i] in finished_task:
					finished_task.add(self.task_data[i])
			self.extro_constrain=The_extro_condition(agent_pose,finished_time_list,unfinished_task_list,begin_time,
                                            task_dic,task_execute_time,broken_agent_list)

		bnb=Branch_And_Bound(self.poset,task_data,input_data)

		bnb.Begin_branch_search_online(search_time,self.extro_constrain,finished_task)
		new_solution=bnb.best_solution
		new_time_table=bnb.task_time_table
		return new_solution,new_time_table


	def data_pretretment(self,Poset_product,data_from_software,data_from_script):
		self.Data_manager=Data_pretreat()
		self.Data_manager.manage_software_data(data_from_software)
		#Data_manager.load_priori_knowledge()
		self.Data_manager.add_data_from_script(Poset_product,data_from_script)
		self.Data_manager.online_estimate_cost_of_tasks()
		input_data=self.Data_manager.input_data
		input_data.Alive_list=self.Data_manager.alive_list
		return input_data

	def find_path(self,start,end):
		path = []
		paths = []
		queue = [(start, path)]
		while queue:
			start, path = queue.pop()
			#print('PATH', path)
			path = path + [start]
			#print('PATH after adding start ', path)
			if start == end:
				#print('end')
				paths.append(path)
			for node in set(self.poset_graph.neighbors(start)).difference(path):
				queue.append((node, path))
			#print('queue', queue)
		if len(paths)>=2:
			removable_label=1
			return removable_label
		else:
			removable_label=0
			return removable_label


class Input_data(object):
	def __init__(self):
		1