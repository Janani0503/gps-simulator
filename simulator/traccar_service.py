import requests
from requests.auth import HTTPBasicAuth
from .exceptions import TraccarError

def send_coordinates_to_traccar(params: dict) -> None:
    server_url = params.pop('server_url')
    
    # Your login credentials
    username = "janani.d@koinnovation.com"
    password = "janani@123"

    try:
        response = requests.get(
            server_url,
            params=params,
            auth=HTTPBasicAuth(username, password)  # Add basic auth
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise TraccarError(params.get('id', 'unknown'), str(e))

