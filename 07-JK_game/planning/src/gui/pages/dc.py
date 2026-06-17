import dash
from dash import html, dcc

dash.register_page(__name__)

divboxstyle_checked = {'padding-left':'14px', 'padding-right':'14px', 'padding-top':'14px', 'padding-bottom':'14px', 
    'border':'3px solid #99b3ff'}
divboxstyle_err = {'padding-left':'14px', 'padding-right':'14px', 'padding-top':'14px', 'padding-bottom':'14px', 
    'border':'3px solid #b3b3b3'}
divboxstyle_default = {'padding-left':'14px', 'padding-right':'14px', 'padding-top':'14px', 'padding-bottom':'14px', 
    'border':'3px solid #b3b3b3'}
titlestyle = {'background-color':'#d5e0ff', 'padding': '8px', 'font-size':'20px', 'font-weight':'bold'}

layout = html.Div(children=[
    html.Div([
        html.Div([
            html.Div([
                html.H3('导出算法', style = titlestyle),
                html.Label('语言选择'),
                dcc.Dropdown(['python', 'c++动态链接库', '所有'], value='所有', placeholder="请选择语言", id='language', className='mySelect'),

                html.Br(),
                html.Label('导出路径'),

                html.Br(),
                dcc.Input('../outputs/', placeholder='请输出保存路径', style={'fontSize':'16px', 'padding': 8}, id='dclj'),

                html.Br(),
                html.Button('导出算法', id='button_dcsf', n_clicks=0, className='button'),
                html.P('', id='dcjg'),
            ], style = divboxstyle_checked, id='box_xdxz'),
        ], style={'padding': 10, 'flex': 3, 'maxHeight': '800px', 'overflow-y': 'scroll'}),

        html.Div(children=[
            html.Div(children=[
                html.Img(id='img1', src='', style={'width':'90%'}),
            ], style={'textAlign':'center'}),
            html.Div(children=[
                html.P('', id='home_xdjs',style={'padding-left':'20px','padding-right':'20px','padding-top':'10px'}),
            ], style={'textAlign':'left'}),
        ], style={'flex': 2, 'textAlign':'center'}),

    ], style={'display': 'flex', 'flex-direction': 'row', 'padding':'12px'}),
])





