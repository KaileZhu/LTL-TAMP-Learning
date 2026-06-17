# -*- coding: utf-8 -*-
from src.ltl_mas.models.buchi import Buchi
from src.ltl_mas.models.product import ProdTsBuchi
from src.ltl_mas.tools.discrete_plan import dijkstra_plan_networkX, dijkstra_plan_optimal, improve_plan_given_history

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
			self.run, plantime = dijkstra_plan_networkX(self.product, self.beta)
		elif style == 'centralize':
			for buchi_init in self.product.graph['buchi'].graph['initial']:
				init_prod_node = self.product.composition(self.product.graph['ts'].graph['initial'][0], buchi_init)
				print(init_prod_node)
			self.product.build_full()
			self.run, plantime,prefix,suffix= dijkstra_plan_networkX(self.product, self.beta, True)
		if self.run == None:
			print ('---No valid has been found!---')
			print ('---Check you FTS or task---')
			return
		#print '\n'
		print ('------------------------------')
		print ('the prefix of plan **states**:')
		print ([n for n in self.run.line])
		print ('the suffix of plan **states**:')
		print ([n for n in self.run.loop])
		print ('------------------------------')
		print ('the prefix of plan ***aps**:')
		print ([self.product.graph['ts'].nodes[n]['label'] for n in self.run.line])
		print ('the suffix of plan **aps**:')
		print ([self.product.graph['ts'].nodes[n]['label'] for n in self.run.loop])
		#print '\n'
		print ('------------------------------')
		return plantime


