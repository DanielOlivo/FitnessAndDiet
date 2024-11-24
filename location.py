import requests

GOOGLE_API_KEY = "your_google_maps_api_key"

def get_geolocation(address):
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_API_KEY}"
    response = requests.get(geocode_url).json()
    if response['results']:
        location = response['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        raise Exception("Invalid address provided")

def find_nearby_studios(lat, lng):
    places_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=gym&key={GOOGLE_API_KEY}"
    response = requests.get(places_url).json()
    if response.get('results'):
        return [
            {"name": place["name"], "address": place["vicinity"]}
            for place in response["results"]
        ]
    else:
        return []

# Example Usage
address = "1600 Amphitheatre Parkway, Mountain View, CA"
lat, lng = get_geolocation(address)
studios = find_nearby_studios(lat, lng)

print("Nearby Studios:", studios)

