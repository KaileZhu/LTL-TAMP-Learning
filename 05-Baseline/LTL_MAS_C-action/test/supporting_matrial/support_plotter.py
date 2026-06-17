import matplotlib.pyplot as plt
import  matplotlib.animation as animation
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
import networkx as nx
import copy

class Support_Plotter(object):
	def __init__(self,data_name,task_data,solution,task_time_table):
		self.task_data=task_data
		self.solution=solution
		self.task_time_table=task_time_table
		self.trajectory=np.load(data_name).item()
		self.task_data_list = [(0, 'scanp2', 'p1'),
		                  (1, 'fixt1', 't1'),
		                  (2, 'washp5', 'p5'),
		                  (3, 'repairp2', 'p2'),
		                  (4, 'scanp3', 'p2'),
		                  (5, 'sweepp2', 'p2')]
		self.agent_data=[(0,'b1','UAV'),
                    (1,'b1','UAV'),
                    (2,'b1','UAV'),
                    (3,'b1','UAV'),
                    (1,'b1','UGV_s'),
                    (2,'b1','UGV_l'),
                       ]
		self.agent_trajectory_x = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
		self.agent_trajectory_y = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
		self.agent_state = [[], [], [], [], [], []]
		for time, agent_path in self.trajectory.items():
			i = 0
			for agent_pose, state in agent_path:
				self.agent_trajectory_x[i].append(agent_pose[0])
				self.agent_trajectory_y[i].append(agent_pose[1])
				self.agent_state[i].append(state)
				i = i + 1
		estimate_task_time_table = [[] for i in range(6)]
		count = 0
		for task_list in self.trajectory.items():
			count = count + 1
			for i in range(6):
				if task_list[1][i][1] not in ['motion', 'stay']:
					if not len(estimate_task_time_table[i]) == 0:
						if task_list[1][i][1] == estimate_task_time_table[i][-1][0]:
							if estimate_task_time_table[i][-1][2] + 1 == count:
								estimate_task_time_table[i][-1][2] = count
							else:
								estimate_task_time_table[i].append([task_list[1][i][1], count, count])
						else:
							estimate_task_time_table[i].append([task_list[1][i][1], count, count])
					else:
						estimate_task_time_table[i].append([task_list[1][i][1], count, count])
		self.estimate_task_time_table=estimate_task_time_table
		self.new_solution=[[((2, 'washp5', 'p5'), 'wash_UAV'),((0, 'scanp1', 'p1'), 'scan'),((4, 'scanp2', 'p2'), 'scan') ],
        [((0, 'scanp1', 'p1'), 'scan'), ((4, 'scanp2', 'p2'), 'scan')],
        [((0, 'scanp1', 'p1'), 'scan'), ((4, 'scanp2', 'p2'), 'scan')],
        [],
 [((3, 'repairp2', 'p2'), 'repair_UGV_s'),
  ((5, 'sweepp2', 'p2'), 'sweep'),
  ((1, 'fixt1', 't1'), 'fix_UGV_s')],
 [((2, 'washp5', 'p5'), 'wash_UGV_l'),
  ((3, 'repairp2', 'p2'), 'repair_UGV_l'),
  ((1, 'fixt1', 't1'), 'fix_UGV_l')]]

	def draw_barchart(self,current_time):
		self.ax.clear()
		self.ax.plot([current_time,current_time],[-1,7],color='black',lw=5)
		self.ax.text(-1,1,str(current_time),size=1)
		color_dic = {}
		color = ['b', 'c', 'k', 'r', 'y', 'm', 'g', 'aqua', 'brown', 'cya']
		i=0
		for i in range(6):
			color_dic[self.task_data_list[i][1]] = color[i]
			i=i+1
		color_dic['error'] = color[i]
		i=-1
		executing_task={}
		unfinished_task={}
		last_execute_task=[[],[],[],[],[],[]]
		for agent in self.estimate_task_time_table:
			i=i+1
			for task in agent:
				if not task[0] == 'error':
					#print(task)
					if task[1]< current_time:
						last_execute_task[i].append(task[0])
						if task[2]< current_time:
							self.ax.barh(i+1, task[2] - task[1], left=task[1], color=color_dic[task[0]])
						else:
							self.ax.barh(i+1, current_time - task[1], left=task[1], color=color_dic[task[0]])
							executing_task[task[0]]=task[1]
					else:
						unfinished_task[task[0]]=task[2]
		#===== extimate the new time
		to_add_time=[]
		i=0
		print('time',current_time)
		print('executing_Task',executing_task)
		print('unfinished_task',unfinished_task)
		print('last_execute_Task',last_execute_task)
		for agent in self.solution:
			estimate_time=0
			j=0
			for task in self.solution[i]:
				#print(task)
				if task[0][1] in executing_task.keys():
					#if self.task_time_table[task[0][0]][2] > current_time  :
						estimate_time=executing_task[task[0][1]]-self.task_time_table[task[0][0]][1]
						estimate_time2=current_time-self.task_time_table[task[0][0]][2]
						estimate_time=max(estimate_time2,estimate_time)
						break
				else:
					if len(last_execute_task[i])==0:
						estimate_time2=current_time-self.task_time_table[task[0][0]][1]
						estimate_time=max(estimate_time2,estimate_time)
						break
					if j==len(last_execute_task[i])-1:
						#print('last_execute_task',last_execute_task[i])
						#print('j',j,'i',i)
						#print('task',task)
						#print(self.task_time_table[task[0][0]][1])
						#print(self.estimate_task_time_table[i][j])
						estimate_time=-self.task_time_table[task[0][0]][2]+self.estimate_task_time_table[i][j][2]
						if j+2<=len(self.solution[i]):
							estimate_time2=current_time-self.task_time_table[self.solution[i][j+1][0][0]][1]
						else:
							estimate_time2=0
						estimate_time=max(estimate_time2,estimate_time)
						#print('estimate_time',estimate_time)
						break
				j=j+1

			to_add_time.append(estimate_time)
			i=i+1
		#=====draw the left graph
		i=0
		#print(to_add_time)
		#print(color_dic)
		for agent in self.solution:
			j=0
			for task in agent:
				#print('task',task)
				if task[0][1] in executing_task.keys():
					right_time=self.task_time_table[task[0][0]][2]+to_add_time[i]
					left_time=executing_task[task[0][1]]
					self.ax.barh(i+1, right_time - left_time, left=left_time, color=color_dic[task[0][1]],alpha=0.4)
				elif task[0][1] in unfinished_task.keys():
					#print(task)
					right_time=self.task_time_table[task[0][0]][2]+to_add_time[i]
					left_time=self.task_time_table[task[0][0]][1]+to_add_time[i]
					self.ax.barh(i+1, right_time - left_time, left=left_time, color=color_dic[task[0][1]],alpha=0.4)
				j=j+1
			i=i+1
		#index_list=[agent[2]+' '+str(agent[0]+1) for agent in  self.agent_data]
		index_list=["$V_{f1}$",'$V_{f2}$','$V_{f3}$','$V_{f4}$','$V_{s1}$','$V_{l1}$']
		i=0
		for name in index_list:
			self.ax.text(-25,i+1,name,size=30,va='center')
			i=i+1
		plt.xlim(0, 230)
		plt.ylim(0.5,6.5)
		plt.xticks(np.arange(0,240,50),size=30)
		x_tick = np.linspace(0, 220, 23)
		y_tick = np.linspace(1, 6, 6)
		#self.ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
		#self.ax.xaxis.set_ticks_position('top')
		self.ax.yaxis.set_ticklabels([])
		labels = [''] * 6
		for f in range(len(labels) - 1):
			labels[f] = "task%d" % (f + 1)
		labels = []
		for subtask in self.task_data_list:
			labels.append(subtask[1])
		# 图例绘制
		labels=['$scan_{p2}$','$fix_{t1}$','$wash_{p5}$','$repair_{p2}$','$scan_{p3}$','$sweep_{p2}$']
		patches = [mpatches.Patch(color=color[i], label="{:s}".format(labels[i])) for i in range(len(labels))]
		#self.ax.legend()
		#plt.legend(loc='lower right', handles=patches, fontsize='25')
		plt.legend(loc=2, bbox_to_anchor=(-0.03, 1.5), handles=patches, fontsize='35', ncol=3)
		# XY轴标签
		plt.xlabel("time/s", fontsize=30)
		#plt.ylabel("agent ID", fontsize=30)

	def animate_plotter(self,end=85,interval=50):
		time_lenth=len(self.trajectory)
		#self.time_plotter=plt.text(-1,1,'',size=50)
		self.fig, self.ax = plt.subplots(figsize=(15, 12))
		self.fig.subplots_adjust(top=0.7,bottom=0.13)
		#self.time_plotter=plt.text(-1,1,'',size=50)
		plt.fill([0,220,220,0],[-0.5,-0.5,6.5,6.5],'palegoldenrod')
		animator = animation.FuncAnimation(self.fig, self.draw_barchart, frames=range(0, end), interval=interval,repeat=False)
		#animator.save('gantt_normal3.gif')
		plt.show()

	def adapt_pretreatment(self):
		#print(self.estimate_task_time_table[0])
		#print(self.estimate_task_time_table[1])
		#print(self.estimate_task_time_table[2])
		self.estimate_task_time_table[0]=[['washp5', 33, 63], ['scanp3', 81, 96], ['scanp2', 131, 144]]
		self.estimate_task_time_table[1]=[['scanp3', 81, 96],  ['scanp2', 131, 144]]
		self.estimate_task_time_table[2]=[['scanp3', 81, 96],  ['scanp2', 131, 144]]
		#adapt
		self.agent_stay_list_normal1={0:[(7,30),(100,128),(143, 220)],
		                      1:[(15,84),(106,135),(146,220)],
		                      2:[(11,82),(106,134),(145,220)],
		                      3:[(8,90),(145,220)],
		                      4:[(24,106)],
		                      5:[(156,210)]}
		#normal
		self.agent_stay_list_normal={0:[(100,220)],
		                      1:[(14,84),(105,135),(146,220)],
		                      2:[(11,80),(106,134),(145,220)],
		                      3:[(12,130),(145,220)],
		                      4:[(24,106)],
		                      5:[(160,208)]}
		self.agent_stay=[0,0,0,0,0,0]


	def draw_barchart_adapt(self,current_time):
		self.ax.clear()
		self.ax.plot([current_time,current_time],[-1,7],color='black',lw=5)
		if current_time>95:
			self.ax.plot([94,94],[-1,7],color='red',lw=6)
			self.task_time_table=self.new_task_time_table
			self.solution=self.new_solution
			self.ax.barh(4,current_time-94,left=94,color='white',hatch='/')
		color_dic = {}
		color = ['b', 'c', 'k', 'r', 'y', 'm', 'g', 'aqua', 'brown', 'cya']
		i=0
		for i in range(6):
			color_dic[self.task_data_list[i][1]] = color[i]
			i=i+1
		color_dic['error'] = color[i]
		i=-1
		executing_task={}
		unfinished_task={}
		last_execute_task=[[],[],[],[],[],[]]
		for agent in self.estimate_task_time_table:
			i=i+1
			for task in agent:
				if not task[0] == 'error':
					#print(task)
					if task[1]< current_time:
						last_execute_task[i].append(task[0])
						if task[2]< current_time:
							self.ax.barh(i+1, task[2] - task[1], left=task[1], color=color_dic[task[0]])
						else:
							self.ax.barh(i+1, current_time - task[1], left=task[1], color=color_dic[task[0]])
							executing_task[task[0]]=task[1]
					else:
						unfinished_task[task[0]]=task[2]
		#===== extimate the new time
		to_add_time=[]
		i=0
		#print('executing_Task',executing_task)
		#print('unfinished_task',unfinished_task)
		#print('last_execute_Task',last_execute_task)
		for agent in self.solution:
			estimate_time=0
			j=0
			for task in self.solution[i]:
				#print(task)
				if task[0][1] in executing_task.keys():
					#if self.task_time_table[task[0][0]][2] > current_time  :
						estimate_time=executing_task[task[0][1]]-self.task_time_table[task[0][0]][1]
						estimate_time2=current_time-self.task_time_table[task[0][0]][2]
						estimate_time=max(estimate_time2,estimate_time)
						break
				else:
					if len(last_execute_task[i])==0:
						estimate_time2=current_time-self.task_time_table[task[0][0]][1]
						estimate_time=max(estimate_time2,estimate_time)
						break
					if i in []:
						if current_time>95:
							print('last_execute_task',last_execute_task[i])
							print('j',j,'i',i)
							print('task',task)
							#print(self.task_time_table[task[0][0]][1])
							#print(self.estimate_task_time_table[i][j])
							estimate_time=-self.task_time_table[task[0][0]][2]+self.estimate_task_time_table[i][j][2]
							if j+2<=len(self.solution[i]):
								estimate_time2=current_time-self.task_time_table[self.solution[i][j+1][0][0]][1]
							else:
								estimate_time2=0
							estimate_time=max(estimate_time2,estimate_time)
							print('estimate_time',estimate_time)
							break
					if j==len(last_execute_task[i])-1:
						#print('last_execute_task',last_execute_task[i])
						#print('j',j,'i',i)
						#print('task',task)
						#print(self.task_time_table[task[0][0]][1])
						#print(self.estimate_task_time_table[i][j])
						estimate_time=-self.task_time_table[task[0][0]][2]+self.estimate_task_time_table[i][j][2]
						if j+2<=len(self.solution[i]):
							estimate_time2=current_time-self.task_time_table[self.solution[i][j+1][0][0]][1]
						else:
							estimate_time2=0
						estimate_time=max(estimate_time2,estimate_time)
						print('estimate_time',estimate_time)
						break
				j=j+1

			to_add_time.append(estimate_time)
			i=i+1
		#=====draw the left graph
		i=0
		print(to_add_time)
		#print(color_dic)
		for agent in self.solution:
			j=0
			for task in agent:
				#print('task',task)
				if task[0][1] in executing_task.keys():
					right_time=self.task_time_table[task[0][0]][2]+to_add_time[i]
					left_time=executing_task[task[0][1]]
					self.ax.barh(i+1, right_time - left_time, left=left_time, color=color_dic[task[0][1]],alpha=0.4)
				elif task[0][1] in unfinished_task.keys():
					#print(task)
					right_time=self.task_time_table[task[0][0]][2]+to_add_time[i]
					left_time=self.task_time_table[task[0][0]][1]+to_add_time[i]
					self.ax.barh(i+1, right_time - left_time, left=left_time, color=color_dic[task[0][1]],alpha=0.4)
				j=j+1
			i=i+1
		#index_list=[agent[2]+' '+str(agent[0]+1) for agent in  self.agent_data]
		index_list=["$V_{f1}$",'$V_{f2}$','$V_{f3}$','$V_{f4}$','$V_{s1}$','$V_{l1}$']
		i=0
		for name in index_list:
			self.ax.text(-25,i+1,name,size=30,va='center')
			i=i+1
		plt.xlim(0, 230)
		plt.ylim(0.5,6.5)
		plt.xticks(np.arange(0,240,50),size=30)
		x_tick = np.linspace(0, 220, 23)
		y_tick = np.linspace(1, 6, 6)
		#self.ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
		#self.ax.xaxis.set_ticks_position('top')
		self.ax.yaxis.set_ticklabels([])
		labels = [''] * 6
		for f in range(len(labels) - 1):
			labels[f] = "task%d" % (f + 1)
		labels = []
		for subtask in self.task_data_list:
			labels.append(subtask[1])
		# 图例绘制
		labels=['$scan_{p2}$','$fix_{t1}$','$wash_{p5}$','$repair_{p2}$','$scan_{p3}$','$sweep_{p2}$']
		patches = [mpatches.Patch(color=color[i], label="{:s}".format(labels[i])) for i in range(len(labels))]
		#self.ax.legend()
		#plt.legend(loc='lower right', handles=patches, fontsize='25')
		plt.legend(loc=2, bbox_to_anchor=(-0.03, 1.5), handles=patches, fontsize='35', ncol=3)
		# XY轴标签
		plt.xlabel("time/s", fontsize=30)
		#plt.ylabel("agent ID", fontsize=30)

	def animate_plotter_adapt(self,interval=50):
		self.adapt_pretreatment()
		time_lenth=len(self.trajectory)
		self.fig, self.ax = plt.subplots(figsize=(15, 12))
		self.fig.subplots_adjust(top=0.7,bottom=0.13)
		plt.fill([0,220,220,0],[-0.5,-0.5,6.5,6.5],'palegoldenrod')
		animator = animation.FuncAnimation(self.fig, self.draw_barchart_adapt, frames=range(0, 230), interval=interval,repeat=False)
		animator.save('gantt_adapt3.gif')
		#plt.show()

	def pre_treat_poset(self,poset):
		self.poset=poset
		poset_graph=nx.DiGraph()
		self.neq_graph=nx.DiGraph()
		for i,j in self.poset['<=']:
			poset_graph.add_edge(i,j)
		for i,j in self.poset['!=']:
			self.neq_graph.add_edge(i,j)
			self.neq_graph.add_edge(j,i)
		for i in range(len(self.task_data)):
			if not self.neq_graph.has_node(i):
				self.neq_graph.add_node(i)
		for i in range(len(self.task_data)):
			if not poset_graph.has_node(i):
				poset_graph.add_node(i)
		self.poset_graph = poset_graph
		node_set = []
		for i in self.poset_graph.nodes():
			node_set.append(i)
		for i in node_set:
			self.poset_graph.add_edge('root', i)

	def draw_poset_adapt(self,current_time):
		self.time_plotter.set_text(str(current_time))
		#self.ax.clear()
		color_dic={}
		color=['b', 'c', 'k', 'r', 'y', 'm', 'g', 'aqua', 'brown', 'cya']
		i=0
		for i in range(6):
			color_dic[self.task_data_list[i][1]] = color[i]
			i=i+1
		color_dic['error'] = color[i]
		executing_task={}
		unfinished_task={}
		started_task={}
		finished_task=[]
		for agent in self.estimate_task_time_table:
			i=i+1
			for task in agent:
				if not task[0] == 'error':
					if task[1]< current_time:
						started_task[task[0]]=task[1]
						if task[2]< current_time:
							finished_task.append(task[0])
						else:
							executing_task[task[0]]=task[1]
					else:
						unfinished_task[task[0]]=task[2]
		#=======================

		#============= get infeasible subtasks
		infeasible_subtasks=set()
		task_name2id={}
		for task in self.task_data:
			task_name2id[task[1]]=task[0]
		#print(task_name2id)
		for task in executing_task.keys():
			#print(task_name2id[task])
			#print(self.neq_graph.succ[task_name2id[task]])
			for subtask in self.neq_graph.succ[task_name2id[task]]:
				#print('infeasible subtask',subtask)
				infeasible_subtasks.add(subtask)
		feasible_subtasks=set()
		started_key=[task_name2id[task] for task in started_task.keys()]
		started_key.append('root')
		#print('started_key',started_key)
		for task in self.poset_graph.nodes:
			feasible = 1
			#print(self.poset_graph.pred[task])
			#print('parent_node',task)
			for subtask in self.poset_graph.pred[task].keys():
				#print('subtask',subtask)
				if not subtask in started_key:
					feasible=0
			if feasible:
				feasible_subtasks.add(task)
			else:
				infeasible_subtasks.add(task)
			if len(self.poset_graph.pred[task].keys())==1:
				#print('pre',self.poset_graph.pred[task].keys())
				feasible_subtasks.add(task)
		feasible_subtasks=feasible_subtasks-{'root'}
		feasible_subtasks=feasible_subtasks-infeasible_subtasks
		print('time',current_time)
		print('infeasible',infeasible_subtasks)
		print('feasible',feasible_subtasks)
		print('started',started_task)
		print('finished',finished_task)
		print('executing',executing_task)
		#==============plot square
		#for task in range(6):
		#	self.rec_color_list[task].set_color('white')
		for task in feasible_subtasks:
			self.rec_color_list[task].set_color('green')
		for task in executing_task:
			self.rec_color_list[task_name2id[task]].set_color('yellow')
		#for task in started_task:
			#self.rec_color_list[task_name2id[task]].set_color('yellow')
		for task in infeasible_subtasks:
			self.rec_color_list[task].set_color('red')
		for task in finished_task:
			self.rec_color_list[task_name2id[task]].set_color('gray')


		#===== extimate the new time


	def animate_plotter_poset(self,interval=100,end=230):
		self.adapt_pretreatment()
		time_lenth=len(self.trajectory)
		self.fig, self.ax = plt.subplots(figsize=(15, 12))
		task_name=['$scan_{p3}$','$fix_{t1}$','$wash_{p5}$','$repair_{p2}$','$scan_{p2}$','$sweep_{p2}$']
		t=0
		squire_pose_list=[(-3,1),(-1,1),(3.3,1),(1,1),(1,3.5),(3.2,3.5)]
		width=[1.8,1.4,1.8,2.0,1.8,2.2]
		plt.arrow(0.3,1.1,0,1.3,
                          length_includes_head=True,head_width=0.05,lw=8,color='red')
		plt.arrow(0.3,2.4,0,-1.3,
                          length_includes_head=True,head_width=0.05,lw=8,color='red')
		plt.arrow(0.5,1.1,0,1.3,
                          length_includes_head=True,head_width=0.05,lw=8,color='black')
		plt.arrow(1.4,1.1,1.8,1.3,
                          length_includes_head=True,head_width=0.05,lw=8,color='red')
		plt.arrow(3.2,2.4,-1.8,-1.3,
                          length_includes_head=True,head_width=0.05,lw=8,color='red')
		plt.arrow(1.0,1.1,1.8,1.3,
                          length_includes_head=True,head_width=0.05,lw=8,color='black')
		self.time_plotter=plt.text(-0,1,'',size=2)
		self.rec_color_list=[]
		for i,j in squire_pose_list:
			rec=plt.Rectangle((i-1.2,j-1),width[t],1,color='green',fill=None,zorder=3)
			self.ax.add_artist(rec)
			self.ax.text(i-1,j-0.5,task_name[t],color='black',size=45,va='center',zorder=3)
			rec1=plt.Rectangle((i-1.2,j-1),width[t],1,color='white',zorder=0,)
			self.ax.add_artist(rec1)
			self.rec_color_list.append(rec1)
			t=t+1
		plt.axis('off')
		color=['green','red','gray','yellow']
		labels=['feasible subtask','infeasible subtask','finished subtask','executing subtask']
		patches = [mpatches.Patch(color=color[i], label="{:s}".format(labels[i])) for i in range(len(labels))]
		#self.ax.legend()
		#plt.legend(loc='lower right', handles=patches, fontsize='25')
		plt.legend(loc=2, bbox_to_anchor=(0.2, 1.1),handles=patches, fontsize='40', ncol=1)
		plt.xlim(-4.4,4.2)
		plt.ylim(-0.5,5.8)
		#plt.fill([-4,4,4,-4],[-1,-1,4,4],'palegoldenrod')
		animator = animation.FuncAnimation(self.fig, self.draw_poset_adapt, frames=range(0, end), interval=interval,repeat=False)
		animator.save('poset_adapt_with_time_3.gif')
		#plt.show()

	def draw_state_adapt(self,current_time):
		#self.ax.clear()
		self.time_plotter.set_text(str(current_time))
		color_dic={}
		color=['b', 'c', 'k', 'r', 'y', 'm', 'g', 'aqua', 'brown', 'cya']
		i=0
		for i in range(6):
			color_dic[self.task_data_list[i][1]] = color[i]
			i=i+1
		color_dic['error'] = color[i]
		i=0
		current_state=[]
		for agent in self.estimate_task_time_table:
			j=0
			for task in agent:
				if task[1]<=current_time:
					if task[2]>=current_time:
						current_state.append(task[0])
			ifstay=0
			if agent[-1][2]<current_time:
				self.agent_stay[i]=1
			if len(current_state)<i+1:
				current_state.append('search')
			i=i+1
		print(current_state)
		i=0
		word_dic={'scanp3':'$scan_{p3}$','fixt1':'$fix_{t1}$','washp5':'$wash_{p5}$',
		          'repairp2':'$repair_{p2}$','scanp2':'$scan_{p2}$','sweepp2':'$sweep_{p2}$'}
		print(current_time)
		for state in current_state:
			if self.agent_stay[i]==1:
				if state=='error':
					self.agent_label_list[i].set_text('error')
					self.agent_label_list[i].set_color('red')
				else:
					self.agent_label_list[i].set_text('stay')
				i=i+1
				continue
			if state=='search':
				#check if motion
				motion=1
				print(self.agent_stay_list_normal[i])
				for start, end in self.agent_stay_list_normal[i]:
					if start<=current_time:
						if end>=current_time:
							motion=0
				if motion:
					self.agent_label_list[i].set_text('motion')
				else:
					self.agent_label_list[i].set_text('wait for cooperator')
					#self.ax.text(agent_pose_list[i][0]+0.5,agent_pose_list[i][1],'motion')
			elif state=='error':
				self.agent_label_list[i].set_text('error')
				self.agent_label_list[i].set_color('red')
				#self.ax.text(agent_pose_list[i][0]+0.5,agent_pose_list[i][1],'error',color='red')
			else:
				print(state)
				self.agent_label_list[i].set_text(word_dic[state])
				#self.ax.text(agent_pose_list[i][0]+0.5,agent_pose_list[i][1],state)
			i=i+1



	def animate_plotter_state(self,normal=1,interval=50):
		self.adapt_pretreatment()
		index_list = ["$V_{f1}$", '$V_{f2}$', '$V_{f3}$', '$V_{f4}$', '$V_{s1}$', '$V_{l1}$']
		agent_pose_list=[(-4.5,1),(0,1),(4.5,1),(-4.5,-0),(0,-0),(4.5,-0)]
		self.fig, self.ax = plt.subplots(figsize=(21, 4))
		plt.text(9,0,'SPEED X3',size=50)
		#plot agent label
		for i in range(4):
			l = 0.15
			agent_shape_x = [agent_pose_list[i][0] + n for n in [-l, l, -l, l]]
			agent_shape_y = [agent_pose_list[i][1]-0.1 + n for n in [-l, -l, l, l]]
			agent_edge_x = [agent_pose_list[i][0] + n for n in [-l, l, 0, -l, l]]
			agent_edge_y = [agent_pose_list[i][1] -0.1+ n for n in [-l, l, 0, l, -l]]
			plt.plot(agent_edge_x, agent_edge_y, 'black', linewidth=3)
			plt.plot(agent_shape_x, agent_shape_y, 'ro', markersize=12, zorder=3)
			plt.text(agent_pose_list[i][0]+0.23,agent_pose_list[i][1]-0.2,'$V_{f'+str(i+1)+'}:$',size=30)
		ugv_nm=30
		shape_list=[[agent_pose_list[4][0]+n/ugv_nm,agent_pose_list[4][1]-0.1+m/ugv_nm] for n,m in [(-5,-4),(5,-4),(7,0),(5,4),(-5,4)]]
		cl='g'
		p01=plt.Polygon(shape_list,color=cl,alpha=1,zorder=2)
		po=plt.Polygon(shape_list,color='black',alpha=1,fill=None,zorder=3)
		self.ax.add_patch(p01)
		self.ax.add_patch(po)
		plt.text(agent_pose_list[4][0]+0.23,agent_pose_list[4][1]-0.20,'$V_{s1}:$',size=30)
		self.time_plotter=plt.text(0,0,'',size=2)
		ugv_nm=23
		shape_list=[[agent_pose_list[5][0]-0.08+n/ugv_nm,agent_pose_list[5][1]-0.1+m/ugv_nm] for n,m in [(-5,-4),(5,-4),(7,0),(5,4),(-5,4)]]
		cl='r'
		p01=plt.Polygon(shape_list,color=cl,alpha=1,zorder=2)
		po=plt.Polygon(shape_list,color='black',alpha=1,fill=None,zorder=3)
		self.ax.add_patch(p01)
		self.ax.add_patch(po)
		self.agent_label_list={}
		for i in range(6):
			self.agent_label_list[i]=plt.text(agent_pose_list[i][0]+1,agent_pose_list[i][1]-0.2,'',fontsize=25)
		plt.text(agent_pose_list[5][0]+0.23,agent_pose_list[5][1]-0.2,'$V_{l1}:$',size=30)
		#====== plot : in pose
		plt.axis('off')
		plt.xlim(-3,12)
		plt.ylim(-1.5,2)
		#plt.axis('scaled')
		#plt.fill([-4,4,4,-4],[-1,-1,4,4],'palegoldenrod')
		animator = animation.FuncAnimation(self.fig, self.draw_state_adapt, frames=range(0, 230), interval=interval,repeat=False)
		animator.save('state_adapt_with_time3.gif')
		#plt.show()
