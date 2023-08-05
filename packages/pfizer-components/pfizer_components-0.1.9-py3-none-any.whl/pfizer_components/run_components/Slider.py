from dash import Dash, dcc, html

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = Dash(__name__, external_stylesheets=external_stylesheets)
app = Dash(__name__)

app.layout = html.Div([
    dcc.Slider(min=0, max=20, step=5, value=10, id='my-slider'),
    dcc.Slider(0, 20, marks=None, value=10, ),
    dcc.Slider(0, 100, value=65,
        marks={
            0: {'label': '0°C', 'style': {'color': '#77b0b1'}},
            26: {'label': '26°C'},
            37: {'label': '37°C'},
            100: {'label': '100°C', 'style': {'color': '#f50'}}
        }
    ),
    dcc.Slider(0, 10, 1, value=5, marks=None,
        tooltip={"placement": "bottom", "always_visible": True}),
    dcc.RangeSlider(0, 20, value=[5, 15]),
        html.Div(id='slider-output-container'),
        ])

if __name__ == '__main__':
    app.run_server(port=8543, debug=True)
