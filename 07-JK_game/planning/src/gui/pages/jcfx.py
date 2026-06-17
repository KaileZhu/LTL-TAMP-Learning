import os
import re
import time
from collections import OrderedDict
import subprocess

import dash
import diskcache
import pandas as pd
import requests
from dash import Dash, DiskcacheManager, ctx, dash_table, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

#__simulate__ = True
__simulate__ = False
host='http://127.0.0.1:9999/decision'


#名词解释
mingcijieshi = {
    "波次":"波次表示战法的不同阶段",
    "战术":"战术为预设好的任务组合，同波次内相同的战术任务会视为同个战术下不同类型任务",
    "目标主体":"执行该任务的智能体类型（我方）",
    "目标地点":"希望执行的地点",
    "目标对象":"该任务针对的对象",
    "目标状态":"描述目标对象可能的状态",
    "子任务":"由任务分解生成的能独立执行，对整体有独特作用的单个任务",
    "贡献度":"子任务对整体效果的贡献",
    "资源消耗":"该任务对资源的消耗指数",
    "战损估计":"执行该子任务预计会带来的损失",
    "战力需求":"对我方智能体数量的需求",
    "优先度":"优先分配优先度较高的任务",
}

#战法解释
zfjs = {
    '步步为营':'依次的蚕食敌方区域，维持占据空间，压缩敌方战场面积。并控制战争烈度。',
    '占场扫描':'攻击并占据地方区域，维持占据空间，压缩敌方战场面积。并重复扫描保证占据地区安全。',
    '全面进攻':'侦查目标区域，摸清敌方的目标分布，并按照设定顺序先后进攻敌方单位。',
    '围点打援':' 攻击目标区域，并利用周围区域牵制来援的敌军。避免援军改变态势。',
    '重点防御':'侦察并感知敌方目标进程，维持己方战场规划布局，重点有针对性地防止敌方突破己方防御阵地。',
    '防守反击':'依次对敌方攻击进行针对防守，在保证我方绝对安全的情况下，实施突破反击，惩戒敌军',
    '大规模清理':"通过对目标区域反复进行各类战法，实现对战场的完全清理"
}

#条例解释
tljs = {
    '协同攻击':'将红方作战单元周围存在友军作为开火前提',
    '有限火力':'约束智能体攻击指令时间间隔，考虑长线作战弹药余量',
    '无限制':'对智能体移动、是否开火以及开火间隔无约束',
    '安全距离':'约束智能体与敌方单位最近距离，避免发生近距离交火',
    '无视威胁':'智能体在执行任务过程中无视敌方兵力部署，优先考虑目标完成度',
    '紧急避险':'当红方作战单元处于血量低于某一阈值或者多面受敌的状态，无视当前任务进行紧急撤退'
}

#战法GIF路径
zfgif = {
    '步步为营':'assets/scene/bbwy.gif',
    '占场扫描':'assets/scene/zcsm.gif',
    '全面进攻':'assets/scene/qmjg.gif',
    '围点打援':'assets/scene/wddy.gif',
    '重点防御':'assets/scene/zdfy.gif',
    '防守反击':'assets/scene/fsfj.gif',
    '大规模清理':''
}

#战法GIF标题
zfgifbt = {
    '步步为营':'战法示意图',
    '占场扫描':'战法示意图',
    '全面进攻':'战法示意图',
    '围点打援':'战法示意图',
    '重点防御':'战法示意图',
    '防守反击':'战法示意图',
    '大规模清理':'想定示意图'
}


dash.register_page(__name__)

df = pd.DataFrame(OrderedDict([
    ('number', []),
    ('method', []),
    ('target_sub', []),
    ('target_loc', []),
    ('target_obj', []),
    ('target_sta', []),
]))

df2 = pd.DataFrame(OrderedDict([
    ('subtask', []),
    ('contribution', []),
    ('consumption', []),
    ('loss', []),
    ('requirement', []),
    ('priority', []),
]))

divboxstyle_checked = {'padding-left':'14px', 'padding-right':'14px', 'padding-top':'14px', 'padding-bottom':'14px', 
    'border':'3px solid #99b3ff'}
divboxstyle_err = {'padding-left':'14px', 'padding-right':'14px', 'padding-top':'14px', 'padding-bottom':'14px', 
    'border':'3px solid #b3b3b3'}
