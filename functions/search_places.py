import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()


def search_places(text_query, language_code=None, max_result_count=None, region_code=None):
    """
    Searches for places based on a text query.

    Args:
        text_query (str): The text string to search for (e.g., "restaurants in San Francisco").
        language_code (str, optional): The language in which to return results (e.g., "en-US"). Defaults to None.
        max_result_count (int, optional): The maximum number of results to return. Defaults to None.
        region_code (str, optional): The region code to bias the search results (e.g., "US"). Defaults to None.

    Returns:
        dict: A dictionary containing a list of place objects.
    """
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_MAPS_API_KEY environment variable not set.")

    url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.id,places.priceRange,places.types,places.rating,places.regularOpeningHours,places.websiteUri,places.userRatingCount,places.allowsDogs,places.goodForChildren,places.goodForGroups,places.goodForWatchingSports,places.servesVegetarianFood,places.priceLevel,places.displayName,places.formattedAddress,places.location"
    }

    data = {
        "textQuery": text_query
    }

    if language_code:
        data["languageCode"] = language_code
    if max_result_count:
        data["maxResultCount"] = max_result_count
    if region_code:
        data["regionCode"] = region_code

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
        # query="New Old Friend Duck Rice, Ipoh"
        # query="Restaurant Kum Kee, Ipoh"
        # query="Restaurant Sun Heng Kee"
        query="Concubine lane, Ipoh"
        places = search_places(query, max_result_count=1)
        print(json.dumps(places, indent=2))
    except ValueError as e:
        print(e)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
#query="New Old Friend Duck Rice, Ipoh"
#query="Restaurant Kum Kee, Ipoh"

#- duck rice. You can buy the whole duck. Really special cooking style that is different than the typical HK style"
# search_places(query,max_result_count=3)

# New Old Friend Restaurant - duck rice. You can buy the whole duck. Really special cooking style that is different than the typical HK style

# Restaurant Kum Kee - chicken feet

# Xibei Good - to me it is THE BEST wanton mee. Used to be better as their shrimp wanton is damn huge. Recently no more whole shrimp, they use shrimp paste but still good

# Restaurant Sun Heng Kee- there is a stall in this kopitiam (mun kee mee stall) sells pretty good beef slice noodles.

# Restaurant number one mei sik wan- best curry fish head (dinner)
# the output example
# {
#     'places':[{
#       "id": "ChIJbcqXWcJHzDERYdxj9h_QOIE",
#       "types": [
#         "chinese_restaurant",
#         "cafe",
#         "restaurant",
#         "food",
#         "point_of_interest",
#         "establishment"
#       ],
#       "formattedAddress": "1, Jalan SS 2/55, SS 2, 47300 Petaling Jaya, Selangor, Malaysia",
#       "location": {
#         "latitude": 3.1166943999999996,
#         "longitude": 101.62177059999999
#       },
#       "rating": 4.7,
#       "websiteUri": "https://www.facebook.com/Togatherrestaurant",
#       "regularOpeningHours": {
#         "openNow": false,
#         "periods": [
#           {
#             "open": {
#               "day": 0,
#               "hour": 11,
#               "minute": 0
#             },
#             "close": {
#               "day": 1,
#               "hour": 1,
#               "minute": 0
#             }
#           },
#           {
#             "open": {
#               "day": 1,
#               "hour": 11,
#               "minute": 0
#             },
#             "close": {
#               "day": 2,
#               "hour": 1,
#               "minute": 0
#             }
#           },
#           {
#             "open": {
#               "day": 2,
#               "hour": 11,
#               "minute": 0
#             },
#             "close": {
#               "day": 3,
#               "hour": 1,
#               "minute": 0
#             }
#           },
#           {
#             "open": {
#               "day": 3,
#               "hour": 11,
#               "minute": 0
#             },
#             "close": {
#               "day": 4,
#               "hour": 1,
#               "minute": 0
#             }
#           },
#           {
#             "open": {
#               "day": 4,
#               "hour": 11,
#               "minute": 0
#             },
#             "close": {
#               "day": 5,
#               "hour": 1,
#               "minute": 0
#             }
#           },
#           {
#             "open": {
#               "day": 5,
#               "hour": 11,
#               "minute": 0
#             },
#             "close": {
#               "day": 6,
#               "hour": 1,
#               "minute": 0
#             }
#           },
#           {
#             "open": {
#               "day": 6,
#               "hour": 11,
#               "minute": 0
#             },
#             "close": {
#               "day": 0,
#               "hour": 1,
#               "minute": 0
#             }
#           }
#         ],
#         "weekdayDescriptions": [
#           "Monday: 11:00\u202fAM\u2009\u2013\u20091:00\u202fAM",
#           "Tuesday: 11:00\u202fAM\u2009\u2013\u20091:00\u202fAM",
#           "Wednesday: 11:00\u202fAM\u2009\u2013\u20091:00\u202fAM",
#           "Thursday: 11:00\u202fAM\u2009\u2013\u20091:00\u202fAM",
#           "Friday: 11:00\u202fAM\u2009\u2013\u20091:00\u202fAM",
#           "Saturday: 11:00\u202fAM\u2009\u2013\u20091:00\u202fAM",
#           "Sunday: 11:00\u202fAM\u2009\u2013\u20091:00\u202fAM"
#         ],
#         "nextOpenTime": "2025-09-25T03:00:00Z"
#       },
#       "priceLevel": "PRICE_LEVEL_MODERATE",
#       "userRatingCount": 2876,
#       "displayName": {
#         "text": "Togather \u8bb2\u996e\u8bb2\u5403 | SS 2",
#         "languageCode": "en"
#       },
#       "servesVegetarianFood": true,
#       "goodForChildren": true,
#       "goodForGroups": true,
#       "goodForWatchingSports": false,
#       "priceRange": {
#         "startPrice": {
#           "currencyCode": "MYR",
#           "units": "20"
#         },
#         "endPrice": {
#           "currencyCode": "MYR",
#           "units": "40"
#         }
#       }
#     }