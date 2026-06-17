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
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)
host='http://127.0.0.1:9999/decision'

app = Dash(__name__, use_pages=True)

dfalg = pd.DataFrame(OrderedDict([
    ('name', ['分支合同网','两级合同网']),
    ('path', [r'planning\src\ltl_mas\tools\B_A_B.py',r'planning\src\ltl_mas\tools\Ct_N.py']),
    ('args', ['15','15']),
]))

pagetitles = {'Home':'场景选择', 'Jcfx':'决策分析', 'Byfx':'博弈分析', 'Dc':'其他功能', 'Return':'重置规划'}
pageref = {'Home':'/', 'Jcfx':'/jcfx', 'Byfx':'/byfx', 'Dc':'/dc', 'Return':'/?restart=1'}

link_main_style = {'padding-top': '8px','padding-bottom': '5px','padding-left': '42px','padding-right': '20px', 
                    'background-image':'url(/assets/菜单栏背景.png)', 'background-size':"100% 100%", 'height':'50px', 'width':'160px'}

link_other_style = {'padding-top': '8px','padding-bottom': '5px','padding-left': '20px','padding-right': '20px', 
                    'background-image':'url(/assets/菜单栏背景_其他.png)', 'background-size':"100% 100%", 'height':'50px', 'width':'160px',
                    'float':'right', 'text-align':'center', 'margin-left':'18px'}

butsty = {'background-color':'#6E6E6E'}
butsty_err = {'background-color':'#6E6E6E'}
butsty_checked = {'background-color':'#3E6EFF'}
store_type = 'memory'

app.layout = html.Div([
    html.Div([
        html.H1("集群协同自主决策与对抗研究平台", style={'textAlign':'center','font-size':'40px', 'font-weight':'bold'}),
    ]),
    
    html.Button("exec", id="exec", n_clicks=0, hidden=True),

    html.Div([
        html.Div(
            [
                html.Div(
                    dcc.Link(
                        pagetitles[idx], href=pageref[idx], style={'fontSize': '20px', 'color':'white', 'text-decoration':'none'}
                    )
                , style=link_main_style, id=idx)
                for idx in ['Home','Jcfx','Byfx']
            ]
            #'border-top':'3px dashed #3E6EFF',
        , style={'display': 'flex', 'flex-direction': 'row', 'flex': 1}),

        html.Div([
            html.Div(
                    dcc.Link(
                        pagetitles['Dc'], href=pageref['Dc'], style={'fontSize': '20px', 'color':'white', 'text-decoration':'none'},
                )
            , style=link_other_style, id='Dc'),
            html.Div(
                    dcc.Link(
                        pagetitles['Return'], href=pageref['Return'], style={'fontSize': '20px', 'color':'white', 'text-decoration':'none'}, refresh=True,
                )
            , style=link_other_style, id='Return'),
        ], style={'flex': 1}),
    
    ], style={'padding-left': '20px','padding-right': '20px','padding-top': '6px','padding-bottom': '6px',
            'display': 'flex', 'flex-direction': 'row','background-color':'#d5e0ff'}),

    #html.Img(src='assets/菜单栏分割线.png',style={'width':'1700px','height':'20px','padding-top':'8px'}),

    dcc.Interval(
        id='img_upd_interval',
        interval=1*1000, # in milliseconds
        n_intervals=0
    ),

    dcc.Store(id='status_init', data=True, storage_type=store_type),
    dcc.Store(id='status_content_adjusting', data=False, storage_type=store_type),
    dcc.Store(id='status_subtask_adjusting', data=False, storage_type=store_type),
    dcc.Store(id='status_executing', data=False, storage_type=store_type),
    
    dcc.Store(id='store_cjxz', data='', storage_type=store_type),
    dcc.Store(id='store_cjlj', data='', storage_type=store_type),
    dcc.Store(id='store_cjjs', data='', storage_type=store_type),
    dcc.Store(id='store_cjlj2', data='', storage_type=store_type),
    dcc.Store(id='store_sfsz', data=dfalg.to_dict('records'), storage_type=store_type),
    dcc.Store(id='store_sfxx', data='', storage_type=store_type),
    dcc.Store(id='store_sfxz', data='', storage_type=store_type),
    dcc.Store(id='store_sflj', data='', storage_type=store_type),
    dcc.Store(id='store_sfcs', data='', storage_type=store_type),
    dcc.Store(id='store_phxz', data='', storage_type=store_type),
    dcc.Store(id='store_tlxz', data='', storage_type=store_type),
    dcc.Store(id='store_zfxz', data='', storage_type=store_type),
    dcc.Store(id='store_zfnr', data=[], storage_type=store_type),  # 战法内容
    dcc.Store(id='store_zrwnr', data=[], storage_type=store_type), # 子任务内容
    dcc.Store(id='store_zrwnr_old', data=[], storage_type=store_type), # 子任务内容2

    dcc.Store(id='ipt_hdl_1', data='', storage_type=store_type),
    dcc.Store(id='opt_hdl_1', data='', storage_type=store_type),
    dcc.Store(id='opt_hdl_2', data='', storage_type=store_type),

    dcc.Location(id='url'),

	dash.page_container
], style={'display': 'flex', 'flex-direction': 'column', 'margin-left':'200px', 'margin-right':'200px'})

