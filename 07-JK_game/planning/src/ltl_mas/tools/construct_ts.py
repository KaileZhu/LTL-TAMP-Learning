# -*- coding: utf-8 -*-
from planning.src.ltl_mas.tools.ltl2ba import run_ltl2ba
from planning.src.ltl_mas.tools.promela import parse as parse_ltl, find_states, find_symbols
from planning.src.ltl_mas.tools.boolean_formulas.parser import parse as parse_guard
import collections

def run_ltl2ba_parse_results(formula):
    """
    Run ltl2ba executable and parse the results.

    Args:
        formula: String. LTL formula as String.

    Returns:
        results: dict. Format {'edges': dict({(f_node, t_node): (guard_formula, guard_expression),
                 'states': [s1,...], 'initials': set([s1,...]), 'accepts': set([s1,...])})}
    """
    promela_string = run_ltl2ba(formula)
    symbols = find_symbols(formula)
    edges = parse_ltl(promela_string)
    (states, initial_states, accept_states) = find_states(edges)
    results = {'edges': {k: (v, parse_guard(v)) for k,v in edges.items()},
               'states': states,
               'initial': initial_states,
               'accept': accept_states}
    return results