divboxstyle_default = {'padding-left':'14px', 'padding-right':'14px', 'padding-top':'14px', 'padding-bottom':'14px', 
    'border':'3px solid #b3b3b3'}
titlestyle = {'background-color':'#e0e0e0', 'padding': '8px', 'font-size':'20px', 'font-weight':'bold'}
titlestyle_err = {'background-color':'#e0e0e0', 'padding': '8px', 'font-size':'20px', 'font-weight':'bold'}
titlestyle_checked = {'background-color':'#d5e0ff', 'padding': '8px', 'font-size':'20px', 'font-weight':'bold'}
tabheadsty = {'backgroundColor': '#b3b3b3', 'color': '#fff'}
tabheadsty_err = {'backgroundColor': '#b3b3b3', 'color': '#fff'}
tabheadsty_checked = {'backgroundColor': '#99b3ff', 'color': '#fff'}
tabcell = {'overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': 0, 'font_family': 'arial', 'font_size': '16px', 'text_align': 'center', 'border': '1px solid #8B8B8B'}
tabcell_err = {'overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': 0, 'font_family': 'arial', 'font_size': '16px', 'text_align': 'center', 'border': '1px solid #8B8B8B'}
tabcell_checked = {'overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': 0, 'font_family': 'arial', 'font_size': '16px', 'text_align': 'center', 'border': '1px solid #658BFF'}
butsty = {'background-color':'#6E6E6E'}
butsty_err = {'background-color':'#6E6E6E'}
butsty_checked = {'background-color':'#3E6EFF'}


