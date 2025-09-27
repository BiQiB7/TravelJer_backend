# You might need to install additional libraries:
# pip install gtfs-realtime-bindings protobuf requests
import requests
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
import json
import csv
import os
import zipfile
from io import BytesIO, StringIO

def get_gtfs_realtime_data(agency: str, category: str = None):
    base_url = "https://api.data.gov.my/gtfs-realtime/vehicle-position/"
    
    if agency == 'prasarana' and not category:
        return {"error": "Category is required for prasarana agency."}

    url = f"{base_url}{agency}"
    if category:
        url += f"?category={category}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)

        vehicle_positions = [MessageToDict(entity.vehicle) for entity in feed.entity]
        
        return {"vehicle_positions": vehicle_positions}

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred during the request: {e}"}
    except Exception as e:
        return {"error": f"An error occurred while parsing the data: {e}"}

# response format of get_gtfs_realtime_data
# {
#   "vehicle_positions": [
#     {
#       "trip": {
#         "tripId": "string",
#         "startTime": "string",
#         "startDate": "string",
#         "routeId": "string"
#       },
#       "position": {
#         "latitude": "float",
#         "longitude": "float",
#         "bearing": "float",
#         "speed": "float"
#       },
#       "timestamp": "string",
#       "vehicle": {
#         "id": "string",
#         "licensePlate": "string"
#       }
#     }
#   ]
# }


def get_gtfs_static_data(agency: str, category: str = None):
    base_url = "https://api.data.gov.my/gtfs-static/"
    
    if agency == 'prasarana' and not category:
        return {"error": "Category is required for prasarana agency."}

    url = f"{base_url}{agency}"
    if category:
        url += f"?category={category}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        gtfs_data = {}
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            for filename in z.namelist():
                if filename.endswith('.txt') and not filename.startswith('__MACOSX/'):
                    # Extract filename without extension to use as key
                    table_name = os.path.splitext(os.path.basename(filename))[0]
                    with z.open(filename) as f:
                        # Decode bytes to string and handle potential BOM
                        content = f.read().decode('utf-8-sig')
                        csv_reader = csv.DictReader(StringIO(content))
                        gtfs_data[table_name] = [row for row in csv_reader]
                        
        return gtfs_data

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred during the request: {e}"}
    except zipfile.BadZipFile:
        return {"error": "Downloaded file is not a valid zip file."}
    except Exception as e:
        return {"error": f"An error occurred while processing the data: {e}"}
# output format
# {
#   "agency": [
#     {
#       "agency_id": "string",
#       "agency_name": "string",
#       "agency_url": "string",
#       "agency_timezone": "string",
#       "agency_lang": "string",
#       "agency_phone": "string"
#     }
#   ],
#   "routes": [
#     {
#       "route_id": "string",
#       "agency_id": "string",
#       "route_short_name": "string",
#       "route_long_name": "string",
#       "route_type": "integer"
#     }
#   ],
#   "trips": [
#     {
#       "route_id": "string",
#       "service_id": "string",
#       "trip_id": "string",
#       "trip_headsign": "string",
#       "shape_id": "string"
#     }
#   ],
#   "stops": [
#     {
#       "stop_id": "string",
#       "stop_code": "string",
#       "stop_name": "string",
#       "stop_lat": "float",
#       "stop_lon": "float"
#     }
#   ],
#   "stop_times": [
#     {
#       "trip_id": "string",
#       "arrival_time": "string",
#       "departure_time": "string",
#       "stop_id": "string",
#       "stop_sequence": "integer"
#     }
#   ],
#   "calendar": [
#     {
#       "service_id": "string",
#       "monday": "integer",
#       "tuesday": "integer",
#       "wednesday": "integer",
#       "thursday": "integer",
#       "friday": "integer",
#       "saturday": "integer",
#       "sunday": "integer",
#       "start_date": "string",
#       "end_date": "string"
#     }
#   ],
#   "frequencies": [
#     {
#         "trip_id": "string",
#         "start_time": "string",
#         "end_time": "string",
#         "headway_secs": "integer"
#     }
#   ],
#   "shapes": [
#     {
#         "shape_id": "string",
#         "shape_pt_lat": "float",
#         "shape_pt_lon": "float",
#         "shape_pt_sequence": "integer"
#     }
#   ]
# }


if __name__ == '__main__':
    # --- Example for GTFS Realtime Data ---
    # print("--- Fetching GTFS Realtime Data ---")
    # # 1. Get realtime data for Prasarana Rapid KL Bus
    # print("\nFetching realtime data for Prasarana Rapid KL Bus...")
    # prasarana_realtime_data = get_gtfs_realtime_data(agency='prasarana', category='rapid-bus-kl')
    # if "error" in prasarana_realtime_data:
    #     print(prasarana_realtime_data["error"])
    # else:
    #     print(f"Total vehicles found: {len(prasarana_realtime_data.get('vehicle_positions', []))}")
    #     if prasarana_realtime_data.get('vehicle_positions'):
    #         print("First vehicle details:")
    #         print(json.dumps(prasarana_realtime_data['vehicle_positions'][0], indent=2))
    
    # print("\n" + "="*50 + "\n")

    # --- Example for GTFS Static Data ---
    # print("--- Fetching GTFS Static Data ---")
    # # 2. Get static data for Prasarana Rapid Rail KL
    # print("\nFetching static data for Prasarana Rapid Rail KL...")
    # prasarana_static_data = get_gtfs_static_data(agency='prasarana', category='rapid-rail-kl')
    # print(prasarana_static_data)
    # if "error" in prasarana_static_data:
    #     print(prasarana_static_data["error"])
    # else:
    #     print("Successfully fetched and processed Prasarana static data.")
    #     print(f"Tables found: {list(prasarana_static_data.keys())}")
    #     if 'routes' in prasarana_static_data:
    #         print(f"Found {len(prasarana_static_data['routes'])} routes.")
    #         print("First route details:")
    #         print(json.dumps(prasarana_static_data['routes'][0], indent=2))

    # print("\n" + "="*50 + "\n")

    # # 3. Get static data for KTMB
    print("\nFetching static data for KTMB...")
    ktmb_static_data = get_gtfs_static_data(agency='ktmb')
    print(ktmb_static_data)
    if "error" in ktmb_static_data:
        print(ktmb_static_data["error"])
    else:
        print("Successfully fetched and processed KTMB static data.")
        print(f"Tables found: {list(ktmb_static_data.keys())}")
        if 'routes' in ktmb_static_data:
            print(f"Found {len(ktmb_static_data['routes'])} routes.")
            print("First route details:")
            print(json.dumps(ktmb_static_data['routes'][0], indent=2))