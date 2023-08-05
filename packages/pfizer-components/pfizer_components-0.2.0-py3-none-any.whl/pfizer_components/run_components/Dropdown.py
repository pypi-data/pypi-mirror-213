from dash import html, dcc
import dash
import os

import dash_bootstrap_components as dbc

current_directory = os.getcwd()
file_name = 'dbc.css'
file_path = os.path.join(current_directory, '../assets', file_name)

app = dash.Dash(external_stylesheets=[file_path])

app.layout = html.Div([
    html.Div([
        # html.H3(className='label', children="Label"),
        dcc.Dropdown(className='custom-dropdown1',
                     disabled=True,
                     options=[{'label': 'JAN', 'value': 'M1'},
                              {'label': 'FEB', 'value': 'M2'},
                              {'label': 'MAR', 'value': 'M3'},
                              {'label': 'APR', 'value': 'M4'},
                              {'label': 'MAY', 'value': 'M5'},
                              {'label': 'JUN', 'value': 'M6'},
                              {'label': 'JUL', 'value': 'M7'},
                              {'label': 'AUG', 'value': 'M8'},
                              {'label': 'SEP', 'value': 'M9'}],
                     placeholder='Choose an Option',
                     clearable=False,
                     style={'font-family': 'Noto Sans'}),
        dcc.Dropdown(className='custom-dropdown',
                     options=[{'label': 'JAN', 'value': 'M1'},
                              {'label': 'FEB', 'value': 'M2'},
                              {'label': 'MAR', 'value': 'M3'},
                              {'label': 'APR', 'value': 'M4'},
                              {'label': 'MAY', 'value': 'M5'},
                              {'label': 'JUN', 'value': 'M6'},
                              {'label': 'JUL', 'value': 'M7'},
                              {'label': 'AUG', 'value': 'M8'},
                              {'label': 'SEP', 'value': 'M9'}],
                     placeholder='Choose an Option',
                     clearable=False,
                     style={'font-family': 'Noto Sans'})],
                            # 'height': 32})],
        style={'position': 'relative',
               'width': 525,
               'height': 282,
               'top': 100,
               'left': 400,
               'border': '1px dashed #7B61FF',
               'border-radius': 5,
               'box-sizing': 'border-box'})],
    style={'backgroundColor': '#ffffff', 'margin': 0})

if __name__ == '__main__':
    app.run_server(port=8023, debug=True)




from dash import html, dcc
import dash
import os

import dash_bootstrap_components as dbc

current_directory = os.getcwd()
file_name = 'dbc.css'
file_path = os.path.join(current_directory, '../assets', file_name)

app = dash.Dash(external_stylesheets=[file_path])

app.layout = html.Div([
    html.Div([
        # html.H3(className='label', children="Label"),
        dcc.Dropdown(className='custom-dropdown1',
                     disabled=True,
                     options=[{'label': 'JAN', 'value': 'M1'},
                              {'label': 'FEB', 'value': 'M2'},
                              {'label': 'MAR', 'value': 'M3'},
                              {'label': 'APR', 'value': 'M4'},
                              {'label': 'MAY', 'value': 'M5'},
                              {'label': 'JUN', 'value': 'M6'},
                              {'label': 'JUL', 'value': 'M7'},
                              {'label': 'AUG', 'value': 'M8'},
                              {'label': 'SEP', 'value': 'M9'}],
                     placeholder='Choose an Option',
                     clearable=False
                     # style={'color': 'yellow', 'backgroundColor': '#000000'}
                     )],
        style={'position': 'relative',
               'width': 525,
               'height': 282,
               'top': 100,
               'left': 400,
               'border': '1px dashed #7B61FF',
               'border-radius': 5,
               'box-sizing': 'border-box'})],
    style={'backgroundColor': '#ffffff', 'margin': 0})

if __name__ == '__main__':
    app.run_server(port=8787, debug=True)
2


from dash import html, dcc
import dash
import os

import dash_bootstrap_components as dbc

current_directory = os.getcwd()
file_name = 'dbc.css'
file_path = os.path.join(current_directory, '../assets', file_name)

app = dash.Dash(external_stylesheets=[file_path])

app.layout = html.Div([
    html.Div([
        # html.H3(className='label', children="Label"),
        dcc.Dropdown(className='custom-dropdown1',
                     disabled=False,
                     options=[{'label': 'JAN', 'value': 'M1'},
                              {'label': 'FEB', 'value': 'M2'},
                              {'label': 'MAR', 'value': 'M3'},
                              {'label': 'APR', 'value': 'M4'},
                              {'label': 'MAY', 'value': 'M5'},
                              {'label': 'JUN', 'value': 'M6'},
                              {'label': 'JUL', 'value': 'M7'},
                              {'label': 'AUG', 'value': 'M8'},
                              {'label': 'SEP', 'value': 'M9'}],
                     placeholder='⚙️   Settings',
                     clearable=False,
                     style={'font-family': 'Noto Sans', 'width': 300, 'height': 48}),
        dcc.Dropdown(className='custom-dropdown2',
                     disabled=False,
                     options=[{'label': 'JAN', 'value': 'M1'},
                              {'label': 'FEB', 'value': 'M2'},
                              {'label': 'MAR', 'value': 'M3'},
                              {'label': 'APR', 'value': 'M4'},
                              {'label': 'MAY', 'value': 'M5'},
                              {'label': 'JUN', 'value': 'M6'},
                              {'label': 'JUL', 'value': 'M7'},
                              {'label': 'AUG', 'value': 'M8'},
                              {'label': 'SEP', 'value': 'M9'}],
                     placeholder='➕   Choose an Option',
                     clearable=False,
                     style={'font-family': 'Noto Sans', 'width': 250, 'height': 48}),
        dcc.Dropdown(className='custom-dropdown2',
                     disabled=False,
                     options=[{'label': 'connie.operator@pfizer.com', 'value': 'M1'},
                              {'label': 'Admin Settings', 'value': 'M2'},
                              {'label': '⥖ Log Out', 'value': 'M3'}],
                     placeholder='⚙️  ',
                     clearable=False,
                     style={'font-family': 'Noto Sans', 'width': 90, 'height': 48}),
        dcc.Dropdown(className='right-aligned-dropdown',
                     disabled=False,
                     options=[{'label': 'Notification', 'value': 'M1'},
                              {'label': 'Notification 1', 'value': 'M2'},
                              {'label': 'Notification 2', 'value': 'M3'},
                              {'label': 'All Notification', 'value': 'M4'}],
                     placeholder='🔔️   ',
                     clearable=False,
                     style={'font-family': 'Noto Sans', 'width': 90, 'height': 48, 'display': 'flex', 'align-items': 'right', 'justify-content': 'center'})],
                     # style={'color': 'yellow', 'backgroundColor': '#000000'}
        style={'position': 'relative',
               'width': 525,
               'height': 282,
               'top': 100,
               'left': 400,
               'border': '1px dashed #7B61FF',
               'border-radius': 5,
               'box-sizing': 'border-box'})],
    style={'backgroundColor': '#ffffff', 'margin': 0})

if __name__ == '__main__':
    app.run_server(port=8087, debug=True)

3