layout = html.Div(children=[
    html.Div(children=[
        html.Div(children=[
        
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("提示")),
                    dbc.ModalBody("算法执行中，请等待该提示框消失，运行集群博弈平台，并打开博弈分析页面查看结果（不超过15s）"),
                    dbc.ModalFooter(
                        dbc.Button(
                            "关闭", id="close", className="ms-auto", n_clicks=0
                        )
                    ),
                ],
                id="modal",
                is_open=False,
            ),

            html.Div([
                html.H3('1.条例选择', id='title_tlxz', style = titlestyle),
                html.Div([
                    dcc.Checklist(options=['协同攻击', '有限火力', '无限制', '安全距离', '无视威胁','紧急避险'], id='checklist_tlxz',labelStyle={'margin-right':'50px'},
                    inputStyle={'margin-right':'6px'}),
                ], style = {'font-size':'18px'}),
                html.P('', id='p_tljs',style={'margin-left':'10px','margin-top':'10px','font-size':'18px'}),
            ], style = divboxstyle_default, id = 'box_tlxz'),

            html.Br(),

            html.Div([
                html.H3('2.战法选择', id='title_zfxz', style = titlestyle),
                dcc.Dropdown(options=['步步为营', '占场扫描', '全面进攻', '围点打援','防守反击','重点防御','大规模清理'] , id='dropdown_zfxz',
                             placeholder="请选择战法", className='mySelect', clearable=False),
                html.Div(children=[
                    html.Button('生成战法内容', id='button_zfqd', n_clicks=0, className='button', style=butsty),
                ], style={'text-align': 'right'}),
            ], style = divboxstyle_default, id = 'box_zfxz'),
            
            html.Br(),

            html.Div([
                html.H3('3.战术编辑', id='title_zsbj', style = titlestyle),
                dash_table.DataTable(
                    id = 'table_methods',
                    data = df.to_dict('records'),
                    columns = [
                        {'id': 'number', 'name': '波次', 'presentation': 'dropdown'},
                        {'id': 'method', 'name': '战术', 'presentation': 'dropdown'},
                        {'id': 'target_sub', 'name': '目标主体', 'presentation': 'dropdown'},
                        {'id': 'target_loc', 'name': '目标地点', 'presentation': 'dropdown'},
                        {'id': 'target_obj', 'name': '目标对象', 'presentation': 'dropdown'},
                        {'id': 'target_sta', 'name': '目标状态', 'presentation': 'dropdown'},
                    ],
                    tooltip_header = {'number':mingcijieshi['波次'], 'method':mingcijieshi['战术'], 'target_sub':mingcijieshi['目标主体'], 
                        'target_loc':mingcijieshi['目标地点'], 'target_obj':mingcijieshi['目标对象'], 'target_sta':mingcijieshi['目标状态'] },
                    css = [{
                        'selector': '.dash-table-tooltip',
                        'rule': 'background-color: white; font-family: monospace; color: gray; font-size: 16px; text-align: center; min-width: 0'
                    }],
                    tooltip_delay = 0,
                    tooltip_duration = None,
                    style_header = tabheadsty,
                    style_cell = tabcell,
                    style_data_conditional = [
                        {
                            'if': {
                                'state': 'active',
                            },
                            'backgroundColor': 'white',
                            'border': '1px solid rgb(0, 116, 217)',
                            'color': 'black'
                        },
                    ],
                    editable = True,
                    row_deletable = True,
                    dropdown = {
                        'number': {
                            'options': [
                                {'label': str(i+1), 'value': str(i+1)}
                                for i in range(15)
                            ]
                        },
                        'method': {
                            'options': [
                                {'label': i, 'value': i}
                                for i in ['联合侦察','联合进攻','联合支持','梯度侦察','梯度进攻','梯度支持','诱骗']
                            ]
                        },
                        'target_sub': {
                            'options': [
                                {'label': i, 'value': i}
                                for i in ['红方','侦查无人机','攻击无人车','导弹']
                            ]
                        },
                        'target_loc': {
                            'options': [
                                {'label': i, 'value': i}
                                for i in ['001','002','003','004','005','006','007','008','009',
                                        '010','011','012','013','014','015','016']
                            ]
                        },
                        'target_obj': {
                            'options': [
                                {'label': i, 'value': i}
                                for i in ['蓝方','无人机','指挥所','雷达','炮兵','步兵']
                            ]
                        },
                        'target_sta': {
                            'options': [
                                {'label': i, 'value': i}
                                for i in ['动态','静态','打击','干扰']
                            ]
                        },
                    }
                ),
                html.Div(children = [
                    html.Button('添加战法内容', id='button_add_row', n_clicks=0, disabled=False, className = 'button', style=butsty),
                    html.Button('生成子任务', id='cal_subtask', n_clicks=0, disabled=False, className = 'button', style=butsty),
                ], style={'text-align': 'right'}),
            ], style = divboxstyle_default, id = 'box_zfnr'),
            
            html.Br(),
            
            html.Div([
                html.H3('4.子任务', id='title_zrwnr', style = titlestyle),
                dcc.Store(id='subtask_old_data'),
                dcc.Store(id='execute_outputs'),
                html.Div(
                    children=[
                        dash_table.DataTable(
                            id='table_subtask',
                            data=df2.to_dict('records'),
                            columns=[
                                {'id': 'subtask', 'name': '子任务'},
                                {'id': 'contribution', 'name': '贡献度'},
                                {'id': 'consumption', 'name': '资源消耗'},
                                {'id': 'loss', 'name': '战损估计'},
                                {'id': 'requirement', 'name': '战力需求'},
                                {'id': 'priority', 'name': '优先度', 'editable': True, 'type': 'numeric'},
                            ],
                            tooltip_header={'subtask':mingcijieshi['子任务'], 'contribution':mingcijieshi['贡献度'], 'consumption':mingcijieshi['资源消耗'],
                                'loss':mingcijieshi['战损估计'], 'requirement':mingcijieshi['战力需求'], 'priority':mingcijieshi['优先度'],},
                            css=[{
                                'selector': '.dash-table-tooltip',
                                'rule': 'background-color: white; font-family: monospace; color: gray; font-size: 16px; text-align: center; min-width: 0'
                            }],
                            tooltip_delay=0,
                            tooltip_duration=None,
                            style_header = tabheadsty,
                            style_cell = tabcell,
                        ),
                    ], style= {'display': 'block'}, id='table_subtask_div'
                ),
                html.Div(
                    children=[
                        dash_table.DataTable(
                            id='table_subtask2',
                            data=df2.to_dict('records'),
                            columns=[
                                {'id': 'subtask', 'name': '子任务'},
                                {'id': 'contribution', 'name': '贡献度'},
                                {'id': 'consumption', 'name': '资源消耗'},
                                {'id': 'loss', 'name': '战损估计'},
                                {'id': 'requirement', 'name': '战力需求'},
                                {'id': 'priority', 'name': '优先度', 'type': 'numeric'},
                            ],
                            tooltip_header={'subtask':mingcijieshi['子任务'], 'contribution':mingcijieshi['贡献度'], 'consumption':mingcijieshi['资源消耗'],
                                'loss':mingcijieshi['战损估计'], 'requirement':mingcijieshi['战力需求'], 'priority':mingcijieshi['优先度'],},
                            css=[{
                                'selector': '.dash-table-tooltip',
                                'rule': 'background-color: white; font-family: monospace; color: gray; font-size: 16px; text-align: center; min-width: 0'
                            }],
                            tooltip_delay=0,
                            tooltip_duration=None,
                            style_header = tabheadsty,
                            style_cell = tabcell,
                            style_data_conditional = [
                                {
                                    'if': {
                                        'column_editable': False  # True | False
                                    },
                                    'backgroundColor': 'rgb(240, 240, 240)',
                                    'cursor': 'not-allowed'
                                },
                            ],
                        ),
                    ], style= {'display': 'none'}, id='table_subtask2_div'
                ),
                
                html.Div(children=[
                    html.Button('更新优先度', id='upd_priority', n_clicks=0, disabled=False, className = 'button', style=butsty),
                    
                ], style={'text-align': 'right'}),
            ], style = divboxstyle_default, id='box_zrw'),
        
            html.Br(),

            html.Div([
                html.Button('计算决策方案', id='confirm', n_clicks=0, disabled=False, className = 'button', style=butsty),
                dcc.Link(html.Button('下一步', id='jcfx_but_next', n_clicks=0, disabled=False, className = 'button', style=butsty), href="/byfx"),
            ], style = {'text-align':'right'}),

            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),

        ], style={'padding': 10, 'flex': 3, 'maxHeight': '800px', 'overflow-y': 'scroll'}),
        
        html.Div(children=[
            html.Div(children=[
                html.H3(id='zfgif_title', children='战法示意图', style = {'background-color':'#d5e0ff', 'padding':'8px', 'margin-left': '16px', 'margin-right': '16px',
                                                                'font-size':'24px', 'font-weight':'bold'}),
            ], style={'textAlign':'left'}),
            html.Div(children=[
                html.Img(id='img1_copy', src='', style={'width':'90%'}),
            ], style={'textAlign':'center', 'min-height':'450px', 'margin-bottom':'12px'}),
            html.Div(children=[
                html.H3(children='战法解释', style = {'background-color':'#d5e0ff', 'padding':'8px', 'margin-left': '16px', 'margin-right': '16px',
                                                                'font-size':'24px', 'font-weight':'bold'}),
            ], style={'textAlign':'left'}),
            html.Div(children=[
                html.P('', id='p_zfjs',style={'padding-left':'20px','padding-right':'20px','padding-top':'10px','font-size':'20px'}),
            ], style={'textAlign':'left'}),
        ], style={'flex': 2, 'textAlign':'center', 'border':'3px solid #99b3ff', 'margin':'6px', 'margin-left':'40px', 'padding':'6px'}),

    ], style={'display': 'flex', 'flex-direction': 'row', 'padding':'12px'}),
])


