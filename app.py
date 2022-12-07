import dash
import dash_bootstrap_components as dbc


external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    '''{
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },'''
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server
