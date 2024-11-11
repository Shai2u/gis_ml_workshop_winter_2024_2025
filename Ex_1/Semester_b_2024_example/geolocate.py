

from geopy.geocoders import Nominatim

# Load spaCy's English model
# Initialize geolocator

def geolocate_text(text):
    # Extract locations
    geolocator = Nominatim(user_agent="geo_locator", timeout=10)

    # Geocode each location
    geolocations = {}
    try:
        place = geolocator.geocode(text)
        if place:
            geolocations['point'] = (place.latitude, place.longitude)
    except Exception as e:
        print(f"Could not geolocate {location}: {e}")

    return geolocations

# Example text

if __name__ == "__main__":
    text = "Amsterdam"
    locations = geolocate_text(text)
