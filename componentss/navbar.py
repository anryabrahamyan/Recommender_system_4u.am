from dash import html
import dash_bootstrap_components as dbc


# Defining the navbar structure
def Navbar():
    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink(dbc.Button("Home", outline=True, color="danger"), active=True, href="/")),
                # home button
                dbc.NavItem(dbc.NavLink(dbc.Button("More", outline=True, color="primary"), href="/page1")),  # more page
                dbc.NavItem(dbc.NavLink(dbc.Button("About us", outline=True, color="success"), href="/page2")),
                # about us page

            ],
            brand_href="/",
            dark=True,
        ),
    ])

    return layout
