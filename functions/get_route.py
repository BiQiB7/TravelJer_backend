import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()


def get_route(origin_place_id, destination_place_id, waypoint_place_ids=None, travel_mode=None):
    """
    Calculates the route between an origin and a destination, with optional waypoints.

    Args:
        origin_place_id (str): The Place ID of the origin.
        destination_place_id (str): The Place ID of the destination.
        waypoint_place_ids (list, optional): A list of Place IDs for intermediate waypoints. Defaults to None.
        travel_mode (str, optional): The mode of travel. Can be "DRIVE", "BICYCLE", "TRANSIT", or "WALK". Defaults to None.

    Returns:
        dict: A dictionary containing the route object.
    """
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"
    }

    data = {
        "origin": {
            "placeId": origin_place_id
        },
        "destination": {
            "placeId": destination_place_id
        }
    }

    if waypoint_place_ids:
        data["intermediates"] = [{"placeId": pid} for pid in waypoint_place_ids]
    
    if travel_mode:
        # Map common variations to the correct API value
        mode_map = {
            "WALKING": "WALK"
        }
        api_travel_mode = mode_map.get(travel_mode.upper(), travel_mode.upper())
        data["travelMode"] = api_travel_mode

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error from Google Directions API: {response.text}")
        response.raise_for_status()

if __name__ == '__main__':
    # Example usage:
    # Make sure to set the GOOGLE_MAPS_API_KEY environment variable before running
    # export GOOGLE_MAPS_API_KEY="YOUR_API_KEY"
    try:
        # Example Place IDs (replace with actual Place IDs from search_places or find_nearby_places)
        origin_id = "ChIJebTp9RxPzDERzQPNcVUbckY"  # kidszania
        destination_id = "ChIJZTE6wl5JzDER4AC0z-Aiw00"  # jump street
        
        route = get_route(origin_id, destination_id, travel_mode="DRIVE")
        print(json.dumps(route, indent=2))
    except ValueError as e:
        print(e)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
# the output example
# {
#   "routes": [
#     {
#       "distanceMeters": 9844,
#       "duration": "1014s",
#       "polyline": {
#         "encodedPolyline": "{wgRslekRBGh@s@R]FSASJMNEPFFNANPVpAfA~@lAz@pAp@pAz@|BXDJA\\SCwAFkAJmACcII]MQMIa@GqFGwDKOGiAEUGkBGaDUwBSWFiA?m@CMBaGw@q@EcA@o@Hq@LkBj@GL_B~@kA|@aAd@s@ZeAn@SBMAWe@Yo@f@]^QxCcBvB_A|By@RFdA[dAObAGx@?zAJtDh@zFl@P@h@FfBL~Pb@nEDhDHzB@`AE~A[d@Oh@YbAo@bHkDfCkAnGeDjC}AnCwAnA{@hCmAlFqCv@g@`Aw@v@w@`@i@RM|HaJt@m@n@[~@UnDUlFm@`BUtHy@dMoAnAGxJgA`AKtCXv@Nj@PnAl@dFzAnD|@rMlE~EbCtCjBn@f@dIjGTCLBVGLOvC_EpCoDjBcCpBkCb@_@RMrDoAbCw@_BmFeAaDMm@mAkEEq@BaDBoBCU~@Lt@F`@EzAg@dAs@zAkAjHkHxBuB_A{@o@{@oAyB_AwBuDdBa@_A?ELG"
#       }
#     }
#   ]
# }