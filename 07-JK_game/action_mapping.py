action_mapping = {
    'moveactions+rule_forbidden_attack': '动作类别1',
    'moveactions+rule_forbidden_damage': '动作类别2',
    'moveactions+rule_limit_fire': '动作类别3',
    'moveactions+rule_ignore_threat': '动作类别4',
    'moveactions+rule_safe_range': '动作类别5',
    'moveactions+': '动作类别6',
    'fireactions+rule_forbidden_attack': '动作类别7',
    'fireactions+rule_forbidden_damage': '动作类别8',
    'fireactions+rule_limit_fire': '动作类别9',
    'fireactions+rule_ignore_threat': '动作类别10',
    'fireactions+rule_safe_range': '动作类别11',
    'fireactions+': '动作类别12',
    'areascoutactions+rule_forbidden_attack': '动作类别13',
    'areascoutactions+rule_forbidden_damage': '动作类别14',
    'areascoutactions+rule_limit_fire': '动作类别15',
    'areascoutactions+rule_ignore_threat': '动作类别16',
    'areascoutactions+rule_safe_range': '动作类别17',
    'areascoutactions+': '动作类别18',
    'linescoutactions+rule_forbidden_attack': '动作类别19',
    'linescoutactions+rule_forbidden_damage': '动作类别20',
    'linescoutactions+rule_limit_fire': '动作类别21',
    'linescoutactions+rule_ignore_threat': '动作类别22',
    'linescoutactions+rule_safe_range': '动作类别23',
    'linescoutactions+': '动作类别24',
    'pointscoutactions+rule_forbidden_attack': '动作类别25',
    'pointscoutactions+rule_forbidden_damage': '动作类别26',
    'pointscoutactions+rule_limit_fire': '动作类别27',
    'pointscoutactions+rule_ignore_threat': '动作类别28',
    'pointscoutactions+rule_safe_range': '动作类别29',
    'pointscoutactions+': '动作类别30',
    'ruleadding+rule_forbidden_attack': '动作类别31',
    'ruleadding+rule_forbidden_damage': '动作类别32',
    'ruleadding+rule_limit_fire': '动作类别33',
    'ruleadding+rule_ignore_threat': '动作类别34',
    'ruleadding+rule_safe_range': '动作类别35',
    'ruleadding+': '动作类别36',

}







def command_printer(command, rule_index=0):
    rule = ['rule_forbidden_attack', 'rule_forbidden_damage', 'rule_limit_fire', 'rule_ignore_threat', 'rule_safe_range', '']
    print("当前仿真步长下，输出动作为", command)
    mapping_list = []
    for key, actions in command.items():
        for action in actions:
            if key == 'scoutactions':
                key = 'point'+key
            mapping_list.append(action_mapping[key+'+'+rule[rule_index]])
    # mapping_list.append(action_mapping['pointscoutactions'+'+'+rule[rule_index]])
    print("映射到行为方案库，动作为",mapping_list)




