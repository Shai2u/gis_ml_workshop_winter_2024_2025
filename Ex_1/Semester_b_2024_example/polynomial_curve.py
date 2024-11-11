from ipywidgets import interact
import ipywidgets as widgets
from IPython.display import display
import matplotlib.pyplot as plt
import numpy as np
import torch
from functools import partial
from IPython.display import display, Math
import plotly.graph_objects as go


def quad(a, b, c, x): 
    return a*x**2 + b*x + c

#if we fix some particular values of a, b, and c, then we'll have made a quadratic. To fix values passed to a function in python, we use the partial function, like so:

def mk_quad(a,b,c): 
    return partial(quad, a,b,c)



def noise(x, scale): 
    return np.random.normal(scale=scale, size=x.shape)
def add_noise(x, mult, add): 
    return x * (1+noise(x,mult)) + noise(x,add)


if __name__ == "__main__":
    
    np.random.seed(42)
    a, b, c = 3, 2, 1
    f = mk_quad(a, b, c)
    x_noise = torch.linspace(-2, 2, steps=20)[:,None]
    y_noise = add_noise(f(x_noise), 0.15, 1.5)
    import dash
    from dash import dcc, html, Input, Output
    import plotly.graph_objects as go
    import numpy as np

    # Initialize the app
    app = dash.Dash(__name__)

    # Define the app layout
    app.layout = html.Div(
        [
            # Sliders for coefficients a, b, and c
            html.Div([
                html.Label("Coefficient a:"),
                dcc.Slider(id="slider-a", min=0, max=5, step=0.1, value=0,
                           marks={i: str(i) for i in range(-5, 6)})
            ], style={"margin-bottom": "20px"}),

            html.Div([
                html.Label("Coefficient b:"),
                dcc.Slider(id="slider-b", min=0, max=5, step=0.1, value=0,
                           marks={i: str(i) for i in range(-5, 6)})
            ], style={"margin-bottom": "20px"}),

            html.Div([
                html.Label("Coefficient c:"),
                dcc.Slider(id="slider-c", min=0, max=10, step=0.1, value=0,
                           marks={i: str(i) for i in range(-10, 11, 2)})
            ], style={"margin-bottom": "20px"}),

            # Graph to display the polynomial curve
            dcc.Graph(id="polynomial-graph")
        ],
        style={"width": "60%", "margin": "auto", "padding-top": "50px"}
    )

    # Callback to update the polynomial graph based on slider values
    @app.callback(
        Output("polynomial-graph", "figure"),
        [Input("slider-a", "value"),
         Input("slider-b", "value"),
         Input("slider-c", "value")]
    )
    def update_graph(a, b, c):
        # Generate x values and corresponding y values for the polynomial
        x = np.linspace(-10, 10, 400)
        y = a * x**2 + b * x + c

        # Create the figure
        fig = go.Figure(go.Scatter(
            x=x, y=y, mode="lines", name="y = ax^2 + bx + c"
        ))
        fig.add_trace(go.Scatter(x=x_noise.squeeze().numpy(), y=y_noise.squeeze().numpy(), mode='markers', marker=dict(color='blue')))


        # Update layout with title and axis labels
        fig.update_layout(
            title=f"y = {a}x^2 + {b}x + {c}",
            xaxis_title="x",
            yaxis_title="y",
            margin=dict(l=20, r=20, t=40, b=20),
            yaxis=dict(range=[0, 7]),
            xaxis=dict(range=[-3, 3]),
            template="plotly_white"
        )

        return fig

    # Run the app
    if __name__ == "__main__":
        app.run_server(debug=True, port=8051)