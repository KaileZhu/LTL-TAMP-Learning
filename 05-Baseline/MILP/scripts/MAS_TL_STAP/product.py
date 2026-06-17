#!/usr/bin/python
# -*- coding: utf-8 -*-

""" ======== Module Description ========
Construct the product of the following tyoes 
* MotAct : motion transition system and the local action model
* Fts    : finite transition system
* TsBuchi: transition system and buchi automaton
* 
"""

from platform import node
from networkx.classes.digraph import DiGraph
from itertools import product
from numpy import full

from .motion import Fts, MotionFts, ActionModel


class ProdMotAct(Fts):
	"""
	Class for the product between the motion transition system and the local action model.
    Note the product is also a finite transition system.
	"""
	def __init__(self, motion_model, action_model):
		super(ProdMotAct, self).__init__(initial=set())
		self._check_input_format(motion_model, action_model)

	def _check_input_format(self, motion_model, action_model):
		if isinstance(motion_model, MotionFts):
			self._motion_model = motion_model
		else:
			raise ValueError('[ProdMotAct]: Input motion model is not an instance of MotionFts!')
		if isinstance(action_model, ActionModel):
			self._action_model = action_model
		else:
			raise ValueError('[ProdMotAct]: Input action model is not an instance of LocalActionFts!')
		
	def construct_full_product(self):
		"""
		Construct the full product.
		"""
		for reg in self.motion_model.nodes:
			for act in self.action_model.action.keys():
				prod_node = self._compose_and_add_node(reg, act)
				self._add_edges_by_action(prod_node)
				self._add_edges_by_motion(prod_node)
		print('[ProdMotAct]: full motion and action model constructed with'
			' %d states and %s transitions' % (self.number_of_nodes(), self.number_of_edges()))

	def _compose_and_add_node(self, reg, act):
		"""
		Args:
			reg (dict): regions.
			act (dict): actions.
		"""
		prod_node = (reg, act)
		if not self.has_node(prod_node):
			labels_reg = self.motion_model.nodes[reg]['label']
			labels_act = self.action_model.action[act][2]
			labels_new = labels_reg.union(labels_act)
			self.add_node(prod_node, label=labels_new)
			if (reg in self.motion_model.graph['initial']) and (act == 'None'):
				self.graph['initial'].add(prod_node)
		return prod_node

	def _add_edges_by_action(self, prod_node):
		reg, act = prod_node[0:2]
		labels_reg = self.motion_model.nodes[reg]['label']
		if act == 'None':
			for act_to in self.action_model.find_allowed_actions(labels_reg):
				prod_node_to = self._compose_and_add_node(reg, act_to)
				act_to_cost = self.action_model.action[act_to][0]
				if act_to != 'None':
					self.add_edge(prod_node, prod_node_to, cost=act_to_cost, label=act_to)
	
	def _add_edges_by_motion(self, prod_node):
		reg, act = prod_node[0:2]
		for reg_to in self.motion_model.successors(reg):
			prod_node_to = self._compose_and_add_node(reg_to, 'None')
			reg_to_cost = self.motion_model[reg][reg_to]['cost']
			self.add_edge(prod_node, prod_node_to, cost=reg_to_cost, label='goto')

	@property
	def action_model(self):
		return self._action_model

	@property
	def motion_model(self):
		return self._motion_model


class ProdFts(Fts):
	"""
	Class for the product between *arbitrary* number of finite transtion systems.
	Note the product is also a finite transition system.
	"""
	def __init__(self, all_fts):
		"""
		Args:
			all_fts (List or Tuple): list of all fts that should be multiplied.
		"""
		super(ProdFts, self).__init__(initial=set())
		self._check_input_format(all_fts)

	def _check_input_format(self, all_fts):
		if (not isinstance(all_fts, list)) and (not isinstance(all_fts, tuple)):
			raise ValueError('[ProdFts]: Input all_fts is not a list or tuple!')
		for fts in all_fts:
			if not isinstance(fts, Fts):
				raise ValueError('[ProdFts]: Input fts is not an instance of Fts!')
		self._all_fts = all_fts

	def construct_full_product(self):
		for prod_node_f in product(*[fts.nodes() for fts in self._all_fts]):
			self._add_prod_node(prod_node_f)
			successors = self._find_all_successors(prod_node_f)
			for prod_node_t in product(*successors):
				full_cost = self._compute_full_cost(prod_node_f, prod_node_t)
				self.add_edge(prod_node_f, prod_node_t, cost=full_cost)
		print('[ProdFts]: full product Fts of %d Fts is computed with %d states and %s transitions'
			   %(len(self._all_fts), self.number_of_nodes(), self.number_of_edges()))

	def _add_prod_node(self, prod_node):
		labels_full = self._compute_full_labels(prod_node)
		self.add_node(prod_node, label=labels_full)
		if self._check_initial_node(prod_node):
			self.graph['initial'.add(prod_node)]

	def _compute_full_labels(self, prod_node):
		labels_full = set()
		for k, ts_node in enumerate(prod_node):
			labels_k = self.all_fts[k].nodes[ts_node]['label']
			labels_full.update(labels_k)			
		return labels_full

	def _check_initial_node(self, prod_node):
		for k, ts_node in enumerate(prod_node):
			if ts_node not in self.all_fts[k].graph['initial']:
				return False
		return True

	def _find_all_successors(self, prod_node):
		successors = []
		for k, ts_node in enumerate(prod_node):
			successors_k = self._all_fts[k].successors(ts_node)
			successors.append(successors_k)
		return successors

	def _compute_full_cost(self, prod_node_f, prod_node_t):
		full_cost = 0.0
		for k, ts_node_f in enumerate(prod_node_f):
			ts_node_t = prod_node_t[k]
			k_cost = self.all_fts[k][ts_node_f][ts_node_t]['cost']
			full_cost += k_cost
		return full_cost

	@property
	def all_fts(self):
		return self._all_fts


