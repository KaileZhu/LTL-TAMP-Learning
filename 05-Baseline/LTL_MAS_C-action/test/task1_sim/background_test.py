import sys
sys.path.append('/home/LZS/LTL/git/LTL_MAS_C-action/src')
from src.ltl_mas.tools.poset_builder import Buchi_poset_builder
from src.ltl_mas.tools.nx_plot.base_plot import plot
from src.ltl_mas.tools import optimize_method
from data import input_data
import numpy as np
import time
import matplotlib.pyplot as plt
from src.ltl_mas.simulate.field_background import field

f=field()
#f.plot_static_back_ground()
f.get_node_in_barrier()
path=f.co_task_planning('check','t1')
for x,y in path[0]:
	plt.plot(x,y,'*')
