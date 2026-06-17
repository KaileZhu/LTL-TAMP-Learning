import datetime
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

#想定解释
xdjs = {
'想定场景1':'我国西部与E国边境线达数千公里，西藏DZ地区属于我国传统领土，战略地位重要，一直为E国觊觎。近年来，其边防军警部队多次对该地区进行骚扰、渗透。'
                '202×年9月23日，我军边防巡逻人员在DZ地区发现不明越线人员，在警告驱离过程中，我边防人员遭遇越线武装分子袭击，发生伤亡。'
                '经查明，E国一支作战分队趁机秘密潜入，占据有利要点，修建坚固工事，前运各型武器，构筑阵地，企图达到侵占我领土的目的。'
 '我方作战分为四个阶段，侦察阶段、防御阶段，诱骗阶段，和火力打击阶段。'
 '火力打击阶段主要区分为两个波次，第一波打击目标预警火控雷达、信息战平台；第二波打击目标敌反斜面野战指挥所、通信节点和有生力量。',

'想定场景2':'R国东南某岛屿B岛自古以来就是R国领土，近年来受A国为代表的西方国家政治蛊惑，B岛妄图从R国版图中分裂出去，并暗中部署作战力量计划对R国东南沿岸指挥中心进行打击。'
                'R国通过卫星捕捉到B岛军事动态，为维护国家主权和领土完整，R国中央军委立即下令在东南沿岸部署无人作战集团，保护己方高价值军事目标，并给予B岛惩罚性打击，'
                '歼灭敌方指挥中心及有生作战力量。'
 'R国行动总体分为两部分。防守阶段：针对来犯蓝方，集中力量摧毁进攻目标，保护红方指挥中心。'
 '察打阶段：派出侦察无人机侦测蓝方作战部署，发动作战单位集中打击蓝方指挥中心，对其他作战单位进行火力压制，将蓝方有生力量全数歼灭。',

'想定场景3':'随着E国国防部高调宣布撤回部分部署在EW边境、此前正在参与大规模军事演习的陆上部队，W国东部危机，似乎呈现出了缓慢降温的趋势。 '
                '一个月后，W国东部地区局势恶化，W政府和当地民间武装相互指责对方在接触线地带发动挑衅性炮击。W东部民间武装宣布，因存在W发起军事行动的危险，'
                '自即日起向E大规模集中疏散当地居民。E总统签署命令，承认W东部的“A共和国”和“B共和国”。EW战争一触即发。'
 'E国前期主要对W国进行侦察和佯攻作战，同时对W国进攻进行防御，待探清敌情后，开始大规模发动进攻，打击W国主要军事设施和有生力量',}


#场景图片路径
cjtppath = {
    '想定场景1':'assets/scene/场景想定1.png',
    '想定场景2':'assets/scene/场景想定2.png',
    '想定场景3':'assets/scene/场景想定3.png'
}


dash.register_page(__name__, path='/')

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
            
            html.Div([
                html.H3('1.场景选择', id='title_xdxz' ,style = titlestyle),
                dcc.Dropdown(list(xdjs.keys()), placeholder='请选择场景...', id='scene', className='mySelect', clearable=False),
            ], style = divboxstyle_default, id='box_xdxz'),
            
            html.Br(),
            
            html.Div([
                html.H3('2.算法设置', id='title_sfxz', style = titlestyle),
                dash_table.DataTable(
                    id='table_algs',
                    data=[],
                    columns=[
                        {'id': 'name', 'name': '算法名称'},
                        {'id': 'path', 'name': '算法信息'},
                        {'id': 'args', 'name': '算法参数'},
                    ],
                    tooltip_header={'args':'计算时长'},
                    css=[{
                        'selector': '.dash-table-tooltip',
                        'rule': 'background-color: white; font-family: monospace; color: gray; font-size: 16px; text-align: center; min-width: 0'
                    }],
                    tooltip_delay=0,
                    tooltip_duration=None,
                    style_data_conditional=[
                        {
                            'if': {
                                'state': 'active',
                            },
                            'backgroundColor': 'white',
                            'border': '1px solid rgb(0, 116, 217)',
                            'color': 'black'
                        },
                    ],
                    style_header = tabheadsty,
                    style_cell = tabcell,
                    row_deletable=True,
                    editable = True,
                ),
                html.Br(),
                dcc.Upload(
                    id='upload_algs',
                    children=html.Div([
                        html.A('添加算法: '),
                        html.U('点击选择文件'),
                        html.A('或将文件拖拽到此处'),
                    ], style={'fontSize':'20px'}),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '0px'
                    },
                    multiple=False
                ),

                html.Br(),
                html.H3('3.算法选择', id='title_sfxz_2', style = titlestyle),
                dcc.Dropdown(id='algs', options = [], placeholder="请选择算法", className='mySelect', clearable=False),
            ], style = divboxstyle_default, id='box_sfxz'),
            
            html.Br(),

            html.Div([
                html.H3('4.偏好选择', id='title_phxz', style = titlestyle),
                dcc.Dropdown(options=['最短时间', '最高效费比', '最高成功率'],  placeholder="请选择偏好", id='pianhao', className='mySelect', clearable=False),
            ], style = divboxstyle_default, id='box_phxz'),

            html.Br(),

            html.Div([
                dcc.Link(html.Button('下一步', id='home_but_next', n_clicks=0, disabled=False, className = 'button', style=butsty), href="/jcfx"),
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
                html.H3(children='想定示意图', style = {'background-color':'#d5e0ff', 'padding':'8px', 'margin-left': '16px', 'margin-right': '16px',
                                                                'font-size':'24px', 'font-weight':'bold'}),
            ], style={'textAlign':'left'}),
            html.Div(children=[
                html.Img(id='img1', src='', style={'width':'90%'}),
            ], style={'textAlign':'center', 'min-height':'450px', 'margin-bottom':'12px'}),
            html.Div(children=[
                html.H3(children='想定解释', style = {'background-color':'#d5e0ff', 'padding':'8px', 'margin-left': '16px', 'margin-right': '16px',
                                                                'font-size':'24px', 'font-weight':'bold'}),
            ], style={'textAlign':'left'}),
            html.Div(children=[
                html.P('', id='home_xdjs',style={'padding-left':'20px','padding-right':'20px','padding-top':'10px','font-size':'20px'}),
            ], style={'textAlign':'left'}),
        ], style={'flex': 2, 'textAlign':'center', 'border':'3px solid #99b3ff', 'margin':'6px', 'margin-left':'40px', 'padding':'6px'}),

    ], style={'display': 'flex', 'flex-direction': 'row', 'padding':'12px'}),
])

