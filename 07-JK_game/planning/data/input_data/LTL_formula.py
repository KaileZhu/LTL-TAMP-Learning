# high level task as:
operation_atom=['Spy_Scout','Cop_Assault','Feint_strike','Follow_protect']
operation_structure={'Spy_Scout':['Scout'],
					'Cop_Assault':['Cop_Assault'],
					'Fei_Strike':['Feint'],
					'Fol_Protect':['Follow','Defend'],
                     'Spy_obs':['obs_s'],
                     'Coordinate_attack':['coordinate_attack']}

# mid level task formula
tactics_atom=['Scout','Assault','Feint','Defend','Follow','obs_s','coordinate_attack']
tactics_structure={'Scout':'<> ( _1_ && <> _2_) && [] ( _1_ -> ! _2_)',
                   'Assault':'<> ( _0_ && <> _2_)',
                   'Feint':'<> ( _0_ && <> _2_)',
                   'Defend':'<> ( _0_ && <> _2_)',
                   'Follow':'<> ( _0_ && <> _2_)',
                   'fire_obs':'<>( _1_a_ && <> _2_b_ && <> _2_c_ ) && [] ( _1_a_ -> !_2_b_) && []'
                           '( _1_a_ -> ! _2_c_) ',
                   'order_obs': '<>( _1_a_ && <> _2_b_ && <> _2_c_ ) && [] ( _1_a_ -> !_2_b_) && []( _1_a_ -> ! _2_c_)',
                   'basic_obs':'<> _1_a_ && <> _2_b_ && _2_c_',
                    'basic_atk':'<> _0_a_ && <> _0_b_ && <> _0_c_',
                   'virtual_atk': '<>_0_a_',
                   'basic_support':'<>_3_a_',
                   'obs_support':  '<>_1_a_ && _3_a_',
                   'order_atk':'<> (_0_a_ && <> _0_b_ && <> _0_c_) && [] (_0_a_ -> ! _0_b_)'
                                       '&& [](_0_a_ -> ! _0_c_) && <> _0_d_ ',
                   'fire_atk':'<>( _1_a_ && <> _2_b_ && <> _2_c_ ) && [] ( _1_a_ -> !_2_b_) && []'
                           '( _1_a_ -> ! _2_c_) ',
                   'basic_trick':'<>_4_a_'
}
#add more
default_tactics_dic={'order_obs':{'a':{'subject':'redall','goal':'all'},
                    'b':{'subject':'redall','goal':'radar'},
                    'c':{'subject':'redall','goal':'Command'}},
'order_atk':{'a':{'subject':'redall','goal':'command'},
                    'b':{'subject':'redall','goal':'radar'},
                    'c':{'subject':'redall','goal':'all'},'d':{'subject':'redall','goal':'all'}},
'basic_obs':{'a':{'subject':'redall','goal':'command'},
                    'b':{'subject':'redall','goal':'radar'},
                    'c':{'subject':'redall','goal':'all'},'d':{'subject':'redall','goal':'all'}} ,
'basic_atk':{'a':{'subject':'redall','goal':'command'},
                    'b':{'subject':'redall','goal':'radar'},
                    'c':{'subject':'redall','goal':'all'},'d':{'subject':'redall','goal':'all'}},
'basic_support':{'a':{'subject':'redall','goal':'command'},
                    'b':{'subject':'redall','goal':'radar'},
                    'c':{'subject':'redall','goal':'all'},'d':{'subject':'redall','goal':'all'}}
                    }
specially_action_structure={'order_atk','order_obs','basic_obs','basic_atk','basic_support','order_support','basic_trick'}
basic_method=['Global_scan','Global_attack','WeiDianDaYuan','Bubuweiying','ZanChangShaoMiao']
basic_rule=['dafault','missile','cannonry','safety','airdefense','guidance']
#战法设计 全面进攻 普通侦查 加 普通攻击
#       步步为营  进攻，占据
#       围点打援  侦查，进攻，占据
#       占场扫描
#       重点防御
#       防御反击
basic_structure={'Global_attack':['basic_obs','order_obs','basic_atk','order_atk','basic_support','order_support','basic_trick'],
                 'Bubuweiying':['basic_obs','order_obs','basic_atk','order_atk','basic_support','order_support','basic_trick'] ,
                 'WeiDianDaYuan':['basic_obs','order_obs','basic_atk','order_atk','basic_support','order_support','basic_trick'],
                 'ZanChangShaoMiao':['basic_obs','order_obs','basic_atk','order_atk','basic_support','order_support','basic_trick'],
                 'Key_defense':['basic_obs','order_obs','basic_atk','order_atk','basic_support','order_support','basic_trick'],
                 'Defense_counterattack':['basic_obs','order_obs','basic_atk','order_atk','basic_support','order_support','basic_trick'],
                 'daguimo':['basic_obs','order_obs','basic_atk','order_atk','basic_support','order_support','basic_trick']
                }

