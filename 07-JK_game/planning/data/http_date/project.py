first_gantt_garph={0: {'task_name': 'observe', 'begin_time': 1.0, 'duration': 1},
 1: {'task_name': 'observe', 'begin_time': 1.0, 'duration': 1},
 2: {'task_name': 'observe', 'begin_time': -0.0, 'duration': 1},
 3: {'task_name': 'attack', 'begin_time': 2.0, 'duration': 1},
 4: {'task_name': 'attack', 'begin_time': 2.0, 'duration': 1},
 5: {'task_name': 'attack', 'begin_time': 3.0, 'duration': 1}}

final_gantt_graph={1: {'task_name': 'observe', 'begin_time': 1, 'duration': 8},
 2: {'task_name': 'observe', 'begin_time': 1, 'duration': 7},
 0: {'task_name': 'observe', 'begin_time': 9, 'duration': 7},
 3: {'task_name': 'attack', 'begin_time': 17, 'duration': 32},
 4: {'task_name': 'attack', 'begin_time': 17, 'duration': 12},
 5: {'task_name': 'attack', 'begin_time': 50, 'duration': 52}}

zanfa_data_list=["全面进攻","步步为营","围点打援","占场扫描","联合防御","围魏救赵"]


zanfa_date={'全面进攻':{
'zanfa_name':"全面进攻",
  "zanfa_group":['基础进攻','顺序进攻','顺序侦查','基础侦查'],
 "zanfa_explain":"全面进攻，能以特定顺序对多个目标区域进行侦查，随后发起进攻",
 'zanfa_example':
'''波次          |     战法            |        主体        地点    目标  （子任务属性）
        1                    基础侦查             红方            g       蓝方
                                                      红方            l        蓝方
                                                      红方            m       蓝方
         2                  基础攻击              红方            l          步兵
                                                       红方            l           炮兵
         3                 基础攻击                红方          l          蓝方'''
},
'步步为营':{
'zanfa_name':"步步为营",
  "zanfa_group":['顺序支持','基础支持','顺序侦查','基础侦查'],
 "zanfa_explain":"依次的蚕食敌方区域，
   维持占据空间，压缩敌方战场面
   积。并控制战争烈度",
 'zanfa_example':
'''  波次          |     战法            |        主体        地点    目标  （子任务属性）
    1                     基础进攻             红方         l           炮兵
                                                     红方         l          步兵
    2                     基础进攻               红方       l          蓝方
    3                     基础支持               红方       l         蓝方
                           基础攻击              红方        g       蓝方
   4                     基础支持              红方          g        蓝方
                          基础攻击              红方         m        蓝方
   5                     基础支持              红方         m        蓝方
 '''
}
}