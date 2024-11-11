import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from geolocate import geolocate_text
import base64
import spacy  # For natural language processing and extracting locations from text

from real_fake_dashboard import extract_most_common_location, load_model
import io



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
        html.Div(id="output-div", style={"border": "1px solid #ddd", "padding": "10px"})
    ],
    style={"width": "50%", "margin": "auto", "padding-top": "50px"}
)

# Define callback to read and display the uploaded CSV file
@app.callback(
    Output("output-div", "children"),
    [Input("upload-data", "contents")],
    [dash.dependencies.State("upload-data", "filename")]
)
def update_output(contents, filename):
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

            geo_located_points = pd.Series(location).apply(lambda p: geolocate_text(p)['point'])
            geo_located_points_lat = geo_located_points.apply(lambda p: p[0])
            geo_located_points_lon = geo_located_points.apply(lambda p: p[1])

            return html.Div([
                html.H5(f"Uploaded file: {filename}"),
                html.H6("Preview of the file content:"),
                html.Pre(location),
                html.Pre(result),
                html.Pre(geo_located_points_lat),
                # html.Pre(df.head().to_string(), style={"white-space": "pre-wrap", "word-break": "break-all"})
            ])
        except Exception as e:
            return f"Error loading file: {str(e)}"
    return "No file uploaded yet."

# Run the app
if __name__ == "__main__":
    nlp = spacy.load("en_core_web_trf")
    model = load_model('model.pkl')
    app.run_server(debug=True)