Place_structure={'Global_attack':{0:{'basic_obs': {'place':('blue',[0,1,2])},
                                     'basic_trick':{'place':('blue',[0,1])}},
                                      1:{'basic_atk':{'place':('blue',[0,0])}},
                                      2:{'basic_atk': {'place':('blue',[0])}}},
                 'Bubuweiying':{0:{'basic_atk':{'place':('blue',[0,0])}},
                                1:{'basic_atk':{'place':('blue',[0])}},
                                2:{'basic_support':{'place':('blue',[0])},
                                   "basic_atk":{'place':('blue',[1])}},
                                3:{"basic_support":{'place':('blue',[1])},
                                   "basic_atk":{'place':('blue',[2])}},
                                4:{"basic_support":{'place':('blue',[2])}}
                     },
'WeiDianDaYuan':{0: {'order_obs': {'place':('blue',[0,1,2])}},
                      1: {'basic_support': {'place':('blue',[1,2])},
                          'order_atk':{'place':('blue',[0,0,0]),'goal':['infantry','artillery','all']}
                          }},
'ZanChangShaoMiao': {0: {'order_obs': {'place':('blue',[0,1,2])},
                         'basic_trick':{'place':('blue',[0,1])}
                         },
                      1: { 'order_atk':{'place':('blue',[0,0,0]),'goal':['infantry','artillery','all']},
                          'basic_atk':{'place':('blue',[1,2])}
                          },
                     2:{'basic_support': {'place':('blue',[1,2])},
                        'basic_obs': {'place':('blue',[1,2])}

                        }},
'Key_defense':{0: {'basic_obs': {'place':('blue',[0,1,2])},
                    'basic_support': {'place':('red',[0,1])}
                   }  }
               ,
'Defense_counterattack':{0: {'basic_obs': {'place':('blue',[0,1,2])},
                        'basic_support': {'place':('red',[0,1])},
                             'basic_trick':{'place':('blue',[0,1])}
                   },
                      1: {'basic_atk':{'place':('blue',[0,1])   } }
               } ,

'daguimo':{0: {'basic_obs': {'place':('blue',[0,1,2])},
                        'basic_support': {'place':('blue',[0,1])}
                   },
            1: {'basic_atk':{'place':('blue',[0,1,2])}
                          },
           2: {'basic_support':{'place':('blue',[0,1,2])}
                          },
           3: { 'order_atk':{'place':('blue',[0,1,2])},
                          'basic_atk':{'place':('blue',[0,1])}
                          },
4: {'basic_obs': {'place':('blue',[0,1,2])},
                        'basic_support': {'place':('blue',[0,1])}
                   },
            5: {'basic_atk':{'place':('red',[0,1,2])}
                          },
           6: {'basic_support':{'place':('red',[0,1,2])}
                          },
           7: { 'order_atk':{'place':('blue',[0,1,2])},
                          'basic_atk':{'place':('blue',[0,1])}
                          }}}

