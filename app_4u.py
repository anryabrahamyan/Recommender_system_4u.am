import dash
from dash import dcc
from dash import html
import pandas as pd
import dash_daq as daq
import numpy as np
from dash.dependencies import Output, Input

data = pd.read_csv('data/data.csv')

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "4u.am: Recommendation System Analytics"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🌹", className="header-emoji"),
                html.H1(
                    children="4u.am: Recommendation System", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of 4u.am "
                    "online gift shop recommendation systems"
                    " in scope of AUA Fall 2022, Marketing Analytics class",
                    className="header-description",
                ),
            ],
            className="header",
        ),

        html.Div(
            children=[
              html.Div(
                children=[
                    html.Div(children='Store', className='menu-title'),
                    dcc.Dropdown(
                        id='store-filter',
                        options=[
                            {"label": store, "value": store}
                            for store in data.store.unique()
                        ],
                        value="DF project",
                        clearable=False,
                        className="dropdown",
                    ),
                ]
              ),
              html.Div(
                  children=[
                      html.Div(
                          children="price range", className='menu-title'
                      ),
                    daq.Slider(
                        min=data.price.min(),
                        max=data.price.max(),
                        value=500,
                        handleLabel={"showCurrentValue": True,"label": " "},
                        step=10,
                        id='price',
                    ),
                    html.Div(id='slider-output-1'),
                  ]
              ),

            ],
            className='menu',
        ),
    ]
)


@app.callback(
    Output('slider-output-1', 'children'),
    Input('price', 'value')
)
def update_output(value):
    return f'Price is {value} drams.'


if __name__ == "__main__":
    app.run_server(debug=True)
