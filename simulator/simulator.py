import time
import logging
from typing import List, Tuple
from .ors_service import get_route  # Using ORS instead of OSRM
from .traccar_service import send_coordinates_to_traccar
from .route_utils import interpolate_route  # Make sure it handles [lon, lat] order from ORS

class GPSSimulator:

    def __init__(self, server_url: str, device_id: str, waypoints: List[Tuple[float, float]], frequency: int = 2):
        """
        :param server_url: Traccar server URL (example: http://example.com:5055)
        :param device_id: Traccar device ID
        :param waypoints: List of waypoints in (lat, lon) format
        :param frequency: Seconds between sending points
        """
        self.server_url = server_url
        self.device_id = device_id
        self.waypoints = waypoints
        self.frequency = frequency

    def run(self) -> None:
        print("Starting GPSSimulator...")
        print(f"Device ID: {self.device_id}")
        print(f"Waypoints: {self.waypoints}")

        try:
            print("Fetching route from ORS...")
            route = get_route(self.waypoints)  # ORS returns coordinates in [lon, lat] order
            
            coordinates = route['coordinates']
            duration = route['duration']
            distance = route['distance']
            
            print(f"Route fetched successfully. Duration: {duration} seconds, Distance: {distance} meters")

        except Exception as e:
            logging.error(f"Route request error: {e}")
            return

        print("Interpolating route...")
        interpolated_route = interpolate_route(coordinates, distance, duration, self.frequency)

        print("Starting simulation...")
        self.simulate(interpolated_route)
        print("Simulation complete.")

    def simulate(self, interpolated_route: List[dict]) -> None:
        """
        Sends each point in the interpolated route to Traccar.
        Assumes each point dict has 'lat', 'lon', and 'speed'.
        """
        for point in interpolated_route:
            params = {
                'server_url': self.server_url,
                'id': self.device_id,
                'valid': 'true',
                'timestamp': int(time.time()),
                'lat': point['lat'],   # Ensure lat/lon are in correct order
                'lon': point['lon'],
                'location': None,
                'cell': None,
                'wifi': None,
                'speed': point.get('speed', 0),
                'altitude': None,
                'accuracy': None,
                'hdop': None,
                'batt': 100,
                'driverUniqueId': None,
                'charge': 'true',
            }
            print(f"Sending coordinates to Traccar: Lat={point['lat']}, Lon={point['lon']}, Device ID={self.device_id}")
            send_coordinates_to_traccar(params)
            time.sleep(self.frequency)
   


