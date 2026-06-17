# -*- coding: utf-8 -*-
from src.baseline.simultaneous.discrete_plan import dijkstra_plan_networkX

class ltl_planner(object):
	def __init__(self, product):
		#buchi = Buchi(hard_spec, soft_spec)#判断是否有为none的约束 转换为buchi
		self.product = product#
		self.Time = 0
		self.cur_pose = None
		self.trace = [] # record the regions been visited
		self.traj = [] # record the full trajectory
		self.opt_log = [] 
		# record [(time, prefix, suffix, prefix_cost, suffix_cost, total_cost)]
		self.com_log = []
		# record [(time, no_messages)]

	def optimal(self, beta=10, style='static'):
		self.beta = beta
		if style == 'static':
			# full graph construction
			#self.product.graph['ts'].build_full()#这个build_full是ts中 MotActmodel的 函数
			#self.product.build_full()#这个build_full是product的函数
			prefix,time_cost= dijkstra_plan_networkX(self.product, self.beta,weight='cost')
		return prefix,time_cost
		#print '\n'