Pre_define_struture={'Global_attack':{0:{'basic_obs': [[{'subject': 'redall', 'place': 'g', 'goal': 'all','state':'stay'},
                                                    {'subject': 'redall', 'place': 'l', 'goal': 'all','state':'stay'},
                                                    {'subject': 'redall', 'place': 'm', 'goal': 'all','state':'stay'}]
                                                   ],
                                         'basic_trick':[[{'subject': 'redall', 'place': 'g', 'goal': 'all','state':'stay'},
                                                    {'subject': 'redall', 'place': 'l', 'goal': 'all','state':'stay'}]]
                                         },
                                      1:{'basic_atk': [[{'subject': 'redall','place': 'l', 'goal': 'infantry','state':'stay'},
                                                    {'subject': 'redall','place': 'l', 'goal': 'artillery','state':'stay'}]
                                                   ]},
                                      2:{'basic_atk': [[{'subject': 'redall', 'place': 'l', 'goal': 'all','state':'stay'}]
                                                   ]}},
'Bubuweiying':{0:{'basic_atk':[[{'subject': 'redall', 'place': 'l', 'goal': 'infantry','state':'stay'},
                                     {'subject': 'redall','place': 'l', 'goal': 'artillery','state':'stay'}]]},
                     1:{'basic_atk':[[{'subject': 'redall','place': 'l', 'goal': 'all','state':'stay'}]]},
                     2:{'basic_support':[[{'subject': 'redall','place': 'l', 'goal': 'all','state':'stay'}]],
                        "basic_atk":[[{'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'}]]},
                     3:{"basic_support":[[{'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'}]],
                        "basic_atk":[[{'subject': 'redall','place': 'm', 'goal': 'all','state':'stay'}]]},
                     4:{"basic_support":[[{'subject': 'redall','place': 'm', 'goal': 'all','state':'stay'}]]}
                     },
'WeiDianDaYuan':{0: {'order_obs': [[{'subject': 'redall', 'place': 'g', 'goal': 'all','state':'stay'},
                                    {'subject': 'redall', 'place': 'l', 'goal': 'all','state':'stay'},
                                    {'subject': 'redall', 'place': 'm', 'goal': 'all','state':'stay'}]
                                   ]},
                      1: {'basic_support': [[{'subject': 'redall','place': 'm', 'goal': 'all','state':'stay'},
                                            {'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'}]
                                            ],
                          'order_atk':[[{'subject': 'redall','place': 'l', 'goal': 'infantry','state':'stay'},
                                        {'subject': 'redall','place': 'l', 'goal': 'artillery','state':'stay'},
                                        {'subject': 'redall', 'place': 'l', 'goal': 'all','state':'stay'}]]
                          }},
'ZanChangShaoMiao': {0: {'order_obs': [[{'subject': 'redall', 'place': 'g', 'goal': 'all','state':'stay'},
                                    {'subject': 'redall', 'place': 'l', 'goal': 'all','state':'stay'},
                                    {'subject': 'redall', 'place': 'm', 'goal': 'all','state':'stay'}]
                                   ],
                        'basic_trick': [[{'subject': 'redall', 'place': 'g', 'goal': 'all','state':'stay'},
                                    {'subject': 'redall', 'place': 'm', 'goal': 'all','state':'stay'}]
                                   ],
                         },
                      1: { 'order_atk':[[{'subject': 'redall','place': 'l', 'goal': 'infantry','state':'stay'},
                                        {'subject': 'redall','place': 'l', 'goal': 'artillery','state':'stay'},
                                        {'subject': 'redall', 'place': 'l', 'goal': 'all','state':'stay'}]],
                          'basic_atk':[[{'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'},
                                        {'subject': 'redall','place': 'm', 'goal': 'artillery','state':'stay'}]]
                          },
                     2:{'basic_support': [[{'subject': 'redall','place': 'm', 'goal': 'all','state':'stay'},
                                            {'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'}]
                                            ],'basic_obs': [[{'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'},
                                            {'subject': 'redall','place': 'l', 'goal': 'all','state':'stay'}]
                                            ]

                        }},
'Key_defense':{0: {'basic_obs': [[{'subject': 'redall', 'place': 'g', 'goal': 'all','state':'stay'},
                                    {'subject': 'redall', 'place': 'l', 'goal': 'all','state':'stay'},
                                    {'subject': 'redall', 'place': 'm', 'goal': 'all','state':'stay'}]
                                   ],
                    'basic_support': [[{'subject': 'redall','place': 'm', 'goal': 'all','state':'stay'},
                                            {'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'}]
                                            ]
                   }  }
               ,
'Defense_counterattack':{0: {'basic_obs': [[{'subject': 'redall', 'place': 'g', 'goal': 'all','state':'stay'},
                                    {'subject': 'redall', 'place': 'l', 'goal': 'all','state':'stay'},
                                    {'subject': 'redall', 'place': 'm', 'goal': 'all','state':'stay'}]
                                   ],
                        'basic_support': [[{'subject': 'redall','place': 'm', 'goal': 'all','state':'stay'},
                                            {'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'}]
                                            ],
                             'basic_trick':[[{'subject': 'redall','place': 'm', 'goal': 'all','state':'stay'},
                                            {'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'}]]
                   },
                      1: {'basic_atk':[[{'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'},
                                        {'subject': 'redall','place': 'm', 'goal': 'artillery','state':'stay'}]]
                          }
               } ,
'daguimo':{0: {'basic_obs': [[{'subject': 'redall', 'place': 'g', 'goal': 'all','state':'stay'},
                                    {'subject': 'redall', 'place': 'l', 'goal': 'all','state':'stay'},
                                    {'subject': 'redall', 'place': 'm', 'goal': 'all','state':'stay'}]
                                   ],
                        'basic_support': [[{'subject': 'redall','place': 'm', 'goal': 'all','state':'stay'},
                                            {'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'}]
                                            ]
                   },
            1: {'basic_atk':[[{'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'},
                                        {'subject': 'redall','place': 'm', 'goal': 'artillery','state':'stay'},
                            {'subject': 'redall','place': 'm', 'goal': 'all','state':'stay'}
                              ]]
                          },
           2: {'basic_support':[[{'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'},
                                        {'subject': 'redall','place': 'm', 'goal': 'artillery','state':'stay'},
                            {'subject': 'redall','place': 'm', 'goal': 'all','state':'stay'}
                              ]]
                          },
           3: { 'order_atk':[[{'subject': 'redall','place': 'l', 'goal': 'infantry','state':'stay'},
                                        {'subject': 'redall','place': 'l', 'goal': 'artillery','state':'stay'},
                                        {'subject': 'redall', 'place': 'l', 'goal': 'all','state':'stay'}]],
                          'basic_atk':[[{'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'},
                                        {'subject': 'redall','place': 'm', 'goal': 'artillery','state':'stay'}]]
                          },
4: {'basic_obs': [[{'subject': 'redall', 'place': 'g', 'goal': 'all','state':'stay'},
                                    {'subject': 'redall', 'place': 'l', 'goal': 'all','state':'stay'},
                                    {'subject': 'redall', 'place': 'm', 'goal': 'all','state':'stay'}]
                                   ],
                        'basic_support': [[{'subject': 'redall','place': 'm', 'goal': 'all','state':'stay'},
                                            {'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'}]
                                            ]
                   },
            5: {'basic_atk':[[{'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'},
                                        {'subject': 'redall','place': 'm', 'goal': 'artillery','state':'stay'},
                            {'subject': 'redall','place': 'm', 'goal': 'all','state':'stay'}
                              ]]
                          },
           6: {'basic_support':[[{'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'},
                                        {'subject': 'redall','place': 'm', 'goal': 'artillery','state':'stay'},
                            {'subject': 'redall','place': 'm', 'goal': 'all','state':'stay'}
                              ]]
                          },
           7: { 'order_atk':[[{'subject': 'redall','place': 'l', 'goal': 'infantry','state':'stay'},
                                        {'subject': 'redall','place': 'l', 'goal': 'artillery','state':'stay'},
                                        {'subject': 'redall', 'place': 'l', 'goal': 'all','state':'stay'}]],
                          'basic_atk':[[{'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'},
                                        {'subject': 'redall','place': 'm', 'goal': 'artillery','state':'stay'}]]
                          },4: {'basic_obs': [[{'subject': 'redall', 'place': 'g', 'goal': 'all','state':'stay'},
                                    {'subject': 'redall', 'place': 'l', 'goal': 'all','state':'stay'},
                                    {'subject': 'redall', 'place': 'm', 'goal': 'all','state':'stay'}]
                                   ],
                        'basic_support': [[{'subject': 'redall','place': 'm', 'goal': 'all','state':'stay'},
                                            {'subject': 'redall','place': 'g', 'goal': 'all','state':'stay'}]
                                            ]
                   }
        }
                     }
