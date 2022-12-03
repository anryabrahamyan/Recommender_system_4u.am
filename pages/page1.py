# Import necessary libraries
from data.metrics import *
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

# defining the layout
layout = html.Div([
    dbc.Row([
        dbc.Col([dcc.Graph(figure=fig2)]),  # figure 2 from metrics
        dbc.Col([dcc.Graph(figure=fig3)])  # figure 3 from metrics
    ])]),