@app.callback(
    Output('Home', 'style'),
    Output('Jcfx', 'style'),
    Output('Byfx', 'style'),
    Output('Dc', 'style'),
    Input('url', 'pathname'),
)
def callback_func(pathname):
    sty_home = link_main_style.copy()
    sty_jcfx = link_main_style.copy()
    sty_byfx = link_main_style.copy()
    sty_dc   = link_other_style.copy()

    if pathname == '/':
        sty_home['background-image']='url(/assets/菜单栏背景_浅色.png)'
    elif pathname == '/jcfx':
        sty_jcfx['background-image']='url(/assets/菜单栏背景_浅色.png)'
    elif pathname == '/byfx':
        sty_byfx['background-image']='url(/assets/菜单栏背景_浅色.png)'
    elif pathname == '/dc':
        sty_dc['background-image']  ='url(/assets/菜单栏背景_其他_浅色.png)'

    return sty_home, sty_jcfx, sty_byfx, sty_dc

@app.callback(
    Output('dcjg', 'children'),
    Input('button_dcsf', 'n_clicks'),
    background=False,
    prevent_initial_call=True,
)
def export_callback(n):
    if n == 0:
        raise PreventUpdate
    os.system("rm -rf ../outputs/*")
    os.system("mkdir ..\\outputs\\tmp")
    os.system("cp ../../test/determine.pyx ../outputs/tmp/determine.pyx")
    os.system("cd ../outputs/tmp & easycython determine.pyx")
    os.system("cp ../../test/determine.py ../outputs/determine.py")
    os.system("cp ../outputs/tmp/determine.cp37-win_amd64.pyd ../outputs/determine.dll")
    return '导出成功'


@app.callback(
    Output('table_subtask', 'data'),
    Output('subtask_old_data', 'data'),
    Output('status_subtask_adjusting', 'data'),
    Input('cal_subtask', 'n_clicks'),
    Input('upd_priority', 'n_clicks'),
    State('table_subtask', 'data'),
    State('store_cjxz', 'data'),
    State('store_sfxz', 'data'),
    State('store_phxz', 'data'),
    State('store_zfxz', 'data'),
    State('store_tlxz', 'data'),
    State('store_sflj', 'data'),
    State('store_sfcs', 'data'),
    State('table_methods', 'data'),
    State('store_zrwnr', 'data'),
    State('store_zrwnr_old', 'data'),
    background=False,
    prevent_initial_call=False,
)
def subtask_callback(n1, n2, rows, cj, sf, ph, zf, tl, sflj, sfcs, zfnr, store_zrwnr, store_zrwnr_old):
    triggered_id = ctx.triggered_id
    if triggered_id == 'cal_subtask' and n1 > 0:
        data_to_send = {'场景选择':cj, '算法选择':sf, '算法路径': sflj, '算法参数': sfcs, '偏好选择':ph, '战法选择':zf,
            '条例选择':tl,'战法内容':packing_zfnr(zfnr)}
        rows = calculate_subtask(data_to_send)
        return (rows, rows, True)
    elif triggered_id == 'upd_priority' and n2 > 0:
        return (rows, rows, True)
    else:
        return store_zrwnr, store_zrwnr_old, True

@app.callback(
    Output('execute_outputs', 'data'),
    Output('status_executing', 'data'),
    Input('exec', 'n_clicks'),
    State('table_subtask', 'data'),
    State('store_cjxz', 'data'),
    State('store_sfxz', 'data'),
    State('store_phxz','data'),
    State('store_zfxz','data'),
    State('store_tlxz','data'),
    State('store_sflj', 'data'),
    State('store_sfcs', 'data'),
    State('table_methods', 'data'),
    background=True,
    manager=background_callback_manager,
    running=[
        (Output("close", "disabled"), True, False),
        (Output("modal", "is_open"), True, False),
        (Output("jcfx_but_next", "style"), butsty_err, butsty_checked),
    ],
    prevent_initial_call = True
)
def confirm_callback(n1, rows, cj, sf, ph, zf, tl, sflj, sfcs, zfnr):
    if n1 == 0:
        raise PreventUpdate
    data_to_send = {'场景选择':cj, '算法选择':sf, '算法路径': sflj, '算法参数': sfcs, '偏好选择':ph, '战法选择':zf,
        '条例选择':tl,'战法内容':packing_zfnr(zfnr), '子任务':rows}
    execute(data_to_send)
    return 0, True

@app.callback(
    Output('exec', 'n_clicks'),
    Input('confirm', 'n_clicks'),
    State('exec', 'n_clicks'),
)
def connect(n1, n2):
    if n1 == 0:
        raise PreventUpdate
    return n2 + 1


def packing_zfnr(zfnr):
    ret = {}
    for r in zfnr:
        if not r['number'] in ret.keys():
            ret[r['number']] = {}
        if not r['method'] in ret[r['number']].keys():
            ret[r['number']][r['method']] = []
        ret[r['number']][r['method']].append([r['target_sub'],r['target_loc'],r['target_obj'],r['target_sta']])
    return ret

def calculate_subtask(inputs):
    #点击子任务按钮，取计算子任务的各类参数
    #这个地方存为文件，有的就更新一次
    if __simulate__:
        print(inputs)
        rows = [{'subtask':'aa','contribution':'bb','consumption':'cc','loss':'dd','requirement':'ee','priority':'3'} for _ in range(3)]
        return rows
    else:
        print(inputs)
        rows = requests.post(host, json={'calculate_subtask': inputs})
        print('fianl_step',rows.json())
        return rows.json()

def execute(inputs):
    if __simulate__:
        print(inputs)
    else:
        rows = requests.post(host, json={'calculate_execute': inputs})
        print(inputs)
        print(rows)
        return rows

if __name__ == '__main__':
    #if __simulate__ is True:
        #print('开始运行')
        #print('host:',host)
        app.run_server(debug=False)











