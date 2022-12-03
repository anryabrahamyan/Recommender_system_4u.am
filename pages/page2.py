# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc


# defining the layout
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Recommendation System for 4u.am"), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(
                html.H6(['The recommendation system for 4u.am helps people who use 4u.am and want to get ', html.Br(),
                         'personalized recommendations and make correct decisions in their online ', html.Br(),
                         'shopping. Our main users are people who already use 4u.am, or are starting to ', html.Br(),
                         'use online shopping tools. For 4u.am the recommendation system will increase ', html.Br(),
                         'sales and redefine the users\' web browsing experience, retain the customers, ', html.Br(),
                         'and enhance their shopping experience.']), className="mb-4")
        ]),
        dbc.Row(dbc.Col([html.H6('For more information and source code:'),
                         html.A(html.H6('here'), href='https://github.com/anryabrahamyan/Recommender_system_4u.am)')]))

    ])])
