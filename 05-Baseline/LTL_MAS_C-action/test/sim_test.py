import sys
sys.path.append('/home/LZS/LTL/git/LTL_MAS_C-action/src')
import os
import numpy as np
import matplotlib.pyplot as plt
from ltl_mas.simulate.field_background import field
from ltl_mas.simulate.Agent_swarm import Agent_swarm

anchor_fun=[[0, 'blowp1', 'p1'],
       [1, 'blowp7', 'p7'],
       [2, 'washp13', 'p13'],
       [3, 'shootp15', 'p15'],
       [4, 'washp1', 'p1'],
       [5, 'shootp3', 'p3'],
       [6, 'weedp12', 'p12']]
solution=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/solution.npy')
time_table=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/time_table.npy')
#anchor_fun=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/anchorfunction.npy')
#poset={(0, 1), (0, 3), (4, 5), (4, 6)}
#poset=np.load('/home/LZS/LTL/git/LTL_MAS_C-action/data/output_data/poset.npy')
poset={(1, 2), (1, 3), (0, 5), (0, 4)}
field_env = field()
#field_env.plot_back_ground()
a=Agent_swarm(solution,poset,anchor_fun,field_env,time_table)
a.pre_planning()
a.begin_run(1500,1)
a.plot(500)
