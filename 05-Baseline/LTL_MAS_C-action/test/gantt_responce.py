import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from data.input_data.task_data import task_type
import numpy as np

plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.figure(figsize=(20, 13), dpi=80)
i=1
color = ['b', 'c', 'pink', 'r', 'y','m', 'g', 'aqua', 'brown','tan']
node=[[[1,10,15]],[[2,15,20]],[[3,20,25]],[[4,30,35]],[[5,25,30]]]
for agent in node:
    for task in agent:
            plt.barh(i,task[2]-task[1],left=task[1],color=color[task[0]])
    i=i+1
plt.xlim(0,40)
x_tick=np.linspace(0,40,9)
y_tick=np.linspace(1,len(node),len(node))
count=1
index_list=[]
agent_data_s2=[
    [0,'s', 'UAV'],
    [1, 's', 'UAV'],
    [2, 's', 'UAV'],
    [3, 's', 'UAV'],
    [4, 's', 'UAV'],
]
for agent in agent_data_s2:
    if agent[2]=='UAV':
        index_list.append(r'$V_{f'+str(count)+'}$')
    if agent[2]=='UGV_l':
        index_list.append(r'$V_{l' + str(count-6) + '}$')
    if agent[2] == 'UGV_s':
        index_list.append(r'$V_{s' + str(count - 9) + '}$')
    count=count+1
#index_list=[agent[2]+' '+str(agent[0]+1) for agent in  agent_data_s2]
plt.xticks(x_tick,fontsize=20)
plt.yticks(y_tick,index_list,fontsize=30)
#plt.title("Task assigment Gantt graph",fontsize=30)
labels = [''] * len(task_type)
for f in range(len(labels)-1):
    labels[f] = "task%d" % (f + 1)
#labels=['(1,blowp1)','(2,shootp1)','(3,sweepp1)','(4,shootp12)','(5,sweepp12)','(6,blowp7)','(7,shootp7)','(8,washp7)']
labels=[]
for i in range(5):
    labels.append(i+1)
#labels=['search_p32','search_p12','support_p32','attack_p32','patrol_p12','patrol_p32','guard_p12','support_p7']
# 4 6 03  05 02
#attack search patrol guard support
#wash  photo  sweep  blow check
#<>(photop32_p32 && <> washp32_p32 && <> sweepp6_p6 && <> checkt6_t6 ) && ' \
#'<> photop15_p15 && <>(sweepp12_p12 && <> blowp12_p12) && <>checkt7_t7'
#'<> (search_a && <> ( formation_f)) && <> (goto_c && <>search_d)'
# 图例
patches=[]
for i in range(5):
    patches.append(mpatches.Patch(color=color[i], label=r"$\omega_"+str(i+1)+'$'))
#patches = [mpatches.Patch(color=color[i], label="{:s}".format(labels[i])) for i in range(len(labels))]
#plt.legend(loc='lower right',handles=patches,fontsize='25')
# XY轴标签
plt.xlabel("time/s",fontsize=30)
plt.ylabel("agent ID",fontsize=30)
# 网格线，此图使用不好看，注释掉
# plt.grid(linestyle="--",alpha=0.5)
plt.legend(loc=2, bbox_to_anchor=(0, 1.15), handles=patches, fontsize='25', ncol=5)
plt.show()