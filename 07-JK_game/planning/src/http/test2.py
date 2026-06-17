
import numpy as np
import matplotlib.pyplot as plt
from dec_data import  *
first_gantt_garph={0: {'task_name': 'observe001', 'begin_time': 1.0, 'duration': 1},
 1: {'task_name': 'observe002', 'begin_time': 1.0, 'duration': 1},
 2: {'task_name': 'observe003', 'begin_time': -0.0, 'duration': 1},
 3: {'task_name': 'attack001', 'begin_time': 2.0, 'duration': 1},
 4: {'task_name': 'attack002', 'begin_time': 2.0, 'duration': 1},
 5: {'task_name': 'attack003', 'begin_time': 3.0, 'duration': 1}}

plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.figure(figsize=(20, 12), dpi=80)
for task_id,task_list  in  first_gantt_garph.items():

    color = ['b', 'c', 'k', 'r', 'y', 'm', 'g', 'aqua', 'brown', 'cya']


    plt.barh(task_id+1, task_list['duration'], left=task_list['begin_time'], color=color[task_id])
plt.xlim(0, 5)
x_tick = np.linspace(0, 5, 6)
y_tick = np.linspace(1, 6, 6)

plt.xlabel("time/s", fontsize=30)
plt.ylabel("agent ID", fontsize=30)
plt.show()