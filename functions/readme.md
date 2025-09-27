

# Functions API Documentation

This document provides details on the functions available in this directory, including their input parameters and output formats.

## `find_nearby_places.py`

### `find_nearby_places(latitude, longitude, radius, included_types=None, excluded_types=None, max_result_count=None, rank_preference=None)`

Searches for places of specific types within a given area.

**Input Params:**
-   `latitude` (float): The latitude of the center of the search area.
-   `longitude` (float): The longitude of the center of the search area.
-   `radius` (float): The radius of the search area in meters.
-   `included_types` (list, optional): A list of place types to search for.
-   `excluded_types` (list, optional): A list of place types to exclude from the search.
-   `max_result_count` (int, optional): The maximum number of results to return.
-   `rank_preference` (str, optional): The ranking preference for the results. Can be "POPULARITY" or "DISTANCE".

**Output Format:**
A dictionary containing a list of place objects. Example:
```json
{
  "places": [
    {
      "id": "ChIJc_atMtVOzDER-lL4cxma7Kk",
      "types": [
        "garden",
        "tourist_attraction",
        "park",
        "point_of_interest",
        "establishment"
      ],
      "formattedAddress": "Upper Roof (above Food Republic, 1 Utama Shopping Centre, Bandar Utama, 47800 Petaling Jaya, Selangor, Malaysia",
      "location": {
        "latitude": 3.1503631,
        "longitude": 101.6158842
      },
      "rating": 4.6,
      "regularOpeningHours": {
        "openNow": false,
        "periods": [
          {
            "open": { "day": 0, "hour": 10, "minute": 0 },
            "close": { "day": 0, "hour": 22, "minute": 0 }
          }
        ],
        "weekdayDescriptions": [
          "Monday: Closed",
          "Tuesday: Closed",
          "Wednesday: Closed",
          "Thursday: Closed",
          "Friday: Closed",
          "Saturday: 10:00 AM – 10:00 PM",
          "Sunday: 10:00 AM – 10:00 PM"
        ]
      },
      "userRatingCount": 371,
      "displayName": {
        "text": "Secret Garden • 1 Utama",
        "languageCode": "en"
      },
      "goodForChildren": true
    }
  ]
}
```

---

## `get_public_transport_data.py`

### `get_gtfs_realtime_data(agency: str, category: str = None)`

Fetches real-time public transport data (vehicle positions) from data.gov.my.

**Input Params:**
-   `agency` (str): The transport agency. Possible values: 'mybas-johor', 'ktmb', 'prasarana'.
-   `category` (str, optional): The category for the agency, required for 'prasarana'. Possible values: 'rapid-bus-kl', 'rapid-bus-mrtfeeder', 'rapid-bus-kuantan', 'rapid-bus-penang'.

**Output Format:**
A dictionary containing the vehicle position data, or an error message. Example:
```json
{
  "vehicle_positions": [
    {
      "trip": {
        "tripId": "...",
        "routeId": "..."
      },
      "position": {
        "latitude": 3.123,
        "longitude": 101.456
      },
      "vehicle": {
        "id": "..."
      }
    }
  ]
}
```

### `get_gtfs_static_data(agency: str, category: str = None, output_dir: str = 'gtfs_static_data')`

Fetches static GTFS data from data.gov.my and saves it as a ZIP file.

**Input Params:**
-   `agency` (str): The transport agency. Possible values: 'mybas-johor', 'ktmb', 'prasarana'.
-   `category` (str, optional): The category for the agency, required for 'prasarana'. Possible values: 'rapid-bus-penang', 'rapid-bus-kuantan', 'rapid-bus-mrtfeeder', 'rapid-rail-kl', 'rapid-bus-kl'.
-   `output_dir` (str, optional): The directory to save the downloaded ZIP file.

**Output Format:**
A string containing the path to the saved ZIP file, or an error message.

---

## `get_route.py`

### `get_route(origin_place_id, destination_place_id, waypoint_place_ids=None, travel_mode=None)`

Calculates the route between an origin and a destination, with optional waypoints.

**Input Params:**
-   `origin_place_id` (str): The Place ID of the origin.
-   `destination_place_id` (str): The Place ID of the destination.
-   `waypoint_place_ids` (list, optional): A list of Place IDs for intermediate waypoints.
-   `travel_mode` (str, optional): The mode of travel. Can be "DRIVE", "BICYCLE", "TRANSIT", or "WALK".

**Output Format:**
A dictionary containing the route object. Example:
```json
{
  "routes": [
    {
      "distanceMeters": 9844,
      "duration": "1014s",
      "polyline": {
        "encodedPolyline": "{wgRslekR...ELG"
      }
    }
  ]
}
```

---

## `get_weather_forecast.py`

### `get_daily_forecast(latitude, longitude, days=None)`

Retrieves the daily weather forecast for a specific location.

**Input Params:**
-   `latitude` (float): The latitude of the location.
-   `longitude` (float): The longitude of the location.
-   `days` (int, optional): The number of forecast days to return (1-10).

**Output Format:**
A dictionary containing the forecast object. Example:
```json
{
  "forecastDays": [
    {
      "interval": {
        "startTime": "2025-09-23T23:00:00Z",
        "endTime": "2025-09-24T23:00:00Z"
      },
      "daytimeForecast": {
        "weatherCondition": {
          "description": {
            "text": "Light rain",
            "languageCode": "en"
          },
          "type": "LIGHT_RAIN"
        }
      },
      "maxTemperature": {
        "degrees": 34.6,
        "unit": "CELSIUS"
      }
    }
  ]
}
```

