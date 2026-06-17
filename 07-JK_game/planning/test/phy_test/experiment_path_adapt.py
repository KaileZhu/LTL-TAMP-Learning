import matplotlib.pyplot as plt
import numpy as np
from ltl_mas.experiment.phy_field_background import field
from ltl_mas.tools.nx_plot.bezier_method import smoothing_base_bezier
#add the back graph
#img=plt.imread('/home/LZS/LTL/git/LTL_MAS_C-action/data/input_data/experiment_data/experiment_background.jpg')
#fig,ax=plt.subplots()
#ax.imshow(img,extent=[-1,5,-1,6])
#trajectory=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/input_data/experiment_data/pathdata/pose_trajectory_of_normal_exam2.npy').item()
f=field()
f.plot_static_back_ground()
trajectory=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/input_data/experiment_data/pathdata/pose_trajectory_of_adapt_exam2.npy').item()
agent_trajectory_x={0:[],1:[],2:[],3:[],4:[],5:[]}
agent_trajectory_y={0:[],1:[],2:[],3:[],4:[],5:[]}
for time, agent_path in trajectory.items():
	i=0
	for agent_pose, state in agent_path:
		agent_trajectory_x[i].append(agent_pose[0])
		agent_trajectory_y[i].append(agent_pose[1])
		i=i+1

agent_0_idlist=list(range(7))
agent_0_idlist.extend([7 for i in range(7,30)])
agent_0_idlist.extend(list(range(30,100)))
agent_0_idlist.extend([100 for i in range(100,128)])
agent_0_idlist.extend(list(range(128,143)))
agent_0_idlist.extend([143 for i in range(143, len(agent_trajectory_x[0]))])
agent_ID_list=[]
agent_ID_list.append(agent_0_idlist)
#====== agent 2

agent_1_idlist=list(range(14))
agent_1_idlist.extend([14 for i in range(15,84)])
agent_1_idlist.extend(list(range(84,100)))
agent_1_idlist.extend([100 for i in range(106,135)])
agent_1_idlist.extend(list(range(135,146)))
agent_1_idlist.extend([146 for i in range(146,len(agent_trajectory_x[1]))])
agent_ID_list.append(agent_1_idlist) # agent 2
# ==== agent 3

agent_2_idlist=list(range(11))
agent_2_idlist.extend([11 for i in range(11,82)])
agent_2_idlist.extend(list(range(82,106)))
agent_2_idlist.extend([106 for i in range(106,134)])
agent_2_idlist.extend(list(range(134,145)))
agent_2_idlist.extend([145 for i in range(145,len(agent_trajectory_x[2]))])
agent_ID_list.append(agent_2_idlist)

# ==== agent 4
agent_3_idlist=list(range(8))
agent_3_idlist.extend([8 for i in range(8,90)])
agent_3_idlist.extend(list(range(90,145)))
agent_3_idlist.extend([145 for i in range(145,len(agent_trajectory_x[3]))])
agent_ID_list.append(agent_3_idlist)
agent_ID_list.append(range(len(agent_trajectory_x[0])))
agent_ID_list.append(range(len(agent_trajectory_x[0])))
i=0
color_table=['g','y','Purple','w','gray','Teal']
i=0

for choose_ID in agent_ID_list:
	trajectory_x=[agent_trajectory_x[i][j] for j in choose_ID]
	trajectory_y=[agent_trajectory_y[i][j] for j in choose_ID]


color_table=['g','y','Purple','w','gray','Teal']
i=0

color_varide = ['Greys', 'Purples',  'Greens',  'Reds','Purples', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu',
                'GnBu']
color_varide = ['Greys', 'Purples',  'Greens',  'Reds','YlOrRd', 'Blues', 'OrRd', 'PuRd', 'RdPu',
                'GnBu']
subtime=0
time=230
for i in [3,4,5]:
	trajectory_x=[agent_trajectory_x[i][j] for j in agent_ID_list[i]]
	trajectory_y=[agent_trajectory_y[i][j] for j in agent_ID_list[i]]
	category_colors = plt.get_cmap(color_varide[i])(np.linspace(0.5, 1, (time - subtime)))
	if i ==4:
		category_colors = plt.get_cmap(color_varide[i])(np.linspace(0.2, 0.5, (time - subtime)))
	if i in [0,1,2,3]:
		path_x = trajectory_x[0:time - subtime:5]
		path_y = trajectory_y[0:time - subtime:5]
	else:
		path_x = trajectory_x[0:time - subtime:3]
		path_y = trajectory_y[0:time - subtime:3]
	# x_curve, y_curve=smoothing_base_bezier(path_x,path_y)
	path_x, path_y = smoothing_base_bezier(path_x, path_y)
	step = (len(path_x) - 1) // len(category_colors) + 1
	for j in range(0, len(path_x) - step, step):
		plt.arrow(path_x[j], path_y[j], path_x[j + step] - path_x[j], path_y[j + step] - path_y[j],
		length_includes_head=True, head_width=0.08, lw=5, color=category_colors[j // step],zorder=3)


plt.show()
for choose_ID in agent_ID_list:
	trajectory_x=[agent_trajectory_x[i][j] for j in choose_ID]
	trajectory_y=[agent_trajectory_y[i][j] for j in choose_ID]
	x,y=smoothing_base_bezier(trajectory_x,trajectory_y, k=0.8, closed=False)
	x=[x[i] for i in range(0,len(x),2)]
	y=[y[i] for i in range(0,len(y),2)]
	plt.plot(x,y,linewidth=3,color=color_table[i])
	i=i+1
plt.show()
s=1