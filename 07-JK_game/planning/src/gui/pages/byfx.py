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

dash.register_page(__name__)

img_style = {'width':'80%','height':'80%'}
div_img_style = {'flex':1, 'border':'3px solid #99b3ff', 'height':'400px', 'width':'400px',
                'text-align':'center','margin':'6px','padding':'8px'}
img_titlestyle = {'background-color':'#d5e0ff', 'padding': '8px', 'font-size':'20px', 'font-weight':'bold'}

div_img_style = {'flex':1, 'border':'3px solid #99b3ff', 'height':'220px', 'width':'350px',
                'text-align':'center','margin':'6px','padding':'8px'}
div_img_style = {'flex':1, 'border':'3px solid #99b3ff', 'height':'300px', 'width':'500px',
                'text-align':'center','margin':'6px','padding':'8px'}

layout = html.Div(children=[
    html.Div(children=[
        html.Div(children=[
            dcc.Interval(
                id='img_upd_interval',
                interval=1*1000, # in milliseconds
                n_intervals=0
            ),
            html.Div(children=[
                html.Div([
                    html.H3('轨迹图', style = img_titlestyle),
                    html.Img(id='img7', src='assets/route/0.png', style = img_style),
                ], style = div_img_style),
                html.Div([
                    html.H3('侦察率变化图', style = img_titlestyle),
                    html.Img(id='img2', src='assets/detect_ratio/0.png', style = img_style),
                ], style = div_img_style),
                html.Div([
                    html.H3('蓝方战损比图', style = img_titlestyle),
                    html.Img(id='img3', src='assets/live_damage_destory/blue_0.png', style = img_style),
                ], style = div_img_style),
            ], style={'display': 'flex', 'flex-direction': 'row', 'textAlign':'center'}),
            html.Div(children=[
                html.Div([
                    html.H3('红方战损比图', style = img_titlestyle),
                    html.Img(id='img4', src='assets/live_damage_destory/red_0.png', style = img_style),
                ], style = div_img_style),
                html.Div([
                    html.H3('累计奖励图', style = img_titlestyle),
                    html.Img(id='img5', src='assets/reward/0.png', style = img_style),
                ], style = div_img_style),
                html.Div([
                    html.H3('战力/价值对比图', style = img_titlestyle),
                    html.Img(id='img6', src='assets/strength_value/0.png', style = img_style),
                ], style = div_img_style),
            ], style={'display': 'flex', 'flex-direction': 'row', 'textAlign':'center'}),
            html.Ul(id = 'info_list', children= []
            ),
        ], style={'flex': 2, 'padding':'12px'}),
        
    ], style={'display': 'flex', 'flex-direction': 'row'}),
])



@dash.callback(
    Output('img2', 'src'),
    Input('img_upd_interval', 'n_intervals'),
    State('img2', 'src'),
    prevent_initial_call=True,
)
def img2_upd(n, name):
    res = re.search('\\d+.png',name)
    if res is None:
        raise PreventUpdate
    else:
        count = int(res[0][0:-4])
        next_path = name[0:res.span()[0]]+str(count+1)+'.png'
        next_next_path = name[0:res.span()[0]]+str(count+2)+'.png'
        if os.path.exists(next_next_path):
            return next_path
        else:
            raise PreventUpdate
            
@dash.callback(
    Output('img3', 'src'),
    Input('img_upd_interval', 'n_intervals'),
    State('img3', 'src'),
    prevent_initial_call=True,
)
def img3_upd(n, name):
    res = re.search('\\d+.png',name)
    if res is None:
        raise PreventUpdate
    else:
        count = int(res[0][0:-4])
        next_path = name[0:res.span()[0]]+str(count+1)+'.png'
        next_next_path = name[0:res.span()[0]]+str(count+2)+'.png'
        if os.path.exists(next_next_path):
            return next_path
        else:
            raise PreventUpdate
            
@dash.callback(
    Output('img4', 'src'),
    Input('img_upd_interval', 'n_intervals'),
    State('img4', 'src'),
    prevent_initial_call=True,
)
def img4_upd(n, name):
    res = re.search('\\d+.png',name)
    if res is None:
        raise PreventUpdate
    else:
        count = int(res[0][0:-4])
        next_path = name[0:res.span()[0]]+str(count+1)+'.png'
        next_next_path = name[0:res.span()[0]]+str(count+2)+'.png'
        if os.path.exists(next_next_path):
            return next_path
        else:
            raise PreventUpdate
            
@dash.callback(
    Output('img5', 'src'),
    Input('img_upd_interval', 'n_intervals'),
    State('img5', 'src'),
    prevent_initial_call=True,
)
def img5_upd(n, name):
    res = re.search('\\d+.png',name)
    if res is None:
        raise PreventUpdate
    else:
        count = int(res[0][0:-4])
        next_path = name[0:res.span()[0]]+str(count+1)+'.png'
        next_next_path = name[0:res.span()[0]]+str(count+2)+'.png'
        if os.path.exists(next_next_path):
            return next_path
        else:
            raise PreventUpdate

@dash.callback(
    Output('img6', 'src'),
    Input('img_upd_interval', 'n_intervals'),
    State('img6', 'src'),
    prevent_initial_call=True,
)
def img6_upd(n, name):
    res = re.search('\\d+.png',name)
    if res is None:
        raise PreventUpdate
    else:
        count = int(res[0][0:-4])
        next_path = name[0:res.span()[0]]+str(count+1)+'.png'
        next_next_path = name[0:res.span()[0]]+str(count+2)+'.png'
        if os.path.exists(next_next_path):
            return next_path
        else:
            raise PreventUpdate

@dash.callback(
    Output('img7', 'src'),
    Input('img_upd_interval', 'n_intervals'),
    State('img7', 'src'),
    prevent_initial_call=True,
)
def img7_upd(n, name):
    res = re.search('\\d+.png',name)
    if res is None:
        raise PreventUpdate
    else:
        count = int(res[0][0:-4])
        next_path = name[0:res.span()[0]]+str(count+1)+'.png'
        next_next_path = name[0:res.span()[0]]+str(count+2)+'.png'
        if os.path.exists(next_next_path):
            return next_path
        else:
            raise PreventUpdate



