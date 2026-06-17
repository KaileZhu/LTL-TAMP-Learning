import sys
sys.path.append('/home/LZS/LTL/git/LTL_MAS_C-action/src')
sys.path.append('/home/dell/LTL_planning/LTL_MAS_C-action/src')
sys.path.append('/home/dell/LTL_planning/LTL_MAS_C-action')
from ltl_mas.tools.poset_builder import Buchi_poset_builder
from ltl_mas.tools.nx_plot.base_plot import plot
from ltl_mas.tools import optimize_method
from data import input_data
import numpy as np
import time
import matplotlib.pyplot as plt
from ltl_mas.experiment.phy_field_background_old import field

f=field()
f.plot_static_back_ground()
path=f.co_task_planning('fix','t1')
print(path)
for x,y in path[0]:
	plt.plot(x,y,'*')
plt.show()

s=1
