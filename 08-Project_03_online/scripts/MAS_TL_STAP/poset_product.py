import numpy as np
from .new_poset_builder import Buchi_poset_builder
import cvxpy as cp
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors


class Poset_producter(object):
	def __init__(self, ltl_formula_list):
		'''
        这部分为偏序处理部分，用于优化偏序结构，处理一些参数细节等等。

        '''
		self.poset_list = ltl_formula_list
		self.gantt_data_dic = {}

	def generate_poset(self):
		self.ltl2poset = {}
		self.ltl2poset[1] = []
		for formula_list in self.poset_list:
			buchi = Buchi_poset_builder(formula_list)	# 根据任务公式构建类的实例
			buchi.main_fun_to_get_poset(20)		# 20为时间预算
			self.ltl2poset[1].append(buchi)

	def prodocter(self):
		self.final_poset = {'||': set(),
							'<=': set(),
							'<': set(),
							'!=': set(),
							'=': set(),
							'action_map': []}
		self.final_task_data_list = []
		final_round_poset = {}
		for round, ltl2poset in self.ltl2poset.items():

			for poset in ltl2poset:
				sub_poset = poset.poset_list[0]
				sub_task_data_list = poset.task_data_list[0]
				# judge the task list
				# 同一个任务可能会被映射到多个编号
				if len(self.final_poset['action_map']) == 0:
					self.final_poset['action_map'] = poset.task_data_list[0]
					self.final_poset['<='] = sub_poset['<=']
					self.final_poset['!='] = sub_poset['!=']
					self.final_task_data_list.extend(sub_task_data_list)
				else:
					n = len(self.final_poset['action_map'])
					new_sub_task_data_list = []
					new_sub_task_idx_list = {} # 存储本次for循环的poset和全局poset中任务编号对应关系
					exist_sub_task_data_list = []
					exist_sub_task_idx_list = {}

					if len(np.shape(poset.task_data_list)) == 3:
						for task in poset.task_data_list[0]:
							# 这里加一步判断，已经存在与final_poset中的任务就不重复添加了
							for task_already_exist in self.final_poset['action_map']:
								if task_already_exist[1:] == task[1:]:
									# 找到重复的任务了
									exist_sub_task_data_list.append(task)
									# 存储相对该poset的编号和相对全局poset的编号的对应关系
									exist_sub_task_idx_list[task[0]]=task_already_exist[0]
									break
									# exist_sub_task_data_list.append((task_already_exist[0], task[1], task[2], task[3], task[4]))
						# 再遍历一遍
						new_task_count = 0 # 记录新加入的任务数量
						for task in poset.task_data_list[0]:
							if task not in exist_sub_task_data_list:
								new_sub_task_data_list.append((new_task_count+n, task[1], task[2], task[3], task[4]))
								new_sub_task_idx_list[task[0]] = new_task_count + n
								new_task_count += 1
					else:
						for task in poset.task_data_list:
							new_sub_task_data_list.append((task[0] + n, task[1], task[2], task[3], task[4]))
					self.final_poset['action_map'].extend(new_sub_task_data_list)
					self.final_task_data_list.extend(new_sub_task_data_list)
					# 这里的i,j编号是相对于sub_poset而言的
					for i, j in sub_poset['<=']:
						# 如果偏序集合中的两个任务都已经被添加到final_poset['action_map']里了，且这个偏序集合还没有被加进去
						if poset.task_data_list[0][i] in exist_sub_task_data_list and poset.task_data_list[0][j] in \
							exist_sub_task_data_list and \
								(exist_sub_task_idx_list[i], exist_sub_task_idx_list[j]) not in self.final_poset['<=']:
							self.final_poset['<='].add((exist_sub_task_idx_list[i], exist_sub_task_idx_list[j]))
						elif poset.task_data_list[0][i] in exist_sub_task_data_list and poset.task_data_list[0][j] not in \
								exist_sub_task_data_list:
							self.final_poset['<='].add((exist_sub_task_idx_list[i], new_sub_task_idx_list[j]))
						elif poset.task_data_list[0][i] not in exist_sub_task_data_list and poset.task_data_list[0][j] in \
								exist_sub_task_data_list:
							self.final_poset['<='].add((new_sub_task_idx_list[i], exist_sub_task_idx_list[j]))
						else:
							self.final_poset['<='].add((new_sub_task_idx_list[i], new_sub_task_idx_list[j]))
					# for i, j in sub_poset['!=']:
					# 	self.final_poset['!='].add((i + n, j + n))
					for i, j in sub_poset['!=']:
						# 如果偏序集合中的两个任务都已经被添加到final_poset['action_map']里了，且这个偏序集合还没有被加进去
						# 问题是找到i,j在全局的poset中对应哪个编号
						if poset.task_data_list[0][i] in exist_sub_task_data_list and poset.task_data_list[0][j] in \
								exist_sub_task_data_list and \
								(exist_sub_task_idx_list[i], exist_sub_task_idx_list[j]) not in self.final_poset['!=']:
							self.final_poset['!='].add((exist_sub_task_idx_list[i], exist_sub_task_idx_list[j]))
						elif poset.task_data_list[0][i] in exist_sub_task_data_list and poset.task_data_list[0][
							j] not in \
								exist_sub_task_data_list:
							self.final_poset['!='].add((exist_sub_task_idx_list[i], new_sub_task_idx_list[j]))
						elif poset.task_data_list[0][i] not in exist_sub_task_data_list and poset.task_data_list[0][
							j] in \
								exist_sub_task_data_list:
							self.final_poset['!='].add((new_sub_task_idx_list[i], exist_sub_task_idx_list[j]))
						else:
							self.final_poset['!='].add((new_sub_task_idx_list[i], new_sub_task_idx_list[j]))
			if len(final_round_poset) == 0:
				final_round_poset = range(len(self.final_task_data_list))
			else:
				for i in range(len(self.final_task_data_list)):
					for j in final_round_poset:
						if not i in final_round_poset:
							self.final_poset['<='].add((j, i))
							self.final_poset['!='].add((j, i))
				final_round_poset = range(len(self.final_task_data_list))

	# 实际上只需要在添加一组考虑波次的order的即可

	def gantt_plotter(self, agent_data, poset, solution, task_time_table, path, idx):
		# # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
		# plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
		# plt.figure(figsize=(10, 5), dpi=80)
		# # fig, ax=plt.subplots()
		# max_time=max([time_list[2] for time_list in task_time_table])
		# color_dic = {}
		# color = ['b', 'c', 'r', 'y', 'm', 'g', 'gold', 'indigo', 'violet', 'lime', 'peru', 'pink', 'brown', 'b',
		# 		 'c', 'r', 'y', 'm', 'brown', 'b', 'c', 'r', 'y', 'm', 'g', 'gold', 'indigo', 'violet', 'b', 'c', 'r',
		# 		 'y', 'm', 'g', 'gold', 'indigo', 'violet', ]
		# # self.poset=poset
		# for i in range(35):
		# 	color_dic[i] = color[i]
		# i = 1
		# color_dic['error'] = color[i]
		# for agent in  solution:
		# 	for task in agent:
		# 		task_id=task[0][0]
		# 		plt.barh(i, task_time_table[task_id][2]-task_time_table[task_id][1],
		# 				 left=task_time_table[task_id][1], color=color_dic[task_id], linewidth=5,
		# 				  alpha=0.8)
		# 	# print('left=',time[task[0][0]][2])
		# 	i = i + 1
		#
		# plt.xlim(0, max_time//10*10+30)
		# plt.ylim(0, 20)
		# x_tick = np.linspace(0, max_time//10*10+30, 11)
		# y_tick = np.linspace(1, len(solution), 5)
		# plt.yticks(y_tick, fontsize=20)
		# plt.xticks(x_tick, fontsize=20)
		# text_list=[]
		# patches = [mpatches.Patch(color=color[i[0]], label=i[1]+i[2]) for i in poset['action_map']]
		# # self.ax.legend()
		# # plt.legend(loc='lower right', handles=patches, fontsize='25')
		# plt.legend(loc=2, bbox_to_anchor=(-0.03, 1.2), handles=patches, fontsize='15', ncol=5)
		#
		# plt.title("Task assigment Gantt graph", fontsize=30)
		# # XY轴标签
		# plt.xlabel("time/s", fontsize=30)
		# plt.ylabel("agent", fontsize=30)
		# plt.show()
		# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
		plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
		plt.figure(figsize=(22, 25))
		# fig, ax=plt.subplots()
		color_dic = {}
		color2 = plt.get_cmap('tab20')(range(20))
		# 生成50种不同的颜色
		hsv = [(x * 2.0 / 50, 0.5, 0.5) for x in range(50)]
		color1 = list(map(lambda x: mcolors.hsv_to_rgb(x), hsv))

		# self.poset=poset
		for i in range(len(color2)):
			color_dic[i] = color2[i]
		i = 1
		color_dic['error'] = color2[i]
		agent_id = 0
		for agent in solution:
			for task in agent:
				task_id = task[0][0]
				task_name = task[0][1] + '_' + task[0][2]
				duration = agent_data[agent_id][2][task_name][0]
				plt.barh(agent_id+1, duration,
						 left=task_time_table[task_id][1]-duration, color=color_dic[task_id], linewidth=5,
						 alpha=0.8)
			agent_id = agent_id + 1
		max_time = max([time_list[1] for time_list in task_time_table])
		plt.xlim(0, max_time // 10 * 10 + 30)
		plt.ylim(0, 21)
		x_tick = np.linspace(0, max_time // 10 * 10 + 30, 11)
		# y_tick = np.linspace(1, len(solution), 5)
		y_tick = [i for i in range(1, len(solution) + 1)]
		# y_tick_name = ['Agent'+str(i) for i in range(1,len(solution)+1) ]
		# y_tick_name = ['$A_{%s}$' % i for i in range(1, len(solution) + 1)]
		y_tick_name = []
		for agent in agent_data:
			y_tick_name.append(agent[1]+'_'+str(agent[3]))
		plt.yticks(y_tick, y_tick_name, fontsize=10)
		plt.xticks(x_tick, fontsize=16)
		text_list = []
		patches = [mpatches.Patch(color=color2[i[0]], label=i[1]+i[4]) for i in poset['action_map']]
		# self.ax.legend()
		# plt.legend(loc='lower right', handles=patches, fontsize='25')
		plt.legend(loc=2, bbox_to_anchor=(-0.03, 1.16), handles=patches, fontsize='16', ncol=7)

		plt.title("Task assignment Gantt graph", fontsize=20)
		# XY轴标签
		plt.xlabel("time/s", fontsize=20)
		plt.ylabel("agent", fontsize=20)
		plt.savefig(f'{path}/figures/offline_scene_0' + str(idx) + '_gantt.png', dpi=200, bbox_inches='tight')

		# plt.show()

	def gantt_plotter_online(self, agent_data, poset, solution1, task_time_table1, solution2, task_time_table2, break_time, \
							 online_calculate_time, broken_agent_list,
							 path, online_scene_idx):
		plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
		plt.figure(figsize=(22, 25))
		# fig, ax=plt.subplots()
		max_time = max([time_list[1] for time_list in task_time_table2])
		x_scale = (max_time + online_calculate_time) // 10 * 10 + 30
		color_dic = {}
  		# 生成50种不同的颜色
		hsv = [(x * 2.0 / 50, 0.5, 0.5) for x in range(50)]
		color1 = list(map(lambda x: mcolors.hsv_to_rgb(x), hsv))
		color2 = plt.get_cmap('tab20')(range(20))

		# self.poset=poset
		for i in range(len(color2)):
			color_dic[i] = np.array(color2[i]).reshape(1,-1)
		i = 1
		color_dic['error'] = color2[i]
		agent_id = 0
		for agent in solution1:
			for task in agent:
				task_id = task[0][0]
				task_name = task[0][1] + '_' + task[0][2]
				duration = agent_data[agent_id][2][task_name][0]
				if task_time_table1[task_id][1] - duration < break_time:
					plt.barh(agent_id+1, duration,
							 left=task_time_table1[task_id][1]-duration, color=color_dic[task_id], linewidth=5,
							 alpha=0.8)
				# elif task_time_table1[task_id][1]-duration < break_time < task_time_table1[task_id][1]:
				# 	plt.barh(agent_id+1, break_time - task_time_table1[task_id][1] + duration,
				# 			 left=task_time_table1[task_id][1]-duration, color=color_dic[task_id], linewidth=5,
				# 			 alpha=0.8)
			agent_id = agent_id + 1

		agent_id = 0
		for agent in solution2:
			for task in agent:
				task_id = task[0][0]
				task_name = task[0][1] + '_' + task[0][2]
				duration = agent_data[agent_id][2][task_name][0]
				for time_table in task_time_table2:
					if task_id in time_table:
						table = time_table
				plt.barh(agent_id+1, duration, left=table[1]-duration+online_calculate_time, color=color_dic[task_id], linewidth=5)
			agent_id = agent_id + 1
		# for agent in solution2:
		# 	for task in agent:
		# 		task_id = task[0][0]
		# 		if task_time_table2[task_id][1] >= break_time:
		# 			plt.barh(i, task_time_table2[task_id][2] - task_time_table2[task_id][1],
		# 					 left=task_time_table2[task_id][1]+online_calculate_time, color=color_dic[task_id], linewidth=5)
		# 	i = i + 1
		# 在图中标注出损坏的智能体
		for broken_agent in broken_agent_list:
			line_x = np.linspace(break_time, x_scale, 1000)
			line_y_up = [broken_agent+1+0.3 for i in range(len(line_x))]
			line_y_bottom = [broken_agent+1-0.3 for i in range(len(line_x))]
			plt.plot(line_x, line_y_up, color='black',linewidth=0.5)
			plt.plot(line_x, line_y_bottom, color='black', linewidth=0.5)
			plt.text(break_time+online_calculate_time+2, broken_agent+0.8, agent_data[broken_agent][1]+'_'+str(agent_data[broken_agent][3])+' is broken',
					 fontdict={'size':9})
		# plt.axvline(x=break_time, linestyle='--', color='r')
		# plt.axvline(x=break_time+online_calculate_time, linestyle='--', color='r')
		xline = np.linspace(break_time, break_time+online_calculate_time, 100)
		agent_num = len(agent_data)
		plt.fill_between(xline, 0, agent_num+1, facecolor='grey')
		# plt.text(break_time+online_calculate_time+2, 18, 'Online Adaptation',fontdict=
		# 				{'size': 9, 'color': 'red'})
		plt.xlim(0, x_scale)
		plt.ylim(0, agent_num+1)

		x_tick = np.linspace(0, x_scale, 11)
		# y_tick = np.linspace(1, len(solution), 5)
		y_tick = [i for i in range(1, len(solution2) + 1)]
		# y_tick_name = ['Agent'+str(i) for i in range(1,len(solution)+1) ]
		# y_tick_name = ['$A_{%s}$' % i for i in range(1, len(solution2) + 1)]
		y_tick_name = []
		for agent in agent_data:
			y_tick_name.append(agent[1]+'_'+str(agent[3]))
		plt.yticks(y_tick, y_tick_name, fontsize=10)
		plt.xticks(x_tick, fontsize=16)
		text_list = []
		# action_map中可能会有重复的元素
		patches = [mpatches.Patch(color=color2[i[0]], label=i[1]+i[4]) for i in poset['action_map']]
		patches.append(mpatches.Patch(color = 'grey', label = 'online replan'))
		# self.ax.legend()
		# plt.legend(loc='lower right', handles=patches, fontsize='25')
		plt.legend(loc=2, bbox_to_anchor=(-0.03, 1.16), handles=patches, fontsize='13', ncol=7)

		plt.title("Task assignment Gantt graph", fontsize=20)
		# XY轴标签
		plt.xlabel("time/s", fontsize=20)
		plt.ylabel("agent", fontsize=20)
		plt.savefig(f'{path}/figures/online_scene_0' + str(online_scene_idx) + '_gantt.png', dpi=200, bbox_inches='tight')

		# plt.show()


def Turn_Matrix(self, M):
	r = [[] for i in M[0]]
	for i in M:
		for j in range(len(i)):
			r[j].append(i[j])
	return r
