from flask import Flask, render_template
import dash_bootstrap_components as dbc
from dash import html, Dash

app = Dash(__name__)

# app.layout = html.Div(
#     [
#         html.P(
#             [
#                 "I wonder what ",
#                 html.Span(
#                     "floccin",
#                     id="tooltip-target",
#                     style={"textDecoration": "underline", "cursor": "pointer"},
#                 ),
#                 " means?",
#             ]
#         ),
#         dbc.Tooltip(
#
#             html.P([
#                 html.P('Title', style={'font-family': 'Noto Sans', 'font-style': 'normal', 'font-weight': 700,
#                                        'font-size': '17px', 'line-height': '24px', 'line-spacing': '-0.5px',
#                                        'color': '#FFFFFF', 'padding': ' 0px 240px -4px 0px'}),
#                 """Noun: rare,
#                     the action or habit of estimating something as worthless.
#                     This is a very long word that has 29 letters.""", ],
#                 style={'font-family': 'Noto Sans', 'font-style': 'normal', 'font-weight': 700, 'font-size': '13px',
#                        'line-height': '24px', 'line-spacing': '24px', 'color': '#FFFFFF',
#                        'padding': ' -4px 20px 3px 20px'}),
#             target="tooltip-target",
#             # style={"maxWidth": "500px", "whiteSpace": "pre-line"},
#             style={'font-family': 'Inter', "maxWidth": "400px", "whiteSpace": "pre-line", "backgroundColor": "#000000",
#                    "borderColor": "#0000c9", 'color': "#ffffff"},
#             placement='bottom',
#             # target="tooltip-target",
#         ),
#     ]
# )

# ---------------------------
app.layout = html.Div(
    [
        html.P(
            [
                "I wonder what ",
                html.Span(
                    "ⓘ",
                    id="tooltip-target",
                    style={"textDecoration": "underline", "cursor": "pointer"},
                ),
                " means?",
            ]
        ),
        dbc.Tooltip(

            html.P([
                """Noun: rare,
                    the action or habit of estimating something as worthless.
                    This is a very long word that has 29 letters.""", ],
                style={'font-family': 'Noto Sans', 'font-style': 'normal', 'font-weight': 700, 'font-size': '13px',
                       'line-height': '24px', 'line-spacing': '24px', 'color': '#FFFFFF',
                       'padding': ' 0px 16px 0px 16px'}),
            target="tooltip-target",
            # style={"maxWidth": "500px", "whiteSpace": "pre-line"},
            style={'font-family': 'Noto Sans', "maxWidth": "400px", "whiteSpace": "pre-line",
                   "backgroundColor": "#000000", "borderColor": "#0000c9", 'color': "#ffffff", "marginTop": "16px"},
            placement='bottom',
            is_open=False
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(port=8666, debug=True)
