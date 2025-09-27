import os
import requests

from dotenv import load_dotenv

load_dotenv()


def get_place_details(place_id, api_key):
    """Helper function to get place details, specifically the location."""
    url = f"https://places.googleapis.com/v1/places/{place_id}"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "location"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def visualize_route_on_map(encoded_polyline, origin_place_id, destination_place_id, waypoint_place_ids=None):
    """
    Generates a map visualization and a navigation link for a route.

    Args:
        encoded_polyline (str): The encoded polyline string representing the route.
        origin_place_id (str): The Place ID of the origin to mark on the map.
        destination_place_id (str): The Place ID of the destination to mark on the map.
        waypoint_place_ids (list, optional): A list of Place IDs for intermediate waypoints to mark on the map. Defaults to None.

    Returns:
        dict: A dictionary containing the URL to a map image and a navigation link.
    """
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_MAPS_API_KEY environment variable not set.")

    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    
    params = {
        "size": "600x400",
        "path": f"enc:{encoded_polyline}",
        "key": api_key
    }

    markers = []
    try:
        # Get origin coordinates
        origin_details = get_place_details(origin_place_id, api_key)
        origin_loc = origin_details['location']
        markers.append(f"color:blue|label:O|{origin_loc['latitude']},{origin_loc['longitude']}")

        # Get destination coordinates
        dest_details = get_place_details(destination_place_id, api_key)
        dest_loc = dest_details['location']
        markers.append(f"color:green|label:D|{dest_loc['latitude']},{dest_loc['longitude']}")

        # Get waypoint coordinates
        waypoints_coords = []
        if waypoint_place_ids:
            for i, place_id in enumerate(waypoint_place_ids):
                waypoint_details = get_place_details(place_id, api_key)
                waypoint_loc = waypoint_details['location']
                coord_str = f"{waypoint_loc['latitude']},{waypoint_loc['longitude']}"
                waypoints_coords.append(coord_str)
                markers.append(f"color:red|label:{i+1}|{coord_str}")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch place details for markers: {e}")

    # The Static Map API has a URL length limit, so we add markers as separate params
    marker_params = [("markers", m) for m in markers]
    
    # Create the request and get the final URL
    request = requests.Request('GET', base_url, params=params)
    prepared_request = request.prepare()
    
    # Manually append marker parameters to avoid issues with URL encoding of '|'
    for key, value in marker_params:
        prepared_request.url += f"&{key}={value}"

    # --- Generate Navigation URL ---
    # --- Generate Navigation URL ---
    # Using coordinates is more reliable than Place IDs for the navigation URL
    origin_coords = f"{origin_loc['latitude']},{origin_loc['longitude']}"
    dest_coords = f"{dest_loc['latitude']},{dest_loc['longitude']}"

    nav_base_url = "https://www.google.com/maps/dir/"
    nav_params = {
        "api": "1",
        "origin": origin_coords,
        "destination": dest_coords
    }
    if waypoints_coords:
        nav_params["waypoints"] = "|".join(waypoints_coords)
    
    nav_request = requests.Request('GET', nav_base_url, params=nav_params)
    prepared_nav_request = nav_request.prepare()
    navigation_url = prepared_nav_request.url

    return {
        "staticMapUrl": prepared_request.url,
        "navigationUrl": navigation_url
    }

# output response example
# {'navigationUrl': 'https://www.google.com/maps/dir/?api=1&origin=3.1580958%2C101.6138072&destination=3.1171708%2C101.63403699999999'}
if __name__ == '__main__':
    # Example usage:
    # Make sure to set the GOOGLE_MAPS_API_KEY environment variable before running
    # export GOOGLE_MAPS_API_KEY="YOUR_API_KEY"
    try:
        # Encoded polyline for a route 
        polyline = "{wgRslekRBGh@s@R]FSASJMNEPFFNANPVpAfA~@lAz@pAp@pAz@|BXDJA\\SCwAFkAJmACcII]MQMIa@GqFGwDKOGiAEUGkBGaDUwBSWFiA?m@CMBaGw@q@EcA@o@Hq@LkBj@GL_B~@kA|@aAd@s@ZeAn@SBMAWe@Yo@f@]^QxCcBvB_A|By@RFdA[dAObAGx@?zAJtDh@zFl@P@h@FfBL~Pb@nEDhDHzB@`AE~A[d@Oh@YbAo@bHkDfCkAnGeDjC}AnCwAnA{@hCmAlFqCv@g@`Aw@v@w@`@i@RM|HaJt@m@n@[~@UnDUlFm@`BUtHy@dMoAnAGxJgA`AKtCXv@Nj@PnAl@dFzAnD|@rMlE~EbCtCjBn@f@dIjGTCLBVGLOvC_EpCoDjBcCpBkCb@_@RMrDoAbCw@_BmFeAaDMm@mAkEEq@BaDBoBCU~@Lt@F`@EzAg@dAs@zAkAjHkHxBuB_A{@o@{@oAyB_AwBuDdBa@_A?ELG"
        origin_id = "ChIJebTp9RxPzDERzQPNcVUbckY"
        destination_id = "ChIJZTE6wl5JzDER4AC0z-Aiw00"
        
        map_data = visualize_route_on_map(polyline, origin_id, destination_id)
        print(map_data)
        # print("Static Map URL:", map_data["staticMapUrl"])
        # print("Navigation URL:", map_data["navigationUrl"])
    except (ValueError, RuntimeError) as e:
        print(e)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")