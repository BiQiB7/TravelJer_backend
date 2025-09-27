import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()


def get_place_details(place_id: str):
    """
    Fetches detailed information for a specific place using its Place ID.

    Args:
        place_id (str): The Place ID of the place to fetch details for.

    Returns:
        dict: A dictionary containing the detailed place information.
    """
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_MAPS_API_KEY environment variable not set.")

    url = f"https://places.googleapis.com/v1/places/{place_id}"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "id,priceRange,types,rating,regularOpeningHours,websiteUri,userRatingCount,allowsDogs,goodForChildren,goodForGroups,goodForWatchingSports,servesVegetarianFood,priceLevel,displayName,formattedAddress,location"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

if __name__ == '__main__':
    # Example usage:
    # Make sure to set the GOOGLE_MAPS_API_KEY environment variable before running
    try:
        # Example Place ID for the Petronas Twin Towers
        place_id = "ChIJbcqXWcJHzDERYdxj9h_QOIE"
        # "ChIJ-Q-v1qzx0TER03mj20F-Q2Q"
        details = get_place_details(place_id)
        print(json.dumps(details, indent=2))
    except ValueError as e:
        print(e)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# the output example
# {
#   "id": "ChIJbcqXWcJHzDERYdxj9h_QOIE",
#   "types": [
#     "chinese_restaurant",
#     "cafe",
#     "restaurant",
#     "point_of_interest",
#     "food",
#     "establishment"
#   ],
#   "formattedAddress": "1, Jalan SS 2/55, SS 2, 47300 Petaling Jaya, Selangor, Malaysia",
#   "location": {
#     "latitude": 3.1166943999999996,
#     "longitude": 101.62177059999999
#   },
#   "rating": 4.7,
#   "websiteUri": "https://www.facebook.com/Togatherrestaurant",
#   "regularOpeningHours": {
#     "openNow": true,
#     "periods": [
#       {
#         "open": {
#           "day": 0,
#           "hour": 11,
#           "minute": 0
#         },
#         "close": {
#           "day": 1,
#           "hour": 1,
#           "minute": 0
#         }
#       },
#       {
#         "open": {
#           "day": 1,
#           "hour": 11,
#           "minute": 0
#         },
#         "close": {
#           "day": 2,
#           "hour": 1,
#           "minute": 0
#         }
#       },
#       {
#         "open": {
#           "day": 2,
#           "hour": 11,
#           "minute": 0
#         },
#         "close": {
#           "day": 3,
#           "hour": 1,
#           "minute": 0
#         }
#       },
#       {
#         "open": {
#           "day": 3,
#           "hour": 11,
#           "minute": 0
#         },
#         "close": {
#           "day": 4,
#           "hour": 1,
#           "minute": 0
#         }
#       },
#       {
#         "open": {
#           "day": 4,
#           "hour": 11,
#           "minute": 0
#         },
#         "close": {
#           "day": 5,
#           "hour": 1,
#           "minute": 0
#         }
#       },
#       {
#         "open": {
#           "day": 5,
#           "hour": 11,
#           "minute": 0
#         },
#         "close": {
#           "day": 6,
#           "hour": 1,
#           "minute": 0
#         }
#       },
#       {
#         "open": {
#           "day": 6,
#           "hour": 11,
#           "minute": 0
#         },
#         "close": {
#           "day": 0,
#           "hour": 1,
#           "minute": 0
#         }
#       }
#     ],
#     "weekdayDescriptions": [
#       "Monday: 11:00\u202fAM\u2009\u2013\u20091:00\u202fAM",
#       "Tuesday: 11:00\u202fAM\u2009\u2013\u20091:00\u202fAM",
#       "Wednesday: 11:00\u202fAM\u2009\u2013\u20091:00\u202fAM",
#       "Thursday: 11:00\u202fAM\u2009\u2013\u20091:00\u202fAM",
#       "Friday: 11:00\u202fAM\u2009\u2013\u20091:00\u202fAM",
#       "Saturday: 11:00\u202fAM\u2009\u2013\u20091:00\u202fAM",
#       "Sunday: 11:00\u202fAM\u2009\u2013\u20091:00\u202fAM"
#     ],
#     "nextCloseTime": "2025-09-26T17:00:00Z"
#   },
#   "priceLevel": "PRICE_LEVEL_MODERATE",
#   "userRatingCount": 2877,
#   "displayName": {
#     "text": "Togather \u8bb2\u996e\u8bb2\u5403 | SS 2",
#     "languageCode": "en"
#   },
#   "servesVegetarianFood": true,
#   "goodForChildren": true,
#   "goodForGroups": true,
#   "goodForWatchingSports": false,
#   "priceRange": {
#     "startPrice": {
#       "currencyCode": "MYR",
#       "units": "20"
#     },
#     "endPrice": {
#       "currencyCode": "MYR",
#       "units": "40"
#     }
#   }
# }