import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()

def find_nearby_places(latitude, longitude, radius, included_types=None, excluded_types=None, max_result_count=None, rank_preference=None):
    """
    Searches for places of specific types within a given area using primary type filtering.

    Args:
        latitude (float): The latitude of the center of the search area.
        longitude (float): The longitude of the center of the search area.
        radius (float): The radius of the search area in meters.
        included_types (list, optional): A list of high-level place types to search for. Defaults to None.
        excluded_types (list, optional): A list of high-level place types to exclude. Defaults to None.
        max_result_count (int, optional): The maximum number of results to return. Defaults to None.
        rank_preference (str, optional): The ranking preference for the results. Can be "POPULARITY" or "DISTANCE". Defaults to None.

    Returns:
        dict: A dictionary containing a list of place objects.
    """
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    url = "https://places.googleapis.com/v1/places:searchNearby"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.id,places.primaryType,places.displayName,places.formattedAddress,places.location,places.rating,places.userRatingCount"
    }

    data = {
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": radius
            }
        }
    }

    # Convert high-level enum values to Google API format (e.g., "Food and Drink" -> "food_and_drink")
    def format_type(t):
        return t.lower().replace(' ', '_').replace('_and_', '_')

    # if included_types:
    #     data["includedPrimaryTypes"] = [format_type(t) for t in included_types]
            
    # if excluded_types:
    #     data["excludedPrimaryTypes"] = [format_type(t) for t in excluded_types]
    if max_result_count:
        data["maxResultCount"] = max_result_count
    if rank_preference:
        data["rankPreference"] = rank_preference

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

if __name__ == '__main__':
    # Example usage:
    # Make sure to set the GOOGLE_MAPS_API_KEY environment variable before running
    # export GOOGLE_MAPS_API_KEY="YOUR_API_KEY"
    try:
        # Coordinates for Kuala Lumpur
        # Lat: 3.120260, Lng: 101.622268
        latitude = 3.120260
        longitude = 101.622268
        radius = 5000.0
        places = find_nearby_places(latitude, longitude, radius, included_types=["tourist_attraction"])
        print(json.dumps(places, indent=2))
    except ValueError as e:
        print(e)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# {
