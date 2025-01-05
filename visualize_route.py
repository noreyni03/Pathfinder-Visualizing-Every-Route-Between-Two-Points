"""
Python Script to Visualize All Possible Routes Between Two Points on an Interactive Map.

This script uses the following libraries:
- Folium: To create interactive maps.
- OSMnx: To extract road network data from OpenStreetMap.
- Geopy: To convert addresses into GPS coordinates (optional).

Instructions:
1. Replace the placeholders for start address, end address, and city name with your desired locations.
2. Run the script to generate an HTML map with all available routes.

Dependencies:
Install the required libraries using:
pip install folium osmnx geopy
"""

import folium
import osmnx as ox
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def get_coordinates(address):
    """
    Convert an address into GPS coordinates (latitude, longitude) using Geopy.

    Args:
        address (str): The address to geocode.

    Returns:
        tuple: GPS coordinates (latitude, longitude).

    Raises:
        ValueError: If the address cannot be geocoded.
    """
    geolocator = Nominatim(user_agent="route_visualizer")
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        else:
            raise ValueError(f"Address '{address}' could not be geocoded. Please check the address or use manual coordinates.")
    except GeocoderTimedOut:
        raise ValueError("Geocoding service timed out. Please check your internet connection.")

def visualize_routes(start_point, end_point, area_name):
    """
    Visualize all available routes between two points on an interactive map.

    Args:
        start_point (tuple): GPS coordinates of the starting point (latitude, longitude).
        end_point (tuple): GPS coordinates of the ending point (latitude, longitude).
        area_name (str): Name of the city or area to analyze.
    """
    # Download the road network for the specified area
    print(f"Downloading road network data for {area_name}...")
    try:
        graph = ox.graph_from_place(area_name, network_type="drive")
    except Exception as e:
        print(f"Error downloading road network: {e}")
        return

    # Convert the graph to a GeoDataFrame
    edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)

    # Create a map centered on the area
    map_center = [(start_point[0] + end_point[0]) / 2, (start_point[1] + end_point[1]) / 2]
    route_map = folium.Map(location=map_center, zoom_start=14)

    # Add start and end points to the map
    folium.Marker(start_point, popup="Start Point", icon=folium.Icon(color="green")).add_to(route_map)
    folium.Marker(end_point, popup="End Point", icon=folium.Icon(color="red")).add_to(route_map)

    # Plot all available roads
    print("Plotting roads...")
    for _, row in edges.iterrows():
        folium.PolyLine(
            locations=[(row['geometry'].coords[0][1], row['geometry'].coords[0][0]),
                       (row['geometry'].coords[-1][1], row['geometry'].coords[-1][0])],
            color="blue",
            weight=1.5,
            opacity=0.7
        ).add_to(route_map)

    # Save the map as an HTML file
    output_file = "all_routes_map.html"
    route_map.save(output_file)
    print(f"Map saved as '{output_file}'.")

if __name__ == "__main__":
    # Replace these placeholders with your desired addresses and area name
    start_address = "Start Address, City, Country"
    end_address = "End Address, City, Country"
    area_name = "City, Country"

    # Convert addresses to GPS coordinates (optional)
    try:
        start_point = get_coordinates(start_address)
        end_point = get_coordinates(end_address)
    except ValueError as e:
        print(e)
        print("Using manual coordinates instead.")
        start_point = (0.0, 0.0)  # Replace with manual coordinates for the start point
        end_point = (0.0, 0.0)    # Replace with manual coordinates for the end point

    # Visualize the routes
    visualize_routes(start_point, end_point, area_name)