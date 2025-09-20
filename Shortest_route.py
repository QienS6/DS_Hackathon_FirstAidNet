#!/usr/bin/env python
# coding: utf-8

# In[1]:m


# Trial with unreal data
import networkx as nx

def get_user_input():
    start_x = int(input("Enter start x (0–9): "))
    start_y = int(input("Enter start y (0–9): "))
    end_x = int(input("Enter end x (0–9): "))
    end_y = int(input("Enter end y (0–9): "))
    return (start_x, start_y), (end_x, end_y)

def shortest_route(start, end, size=10):
    # Build a grid graph (size x size)
    G = nx.grid_2d_graph(size, size)

    # Find shortest path using Dijkstra
    route = nx.shortest_path(G, source=start, target=end, weight=None)
    length = len(route) - 1
    return route, length

if __name__ == "__main__":
    start, end = get_user_input()
    route, length = shortest_route(start, end)

    print("\nShortest path (grid cells):", route)
    print(f"Route length: {length} steps")


# In[3]:


get_ipython().system('pip install osmnx')


# In[2]:


pip install --upgrade osmnx


# In[3]:


import random

def generate_random_coords(lat_min, lat_max, lon_min, lon_max):
    """
    Generate random latitude and longitude within the bounding box.
    """
    lat = random.uniform(lat_min, lat_max)
    lon = random.uniform(lon_min, lon_max)
    return lat, lon

if __name__ == "__main__":
    # Example bounding box for Dallas, Texas
    dallas_lat_min = 32.70
    dallas_lat_max = 32.85
    dallas_lon_min = -96.90
    dallas_lon_max = -96.70

    # Generate random start and end points
    start_lat, start_lon = generate_random_coords(dallas_lat_min, dallas_lat_max,
                                                  dallas_lon_min, dallas_lon_max)
    end_lat, end_lon = generate_random_coords(dallas_lat_min, dallas_lat_max,
                                              dallas_lon_min, dallas_lon_max)


# In[5]:


import osmnx as ox
import networkx as nx
import random

def generate_random_coords(lat_min, lat_max, lon_min, lon_max):
    """
    Generate random latitude and longitude within the bounding box.
    """
    lat = random.uniform(lat_min, lat_max)
    lon = random.uniform(lon_min, lon_max)
    return lat, lon

def shortest_route_with_stops(start_lat, start_lon, end_lat, end_lon,
                              speed_kph=40, avg_stop_sec=30):
    """
    Find shortest driving route between two lat/lon points.
    Includes estimated stop sign/traffic light delays.
    """
    # 1. Create bounding box around both points
    north = max(start_lat, end_lat) + 0.01
    south = min(start_lat, end_lat) - 0.01
    east = max(start_lon, end_lon) + 0.01
    west = min(start_lon, end_lon) - 0.01

    # 2. Build graph
    G = ox.graph_from_bbox(north, south, east, west, network_type="drive")

    # 3. Find nearest nodes
    orig_node = ox.distance.nearest_nodes(G, start_lon, start_lat)
    dest_node = ox.distance.nearest_nodes(G, end_lon, end_lat)

    # 4. Compute shortest path
    try:
        route = nx.shortest_path(G, orig_node, dest_node, weight="length")
        route_length_m = nx.shortest_path_length(G, orig_node, dest_node, weight="length")
    except nx.NetworkXNoPath:
        print(" No route found between these points.")
        return None, 0, 0

    # 5. Count approximate stops (intersections with >2 neighbors)
    stop_count = sum(1 for node in route if len(list(G.neighbors(node))) > 2)

    # 6. Convert distance to km and estimate base travel time
    route_length_km = route_length_m / 1000
    travel_time_hr = route_length_km / speed_kph
    travel_time_min = travel_time_hr * 60

    # 7. Add stop time
    total_stop_time_min = (stop_count * avg_stop_sec) / 60
    travel_time_min_with_stops = travel_time_min + total_stop_time_min

    return route, route_length_km, travel_time_min_with_stops, stop_count

if __name__ == "__main__":
    # Dallas bounding box
    lat_min, lat_max = 32.70, 32.85
    lon_min, lon_max = -96.90, -96.70

    # Generate random start/end points
    start_lat, start_lon = generate_random_coords(lat_min, lat_max, lon_min, lon_max)
    end_lat, end_lon = generate_random_coords(lat_min, lat_max, lon_min, lon_max)

    print(f"Random Start:  Latitude {start_lat:.6f}, Longitude {start_lon:.6f}")
    print(f"Random End:    Latitude {end_lat:.6f}, Longitude {end_lon:.6f}")

    route, dist_km, time_min, stop_count = shortest_route_with_stops(
        start_lat, start_lon, end_lat, end_lon
    )

    if route:
        print(f"\n Shortest route has {len(route)} nodes")
        print(f" Distance: {dist_km:.2f} km")
        print(f" Approx. stop signs/intersections: {stop_count}")
        print(f" Estimated travel time: {time_min:.1f} minutes")


# In[ ]:




