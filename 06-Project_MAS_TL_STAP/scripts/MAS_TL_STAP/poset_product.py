import os
import numpy as np
import cvxpy as cp

import matplotlib.pyplot as plt
from graphviz import Source, Digraph
import matplotlib.patches as mpatches

from .poset_builder import Buchi_poset_builder

class DotGraph:
    """
    Class for the graph in DOT format, which is used to draw the buchi automaton.
    """
    def __init__(self):
        self.dot = Digraph()

    def title(self, str):
        self.dot.graph_attr.update(label=str)

    def node(self, name, label, accepting=False):
        num_peripheries = '2' if accepting else '1'
        self.dot.node(name, label, shape='box', peripheries=num_peripheries)

    def edge(self, src, dst, label):
        self.dot.edge(src, dst, label)

    def show(self):
        self.dot.render(view=True)

    def save_render(self, path, on_screen):
        self.dot.render(path, view=on_screen)

    def save_dot(self, path):
        self.dot.save(path)

    def __str__(self):
        return str(self.dot)


class Poset_producter(object):
	def __init__(self, formula_list):
		"""
		这部分为偏序处理部分，用于优化偏序结构，处理一些参数细节等等。
		"""
		self.poset_list = formula_list
		self.gantt_data_dic = dict()
		self.final_poset = {'||': set(),
							'<=': set(),
							'<': set(),
							'!=': set(),
							'=': set(),
							'action_map': list()}
	def generate_poset(self):
		self.ltl2poset = dict()
		self.ltl2poset[1] = list()
		for formula in self.poset_list :
				buchi = Buchi_poset_builder(formula)
				buchi.main_fun_to_get_poset(20)
				self.ltl2poset[1].append(buchi)

	def prodocter(self):
		self.final_task_data_list = []
		final_round_poset = {}
		for round, ltl2poset in self.ltl2poset.items():
			for poset in ltl2poset:
				sub_poset = poset.poset_list[0]
				sub_task_data_list = poset.task_data_list[0]
				#judge the task list
				if len(self.final_poset['action_map'])==0:
					self.final_poset['action_map'] = poset.task_data_list[0]
					self.final_poset['<=']=sub_poset['<=']
					self.final_poset['!=']=sub_poset['!=']
					self.final_task_data_list.extend(sub_task_data_list)
				else:
					n = len(self.final_poset['action_map'])
					new_sub_task_data_list=[]
					if len(np.shape(poset.task_data_list))==3:
						for task in poset.task_data_list[0] :
							# new_sub_task_data_list.append((task[0]+n,task[1],task[2],task[3],task[4]))
							new_sub_task_data_list.append((task[0]+n, task[1], task[2], task[3],))
					else:
						for task in poset.task_data_list :
							# new_sub_task_data_list.append((task[0]+n,task[1],task[2],task[3],task[4]))
							new_sub_task_data_list.append((task[0]+n, task[1], task[2], task[3],))
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

	def draw_poset(self,  view=True):
		"""
		Draw the graph of the buchi automaton by DOT.
		"""
		dirpath = os.path.abspath(os.path.dirname(
									os.path.dirname(
										os.path.dirname(__file__))))
		path = os.path.join(dirpath, 'figures', 'poset')
		graph = DotGraph()
		for act in self.final_poset['action_map']:
			graph.node(act[1], act[1])
		for leq_str, leq_dst in self.final_poset['<=']:
			act_str = self.final_poset['action_map'][leq_str][1]
			act_dst = self.final_poset['action_map'][leq_dst][1]
			graph.edge(act_str, act_dst, '<=')
		for neq_str, neq_dst in self.final_poset['!=']:
			act_str = self.final_poset['action_map'][neq_str][1]
			act_dst = self.final_poset['action_map'][neq_dst][1]
			graph.edge(act_str, act_dst, '!=')
		graph.save_render(path, view)

	def gantt_plotter(self,  poset, estimate_time_table, task_time_table, path, scene_index):
		# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
		plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
		plt.figure(figsize=(19.2,10.8))
		# fig, ax=plt.subplots()
		max_time = max([time_list[2] for time_list in task_time_table])
		color_dic = {}
		color = plt.get_cmap('tab20')(range(20))

		# self.poset=poset
		for i in range(len(color)):
			color_dic[i] = color[i]
		i = 1
		color_dic['error'] = color[i]
		for agent in  estimate_time_table:
			for task in agent:
				task_id=task[0][0]
				plt.barh(i, task_time_table[task_id][2]-task_time_table[task_id][1],
						 left=task_time_table[task_id][1], color=color_dic[task_id], linewidth=5,
						  alpha=0.8)
			# print('left=',time[task[0][0]][2])
			i = i + 1

		plt.xlim(0, max_time//10*10+30)
		plt.ylim(0, 21)
		x_tick = np.linspace(0, max_time//10*10+30, 11)
		# y_tick = np.linspace(1, len(estimate_time_table), 5)
		y_tick = [i for i in range(1,len(estimate_time_table)+1)]
		# y_tick_name = ['Agent'+str(i) for i in range(1,len(estimate_time_table)+1) ]
		y_tick_name = ['$A_{%s}$'%i for i in range(1, len(estimate_time_table) + 1)]
		plt.yticks(y_tick, y_tick_name,fontsize=16)
		plt.xticks(x_tick, fontsize=16)
		text_list=[]
		patches = [mpatches.Patch(color=color[i[0]], label=i[1]) for i in poset['action_map']]
		# self.ax.legend()
		# plt.legend(loc='lower right', handles=patches, fontsize='25')
		plt.legend(loc=2, bbox_to_anchor=(-0.03, 1.16), handles=patches, fontsize='16', ncol=7)

		plt.title("Task assignment Gantt graph", fontsize=20)
		# XY轴标签
		plt.xlabel("time/s", fontsize=20)
		plt.ylabel("agent", fontsize=20)
		plt.savefig(f'{path}/figures/demo_0'+str(scene_index)+'_gantt.png', dpi=200, bbox_inches='tight')
		# plt.show()

	def Turn_Matrix(self, M):
		r = [[] for i in M[0]]
		for i in M:
			for j in range(len(i)):
				r[j].append(i[j])
		return r