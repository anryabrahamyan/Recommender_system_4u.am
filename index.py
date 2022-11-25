import dash
from dash import dcc, ctx
from dash import html
from pages import page1, page2
import pandas as pd
from app import app
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from componentss import navbar
nav = navbar.Navbar()

data = pd.read_csv('data/data.csv')
card_content1 = [
    dbc.CardHeader("Average Time Spent in Website"),
    dbc.CardBody(
        [
            html.H5("569415", className="info"),

        ]
    ),
]

card_content2 = [
    dbc.CardHeader("Total Revenue Gain"),
    dbc.CardBody(
        [
            html.H5("25626", className="info"),

        ]
    ),
]

card_content3 = [
    dbc.CardHeader("Revenue per Click"),
    dbc.CardBody(
        [
            html.H5("526848", className="info"),

        ]
    ),
]

card_content4 = [
    dbc.CardHeader("The rate of 'add to cart and buy'"),
    dbc.CardBody(
        [
            html.H5("58145", className="info"),

        ]
    ),
]

card_content5 = [
    dbc.CardHeader("Mean Average Precision"),
    dbc.CardBody(
        [
            html.H5("485616", className="info"),

        ]
    ),
]

card_content6 = [
    dbc.CardHeader("Conversion Rate"),
    dbc.CardBody(
        [
            html.H5("5436", className="info"),

        ]
    ),
]

row_1 = dbc.Row(
    [
        dbc.Col(dbc.Card(card_content1, color="primary", outline=True), width=6, lg=3),
        dbc.Col(dbc.Card(card_content2, color="secondary", outline=True), width=6, lg=3),
        dbc.Col(dbc.Card(card_content3, color="info", outline=True), width=6, lg=3),
    ],
    className="mb-4",
)

row_2 = dbc.Row(
    [
        dbc.Col(dbc.Card(card_content4, color="success", outline=True), width=6, lg=3),
        dbc.Col(dbc.Card(card_content5, color="warning", outline=True), width=6, lg=3),
        dbc.Col(dbc.Card(card_content6, color="danger", outline=True), width=6, lg=3),
    ],
    className="mb-4",
)

app.layout = html.Div(children=
                [html.Div(children=
                    [dbc.Row([dbc.Col(html.Img(src=r'assets/logo.jpg', alt='image', height=70), md=2),

                dbc.Col(
                    [
                        nav,
             ]),

                              ],
                        )],
        ),
                html.Div([row_1, row_2]),
                                  ],
)

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return page1.layout
    if pathname == '/page2':
        return page2.layout
    else:
        return 'hello'


if __name__ == "__main__":
    app.run_server(debug=True)
