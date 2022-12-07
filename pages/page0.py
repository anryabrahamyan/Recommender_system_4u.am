# Import necessary libraries
from data.metrics import *
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

# defining the card contents
card_content1 = [
    dbc.CardHeader("Avg Time Spent in Website"),
    dbc.CardBody(
        [
            html.H5(f'{average_time:,}', className="info"),

        ]
    ),
]

card_content2 = [
    dbc.CardHeader("Total Revenue Gain"),
    dbc.CardBody(
        [
            html.H5(f'{total_revenue:,}', className="info"),

        ]
    ),
]

card_content3 = [
    dbc.CardHeader("Revenue per Click"),
    dbc.CardBody(
        [
            html.H5(f'{revenue_per_click:,}', className="info"),

        ]
    ),
]

card_content4 = [
    dbc.CardHeader("The rate of 'add to cart and buy'"),
    dbc.CardBody(
        [
            html.H5(f'{add_to_cart_rate:,}', className="info"),

        ]
    ),
]

card_content5 = [
    dbc.CardHeader("Revenue per minute"),
    dbc.CardBody(
        [
            html.H5(f'{revenue_per_minute:,}', className="info"),

        ]
    ),
]

card_content6 = [
    dbc.CardHeader("Conversion Rate"),
    dbc.CardBody(
        [
            html.H5(f'{conversion_rate:,}', className="info"),

        ]
    ),
]

# turning the cards into two rows
row_1 = dbc.Row(

    [
        dbc.Col(dbc.Card(card_content1, color="primary", outline=True), width=3),
        dbc.Col(dbc.Card(card_content2, color="secondary", outline=True), width=3),
        dbc.Col(dbc.Card(card_content3, color="info", outline=True), width=3),
    ],
    className="mb-4",
)

row_2 = dbc.Row(
    [
        dbc.Col(dbc.Card(card_content4, color="success", outline=True), width=3),
        dbc.Col(dbc.Card(card_content5, color="warning", outline=True), width=3),
        dbc.Col(dbc.Card(card_content6, color="danger", outline=True), width=3),
    ],
    className="mb-4",
)

# defining the layout
layout = html.Div([
    dbc.Row([
        dbc.Col(html.Div([row_1, row_2])),
        dbc.Col([
            dcc.Graph(figure=fig1
                      )  # figure 1 called from metrics
        ]
        ),
    ]),
    dbc.Row(dcc.Graph(figure=fig4))]),
