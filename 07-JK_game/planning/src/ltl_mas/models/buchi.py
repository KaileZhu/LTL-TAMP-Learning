# -*- coding: utf-8 -*-
from networkx.classes.digraph import DiGraph

from planning.src.ltl_mas.tools.construct_ts import run_ltl2ba_parse_results


class Buchi(DiGraph):
    """
    Class for buchi automaton.
    """
    def __init__(self, ltl_formula):
        super(Buchi, self).__init__(initial=set(), accept=set())#
        self._formula = ltl_formula
        self._construct_buchi_automaton()


    def _construct_buchi_automaton(self):
        results = run_ltl2ba_parse_results(self.formula)
        #print(self.graph.keys())
        for key in ['initial', 'accept']:
            self.graph[key] = results[key]
        for state in results['states']:
            self.add_node(state)
        for (ef,et) in results['edges'].keys():
            guard_formula, guard_expr = results['edges'][(ef,et)]
            self.add_edge(ef, et, guard_formula=guard_formula, guard=guard_expr)
        print('[Buchi]: Buchi construct from formula %s:'
              ' %d states and %d edges' % (self.formula,
                                           self.number_of_nodes(),
                                           self.number_of_edges()))

    def check_label_for_buchi_edge(self, label, f_buchi_node, t_buchi_node):
        """
        Check buchi edge against a label.
        """        
        if not self.has_edge(f_buchi_node, t_buchi_node):
            raise KeyError('[Buchi]: Edge (%s, %s) not in buchi' % (f_buchi_node, t_buchi_node))
        truth = self.edges[f_buchi_node, t_buchi_node]['guard'].check(label)
        dist = 0
        return truth, dist

    @property
    def formula(self):
        return self._formula