---

## `search_places.py`

### `search_places(text_query, language_code=None, max_result_count=None, region_code=None)`

Searches for places based on a text query.

**Input Params:**
-   `text_query` (str): The text string to search for (e.g., "restaurants in San Francisco").
-   `language_code` (str, optional): The language in which to return results (e.g., "en-US").
-   `max_result_count` (int, optional): The maximum number of results to return.
-   `region_code` (str, optional): The region code to bias the search results (e.g., "US").

**Output Format:**
A dictionary containing a list of place objects. Example:
```json
{
  "places": [
    {
      "id": "ChIJbcqXWcJHzDERYdxj9h_QOIE",
      "types": [
        "chinese_restaurant",
        "cafe",
        "restaurant",
        "food",
        "point_of_interest",
        "establishment"
      ],
      "formattedAddress": "1, Jalan SS 2/55, SS 2, 47300 Petaling Jaya, Selangor, Malaysia",
      "location": {
        "latitude": 3.1166944,
        "longitude": 101.6217706
      },
      "rating": 4.7,
      "websiteUri": "https://www.facebook.com/Togatherrestaurant",
      "regularOpeningHours": {
        "openNow": false,
        "periods": [
          {
            "open": { "day": 0, "hour": 11, "minute": 0 },
            "close": { "day": 1, "hour": 1, "minute": 0 }
          }
        ],
        "weekdayDescriptions": [
          "Monday: 11:00 AM – 1:00 AM",
          "Tuesday: 11:00 AM – 1:00 AM",
          "Wednesday: 11:00 AM – 1:00 AM",
          "Thursday: 11:00 AM – 1:00 AM",
          "Friday: 11:00 AM – 1:00 AM",
          "Saturday: 11:00 AM – 1:00 AM",
          "Sunday: 11:00 AM – 1:00 AM"
        ]
      },
      "priceLevel": "PRICE_LEVEL_MODERATE",
      "userRatingCount": 2876,
      "displayName": {
        "text": "Togather 讲饮讲食 | SS 2",
        "languageCode": "en"
      },
      "servesVegetarianFood": true,
      "goodForChildren": true,
      "goodForGroups": true
    }
  ]
}
```

---

## `search_reddit.py`

### `search_reddit_for_links(query, subreddit_limit=5, post_limit=10)`

Searches for subreddits and retrieves top post links from them.

**Input Params:**
-   `query` (str): The search term to find relevant subreddits.
-   `subreddit_limit` (int, optional): The maximum number of subreddits to search.
-   `post_limit` (int, optional): The maximum number of posts to retrieve from each subreddit.

**Output Format:**
A JSON string containing the results. Example:
```json
{
  "r/malaysia": [
    {
      "title": "...",
      "score": 123,
      "url": "..."
    }
  ]
}
This is the raw output, should scrape and return the summarized information instead
```

---

## `visualize_route_on_map.py`

### `visualize_route_on_map(encoded_polyline, origin_place_id, destination_place_id, waypoint_place_ids=None)`

Generates a map visualization and a navigation link for a route.

**Input Params:**
-   `encoded_polyline` (str): The encoded polyline string representing the route.
-   `origin_place_id` (str): The Place ID of the origin to mark on the map.
-   `destination_place_id` (str): The Place ID of the destination to mark on the map.
-   `waypoint_place_ids` (list, optional): A list of Place IDs for intermediate waypoints to mark on the map.

**Output Format:**
A dictionary containing the URL to a map image and a navigation link. Example:
```json
{
  "staticMapUrl": "https://maps.googleapis.com/maps/api/staticmap?...",
  "navigationUrl": "https://www.google.com/maps/dir/?..."
}


python -m city_weaver_ai.api.main
python city_weaver_ai/test_flow.py

---

## `search_twitter.py`

### `find_trending_places(keywords, min_faves=100, min_retweets=20, search_type="top", content_filters=None, lang="en", from_date=None)`

Finds trending and popular places by searching for posts with high engagement.

**Input Params:**
-   `keywords` (str): Keywords to search for, including operators.
-   `min_faves` (int, optional): Minimum number of likes.
-   `min_retweets` (int, optional): Minimum number of retweets.
-   `search_type` (str, optional): "top" or "latest".
-   `content_filters` (list, optional): Filters for content like "images".
-   `lang` (str, optional): Language code.
-   `from_date` (str, optional): Start date for the search.

**Output Format:**
A dictionary containing the API response.

### `analyze_place_sentiment(keywords, search_type="latest", max_posts=500, lang="en")`

Analyzes what people are saying about specific places.

**Input Params:**
-   `keywords` (str): Keywords to search for, including operators.
-   `search_type` (str, optional): "top" or "latest".
-   `max_posts` (int, optional): Maximum number of posts to retrieve.
-   `lang` (str, optional): Language code.

**Output Format:**
A dictionary containing the API response.

### `perform_social_media_analysis(keywords, search_type="users", max_profiles=100)`

Performs broader social media analysis, like finding influential profiles.

**Input Params:**
-   `keywords` (str): Keywords to search for, including operators.
-   `search_type` (str, optional): "users".
-   `max_profiles` (int, optional): Maximum number of profiles to retrieve.

**Output Format:**
A dictionary containing the API response.
