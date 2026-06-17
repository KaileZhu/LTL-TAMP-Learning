dic_zanshu={'basic_obs':'基础侦查',
                    'basic_atk':'基础进攻',
                    'order_obs':'顺序侦查',
                    'order_atk':'顺序进攻',
                    'order_support':'顺序支持',
                    'basic_support':'基础支持'}
anti_dic_zanshu={v:k for k,v in dic_zanshu.items()}
map_dic_to_num={'a':'001','b':'002','c':'003','d':'004','e':'005','f':'006','g':'007','h':'008','i':'009','j':'010',
                'k':'011','l':'012','m':'013','n':'014','o':'015','p':'016','q':'017','r':'018','s':'019','t':'020',
                'u':'021','v':'022','w':'023','x':'024','y':'025','z':'026'}
num_dic_to_map={v:k for k,v in map_dic_to_num.items()}
operation_dic={'全面进攻':'Global_attack',

'步步为营':'Bubuweiying',

'围点打援':'WeiDianDaYuan',

'占场扫描':'ZanChangShaoMiao',

'重点防御':'Key_defense',
'防守反击':'Defense_counterattack',
'大规模任务测试':'daguimo'
}
red_dic_to_name={'红方':'redall'}
blue_dic_to_name={'蓝方':'all','无人机':'uav','炮兵':'artillery','步兵':'infantry'}
name_dic_to_blue={v:k for k,v in blue_dic_to_name.items()}

def change_goal_task_pair( input):
    # 调整一下格式
    # {'场景选择': '想定场景2', '算法选择': '分支定界法', '算法路径':
    # 'planning\\src\\ltl_mas\\tools\\B_A_B.py', '偏好选择':
    # '执行速度优先', '战法选择': '占场扫描', '条例选择': ['禁止攻击'],
    # '战法内容': {'1': {'顺序侦查': [['红方', '001', '蓝方', '动态'],
    # ['红方', '002', '蓝方', '动态'], ['红方', '003', '蓝方', '动态']]},
    # '2': {'顺序进攻': [['红方', '001', '蓝方', '动态'], ['红方', '001', '蓝方', '动态'],
    # ['红方', '001', '蓝方', '动态']], '基础进攻': [['红方', '002', '蓝方', '动态'],
    # ['红方', '003', '蓝方', '动态']]}, '3': {'基础支持': [['红方', '002', '蓝方', '动态'],
    # ['红方', '003', '蓝方', '动态']], '基础侦查': [['红方', '002', '蓝方', '动态'], ['红方', '003', '蓝方', '动态']]}}}
    new_input = {}
    prefer = input['偏好选择']
    # {0:{'basic_atk':[[{'place': 'l', 'goal': 'infantry'},
    #                             {'place': 'l', 'goal': 'artillery'}]]},
    #             1:{'basic_atk':[[{'place': 'l', 'goal': 'all'}]]},
    #             2:{'basic_support':[[{'place': 'l', 'goal': 'all'}]],
    #                "basic_atk":[[{'place': 'g', 'goal': 'all'}]]},
    #             3:{"basic_support":[[{'place': 'g', 'goal': 'all'}]],
    #                "basic_atk":[[{'place': 'm', 'goal': 'all'}]]},
    #             4:{"basic_support":[[{'place': 'm', 'goal': 'all'}]]}
    #             }
    for waves, operation_list in input['战法内容'].items():
        new_input[int(waves) - 1] = {}
        for method_name, detail_list in operation_list.items():
            new_input[int(waves) - 1][anti_dic_zanshu[method_name]] = []
            part_list = []
            for red, place, blue, state in detail_list:
                red_name = 'redall'
                place_name = num_dic_to_map[place]
                blue_name = blue_dic_to_name[blue]
                part_list.append({'subject': red_name, 'place': place_name, 'goal': blue_name})
            new_input[int(waves) - 1][anti_dic_zanshu[method_name]].append(part_list)
    print('new_input', new_input)
    return new_input, prefer