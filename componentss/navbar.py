from dash import html
import dash_bootstrap_components as dbc
from dash import dcc, ctx


# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.Button("Home", outline=True, color="danger"),
                dcc.Link(dbc.Button("Personalized", outline=True, color="primary"), href='/page1'),
                dcc.Link(dbc.Button("Non-personalized", outline=True, color="success"), href='/page2')
            ] ,
            #brand="Multipage Dash App",
            brand_href="/",
            #color="dark",
            dark=True,
        ),
    ])

    return layout