@dash.callback(
    Output('box_tlxz', 'style'),
    Output('title_tlxz', 'style'),
    Input('checklist_tlxz', 'value'),
)
def box_check_tl(v):
    if v is not None and len(v) is not 0:
        return divboxstyle_checked, titlestyle_checked
    else:
        return divboxstyle_err, titlestyle_err
        
@dash.callback(
    Output('box_zfxz', 'style'),
    Output('title_zfxz', 'style'),
    Output('button_zfqd', 'style'),
    Input('dropdown_zfxz', 'value'),
)
def box_check_zf(v):
    if v is not None and  len(v) is not 0:
        return divboxstyle_checked, titlestyle_checked, butsty_checked
    else:
        return divboxstyle_err, titlestyle_err, butsty_err
        
@dash.callback(
    Output('box_zfnr', 'style'),
    Output('title_zsbj', 'style'),
    Output('table_methods', 'style_header'),
    Output('table_methods', 'style_cell'),
    Output('button_add_row', 'style'),
    Output('cal_subtask', 'style'),
    Input('table_methods', 'data'),
)
def box_check_zfnr(v):
    if v is not None and  len(v) is not 0:
        return divboxstyle_checked, titlestyle_checked, tabheadsty_checked, tabcell_checked, butsty_checked, butsty_checked
    else:
        return divboxstyle_err, titlestyle_err, tabheadsty_err, tabcell_err, butsty_err, butsty_err