class ProdTsBuchi(DiGraph):
	"""
	Class for the product between a transition system and a buchi automaton.
	"""
	def __init__(self, ts, buchi):
		super(ProdTsBuchi, self).__init__(initial=set(), accept=set(), ts=ts, buchi=buchi)
		self._check_input_format(ts, buchi)
	
	def _check_input_format(self, ts, buchi):
		if isinstance(ts, Fts):
			self._ts = ts
		else:
			raise ValueError('[ProdTsBuchi]: Input transition system is not an instance of Fts!')
		if isinstance(buchi, Buchi):
			self._buchi = buchi
		else:
			raise ValueError('[ProdTsBuchi]: Input buchi automaton is not an instance of Buchi!')
	
	def construct_full_product(self):
		for ts_node_f in self.ts.nodes():
			for buchi_node_f in self.buchi.nodes():
				prod_node_f = self._compose_and_add_node(ts_node_f, buchi_node_f)
				for ts_node_t in self.ts.successors(ts_node_f):
					for buchi_node_t in self.buchi.successors(buchi_node_f):
						prod_node_t = self._compose_and_add_node(ts_node_t, buchi_node_t)
						label = self.ts.nodes[ts_node_f]['label']
						cost = self.ts[ts_node_f][ts_node_t]['cost']
						truth, dist = self.buchi.check_label_for_buchi_edge(label, buchi_node_f, buchi_node_t)
						if truth:
							self.add_edge(prod_node_f, prod_node_t, cost=cost)
		print('[ProdTsbuchi]: full product buchi automaton constructed with %d states and %s transitions.'
			  %(self.number_of_nodes(), self.number_of_edges()))

	def _compose_and_add_node(self, ts_node, buchi_node):
		prod_node = (ts_node, buchi_node)
		if not self.has_node(prod_node):
			self.add_node(prod_node, ts=ts_node, buchi=buchi_node)
			if (ts_node in self.ts.graph['initial'] and 
				buchi_node in self.buchi.graph['initial']):
				self.graph['initial'].add(prod_node)
			if buchi_node in self.buchi.graph['accept']:
				self.graph['accept'].add(prod_node)
		return prod_node

	@property
	def ts(self):
		return self._ts
	
	@property
	def buchi(self):
		return self._buchi


class ProdAut_Run(object):
	"""
	Class for the product between a transition system and a buchi automaton.
	"""
	# prefix, suffix in product run
	# prefix: init --> accept, suffix accept --> accept
	# line, loop in ts
	def __init__(self, product, prefix, precost, suffix, sufcost, totalcost):
		self.prefix = prefix
		self.precost = precost
		self.suffix = suffix
		self.sufcost = sufcost
		self.totalcost = totalcost
		#self.prod_run_to_prod_edges(product)
		self.plan_output(product)
		#self.plan = chain(self.line, cycle(self.loop))
		#self.plan = chain(self.loop)

	def prod_run_to_prod_edges(self, product):
		self.pre_prod_edges = zip(self.prefix[0:-2], self.prefix[1:-1])
		self.suf_prod_edges = zip(self.suffix[0:-2], self.suffix[1:-1])

	def plan_output(self, product):
		self.line = [product.nodes[node]['ts'] for node in self.prefix]
		self.loop = [product.nodes[node]['ts'] for node in self.suffix]
		if len(self.line) == 2:
			self.pre_ts_edges = [(self.line[0], self.line[1])]
		else:
			self.pre_ts_edges = list(zip(self.line[0:-1], self.line[1:]))
		if len(self.loop) == 2:
			self.suf_ts_edges = [(self.loop[0], self.loop[1])]
		else:
			self.suf_ts_edges = list(zip(self.loop[0:-1], self.loop[1:]))
			self.suf_ts_edges.append((self.loop[-1], self.loop[0]))
		# output plan
		self.pre_plan = list()
		self.pre_plan.append(self.line[0][0]) 
		for ts_edge in self.pre_ts_edges:
			if product.graph['ts'][ts_edge[0]][ts_edge[1]]['label'] == 'goto':
				self.pre_plan.append(ts_edge[1][0]) # motion
			else:
				self.pre_plan.append(ts_edge[1][1]) # action
		bridge = (self.line[-1], self.loop[0])
		if product.graph['ts'][bridge[0]][bridge[1]]['label'] == 'goto':
			self.pre_plan.append(bridge[1][0]) # motion 
		else:
			self.pre_plan.append(bridge[1][1]) # action
		self.suf_plan = list()
		for ts_edge in self.suf_ts_edges:
			if product.graph['ts'][ts_edge[0]][ts_edge[1]]['label'] == 'goto':
				self.suf_plan.append(ts_edge[1][0]) # motion 
			else:
				self.suf_plan.append(ts_edge[1][1]) # action