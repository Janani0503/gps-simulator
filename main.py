import threading
import logging
from simulator.config import Config
from simulator.simulator import GPSSimulator

ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjE5MjM0MjIxOTE2YjRhNmY4ODJlNTIxZWYxNDViYzU3IiwiaCI6Im11cm11cjY0In0="  # Get this from your ORS account

def geocode_address_ors(address, api_key):
    import requests
    url = "https://api.openrouteservice.org/geocode/search"
    params = {'api_key': api_key, 'text': address, 'size': 1}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    coords = data['features']['geometry']['coordinates']
    return (coords[1], coords)  # (lat, lon)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# def main():
#     config = Config('config/config.json')
#     server_url = config.server_url
#     devices = config.devices
#     frequency = config.frequency
#     threads = []

#     for device in devices:
#         device_name = device['serial_number']
#         start_address = device['start_address']
#         end_address = device['end_address']

#         # Geocode addresses
#         start_coords = geocode_address_ors(start_address, ORS_API_KEY)
#         end_coords = geocode_address_ors(end_address, ORS_API_KEY)
#         waypoints = [start_coords, end_coords]

#         tracker = GPSSimulator(server_url, device_name, waypoints, frequency, use_osrm=True)
#         thread = threading.Thread(target=tracker.run)
#         thread.start()
#         threads.append(thread)

#     for thread in threads:
#         thread.join()

def main():
    config = Config('config/config.json') # Note: remove 'config/' if file is in root
    server_url = config.server_url
    devices = config.devices
    frequency = config.frequency

    threads = []

    for device in devices:
        device_name = device['serial_number']
        waypoints = device['waypoints']  # Use waypoints directly
        
        # Convert to (lat, lon) tuples if needed
        waypoints = [(wp[0], wp[1]) for wp in waypoints]

        tracker = GPSSimulator(server_url, device_name, waypoints, frequency)
        thread = threading.Thread(target=tracker.run)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
