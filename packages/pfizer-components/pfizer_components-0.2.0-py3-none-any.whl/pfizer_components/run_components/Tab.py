import os
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

current_directory = os.getcwd()
file_name = 'style.css'
file_path = os.path.join(current_directory, '../assets', file_name)

app = Dash(__name__, external_stylesheets=[file_path])

tabs_styles = {
    'height': '52px',
    'width': '2240px'
}

tab_style1 = {
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #DEE0E6',
    # 'backgroundColor': '#E5E5E5',
    'padding': '13px',
    'color': '#000000',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
}
tab_selected_style1 = {
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #003FE2',
    'backgroundColor': '#F2F2F8',
    'color': '#000000',
    'padding': '13px',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
}

tab_disabled_style2 = {
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #ebebed',
    # 'backgroundColor': '#E5E5E5',
    'padding': '13px',
    'color': '#858d97',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
}

tab_style2 = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'font-family': 'Inter',
    'backgroundColor': '#FFFFFF',
}

tab_selected_style2 = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#0000c9',
    'color': 'white',
    'padding': '6px',
    'font-family': 'Inter'
}

tab_style3 = {
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #DEE0E6',
    'color': '#000000',
    'padding': '13px',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
}

tab_selected_style3 = {
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #DEE0E6',
    'color': '#000000',
    'padding': '13px',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
}

tab_style4 = {
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #DEE0E6',
    'color': '#000000',
    'padding': '13px',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
}

tab_selected_style4 = {
    'borderTop': '0px',
    'borderRight': '0px',
    'borderLeft': '0px',
    'borderBottom': '2px solid #DEE0E6',
    'color': '#000000',
    'padding': '13px',
    'font-family': 'Noto Sans',
    'fontWeight': '400px',
    'font-size': '19px',
    'letter-spacing': '-0.5px',
    'align': 'Center',
}

app.layout = html.Div([
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', children=[
        dcc.Tab(label='Tab 1', value='tab-1', style=tab_style1, selected_style=tab_selected_style1, className="page"
                                                                                                              "-link"),
        dcc.Tab(label='Tab 2', value='tab-2', disabled=True, disabled_style=tab_disabled_style2, style=tab_style2,
                selected_style=tab_selected_style2, className="page-link"),
        dcc.Tab(label='⚙️ Settings', value='tab-3', style=tab_style3, selected_style=tab_selected_style3,
                className="page-link"),
        dcc.Tab(label='Tab Label ⓘ', value='tab-4', style=tab_style4, selected_style=tab_selected_style4,
                className="page-link"),
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline')
])


@app.callback(Output('tabs-content-inline', 'children'),
              Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ])


if __name__ == '__main__':
    app.run_server(port=8077, debug=True)
