# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})


colors = {
    'background': '#ffe0b8',
    'text': 'black'
}

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

fig.update_layout(
        plot_bgcolor= 'rgba(0,0,0,0)',
        paper_bgcolor= 'rgba(0,0,0,0)',
        font_color=colors['text']
        )

app.layout = html.Div(children=[
    html.H1(children='Hello Dash', 
            style={
            'textAlign': 'center',
        }),

    html.Div(children='Dash: A web application framework for your data.',
        style={
            'textAlign': 'center',
        }),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
], style={
    'height': '100vh',
    'width': '100vw',
    'margin': '0',
    'top': '0'
    })

if __name__ == '__main__':
    app.run_server(debug=True)


for range in (10):