# missile 导弹干扰  有防空火力则发射巡飞弹到目标区域
# cannonry 火炮支持  攻击目标
# behead  斩首 若有敌方的commander 则进行攻击
# airdefense 防空支持  对目标区域添加防空单位
# guidance 激光引导  对攻击目标进行激光引导
rule_structure={'missile':{'LTL': '<> _0_','0':{'subject':'missile','act':'support','goal':'all'},
                           'condition':{'with':['airdefense']}},
                'cannonry':{'LTL': '<> _0_','0':{'subject':'cannonry','act':'support','goal':'airdefense'},
                            'condition':{'with':['airdefense']}} ,
                'airdefense':{'LTL': '<> _0_', '0':{'subject':'airdefense','act':'support','goal':'all'}},
                'guidance':{'LTL' : '[]( _0_ -> _1_ )','0' :{'subject':'cannonry','act':'support','goal':'all'} },
                'behead':{'LTL':'<> _0_','0':{'subject':'all','act':'attack','goal':'commander'},'condition':{'with':['commander']}}
                }
#nolimit_weapen无武器限制，limit_weapen限制武器，no_weapen不使用武器,Radical激进 强力型,conservation保守 空中型
#synthesize 综合 奇迹型

Control_level_rule={'limit_weapen','no_weapen','nolimit_weapen','Radical','conservation','synthesize'}

basic_detail={'obs_s':{'default':''}}

# low level task specification
action_atom={'0':'attack','1':'observe','2':'follow','3':'support','4':'trick'}
action_2_commander={'attack':'fireactions','observe':'scoutactions','follow':'moveactions',
                    'support':'moveactions','cannory':'fireactions','airdefense':'moveactions'}
dic_zanshu={'basic_obs':'联合侦察',
            'basic_atk':'联合进攻',
            'order_obs':'梯度侦察',
                    'order_atk':'梯度进攻',
                    'order_support':'梯度支持',
                    'basic_support':'联合支持',
                    'basic_trick':'诱骗'}
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
'大规模清理':'daguimo'
}
red_dic_to_name={'红方':'redall'}
blue_dic_to_name={'蓝方':'all','无人机':'uav','炮兵':'artillery','步兵':'infantry','指挥所':'all','雷达':'all'}
name_dic_to_blue={'all':'蓝方','uav':'无人机','artillery':'炮兵','infantry':'步兵'}