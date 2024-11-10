import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split

def load_model(file_path):
    with open(file_path, 'rb') as file:
        model = pickle.load(file)
    return model

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout
app.layout = html.Div(
    [
        # Text input
        dcc.Input(id="input-text", type="text", placeholder="Enter text here", style={"margin-bottom": "10px"}),

        # Submit button
        html.Button("Submit", id="submit-button", n_clicks=0, style={"margin-bottom": "10px"}),

        # HTML Div to display the output text
        html.Div(id="output-div", style={"border": "1px solid #ddd", "padding": "10px"})
    ],
    style={"display": "flex", "flex-direction": "column", "width": "300px", "margin": "auto"}
)

# Define the callback to update the output div
@app.callback(
    Output("output-div", "children"),
    [Input("submit-button", "n_clicks")],
    [dash.dependencies.State("input-text", "value")]
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        result = model.predict([value])
        if result[0] == 1:
            return "This is a real news article."
        else:
            return f"{result[0]} This is a fake news article."
    return "Enter some text and click submit."

# Run the app
if __name__ == "__main__":
    model = load_model('model.pkl')
    app.run_server(debug=True)