@dash.callback(
    Output('box_xdxz', 'style'),
    Output('title_xdxz', 'style'),
    Input('scene', 'value'),
)
def box_check_xd(v):
    if  v is not None and  len(v) is not 0:
        return divboxstyle_checked, titlestyle_checked
    else:
        return divboxstyle_err, titlestyle_err

@dash.callback(
    Output('box_sfxz', 'style'),
    Output('title_sfxz', 'style'),
    Output('table_algs', 'style_header'),
    Output('table_algs', 'style_cell'),
    Output('title_sfxz_2', 'style'),
    Input('algs', 'value'),
)
def box_check_sf(v):
    if v is not None and  len(v) is not 0:
        return divboxstyle_checked, titlestyle_checked, tabheadsty_checked, tabcell_checked, titlestyle_checked
    else:
        return divboxstyle_err, titlestyle_err, tabheadsty_err, tabcell_err, titlestyle_err

@dash.callback(
    Output('box_phxz', 'style'),
    Output('title_phxz', 'style'),
    Output('home_but_next', 'style'),
    Input('pianhao', 'value'),
)
def box_check_ph(v):
    if v is not None and  len(v) is not 0:
        return divboxstyle_checked, titlestyle_checked, butsty_checked
    else:
        return divboxstyle_err, titlestyle_err, butsty_err


@dash.callback(
    Output('scene', 'value'),
    Input('ipt_hdl_1', 'data'),
    State('store_cjxz', 'data'),
)
def load_cjxz(_, d):
    if d is not '':
        return d
    else:
        raise PreventUpdate

@dash.callback(
    Output('img1', 'src'),
    Output('store_cjxz', 'data'),
    Output('store_cjlj', 'data'),
    Input('scene', 'value'),
)
def scene_draw(v):
    if (v is None) or (len(v)==0):
        return '', '', ''
    else:
        return cjtppath[v],v,cjtppath[v]


@dash.callback(
    Output('home_xdjs', 'children'),
    Output('store_cjjs', 'data'),
    Input('scene', 'value'),
    State('store_cjxz', 'data'),
)
def dropdown_zfxz_callback(v, d):
    if v is None or len(v)==0:
        if len(d) == 0:
            return '', ''
        else:
            return xdjs[d], xdjs[d]
    else:
        return xdjs[v], xdjs[v]


@dash.callback(
    Output('table_algs', 'data'),
    Input('upload_algs', 'contents'),
    State('upload_algs', 'filename'),
    State('upload_algs', 'last_modified'),
    State('table_algs', 'data'),
    State('table_algs', 'columns'),
    State('store_sfsz', 'data'),
)
def add_alg(con, fn, lm, rows, columns,store_sfsz):
    if con is None:
        return store_sfsz
    else:
        rows.append({'name':fn, 'path':fn + '  ' + datetime.datetime.fromtimestamp(lm).strftime('%Y-%m-%d %H:%M:%S'), 'args':15})
        return rows

@dash.callback(
    Output('store_sfsz', 'data'),
    Output('algs', 'options'),
    Output('store_sfxx', 'data'),
    Input('table_algs', 'data'),
)
def set_sfsz(d):
    return d, [c['name'] for c in d], [c['name'] for c in d]


# 算法选择的保存与导入
@dash.callback(
    Output('algs', 'value'),
    Input('ipt_hdl_1', 'data'),
    State('store_sfxz', 'data'),
)
def load_sfxz(_, d):
    return d

@dash.callback(
    Output('store_sfxz', 'data'),
    Output('store_sflj', 'data'),
    Output('store_sfcs', 'data'),
    Input('algs', 'value'),
    State('store_sfsz', 'data'),
)
def set_sfxz(d, sfsz):
    __ = [_['path'] for _ in sfsz if _['name']==d]
    __2 = [_['args'] for _ in sfsz if _['name']==d]
    if len(__)>0:
        lj = __[0]
        cs = __2[0]
    else:
        lj = ''
        cs = 0
    return d, lj, cs


# 偏好选择的保存与导入
@dash.callback(
    Output('pianhao', 'value'),
    Input('ipt_hdl_1', 'data'),
    State('store_phxz', 'data'),
)
def load_phxz(_, d):
    return d

@dash.callback(
    Output('store_phxz', 'data'),
    Input('pianhao', 'value'),
)
def set_phxz(d):
    return d
