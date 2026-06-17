# -*- coding: utf-8 -*-
from src.ltl_mas.visualization.LTL_plotter import ProdAut_Run
from collections import defaultdict
from networkx import dijkstra_predecessor_and_distance
import time
import numpy as np


#===========================================
#optimal initial synthesis
#===========================================

def vitural_dijkstra_predecessor_and_distance(agents,product,buchi,time_budget,start,end):
	'''
	input fianl buchi,
	cost definition (0,pre_max_time)
	cost relation 1
	'''
	for prod_init in product.graph['initial']:
	#prod_init=product.graph['initial']
	#print('init=',prod_init)
		line = {}
		line_pre, line_dist = dijkstra_predecessor_and_distance(product, prod_init,weight='cost')
		accept_node_set=[]
		for node in product.graph['accept']:
			if line_dist[node]!=np.inf:
				accept_node_set.append(node)
		path_list=[]
		for node in accept_node_set:
			path_list=compute_path_from_pre(line_pre,line)
		path_dic={}
		for path in path_list:
			num_list=[node[0] for node in path]
			node_dic={}
			for i in range(len(num_list)):
				if num_list[i] not in node_dic.keys():
					node_dic[num_list[i]]=line_dist[path[i]]
				else:
					node_dic[num_list[i]]=max(line_dist[path[i]],node_dic[num_list[i]])
			keys_list=np.sort(node_dic.keys())
			for i in range(len(keys_list)-1):
				node_dic[i+1]=node_dic[keys_list[i+1]]-node_dic[keys_list[i]]
			max_time=0
			for i,j in node_dic.items():
				max_time=max(max_time,j)
			path_dic[path]=max_time
		shortest_time=100000000
		for i,j in path_dic:
			shortest_time=min(shortest_time,j)
	return path_dic, shortest_time

def dijkstra_plan_networkX(product, beta=10,weight='cost'):
	# requires a full construct of product automaton
	start = time.time()
	runs = {}
	loop = {}
	# minimal circles
	#print(product.graph['accept'])
	for prod_init in product.graph['initial']:
		#prod_init=product.graph['initial']
		#print('init=',prod_init)
		line = {}
		line_pre, line_dist = dijkstra_predecessor_and_distance(product, prod_init,weight=weight)
		for target in iter( product.graph['accept']):
			if target in line_dist:
				line[target] =line_dist[target]
		opti_targ = min(line, key = line.get)
		print('final_node',opti_targ)
		prefix = compute_path_from_pre(line_pre, opti_targ)
		precost = line_dist[opti_targ]
		print('cost =',precost)
		print('prefix =',prefix)
		print('synchronize times')
	# best combination
	return line_pre,line_dist,prefix

def compute_path_from_pre(pre, target):#here occur the dead circle!!
	#print 'pre: %s with size %i' %(pre, len(pre))
	n = target
	path = [n]
	#print('n==',n)
	#print('pre=',pre)
	while (n in pre):
		'''
		the function here fall into the (((0, 0, 1), 'None'), 'T2_init')
		n=(((0, 0, 1), 'None'), 'T2_init')
		pre[n]=(((0, 0, 1), 'None'), 'T2_init')
		n=pre[n][0]
		'''
		#print 'before append'
		#print 'now at node %s' %str(n)
		pn_list = pre[n]
		#print 'its pre_list %s' %str(pn_list)
		if not pn_list:
			break
		if (pn_list[0]==n):
			break
		pn = pn_list[0]
		#print '[0] of pn_list %s' %str(pn)
		path.append(pn)
		#print 'path: %s' %path
		n = pn
		#print(n)
	path.reverse()
	return path





