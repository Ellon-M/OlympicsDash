from dash import Dash, html, dcc

# dropdown component
def NamedDropdown(name, **kwargs):
    return html.Div(
        style={"margin": "10px 0px"},
        children=[
            html.P(children=f"{name}", style={"margin-left": "3px"}),
            dcc.Dropdown(**kwargs),
        ],
      )


def NamedSlider(name, **kwargs):
    return html.Div(
        style={"padding": "20px 10px 25px 4px"},
        children=[
            html.P(f"{name}"),
            html.Div(style={"margin-left": "6px"}, children=dcc.Slider(**kwargs)),
        ],
      )
