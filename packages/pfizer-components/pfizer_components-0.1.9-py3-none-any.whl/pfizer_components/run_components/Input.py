import dash
from dash import html
from dash import dcc

app = dash.Dash(__name__)

app.layout = html.Div([html.H1(id="input-text2", children='Label',
                               style={'Ag': 'font-size-700/bold', 'height': 18, 'width': 36, 'font-family': 'Noto Sans',
                                      'font-weight': 700, 'font-size': 14, 'line-height': 18, 'letter': '-0.5px'}),
                       dcc.Input(id='my-input',
                                 type='text',
                                 placeholder='Input text',
                                 className='my-input',
                                 style={'font-family': 'Noto Sans', 'font-style': 'normal', 'font-weight': 400,
                                        'font-size': 17, 'line-height': 24, 'letter': '-0.5px'},
                                 min='5',
                                 max='100',
                                 maxLength=10,
                                 ),
                       dcc.Input(id='my-input',
                                 type='text',
                                 placeholder='Input text',
                                 className='my-input',
                                 style={'font-family': 'Noto Sans', 'font-style': 'normal', 'font-weight': 400,
                                        'font-size': 17, 'line-height': 24, 'letter': '-0.5px',
                                        'border': 'Transparent'},
                                 min='5',
                                 max='100',
                                 maxLength=10,
                                 # disabled=True,
                                 )])

if __name__ == '__main__':
    app.run_server(port=8707, debug=True)
