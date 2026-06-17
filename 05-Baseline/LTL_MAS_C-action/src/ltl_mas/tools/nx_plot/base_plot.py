import networkx as nx
import numpy as np

def getweight(bu,i):
	return bu.edges[i]['guard_formula']


def getmiddlepos(e,p):
	x=np.array(p[e[0]])
	y=np.array(p[e[1]])
	z=(x+x+y)/3
	return tuple(z)


def plot(j,bu):
	pos=nx.shell_layout(bu)
	li=list(bu.nodes)
	nx.draw_networkx_nodes(bu,pos,li)
	nx.draw_networkx_edges(bu,pos)
	lables={}
	for i in li:
		lables[i]=i
	nx.draw_networkx_labels(bu,pos,lables)
	label={}
	for i in bu.edges:
		if j:
			if not i[0]==i[1]:
				label[i]=getweight(bu,i)
		else:
			label[i] = getweight(bu,i)
	pos2={}
	for e in bu.edges:
		if j:
			if not e[0]==e[1]:
				pos2[e]=getmiddlepos(e,pos)
				pos2[0]=(0,0)
		else:
			pos2[e] = getmiddlepos(e, pos)
			pos2[0] = (0, 0)
	nx.draw_networkx_labels(bu,pos2,label,alpha=1)