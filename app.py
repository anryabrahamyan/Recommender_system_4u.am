import dash
from dash import dcc, ctx
from dash import html
import pandas as pd
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    '''{
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },'''
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)