@dash.callback(
    Output('box_zrw', 'style'),
    Output('title_zrwnr', 'style'),
    Output('table_subtask', 'style_header'),
    Output('table_subtask2', 'style_header'),
    Output('table_subtask', 'style_cell'),
    Output('table_subtask2', 'style_cell'),
    Output('upd_priority', 'style'),
    Output('confirm', 'style'),
    Input('table_subtask', 'data'),
)
def box_check_zrw(v):
    if v is not None and  len(v) is not 0:
        return divboxstyle_checked, titlestyle_checked, tabheadsty_checked, tabheadsty_checked, tabcell_checked, tabcell_checked, butsty_checked, butsty_checked
    else:
        return divboxstyle_err, titlestyle_err, tabheadsty_err, tabheadsty_err, tabcell_err, tabcell_err, butsty_err, butsty_err


@dash.callback(
    Output('img1_copy', 'src'),
    Input('store_cjlj', 'data'),
    Input('store_cjlj2', 'data'),
)
def scene_draw(v, v2):
    if len(v2) == 0:
        if len(v) == 0:
            raise PreventUpdate
        return v
    else:
        return v2

@dash.callback(
    Output('p_tljs', 'children'),
    Output('checklist_tlxz', 'value'),
    Output('store_tlxz', 'data'),
    Input('checklist_tlxz', 'value'),
    State('store_tlxz', 'data'),
)
def checklist_tlxz_callback(v, d):
    if v is None or len(v)==0:
        if len(d) == 0:
            return '',[],''
        else:
            return tljs[d],[d],d
    else:
        if len(v)>1:
            return tljs[v[1]],[v[1]],v[1]
        else:
            return tljs[v[0]],[v[0]],v[0]

@dash.callback(
    Output('p_zfjs', 'children'),
    Output('store_cjlj2', 'data'),
    Input('dropdown_zfxz', 'value'),
    State('store_zfxz', 'data'),
)
def dropdown_zfxz_callback(v, d):
    if v is None or len(v)==0:
        if len(d) == 0:
            return '', ''
        else:
            return zfjs[d],zfgif[d]
    else:
        return zfjs[v],zfgif[v]

@dash.callback(
    Output('dropdown_zfxz', 'value'),
    Input('ipt_hdl_1', 'data'),
    State('store_zfxz', 'data'),
)
def load_phxz(_, d):
    return d

@dash.callback(
    Output('store_zfxz', 'data'),
    Input('dropdown_zfxz', 'value'),
    prevent_initial_call=True,
)
def set_phxz(d):
    return d


@dash.callback(
    Output('table_subtask', 'style_data_conditional'),
    Input('table_subtask', 'data'),
    Input('subtask_old_data', 'data'),
    prevent_initial_call=True,
)
def table_subtask_modified_callback(data,old_data):
    if len(data) == 0:
        raise PreventUpdate
    else:
        old_priority = [c['priority'] for c in old_data]
        new_priority = [c['priority'] for c in data]
        idx = [c for c in range(len(old_priority)) if not old_priority[c] == new_priority[c]]
        ridx = [c for c in range(len(old_priority)) if old_priority[c] == new_priority[c]]
        return  [
                    {
                        'if': {
                            'column_id': 'priority',
                            'row_index': idx,
                        },
                        'backgroundColor': '#7FDBFF',
                        'color': 'white'
                    },
                    {
                        'if': {
                            'column_id': 'priority',
                            'row_index': idx,
                            'state': 'active',
                        },
                        'border': '1px solid rgb(0, 116, 217)',
                        'backgroundColor': '#7FDBFF',
                        'color': 'white'
                    },
                    {
                        'if': {
                            'column_id': 'priority',
                            'row_index': ridx,
                            'state': 'active',
                        },
                        'backgroundColor': 'white',
                        'border': '1px solid rgb(0, 116, 217)',
                        'color': 'black'
                    },
                    {
                        'if': {
                            'column_editable': False  # True | False
                        },
                        'backgroundColor': 'rgb(240, 240, 240)',
                        'cursor': 'not-allowed'
                    },
                ]


