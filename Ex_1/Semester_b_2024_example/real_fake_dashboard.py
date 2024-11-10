import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
import spacy  # For natural language processing and extracting locations from text
from collections import Counter  # For counting occurrences of extracted locations


# Define synonyms for "United States" to unify different variations under a single label
United_states_synonyms = ["U.S", "America", "States", "US", "U.S.", "the United States"]



def load_model(file_path):
    with open(file_path, 'rb') as file:
        model = pickle.load(file)
    return model


def extract_most_common_location(text):
    # Process the text using spaCy's NLP model
    doc = nlp(text)

    # Extract entities labeled as "GPE" (geopolitical entities, e.g., countries, cities)
    locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

    # Replace any synonyms for "United States" with the standard "United States"
    locations = ["United States" if loc in United_states_synonyms else loc for loc in locations]

    # If locations were found, count their occurrences and find the most common one
    if locations:
        location_counts = Counter(locations)  # Count the frequency of each location
        most_common_location = location_counts.most_common(1)[0][0]  # Find the most common location

        # Handle cases where the most common location is invalid (e.g., contains "@")
        if "@" in most_common_location:
            return "No location"

        # If the most common location is "United States", try to return the second most common location
        if most_common_location == "United States":
            if len(location_counts) > 1:  # Check if there's another location available
                most_common_location = location_counts.most_common(2)[1][0]  # Return second most common location
            else:
                # If no other locations are available, keep "United States"
                return most_common_location

        return most_common_location  # Return the most common location

    # If no locations were found in the text, return "No location"
    return "No location"
# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the app layout
app.layout = html.Div(
    [
        # Text input
        dcc.Input(id="input-text", type="text", value="XIAMEN, China (Reuters) - China wants to put its relationship with India on the  right track , President Xi Jinping told Prime Minister Narendra Modi on Tuesday, as the two countries sought to mend ties damaged by a recent tense Himalayan border standoff. The meeting was the first between the two leaders since Chinese and Indian troops ended a standoff in the Doklam border region about a week ago that was the neighbors  most serious military confrontation in decades. Talks between Xi and Modi had been in question before the  de-escalation, which came just in time for China to host the BRICS summit of emerging economies, which also includes Brazil, Russia and South Africa, in the southeastern city of Xiamen. Healthy, stable ties were in the  interests of both countries, Xi told Modi in a meeting on the sidelines of the summit, according to a statement from China s foreign ministry.  China is willing to work with India ... to increase political trust, advance mutually beneficial cooperation and promote the further development of China-India relations along the correct path,  Xi said.  China and India must maintain the fundamental determination that each other constitute mutual development opportunities and do not constitute a mutual threat,  Xi said, adding that peaceful, cooperative relations were the  only correct choice . Xi and Modi spoke for more than an hour and the discussions were  constructive , Indian Foreign Secretary Subrahmanyam Jaishankar told reporters in Xiamen after the meeting.  There was a sense that if the relationship is to go forward, then peace and tranquility on the border area should be maintained,  Jaishankar said, adding that both sides agreed that strong contacts between their defense personnel were needed to prevent another border incident.  On both sides there was a sense that more efforts need to be made to ensure that these kinds of situations don t reoccur.  Pressed on how the Doklam dispute was discussed, Jaishankar said,  Both of us know what happened. This was not a backwards looking conversation. This was a forward-looking conversation.   Hundreds of troops were deployed on the Doklam plateau, near the borders of India, its ally Bhutan, and China after New Delhi objected to China building a road through the mountainous area. The quiet diplomacy that ultimately ended in de-escalation was based on a principle of stopping  differences becoming disputes  that Modi and Xi had agreed at a June meeting in Astana, an Indian official has said. Still, China and India remain divided on many fronts, including India s deep suspicions of China s growing military activities in and around the Indian Ocean. For its part, Modi s government has upset China with its public embrace of Tibetan spiritual leader Dalai Lama, whom the Chinese regard as a dangerous separatist, and growing military ties with the United States and Japan. China has said its forces will continue to patrol in Doklam, which is claimed by Bhutan, and that it hoped India had learned a lesson from the incident", style={"margin-bottom": "10px"}),

        # Submit button
        html.Button("Submit", id="submit-button", n_clicks=0, style={"margin-bottom": "10px"}),

        # HTML Div to display the output text
        html.Div(id="output-div", style={"border": "1px solid #ddd", "padding": "10px"})
    ],
    style={"display": "flex", "flex-direction": "column", "width": "1200px", "margin": "auto"}
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
        location = extract_most_common_location(value)
        
        if result[0] == 1:
            return f"This is a real news article. {location}"
        else:
            return f"{result[0]} This is a fake news article. {location}"
    return "Enter some text and click submit."

# Run the app
if __name__ == "__main__":
    model = load_model('model.pkl')
    nlp = spacy.load("en_core_web_trf")
    app.run_server(debug=True)





