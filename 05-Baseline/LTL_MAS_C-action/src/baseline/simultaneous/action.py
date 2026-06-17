# -*- coding: utf-8 -*-
from src.ltl_mas.tools.boolean_formulas.parser import parse as parse_guard

class LocalActionModel(object):
    """
    Class for local actions.
    """
    def __init__(self, field, under_flow=0.001):
        """
        Args:
            action_dict: dict. Format {act_name: (cost, guard_formula, labels)}
        """

        self._raw = field.input_data.task_type
        self._action = dict()
        for act_name, attrib in self.raw.items():
            if act_name[-2] in ['0','1','2','3','4','5','6','7','8','9']:
                guard_formula=act_name[-3::]
                new_act_name=act_name[0:-3]
            else:
                guard_formula=act_name[-2::]
                new_act_name=act_name[0:-2]
            cost =attrib[0]
            if guard_formula is None:
                guard_expr=parse_guard('1')
                guard_labels={'1'}
            else:
                guard_expr = parse_guard(guard_formula)
                guard_labels={guard_formula}
            labels=set([act_name])
            self._action[act_name] = (cost, guard_expr, labels,guard_labels)
        #for act_name, attrib in self.raw.items():
        #    cost, guard_formula, labels = attrib[0:3]
        #    if guard_formula is None :
        #        guard_expr = parse_guard('1')
        #    else:
        #        guard_expr = parse_guard(guard_formula)
        #    self._action[act_name] = (cost, guard_expr, labels)
        self._action['None'] = (under_flow, parse_guard('1'), set(),set())

    def find_allowed_local_actions(self, props):
        """
        Args:
            props: set. Set of propositions that are true.
        """
        allowed_actions = set()
        for act_name, attrib in self.action.items():
            guard_expr = attrib[1]
            if (guard_expr.check(props)):
                allowed_actions.add(act_name)
        return allowed_actions

    @property
    def raw(self):
        return self._raw

    @property
    def action(self):
        return self._action


class MacroActionModel(object):
    """
    Class for marco actions.
    """

    def __init__(self, marco_actions):
        """
        Args:
            marco_actions: dict. Format: {marco_act_name: (cost, condition, labels)}
                           where condition = {{agent_name1, agent_name2...}: local_act_name,...}.
                           It means that any agent of the set should perform local_act_name.
                           *FOR NOW, only one agent is asked for one local action, and non repetitive.*
        """
        self.action = marco_actions

    def find_allowed_marco_actions(self, agents_action_data):
        """
        Check which marco actions are allowed given the agents action data.
        Args:
            agents_action_data: dict. {agent_1_name: set([allowed_local_actions]),...}
        """
        allowed_marco_actions = []
        for marco_act, attrib in self.action.items():
            condition = attrib[1]
            if self._check_marco_act_condition(condition, agents_action_data):
                allowed_marco_actions.append(marco_act)
        return allowed_marco_actions

    @staticmethod
    def _check_marco_act_condition(condition, agents_action_data):
        for agents, local_act in condition.items():
            # **** EXTENSION HERE ****
            if len(agents) > 1:
                raise ValueError('[MarcoActionModel]: No than one agent per local'
                                 ' action is not implemented yet.')
            # **** EXTENSION HERE ****
            # THIS ONLY WORKS FOR SINGLE AGENT, AND NON REPETITIVE.
            agent = list(agents)[0]
            if (agent not in agents_action_data) or (local_act not in agents_action_data[agent]):
                return False
        return True

    @property
    def action(self):
        return self._action
