# -*- coding: utf-8 -*-
import random
from itertools import chain,combinations
from src.baseline.sampling_based.discrete_plan import dijkstra_plan_networkX
from networkx import dijkstra_predecessor_and_distance
from networkx.classes.digraph import DiGraph
import time
from random import choice
import itertools
from src.ltl_mas.tools.poset_builder import Buchi_poset_builder

class ltl_planner(object):
	def __init__(self, PBA):
		#buchi = Buchi(hard_spec, soft_spec)#判断是否有为none的约束 转换为buchi
		self.PBA = PBA#
		self.search_graph=DiGraph(PTS=PBA['PTS'],buchi=PBA['NBA'])
		self.Time = 0
		self.cur_pose = None
		self.trace = [] # record the regions been visited
		self.traj = [] # record the full trajectory
		self.opt_log = [] 
		# record [(time, prefix, suffix, prefix_cost, suffix_cost, total_cost)]
		self.com_log = []
		# record [(time, no_messages)]

	def optimal(self, search_round=200,search_time=50):
		self.get_initial_state()
		self.set_root_of_the_tree()
		self.constructTree(search_round=search_round)
		self.find_path()
			#define the construct tree
			#find the path
			#get the value
		#return the path

	def optimal_star(self,search_round=200):
		self.get_initial_state()
		self.set_root_of_the_tree()
		self.define_depth_of_NBA()
		self.constructTree_star(search_round=search_round)
		self.define_accept_set()
		line_pre, line_dist, time_cost = dijkstra_plan_networkX(self.search_graph, 3, weight='cost')
		return line_pre,line_dist,time_cost

	def constructTree_star(self,search_round=1000):
		#round=0
		start=time.time()
		self.buchi_node_list=[]
		check_time=20
		while time.time()-start<search_round:
			#print(round)
			if check_time<time.time()-start:
				check_time=check_time+10
				self.define_accept_set()
				for prod_init in self.search_graph.graph['initial']:
					line = {}
					line_pre, line_dist = dijkstra_predecessor_and_distance(self.search_graph, prod_init,weight='cost')
					for target in iter( self.search_graph.graph['accept']):
						if target in line_dist:
							line[target] =line_dist[target]
					if len(line)==0:
						print('still not found the feasible solution in',check_time-200)
						depth=0
						NBA_set=set()
						for node in line_dist.keys():
							depth=max(depth,self.line_dist[node[1]])
							NBA_set.add(node[1])
						print('the depth distance is',depth)
						print('already found NBA node', len(NBA_set),'/',len(self.PBA['NBA'].nodes))
					else:
						return
			q_pts_new=self.sampling_star()
			for q_NBA in self.PBA['NBA'].nodes:
				q_p_new=(tuple(q_pts_new),q_NBA)
				if q_p_new in self.search_graph.nodes:
					1
				else:
					self.extend_fast(q_p_new,round,0)
			#round=round+1

	def define_depth_of_NBA(self):
		line_pre,line_dist,prefix=dijkstra_plan_networkX(self.search_graph.graph['buchi'])
		self.line_dist=line_dist


	def optimal_improve(self,search_round):
		self.buchi_set=set()
		self.get_initial_state()
		self.set_root_of_the_tree()
		self.constructTree_improve(search_round=search_round)
		self.define_accept_set()
		line_pre, line_dist, time_cost = dijkstra_plan_networkX(self.search_graph, 3, weight='cost')
		return line_pre,line_dist,time_cost
			#define the construct tree
			#find the path
			#get the value
		#return the path

	def get_initial_state(self):
		pts_initial_state_list=[]
		for wts in self.PBA['PTS']:
			for node in wts.motact_model.graph['initial']:
				pts_initial_state_list.append(node)
		NBA_initial_state=self.PBA['NBA'].graph['initial']
		self.initial_state=(tuple(pts_initial_state_list),NBA_initial_state)
		self.search_graph.add_node((tuple(pts_initial_state_list),NBA_initial_state[0]))

	def optimal_fast(self,search_round=200):
		self.get_initial_state()
		self.set_root_of_the_tree()
		self.constructTree_fast(search_round=search_round)
		self.define_accept_set()
		line_pre, line_dist= dijkstra_plan_networkX(self.search_graph, 3, weight='cost')
		return line_pre,line_dist

	def optimal_fast2(self,task,search_round=1):
		self.get_initial_state()
		self.set_root_of_the_tree()
		#self.get_pruned_Buchi(task)
		self.define_depth_of_NBA()
		self.constructTree_fast2(search_round=search_round)
		self.define_accept_set()
		line_pre, line_dist,prefix= dijkstra_plan_networkX(self.search_graph, 3, weight='cost')
		return line_pre,line_dist,prefix

	def get_pruned_Buchi(self,task):
		Bu=Buchi_poset_builder(task)
		Bu.delete_the_self_loop()
		Bu.remove_the_1_edge_with_node()
		Bu.remove_pue_negative_edges()
		self.add_self_loop(Bu.new_buchi,self.PBA['NBA'])
		self.PBA['NBA']=Bu.new_buchi
		self.search_graph.graph['buchi']=Bu.new_buchi

	def add_self_loop(self,product,product2):
		for node in product.nodes:
			if product2.has_edge(node,node):
				product.add_edge(node,node,guard=product2[node][node]['guard'],guard_formula=product2[node][node]['guard_formula'])

	def constructTree_fast(self,search_round=2000):
		round=0
		method=0
		start=time.time()
		self.define_node_set()
		while time.time()-start<search_round:
			print(round)
			q_pts_new,sampling_label=self.sampling_fast()
			if sampling_label==1:
				break
			for q_NBA in self.PBA['NBA'].nodes:
				print(q_NBA)
				q_p_new=(tuple(q_pts_new),q_NBA)
				self.extend_improve(q_p_new,round,method)
			round=round+1

	def sampling_star(self,random_value=0.4):
		#==============pick up the list node nor the far node
		depth_list=[]
		for node in self.search_graph.nodes:
			depth_list.append(self.line_dist[node[1]])
		n=max(depth_list)
		D_min=[]
		D_min_no=[]
		for node in self.search_graph.nodes:
			if n == self.line_dist[node[1]]:
				D_min.append(node)
			else:
				D_min_no.append(node)
		if not len(D_min_no)==0:
			ran=random.random()
			if ran>random_value:
				node=choice(D_min)
			else:
				node=choice(D_min_no)
		else:
			node=choice(D_min)
		q_rand_b=node[1]
		q_pts_b=node[0]
		R_B_q_rand_b_list=list(self.search_graph.graph['buchi'].successors(q_rand_b))
		if len(R_B_q_rand_b_list)==0:
			return
		#compute M(R B)
		depth_list=[]
		for node in R_B_q_rand_b_list:
			depth_list.append(self.line_dist[node])
		n=max(depth_list)
		M_B_q_rand_b_list=[]
		for i in range(len(depth_list)):
			if n == depth_list[i]:
				M_B_q_rand_b_list.append(R_B_q_rand_b_list[i])
		q_b_decr=choice(M_B_q_rand_b_list)
		#==== get the sigma of path
		guard=self.search_graph.graph['buchi'][q_rand_b][q_b_decr]['guard_formula']
		sequence_checker=self.search_graph.graph['buchi'][q_rand_b][q_b_decr]['guard']
		formula = list(self.powerset(self.symbols_extracter(guard)))
		found_number=0
		#=== get only one word for feasible
		sigma=None
		for subset in formula:
			if sequence_checker.check(' '.join(subset)) ==1:
				sigma=subset
				#print(sigma)
				break
		if sigma==None:
			new_pts_node=[]
			for i in range(len(self.PBA['PBA'])):
				new_pts_node.append(choice(self.PBA['PTS'][i].nodes))
		else:
			n=len(self.PBA['PTS'])
			agent_ID=random.randint(0,n-1)
			q_ts_i=q_pts_b[agent_ID]
			#get the reachable node of q_ts_i
			R_q_ts_i=self.PBA['PTS'][agent_ID].motact_model.successors(q_ts_i)
			labeled_set=[]
			unlabeled_set=[]
			for node in R_q_ts_i:
				if sigma in self.PBA['PTS'][agent_ID].motact_model.nodes[node]['label']:
					labeled_set.append(node)
				else:
					unlabeled_set.append(node)
			pnew=random.random()
			if len(labeled_set)==0:
				q_i_node=choice(unlabeled_set)
			else:
				if pnew>random_value:
					q_i_node=choice(labeled_set)
				else:
					q_i_node=choice(unlabeled_set)
			new_pts_node=[]
			for i in range(len(self.PBA['PTS'])):
				if not i ==agent_ID:
					new_pts_node.append(choice(list(self.PBA['PTS'][i].motact_model.nodes)))
				else:
					new_pts_node.append(q_i_node)
		return new_pts_node

	def powerset(self,iterable):
		s = list(iterable)
		return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

	def symbols_extracter(self,string):
		symbols_set = set()
		symbol = ''
		for i in string:
			if i not in '|() &!':
				symbol = symbol + i
			else:
				if symbol != '':
					symbols_set.add(symbol)
					symbol = ''
		return symbols_set

	def constructTree_fast2(self,search_round=2000):
		round=0
		method=0
		start=time.time()
		self.buchi_set=set()
		self.find_accept=0
		#self.define_node_set()
		self.len_buchi_set=0
		total_buchi_set=len(self.PBA['NBA'].nodes)
		while self.find_accept<search_round:
			#print(round)
			#check has found how many buchi node
			if self.len_buchi_set<len(self.buchi_set):
				print('already sampling ',len(self.buchi_set),'/',total_buchi_set,' buchi set')
				self.len_buchi_set=len(self.buchi_set)
			#if 'accept_all' in list(self.buchi_set):
				#print('already found the accepting state1')
				#break
			#if 'accept_S26' in list(self.buchi_set):
				#print('already found the accepting state2')
				#break
			q_pts_new=self.sampling_star()
			#print(q_pts_new)
			s=1
			for q_NBA in self.PBA['NBA'].nodes:
				#print(q_NBA)
				q_p_new=(tuple(q_pts_new),q_NBA)
				self.extend_improve(q_p_new,round,method)
			round=round+1

	def define_node_set(self):
		node_list_list=[]
		for agent in self.PBA['PTS']:
			node_list_list.append(list(agent.motact_model.nodes))
		self.search_node_list=list(itertools.product(*node_list_list))
		self.searched_node_list=[]

	def sampling_fast(self):
		node = choice(self.search_graph.nodes)
		node_list=[]
		for i in range(len(self.PBA['PTS'])):
			self.PBA['PTS'][i].motact_model.successors(node[0][i])
		n=len(self.search_node_list)
		if n==0:
			return 0,1
		node=self.search_node_list.pop(random.randint(0,n-1))
		return node,0

	def sampling_fast2(self):
		while 1:
			root_node=choice(list(self.search_graph.nodes))
			new_pts_set=self.get_reachable_set(root_node[0])
			if root_node[0] in self.search_pts_node_list:
				break
		return  new_pts_set

	def set_root_of_the_tree(self):
		'''
		node structure is ((PTS_node),NBA_node)
		'''
		init_PTS_node_set=[]
		for agent in self.PBA['PTS']:
			for node in agent.motact_model.graph['initial']:
				init_PTS_node_set.append(node)
		init_NBA_node=self.PBA['NBA'].graph['initial']
		self.search_graph.graph['initial']={(tuple(init_PTS_node_set),init_NBA_node[0])}
		self.search_graph.add_node((tuple(init_PTS_node_set),init_NBA_node[0]),cost=0)

	def define_accept_set(self):
		self.search_graph.graph['accept']=[]
		for node in self.search_graph.nodes:
			if node[1] in self.PBA['NBA'].graph['accept']:
				self.search_graph.graph['accept'].append(node)

	def constructTree(self,search_round=100,method='classic'):
		round=0
		while round<search_round:
			print(round)
			q_pts_new=self.sampling()
			for q_NBA in self.PBA['NBA'].nodes:
				q_p_new=(tuple(q_pts_new),q_NBA)
				if q_p_new not in self.search_graph.nodes:
					self.extend(q_p_new,round,method)
				else:
					self.rewire(q_p_new)
			round=round+1


	def constructTree_improve(self,search_round=100,method='classic'):
		round=0
		start=time.time()

		while time.time()-start<search_round:
			print(round)
			q_pts_new_list=self.sampling_improve()
			for q_pts_new in q_pts_new_list:
				for q_NBA in self.PBA['NBA'].nodes:
					q_p_new=(tuple(q_pts_new),q_NBA)
					self.extend_improve(q_p_new,round,method)
			round=round+1

	def extend_improve(self,q_p_new,round,method):
		if q_p_new in self.search_graph.nodes:
			return
		#self.search_graph.add_node(q_p_new)
		to_add_list=[]
		for node in self.search_graph.nodes:
			if self.PBA['NBA'].has_edge(node[1],q_p_new[1]):
				new_cost=0
				labels_set=set()
				unfeasible_edge=0
				for i in range(len(node[0])):
					if self.PBA['PTS'][i].motact_model.has_edge(node[0][i],q_p_new[0][i]):
						labels_set=labels_set|self.PBA['PTS'][i].motact_model.nodes[node[0][i]]['label']
						cost=self.PBA['PTS'][i].motact_model.edges[(node[0][i],q_p_new[0][i])]['cost']
						new_cost=max(cost,new_cost)
					else:
						unfeasible_edge=1
						break
				if unfeasible_edge:
					continue
				else:
					if node[1]==q_p_new[1]:
						to_add_list.append([node,q_p_new,new_cost])
					else:
						if self.PBA['NBA'].edges[node[1],q_p_new[1]]['guard'].check(labels_set):
							#self.search_graph.add_node(q_p_new)
							to_add_list.append([node,q_p_new,new_cost])
							#self.search_graph.add_edge(node,q_p_new,cost=new_cost)
							#if q_p_new[1] in self.PBA['NBA'].graph['accept']:
							#if q_p_new[1] == 'accept_all':
							if q_p_new[1] =='accept_S26':
								self.find_accept=self.find_accept+1
								print('already found accept :',self.find_accept)
						#self.search_graph.add_edge(node,q_p_new)
			if self.PBA['NBA'].has_edge(q_p_new[1],node[1]):
				new_cost=0
				labels_set=set()
				unfeasible_edge=0
				for i in range(len(node[0])):
					if self.PBA['PTS'][i].motact_model.has_edge(q_p_new[0][i],node[0][i]):
						labels_set=labels_set|self.PBA['PTS'][i].motact_model.nodes[q_p_new[0][i]]['label']
						cost=self.PBA['PTS'][i].motact_model.edges[(q_p_new[0][i],node[0][i])]['cost']
						new_cost=max(cost,new_cost)
					else:
						unfeasible_edge=1
						break
				if unfeasible_edge:
					continue
				else:
					if node[1]==q_p_new[1]:
						to_add_list.append([q_p_new,node,new_cost])
					else:
						if self.PBA['NBA'].edges[q_p_new[1],node[1]]['guard'].check(labels_set):
							#self.search_graph.add_node(q_p_new)

							to_add_list.append([q_p_new,node,new_cost])
							#self.search_graph.add_edge(q_p_new,node,cost=new_cost)
							if q_p_new[1] in self.PBA['NBA'].graph['accept']:
								self.find_accept=self.find_accept+1
		for node1,node2,cost in to_add_list:
			self.search_graph.add_edge(node1,node2,cost=cost)
			self.buchi_set=self.buchi_set | set([q_p_new[1]])
			#self.search_graph.add_edge(node,q_p_new)

	def extend_fast(self,q_p_new,round,method):
		self.search_graph.add_node(q_p_new)

		for node in self.search_graph.nodes:
			if self.PBA['NBA'].has_edge(node[1],q_p_new[1]):
				new_cost=0
				labels_set=set()
				unfeasible_edge=0
				for i in range(len(node[0])):
					if self.PBA['PTS'][i].motact_model.has_edge(node[0][i],q_p_new[0][i]):
						labels_set=labels_set|self.PBA['PTS'][i].motact_model.nodes[node[0][i]]['label']
						cost=self.PBA['PTS'][i].motact_model.edges[(node[0][i],q_p_new[0][i])]['cost']
						new_cost=cost+new_cost
					else:
						unfeasible_edge=1
						break
				if unfeasible_edge:
					continue
				else:
					if self.PBA['NBA'].edges[node[1],q_p_new[1]]['guard'].check(labels_set):
						self.search_graph.add_edge(node,q_p_new,cost=cost)
					#self.search_graph.add_edge(node,q_p_new)
			if self.PBA['NBA'].has_edge(q_p_new[1],node[1]):
				new_cost=0
				labels_set=set()
				unfeasible_edge=0
				for i in range(len(node[0])):
					if self.PBA['PTS'][i].motact_model.has_edge(q_p_new[0][i],node[0][i]):
						labels_set=labels_set|self.PBA['PTS'][i].motact_model.nodes[q_p_new[0][i]]['label']
						cost=self.PBA['PTS'][i].motact_model.edges[(q_p_new[0][i],node[0][i])]['cost']
						new_cost=cost+new_cost
					else:
						unfeasible_edge=1
						break
				if unfeasible_edge:
					continue
				else:
					if self.PBA['NBA'].edges[q_p_new[1],node[1]]['guard'].check(labels_set):
						self.search_graph.add_edge(q_p_new,node,cost=cost)
					#self.search_graph.add_edge(node,q_p_new)

	def constructTree_faster(self,search_round=10000):
		round=0
		while round<search_round:
			q_pts_new=self.sample()
			for q_NBA in self.PBA['NBA'].nodes:
				q_p_new=(tuple(q_pts_new),q_NBA)
			if q_p_new not in self.search_graph.nodes:
				self.search_graph.add_node(q_p_new)
				self.add_related_edges(q_p_new)
			else:
				self.update_related_edges(q_p_new)
		#use dij to find the path
		line_pre, line_dist, time_cost = dijkstra_plan_networkX(self.product, self.beta, weight='cost')
		return line_pre,line_dist,time_cost

	def extend(self,q_p_new,round,method='classic'):
		'''
		classic method is slow
		and the new method is better that I use the round count to avoid search for too many node as transition
		'''
		edge_cost_dic={}
		for node in self.search_graph.nodes:
			if self.PBA['NBA'].has_edge(node[1],q_p_new[1]):
				new_cost=0
				labels_set=set()
				unfeasible_edge=0
				for i in range(len(node[0])):
					if self.PBA['PTS'][i].motact_model.has_edge(node[0][i],q_p_new[0][i]):
						labels_set=labels_set|self.PBA['PTS'][i].motact_model.nodes[node[0][i]]['label']
						cost=self.PBA['PTS'][i].motact_model.edges[(node[0][i],q_p_new[0][i])]['cost']
						new_cost=cost+new_cost
					else:
						unfeasible_edge=1
						break
				if unfeasible_edge:
					continue
				else:
					if self.PBA['NBA'].edges[node[1],q_p_new[1]]['guard'].check(labels_set):

						edge_cost_dic[node]=new_cost
					#self.search_graph.add_edge(node,q_p_new)
		min_cost=100000
		if len(edge_cost_dic)==0:
			return
		for node,cost in edge_cost_dic.items():
			prob_cost=cost+self.search_graph.nodes[node]['cost']
			if prob_cost<min_cost:
				min_cost=prob_cost
				parent_node=node
		self.search_graph.add_node(q_p_new,cost=min_cost,parent_node=parent_node)
		self.search_graph.add_edge(parent_node,q_p_new)

	def rewire(self,q_p_new):
		edge_cost_dic={}
		for node in self.search_graph.nodes:
			if self.PBA['NBA'].has_edge(node[1],q_p_new[1]):
				new_cost=0
				labels_set=set()
				unfeasible_edge=0
				for i in range(len(node[0])):
					if self.PBA['PTS'][i].motact_model.has_edge(node[[0][i]],q_p_new[0][i]):
						labels_set=labels_set|self.PBA['PTS'][i].motact_model.edges[(node[[0][i]],q_p_new[0][i])]['label']
						cost=self.PBA['PTS'][i].motact_model.motact_model.edges[(node[0][i],q_p_new[0][i])]['cost']
						new_cost=cost+new_cost
					else:
						unfeasible_edge=1
						break
				if unfeasible_edge:
					continue
				else:
					if self.PBA['NBA'][node[1],q_p_new[1]]['guard'].check(labels_set):

						edge_cost_dic[node]=new_cost
					#self.search_graph.add_edge(node,q_p_new)
		if len(edge_cost_dic)==0:
			return
		min_cost=100000
		for node,cost in edge_cost_dic.items():
			prob_cost=cost+self.search_graph.nodes[node]['cost']
			if prob_cost<min_cost:
				self.search_graph.remove_edge()
				min_cost=prob_cost
				parent_node=node
		self.search_graph.remove_edge(self.search_graph.nodes[q_p_new]['parent_node'],q_p_new)
		self.search_graph.nodes[q_p_new]['parent_node']=parent_node
		self.search_graph.nodes[q_p_new]['cost']=min_cost
		self.search_graph.add_edge(parent_node,q_p_new)

	def sampling(self):
		#pick a state from a given distribution
		#choose a already found node first

		q_rand_pts_node=self.RqpVt(self.search_graph.nodes)
		#choose a new node randomly?
		new_pts_set=self.get_reachable_set(q_rand_pts_node[0])

		return new_pts_set

	def sampling_improve(self):
		#pick a state from a given distribution
		#choose a already found node first
		q_rand_pts_node=self.RqpVt(self.search_graph.nodes)
		#choose a new node randomly?
		new_pts_set=self.get_reachable_set_list(q_rand_pts_node[0])
		return new_pts_set

	def find_path(self):
		#the method seems to difficult
		#I think use dijstar method is much better?
		#it the performance is really better,just use the old one
		inital=self.initial_state
		goal_list=[]
		for node in self.search_graph.nodes:
			if node[1] in self.PBA['NBA'].graph['accept']:
				goal_list.append(node)
		for goal in goal_list:
			P_T=[goal]
			q_prev=self.search_graph.nodes[goal]['parent_node']
			while not q_prev == inital:
				P_T.append(q_prev)
				q_prev=self.search_graph.nodes[q_prev]['parent_node']
			P_T.append(inital)
		return P_T


	def RqpVt(self,nodes):
		#get a random node of q_rand_pts_node
		node=choice(list(self.search_graph.nodes))
		return node

	def Rpts(self,q_rand_node):
		1

	def get_reachable_set_list(self,q_rand_pts_node,round=10):
		reachable_list=[]
		for j in range(round):
			reachable=[]
			for i in range(len(q_rand_pts_node)):
				reachable.append(choice(list(self.PBA['PTS'][i].motact_model.successors(q_rand_pts_node[i]))))
			reachable_list.append(tuple(reachable))
		return reachable_list

	def get_reachable_set(self,q_rand_pts_node):
		reachable_set=[]
		for i in range(len(q_rand_pts_node)):
			reachable_set.append(choice(list(self.PBA['PTS'][i].motact_model.successors(q_rand_pts_node[i]))))
		return  tuple(reachable_set)