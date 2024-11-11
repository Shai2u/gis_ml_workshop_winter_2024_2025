import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from geolocate import geolocate_text
import numpy as np
import base64
import spacy  # For natural language processing and extracting locations from text

from real_fake_dashboard import extract_most_common_location, load_model
import io




def generate_map(lat=[45.501], lon=[-73.5673], location=['Montreal'], fake=[True]):
    colors_list = []
    text_list = []
    for i, item in enumerate(fake):
        if item == 1:
            color = 'green'
            fake_text = 'real'
            
        else:
            color = 'red'
            fake_text = 'fake'
        colors_list.append(color)
        text_list.append(f"{location[i]}: {fake_text}")
    print(text_list)
    
    fig = go.Figure(go.Scattermapbox(
        lat=lat,
        lon=lon,
        mode="markers",
        marker=dict(
            size=14,
            color=colors_list
        ),
        text=text_list,
        textposition="top right"
    ))


    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=np.mean(lat), lon=np.mean(lon)),
            zoom=6
        ),
        height=800,
        margin={"l": 0, "r": 0, "t": 0, "b": 0}
    )
    return fig

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout
app.layout = html.Div(
    [
        # File upload input
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select a CSV File")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin-bottom": "10px",
            },
            multiple=False,
        ),
        
        # Output Div to display file information
        html.Div(id="output-div", style={"border": "1px solid #ddd", "padding": "10px"}),
        dcc.Graph(id="scatter-map", config={"displayModeBar": False})

    ],
    style={"width": "50%", "margin": "auto", "padding-top": "50px"}
)

# Define callback to read and display the uploaded CSV file
@app.callback(
    [Output("output-div", "children"), Output("scatter-map", "figure")],
    [Input("upload-data", "contents")],
    [dash.dependencies.State("upload-data", "filename")]
)
def update_output(contents, filename):
    html_div = "No file uploaded yet."
    map_fig = generate_map()
    if contents is not None:
        # Decode the contents of the file
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        
        # Load the content into a Pandas DataFrame
        try:
            # Read the content as CSV
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            # Display the first few rows of the DataFrame
            result = model.predict(df['text'])
            location = df['text'].apply(lambda t: extract_most_common_location(t, nlp))
            print('print loc[0]',location[0])
            print('loc lisgt',location)
            geo_located_points = pd.Series(location).apply(lambda p: geolocate_text(p)['point'])

            geo_located_points_lat = geo_located_points.apply(lambda p: p[0])
            geo_located_points_lon = geo_located_points.apply(lambda p: p[1])

            html_div =  html.Div([
                html.H5(f"Uploaded file: {filename}"),
                html.H6("Preview of the file content:"),
                html.Pre(location),
                html.Pre(result),
                html.Pre(geo_located_points_lat),
                # html.Pre(df.head().to_string(), style={"white-space": "pre-wrap", "word-break": "break-all"})
            ])
            map_fig = generate_map(geo_located_points_lat, geo_located_points_lon, location.values.tolist(), result)
        except Exception as e:
            html_div =  f"Error loading file: {str(e)}"
    return [html_div, map_fig]

# Run the app
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_trf")
    model = load_model('model.pkl')
    app.run_server(debug=True)