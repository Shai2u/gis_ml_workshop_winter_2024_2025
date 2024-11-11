from ipywidgets import interact
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
import torch
from functools import partial
from IPython.display import display, Math
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
import numpy as np


def quad(a, b, c, x):
    return a*x**2 + b*x + c

# if we fix some particular values of a, b, and c, then we'll have made a quadratic. To fix values passed to a function in python, we use the partial function, like so:


def mk_quad(a, b, c):
    return partial(quad, a, b, c)

# Mean absolute errror


def mae(preds, acts):
    return (torch.abs(preds-acts)).mean()


def quad_mae(params, x, y):
    f = mk_quad(*params)
    return mae(f(x), y)


def noise(x, scale):
    return np.random.normal(scale=scale, size=x.shape)


def add_noise(x, mult, add):
    return x * (1+noise(x, mult)) + noise(x, add)


np.random.seed(42)
x_noise = torch.linspace(-2, 2, steps=20)[:, None]
a, b, c = 3, 2, 1
f = mk_quad(a, b, c)
y_noise = add_noise(f(x_noise), 0.15, 1.5)
loss_list = []

# Initialize the app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(
    [
        # Sliders for coefficients a, b, and c
        html.Div([
            html.Label("Coefficient a:"),
            dcc.Slider(id="slider-a", min=0, max=5, step=0.1, value=0.1,
                       marks={i: str(i) for i in range(-5, 6)})
        ], style={"margin-bottom": "20px"}),

        html.Div([
            html.Label("Coefficient b:"),
            dcc.Slider(id="slider-b", min=0, max=5, step=0.1, value=0.1,
                       marks={i: str(i) for i in range(-5, 6)})
        ], style={"margin-bottom": "20px"}),

        html.Div([
            html.Label("Coefficient c:"),
            dcc.Slider(id="slider-c", min=0, max=5, step=0.1, value=0.1,
                       marks={i: str(i) for i in range(-5, 6)})
        ], style={"margin-bottom": "20px"}),
        # Button to trigger the update
        html.Button("Update Graph", id="update-button", n_clicks=0),
        # Graph to display the polynomial curve
        html.Div([
            dcc.Graph(id="polynomial-graph",
                      style={"width": "48%", "display": "inline-block"}),
            dcc.Graph(id="loss-graph",
                      style={"width": "48%", "display": "inline-block"})
        ], style={"display": "flex", "justify-content": "space-between"})
    ],
    style={"width": "60%", "margin": "auto", "padding-top": "50px"}
)

# Callback to update the polynomial graph based on slider values


@app.callback(
    [Output("polynomial-graph", "figure"), Output("loss-graph", "figure")],
    [Input("update-button", "n_clicks")],
    [State("slider-a", "value"),
        State("slider-b", "value"),
        State("slider-c", "value")]
)
def update_graph(n_clicks, a, b, c):
    # Generate x values and corresponding y values for the polynomial
    abc_dash = torch.tensor([a, b, c])
    abc_dash.requires_grad_()
    x = np.linspace(-10, 10, 400)
    y = a * x**2 + b * x + c
    loss = quad_mae(abc_dash, x_noise, y_noise)
    loss.backward()
    der = 0
    with torch.no_grad():
        der = abc_dash.grad

        der = -der * 0.1

    loss_list.append(loss.item())

    # Create the figure
    fig_poly = go.Figure(go.Scatter(
        x=x, y=y, mode="lines", name="y = ax^2 + bx + c"
    ))
    fig_poly.add_trace(go.Scatter(x=x_noise.squeeze().numpy(), y=y_noise.squeeze(
    ).numpy(), mode='markers', marker=dict(color='blue')))

    # Update layout with title and axis labels
    fig_poly.update_layout(
        title=f"y = {a}x^2 + {b}x + {c}",
        xaxis_title="x",
        yaxis_title="y",
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis=dict(range=[0, 7]),
        xaxis=dict(range=[-3, 3]),
        template="plotly_white"
    )
    loss_list_u = loss_list
    steps = list(range(len(loss_list_u)))
    derivative_fig = go.Figure(go.Scatter(
        x=steps, y=loss_list_u, mode="lines", name="dy/dx = 2ax + b"
    ))
    # Update layout with title and axis labels
    derivative_fig.update_layout(
        title=f"loss = {round(loss.item(),2)} da~={round(der[0].item(),4)} db~={round(der[1].item(),4)} dc~={round(der[2].item(),4)}",
        xaxis_title="steps",
        yaxis_title="loss",
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis=dict(range=[0, 20]),
        xaxis=dict(range=[0, 50]),
        template="plotly_white"
    )

    return [fig_poly, derivative_fig]


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8052)
