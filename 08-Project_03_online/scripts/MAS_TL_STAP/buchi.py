#！/usr/bin/env python3
'''
@Date   : 2023/11 -->  
@Authors: Junjie Wang
@Contact: pkuwjj1998@163.com
@Version: 1.0
@Descrip: the module contains basic class for the buchi automaton, and provides
        a series of function to modify the automaton.
@Log:
        - 2023/11/16: the first version
'''

from graphviz import Digraph
from networkx.classes.digraph import DiGraph
from itertools import chain, combinations

from .LTL2BA.gltl2ba import run_ltl2ba, parse_promela
from .LTL2BA.boolean_formulas.parser import parse_guard as parse

class DotGraph:
    """
    Class for the graph in DOT format, which is used to draw the buchi automaton.
    """
    def __init__(self):
        self.dot = Digraph()

    def title(self, str):
        self.dot.graph_attr.update(label=str)

    def node(self, name, label, accepting=False):
        num_peripheries = '2' if accepting else '1'
        self.dot.node(name, label, shape='circle', peripheries=num_peripheries)

    def edge(self, src, dst, label):
        self.dot.edge(src, dst, label)

    def show(self):
        self.dot.render(view=True)

    def save_render(self, path, on_screen):
        self.dot.render(path, view=on_screen)

    def save_dot(self, path):
        self.dot.save(path)

    def __str__(self):
        return str(self.dot)


class BuchiAuto(DiGraph):
    """
    Class for the Buchi Automaton.
    """
    def __init__(self, task_formula, ):
        super(BuchiAuto, self).__init__(initial=set(), accept=set())
        self._formula = task_formula
        self.constr_buchi_auto()

    def constr_buchi_auto(self):
        """
        Construct the buchi automaton according to the ltl formula.
        """
        self._promela = run_ltl2ba(self.formula)    # ltl2ba的输出是一串string
        nodes, edges = parse_promela(self.promela)  # 根据string得到节点与边的信息
        # 根据nodes信息把节点添加到buchi自动机的有向图中
        for node in nodes:
            if 'init' in nodes[node]:   # nodes的数据格式：{'name':[label,'accept'(若可接收则有这一项)]}
                self.add_node(node, label=nodes[node][0], accept=False)
                self.graph['initial'].add(node)     # add：集合中添加元素
            elif 'accept' in nodes[node]:
                self.graph['accept'].add(node)
                self.add_node(node, label=nodes[node][0], accept=True)
            else:
                self.add_node(node, label=nodes[node][0], accept=False)
        # 根据edges信息把边添加到buchi自动机的有向图中
        for (ef, et) in edges:   # edges的数据格式：{(src_node, dst_node):(label,parse_guard(label))}
            (formula, express) = edges[(ef, et)]
            self.add_edge(ef, et, guard_formula=formula, guard_express=express)
        print('\n----------------------------------------')
        print('[Buchi]: Construct from formula %s: %d states and %d edges.' 
                %(self.formula, self.number_of_nodes(), self.number_of_edges()))

    def draw_buchi_auto(self):
        """
        Draw the graph of the buchi automaton by DOT.
        """
        graph = DotGraph()
        for node in self.nodes():
            if self.nodes[node]['accept']:
                graph.node(node, self.nodes[node]['label'], accepting=True)
            else:
                graph.node(node, self.nodes[node]['label'], accepting=False)
        for edge in self.edges():
            graph.edge(edge[0], edge[1], self.edges[edge]['formula'])
        graph.show()

    def gener_poset_by_anytime(self, time_budget):
        """
        Generate the set of partial relations according to the buchi automaton.
        * (wang): this is for temporary use
        """
        from .new_poset_builder import Buchi_poset_builder
        self.poset = Buchi_poset_builder(self.formula)
        self.poset.main_fun_to_get_poset(time_budget)

    def check_label_for_buchi_edge(self, label, node_s, node_t):
        """
        Check buchi edge against a label.
        """
        if not self.has_edge(node_s, node_t):
            raise KeyError('[Buchi]: Edge (%s, %s) not in buchi!'
                            %(node_s, node_t))
        truth = self.edges[node_s, node_t]['guard'].check(label)
        dist = 0
        return truth, dist

    @property
    def formula(self):
        return self._formula

    @property
    def promela(self):
        return self._promela