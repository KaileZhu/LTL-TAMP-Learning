import matplotlib.pyplot as plt
import numpy as np
from ltl_mas.experiment.phy_field_background import field
from ltl_mas.tools.nx_plot.bezier_method import smoothing_base_bezier
import matplotlib.patches as mpatches
#add the back graph
#img=plt.imread('/home/LZS/LTL/git/LTL_MAS_C-action/data/input_data/experiment_data/experiment_background.jpg')
#fig,ax=plt.subplots()
#ax.imshow(img,extent=[-1,5,-1,6])
#trajectory=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/input_data/experiment_data/pathdata/pose_trajectory_of_normal_exam2.npy').item()
trajectory=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/input_data/experiment_data/pathdata/pose_trajectory_of_adapt_exam2.npy').item()
agent_trajectory_x={0:[],1:[],2:[],3:[],4:[],5:[]}
agent_trajectory_y={0:[],1:[],2:[],3:[],4:[],5:[]}
agent_state=[[],[],[],[],[],[]]
for time, agent_path in trajectory.items():
	i=0
	for agent_pose, state in agent_path:
		agent_trajectory_x[i].append(agent_pose[0])
		agent_trajectory_y[i].append(agent_pose[1])
		agent_state[i].append(state)
		i=i+1
estimate_task_time_table=[[] for i in range(6)]
count=0
for task_list in trajectory.items():
	count=count+1
	for i in range(6):
		if task_list[1][i][1] not in ['motion','stay']:
			if not len(estimate_task_time_table[i])==0:
				if task_list[1][i][1] == estimate_task_time_table[i][-1][0]:
					if estimate_task_time_table[i][-1][2]+1==count:
						estimate_task_time_table[i][-1][2]=count
					else:
						estimate_task_time_table[i].append([task_list[1][i][1],count,count])
				else:
					estimate_task_time_table[i].append([task_list[1][i][1],count,count])
			else:
				estimate_task_time_table[i].append([task_list[1][i][1],count,count])
task_data_list=[(0, 'scanp2', 'p1'),
 (1, 'fixt1', 't1'),
 (2, 'washp5', 'p5'),
 (3, 'repairp2', 'p2'),
 (4, 'scanp3', 'p2'),
 (5, 'sweepp2', 'p2')]
agent_data_s0=[(0,'b1','UAV'),
                    (1,'b1','UAV'),
                    (2,'b1','UAV'),
                    (3,'b1','UAV'),
                    (4,'b1','UGV_s'),
                    (5,'b1','UGV_l'),
                       ]
agent_data=[(0,'b1','UAV'),
                    (1,'b1','UAV'),
                    (2,'b1','UAV'),
                    (3,'b1','UAV'),
                    (1,'b1','UGV_s'),
                    (2,'b1','UGV_l'),
                       ]

def gantt_plotter(node_time):
	plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
	plt.figure(figsize=(20, 12), dpi=80)
	i=1
	color_dic={}
	color = ['b', 'c', 'k', 'r', 'y','m', 'g', 'aqua', 'brown', 'cya']
	for i in range(len(task_data_list)):
		color_dic[task_data_list[i][1]]=color[i]
	i=1
	color_dic['error']=color[i]
	for agent in node_time:
		for task in agent:
			if not task[0]=='error':
				plt.barh(i,task[2]-task[1],left=task[1],color=color_dic[task[0]])
		i=i+1

	plt.xlim(0,220)
	x_tick=np.linspace(0,220,23)
	y_tick=np.linspace(1,6,6)
	index_list=[agent[2]+' '+str(agent[0]+1) for agent in  agent_data]

	plt.xticks(x_tick,fontsize=20)
	plt.yticks(y_tick,index_list,fontsize=20)
	plt.title("Task assigment Gantt graph",fontsize=30)
	labels = [''] * 6
	for f in range(len(labels)-1):
		labels[f] = "task%d" % (f + 1)
	labels=[]
	for subtask in task_data_list:
		labels.append(subtask[1])
	# 图例绘制
	patches = [mpatches.Patch(color=color[i], label="{:s}".format(labels[i])) for i in range(len(labels))]
	plt.legend(loc='lower right',handles=patches,fontsize='25')
	# XY轴标签
	plt.xlabel("time/s",fontsize=30)
	plt.ylabel("agent ID",fontsize=30)
	plt.show()

gantt_plotter(estimate_task_time_table)