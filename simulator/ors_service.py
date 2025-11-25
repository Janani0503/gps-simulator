import requests

API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjE5MjM0MjIxOTE2YjRhNmY4ODJlNTIxZWYxNDViYzU3IiwiaCI6Im11cm11cjY0In0="

def get_route(waypoints):
    """
    Fetches route from OpenRouteService between waypoints.
    waypoints: List of (lat, lon)
    Returns dict with coordinates, distance, duration
    """
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"

    # ORS expects [lon, lat] order
    coords = [[wp[1], wp[0]] for wp in waypoints]

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": coords
    }

    resp = requests.post(url, json=body, headers=headers)
    if resp.status_code != 200:
        raise Exception(f"ORS error: {resp.status_code} - {resp.text}")

    data = resp.json()
    features = data['features'][0]
    coordinates = features['geometry']['coordinates']  # [lon, lat]
    distance = features['properties']['segments'][0]['distance']  # meters
    duration = features['properties']['segments'][0]['duration']  # seconds

    return {
        'coordinates': coordinates,
        'distance': distance,
        'duration': duration
    }
