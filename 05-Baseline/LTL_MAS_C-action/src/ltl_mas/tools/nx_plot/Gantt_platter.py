import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from data.input_data.task_data import task_type
import numpy as np

agent_data_s1=[(0,'b1','UAV'),
                    (1,'b1','UAV'),
                    (2,'b1','UAV'),
                    (3,'b1','UAV'),
                    (4,'b1','UGV_l'),
                    (5,'b1','UGV_l'),
                    (6,'b1','UGV_s'),
                    (7,'b1','UGV_s')
                    ]
agent_data_s2=[(0,'b1','UAV'),
                    (1,'b1','UAV'),
                    (2,'b1','UAV'),
                    (3,'b1','UAV'),
                    (4,'b1','UAV'),
                    (5, 'b1', 'UAV'),

                    (6,'b1','UGV_l'),
                    (7,'b1','UGV_l'),
                    (8,'b1','UGV_l'),

                    (9,'b1','UGV_s'),
                    (10,'b1','UGV_s'),
                    (11,'b1','UGV_s'),
                       ]
agent_data_s3=[(0,'b1','UAV'),
                    (1,'b1','UAV'),
                    (2,'b1','UAV'),
                    (3,'b1','UAV'),
                    (4,'b1','UAV'),
                    (5,'b1','UAV'),
                    (6,'b1','UAV'),
                    (7,'b1','UAV'),
                    (8,'b1','UAV'),
                    (9,'b1','UAV'),

                    (10,'b1','UGV_l'),
                    (11,'b1','UGV_l'),
                    (12,'b1','UGV_l'),
                    (13,'b1','UGV_l'),
                    (14,'b1','UGV_l'),

                    (15,'b1','UGV_s'),
                    (16,'b1','UGV_s'),
                    (17,'b1','UGV_s'),
                    (18,'b1','UGV_s'),
                    (19,'b1','UGV_s'),
                       ]


def gantt_plotter(task_number,situation ):
	#plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
	plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
	node_name='/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task'+task_number+'/solution_s'+situation+'.npy'
	node=np.load(node_name)
	#node=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task2/solution_s3.npy')
	time_name='/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task'+task_number+'/time_table_s'+situation+'.npy'
	time=np.load(time_name)
	#time=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task2/time_table_s3.npy')
	task_data_list_name='/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task'+task_number+'/task_data_list.npy'
	task_data_list=np.load(task_data_list_name)
	#task_data_list=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task2/task_data_list.npy')
	plt.figure(figsize=(20, 12), dpi=80)
	i=1

	color = ['b', 'c', 'k', 'r', 'y','m', 'g', 'aqua', 'brown', 'cya']

	for agent in node:
		for task in agent:
			print(time[task[0][0]][1])
			plt.barh(i,time[task[0][0]][2]-time[task[0][0]][1],left=time[task[0][0]][1],color=color[task[0][0]])
			print('left=',time[task[0][0]][2])
		i=i+1
	plt.xlim(0,1200)
	x_tick=np.linspace(0,1000,11)
	len(node)
	y_tick=np.linspace(1,len(node),len(node))
	if situation=='0':
		index_list=[agent[2]+' '+str(agent[0]+1) for agent in  agent_data_s2]
	if situation=='1':
		index_list=[agent[2]+' '+str(agent[0]+1) for agent in  agent_data_s1]
	if situation=='2':
		index_list=[agent[2]+' '+str(agent[0]+1) for agent in  agent_data_s2]
	if situation=='3':
		index_list=[agent[2]+' '+str(agent[0]+1) for agent in  agent_data_s3]

	plt.xticks(x_tick,fontsize=20)
	plt.yticks(y_tick,index_list,fontsize=20)
	plt.title("Task assigment Gantt graph",fontsize=30)
	labels = [''] * len(task_type)
	for f in range(len(labels)-1):
		labels[f] = "task%d" % (f + 1)
	#labels=['(1,blowp1)','(2,shootp1)','(3,sweepp1)','(4,shootp12)','(5,sweepp12)','(6,blowp7)','(7,shootp7)','(8,washp7)']
	labels=[]
	for subtask in task_data_list:
		labels.append(subtask[1])
	#labels=['search_p32','search_p12','support_p32','attack_p32','patrol_p12','patrol_p32','guard_p12','support_p7']
# 4 6 03  05 02
	#attack search patrol guard support
#wash  photo  sweep  blow check
	#<>(photop32_p32 && <> washp32_p32 && <> sweepp6_p6 && <> checkt6_t6 ) && ' \
	#'<> photop15_p15 && <>(sweepp12_p12 && <> blowp12_p12) && <>checkt7_t7'
	#'<> (search_a && <> ( formation_f)) && <> (goto_c && <>search_d)'
	# 图例绘制
	patches = [mpatches.Patch(color=color[i], label="{:s}".format(labels[i])) for i in range(len(labels))]
	plt.legend(handles=patches,fontsize='25')
	# XY轴标签
	plt.xlabel("time/s",fontsize=30)
	plt.ylabel("agent ID",fontsize=30)
	# 网格线，此图使用不好看，注释掉
	# plt.grid(linestyle="--",alpha=0.5)
	plt.savefig('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/task'+task_number+'/gantt_s'+situation+'.eps', dpi=300)
	#plt.show()
for i in ['0']:
	gantt_plotter('2',i)
