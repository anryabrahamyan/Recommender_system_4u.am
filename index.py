# Importing necessary libraries
from dash import dcc, ctx
from dash import html
from pages import page1, page2, page0
from app import app
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from componentss import navbar

# calling the navigation bar with buttons
nav = navbar.Navbar()

# defining the layout
app.layout = html.Div([
    dbc.Row([
        dcc.Location(id='url', refresh=False),
        dbc.Col(html.Img(src=r'assets/logo.jpg', alt='image', height=70)),
        dbc.Col(nav),
    ]),  # the navigation bar
    html.Br(),
    html.Br(),
    html.Div(id='page-content', children=[]), # calling the page content according to page
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return page1.layout
    if pathname == '/page2':
        return page2.layout
    else:
        return page0.layout


if __name__ == "__main__":
    app.run_server(debug=False, port=80,host ='0.0.0.0')