@dash.callback(
    Output('button_zfqd', 'disabled'),
    Output("cal_subtask", "disabled"),
    Output("upd_priority", "disabled"),
    Output('button_add_row', 'disabled'),
    Output('confirm', 'disabled'),
    Output('table_subtask', 'columns'),
    #Output('table_subtask_div', 'style'),
    #Output('table_subtask2_div', 'style'),
    Input('status_content_adjusting', 'data'),
    Input('status_subtask_adjusting', 'data'),
    Input('status_executing', 'data'),
    State('table_subtask', 'columns'),
    prevent_initial_call=True,
)
def status_change(ca, sa, ex, col):
    raise PreventUpdate
    print(ctx.triggered_id, ca, sa, ex)
    bz_disable = False
    cs_disable = False#True
    up_disable = False#True
    ar_disable = False#True
    c_disable = False#True
    #sty = {'display': 'block'}
    #sty2 = {'display': 'none'}
    if ex:
        col=[
                {'id': 'subtask', 'name': '子任务'},
                {'id': 'contribution', 'name': '贡献度'},
                {'id': 'consumption', 'name': '资源消耗'},
                {'id': 'loss', 'name': '战损估计'},
                {'id': 'requirement', 'name': '战力需求'},
                {'id': 'priority', 'name': '优先度', 'type': 'numeric'},
            ]
        #sty = {'display': 'none'}
        #sty2 = {'display': 'block'}
        pass
    elif sa:
        cs_disable = False
        up_disable = False
        ar_disable = False
        c_disable = False
    elif ca:
        cs_disable = False
        ar_disable = False

    #return bz_disable, cs_disable, up_disable, ar_disable, c_disable, sty, sty2
    return bz_disable, cs_disable, up_disable, ar_disable, c_disable, col

@dash.callback(
    Output('table_methods', 'data'),
    #Output('status_content_adjusting', 'data'),
    Input('button_add_row', 'n_clicks'),
    Input('button_zfqd', 'n_clicks'),
    State('table_methods', 'data'),
    State('table_methods', 'columns'),
    State('store_cjxz', 'data'),
    State('store_sfxz', 'data'),
    State('store_phxz','data'),
    State('store_zfxz','data'),
    State('store_tlxz','data'),
    State('store_sflj', 'data'),
    State('store_zfnr', 'data'),
    prevent_initial_call=False,
)
def add_row(n_clicks, n_clicks2, rows, columns, cj, sf, ph, zf, tl, sflj, store_zfnr):
    triggered_id = ctx.triggered_id
    if triggered_id == 'button_add_row' and n_clicks > 0:
        if len(rows) > 0:
            rows.append({c['id']:rows[-1][c['id']] for c in columns})
        else:
            rows.append({c['id']:'' for c in columns})
        return rows
    elif triggered_id == 'button_zfqd' and n_clicks2>0:
        data_to_send = {'场景选择':cj, '算法选择':sf, '算法路径': sflj,'偏好选择':ph, '战法选择':zf,
            '条例选择':tl}
        print('calculate to here')
        rows = calculate_content(data_to_send)
        return rows
    else:
        return store_zfnr


def calculate_content(inputs):
    #点击确定按钮，调用计算背景函数
    if __simulate__:
        print(inputs)
        rows = [{'number':'1','method':'联合侦察','target_sub':'红方','target_loc':'001','target_obj':'蓝方','target_sta':'动态'} for _ in range(5)]
        time.sleep(0.3)
        return rows
    else:
        rows=requests.post(host, json={'calculate_content':inputs})
        rows = rows.json()
        #print(inputs)
        #rows1 = [{'number':'1','method':'基础侦查','target_sub':'红方','target_loc':'001','target_obj':'蓝方','target_sta':'动态'} for _ in range(5)]
        time.sleep(0.3)
        print('fianl_step', rows)
        #print('final_step',rows1)
        return rows


# 战法内容的载入
@dash.callback(
    Output('store_zfnr', 'data'),
    Input('table_methods', 'data'),
    prevent_initial_call=True,
)
def set_zfnr(d):
    return d


# 子任务内容的载入
@dash.callback(
    Output('store_zrwnr', 'data'),
    Input('table_subtask', 'data'),
    prevent_initial_call=True,
)
def set_zrwnr(d):
    return d

# 子任务内容2的载入
@dash.callback(
    Output('store_zrwnr_old', 'data'),
    Input('subtask_old_data', 'data'),
    prevent_initial_call=True,
)
def set_zrwnr_old(d):
    return d