#   "places": [
#     {
#       "id": "ChIJq9te9e9JzDERX-ByCY7XagM",
#       "formattedAddress": "6, Jalan SS 21/37, Damansara Utama, 47400 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.1353852,
#         "longitude": 101.6230065
#       },
#       "rating": 4.1,
#       "userRatingCount": 12236,
#       "displayName": {
#         "text": "the Starling",
#         "languageCode": "en"
#       },
#       "primaryType": "shopping_mall"
#     },
#     {
#       "id": "ChIJIfYLMzFJzDERPG9vHZ7DqiE",
#       "formattedAddress": "5, Jalan SS 21/37, Damansara Utama, 47400 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.1376947,
#         "longitude": 101.6233261
#       },
#       "rating": 4.3,
#       "userRatingCount": 12317,
#       "displayName": {
#         "text": "Village Park Restaurant",
#         "languageCode": "en"
#       },
#       "primaryType": "restaurant"
#     },
#     {
#       "id": "ChIJ8bk3pUxJzDERrFejLGpKfIg",
#       "formattedAddress": "Jalan SS 22/23, Damansara Jaya, 47400 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.1270963,
#         "longitude": 101.6165176
#       },
#       "rating": 4,
#       "userRatingCount": 8617,
#       "displayName": {
#         "text": "Atria Shopping Gallery",
#         "languageCode": "en"
#       },
#       "primaryType": "shopping_mall"
#     },
#     {
#       "id": "ChIJe9aC1F1JzDERgZCaZVmX0fc",
#       "formattedAddress": "72A, Jln Profesor Diraja Ungku Aziz, Seksyen 13, 46200 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.1184035,
#         "longitude": 101.63543709999999
#       },
#       "rating": 3.9,
#       "userRatingCount": 6550,
#       "displayName": {
#         "text": "Jaya One",
#         "languageCode": "en"
#       },
#       "primaryType": "shopping_mall"
#     },
#     {
#       "id": "ChIJQd-9d0hJzDER65xpZRO9F6c",
#       "formattedAddress": "3, Jalan SS 20/27, Damansara Intan, 47400 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.1304749,
#         "longitude": 101.6269411
#       },
#       "rating": 3.8,
#       "userRatingCount": 6218,
#       "displayName": {
#         "text": "3 Damansara",
#         "languageCode": "en"
#       },
#       "primaryType": "shopping_mall"
#     },
#     {
#       "id": "ChIJL1DQlOBLzDERdyz6BPjUSxY",
#       "formattedAddress": "Jalan 14/17, Seksyen 14, 46100 Petaling Jaya, Selangor, Malaysia",    
#       "location": {
#         "latitude": 3.1091889999999998,
#         "longitude": 101.63718080000001
#       },
#       "rating": 3.9,
#       "userRatingCount": 6661,
#       "displayName": {
#         "text": "Jaya Shopping Centre",
#         "languageCode": "en"
#       },
#       "primaryType": "shopping_mall"
#     },
#     {
#       "id": "ChIJ2WkFhOBLzDERiFeMgw-BpDA",
#       "formattedAddress": "1, Jalan Kemajuan, Seksyen 13, 46200 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.1098681999999997,
#         "longitude": 101.6382911
#       },
#       "rating": 3.9,
#       "userRatingCount": 1080,
#       "displayName": {
#         "text": "Plaza 33",
#         "languageCode": "en"
#       }
#     },
#     {
#       "id": "ChIJqeDz-DlJzDERQpTaqfRKTfU",
#       "formattedAddress": "119, Jalan SS 20/10, Damansara Utama, 47400 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.137556,
#         "longitude": 101.627535
#       },
#       "rating": 4.4,
#       "userRatingCount": 2139,
#       "displayName": {
#         "text": "Damansara Specialist Hospital",
#         "languageCode": "en"
#       },
#       "primaryType": "hospital"
#     },
#     {
#       "id": "ChIJX98W1VZJzDEROmleEXGs1wM",
#       "formattedAddress": "7680, Jalan SS 2/24, SS 2, 47300 Petaling Jaya, Selangor, Malaysia",  
#       "location": {
#         "latitude": 3.1177284000000003,
#         "longitude": 101.6240483
#       },
#       "rating": 4.2,
#       "userRatingCount": 7403,
#       "displayName": {
#         "text": "DurianMan",
#         "languageCode": "en"
#       },
#       "primaryType": "dessert_restaurant"
#     },
#     {
#       "id": "ChIJEzJLjGdIzDERhhHLtniAFO0",
#       "formattedAddress": "13, Jalan 16/11, Pusat Perdagangan Phileo Damansara, 46350 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.1263806,
#         "longitude": 101.64475139999999
#       },
#       "rating": 4.1,
#       "userRatingCount": 4189,
#       "displayName": {
#         "text": "Eastin Hotel Kuala Lumpur",
#         "languageCode": "en"
#       },
#       "primaryType": "hotel"
#     },
#     {
#       "id": "ChIJQ7cz5t9LzDERvPSNR2XJblI",
#       "formattedAddress": "Jalan 13/1, Pjs 13, 46200 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.1117288999999997,
#         "longitude": 101.6392304
#       },
#       "rating": 3.7,
#       "userRatingCount": 2248,
#       "displayName": {
#         "text": "Centrestage Petaling Jaya",
#         "languageCode": "en"
#       },
#       "primaryType": "lodging"
#     },
#     {
#       "id": "ChIJ-zS4G6xJzDERgg2u3VqPaWE",
#       "formattedAddress": "Seksyen 13, 46200 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.1186582,
#         "longitude": 101.6346445
#       },
#       "rating": 3.4,
#       "userRatingCount": 89,
#       "displayName": {
#         "text": "Ryan & Miho Service Apartment",
#         "languageCode": "en"
#       },
#       "primaryType": "condominium_complex"
#     },
#     {
#       "id": "ChIJ-_AlO-lLzDERmz5muf_I1E0",
#       "formattedAddress": "28, Jalan 51a/223, Seksyen 51a, 46100 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.1022578999999997,
#         "longitude": 101.6334285
#       },
#       "rating": 4.6,
#       "userRatingCount": 1500,
#       "displayName": {
#         "text": "Amway",
#         "languageCode": "en"
#       },
#       "primaryType": "corporate_office"
#     },
#     {
#       "id": "ChIJ3w2vVmlJzDERKmObhAdHvHA",
#       "formattedAddress": "8, Jalan SS 21/37, Damansara Utama, 47400 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.1335142,
#         "longitude": 101.62359370000001
#       },
#       "rating": 4.1,
#       "userRatingCount": 85,
#       "displayName": {
#         "text": "Imazium",
#         "languageCode": "en"
#       },
#       "primaryType": "corporate_office"
#     },
#     {
#       "id": "ChIJPWu-pvJPzDER1ms4E0GV6cM",
#       "formattedAddress": "Jln SS 24/8, Taman Megah, 47301 Petaling Jaya, Selangor, Malaysia",   
#       "location": {
#         "latitude": 3.1143577,
#         "longitude": 101.61170159999999
#       },
#       "rating": 4,
#       "userRatingCount": 633,
#       "displayName": {
#         "text": "Megah Rise Mall",
#         "languageCode": "en"
#       },
#       "primaryType": "shopping_mall"
#     },
#     {
#       "id": "ChIJGYrCEkFJzDERptEPU8zlMrA",
#       "formattedAddress": "998, Jalan 17/38, Seksyen 17, 46400 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.1284943999999997,
#         "longitude": 101.6350264
#       },
#       "rating": 3.8,
#       "userRatingCount": 1268,
#       "displayName": {
#         "text": "Seventeen Mall",
#         "languageCode": "en"
#       },
#       "primaryType": "shopping_mall"
#     },
#     {
#       "id": "ChIJG4bA5-BLzDERBA_2v0Bg-ek",
#       "formattedAddress": "Digital Mall, 2, Jalan 14/20, Seksyen 14 Petaling Jaya, 46100 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.1092559,
#         "longitude": 101.6364124
#       },
#       "rating": 4.1,
#       "userRatingCount": 8145,
#       "displayName": {
#         "text": "Digital Mall",
#         "languageCode": "en"
#       },
#       "primaryType": "shopping_mall"
#     },
#     {
#       "id": "ChIJB10hLmBJzDER-WDB0D2tw4U",
#       "formattedAddress": "Jalan Kemajuan, Seksyen 13, 46200 Petaling Jaya, Selangor, Malaysia", 
#       "location": {
#         "latitude": 3.1133813999999997,
#         "longitude": 101.6408599
#       },
#       "rating": 3.9,
#       "userRatingCount": 344,
#       "displayName": {
#         "text": "PJ Midtown",
#         "languageCode": "en"
#       },
#       "primaryType": "consultant"
#     },
#     {
#       "id": "ChIJS3bFHcxOzDER80732vDIXCc",
#       "formattedAddress": "3, Lebuh Bandar Utama, Bandar Utama, 47800 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.137466,
#         "longitude": 101.609805
#       },
#       "rating": 3.9,
#       "userRatingCount": 3594,
#       "displayName": {
#         "text": "Centrepoint Bandar Utama",
#         "languageCode": "en"
#       },
#       "primaryType": "shopping_mall"
#     },
#     {
#       "id": "ChIJvaGtCJ5JzDERxkq1vMsMcgQ",
#       "formattedAddress": "83 Ground Floor, Jalan SS 21/1a, Damansara Utama, 47400 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.1343413,
#         "longitude": 101.6210164
#       },
#       "rating": 4.8,
#       "userRatingCount": 9243,
#       "displayName": {
#         "text": "Hot Bird",
#         "languageCode": "en"
#       },
#       "primaryType": "restaurant"
#     }
#   ]
# }
#       "location": {
#         "latitude": 3.1343413,
#         "longitude": 101.6210164
#       },
#       "rating": 4.8,
#       "userRatingCount": 9243,
#       "displayName": {
#         "text": "Hot Bird",
#         "languageCode": "en"
#       },
#       "primaryType": "restaurant"
#     }
#   ]
# }
#       },
#       "rating": 4.8,
#       "userRatingCount": 9243,
#       "displayName": {
#         "text": "Hot Bird",
#         "languageCode": "en"
#       },
#       "primaryType": "restaurant"
#     }
#   ]
# }
#       "userRatingCount": 9243,
#       "displayName": {
#         "text": "Hot Bird",
#         "languageCode": "en"
#       },
#       "primaryType": "restaurant"
#     }
#   ]
# }
#         "languageCode": "en"
#       },
#       "primaryType": "restaurant"
#     }
#   ]
# }
#       "primaryType": "restaurant"
#     }
#   ]
# }
#   ]
# }