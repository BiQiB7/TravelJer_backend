import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

def get_daily_forecast(latitude, longitude, days=None):
    """
    Retrieves the daily weather forecast for a specific location.

    Args:
        latitude (float): The latitude of the location.
        longitude (float): The longitude of the location.
        days (int, optional): The number of forecast days to return (1-10). Defaults to None.

    Returns:
        dict: A dictionary containing the forecast object.
    """
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_MAPS_API_KEY environment variable not set.")

    base_url = "https://weather.googleapis.com/v1/forecast/days:lookup"
    
    params = {
        "key": api_key,
        "location.latitude": latitude,
        "location.longitude": longitude
    }

    if days:
        params["days"] = days

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

if __name__ == '__main__':
    # Example usage:
    # Make sure to set the GOOGLE_MAPS_API_KEY environment variable before running
    try:
        # Coordinates for Kuala Lumpur
        latitude = 3.1390
        longitude = 101.6869
        forecast = get_daily_forecast(latitude, longitude, days=3)
        print(json.dumps(forecast, indent=2))
    except ValueError as e:
        print(e)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# the output example
# {
#   "forecastDays": [
#     {
#       "interval": {
#         "startTime": "2025-09-23T23:00:00Z",
#         "endTime": "2025-09-24T23:00:00Z"
#       },
#       "displayDate": {
#         "year": 2025,
#         "month": 9,
#         "day": 24
#       },
#       "daytimeForecast": {
#         "interval": {
#           "startTime": "2025-09-23T23:00:00Z",
#           "endTime": "2025-09-24T11:00:00Z"
#         },
#         "weatherCondition": {
#           "iconBaseUri": "https://maps.gstatic.com/weather/v1/drizzle",
#           "description": {
#             "text": "Light rain",
#             "languageCode": "en"
#           },
#           "type": "LIGHT_RAIN"
#         },
#         "relativeHumidity": 62,
#         "uvIndex": 8,
#         "precipitation": {
#           "probability": {
#             "percent": 20,
#             "type": "RAIN"
#           },
#           "snowQpf": {
#             "quantity": 0,
#             "unit": "MILLIMETERS"
#           },
#           "qpf": {
#             "quantity": 0.7366,
#             "unit": "MILLIMETERS"
#           }
#         },
#         "thunderstormProbability": 30,
#         "wind": {
#           "direction": {
#             "degrees": 291,
#             "cardinal": "WEST_NORTHWEST"
#           },
#           "speed": {
#             "value": 10,
#             "unit": "KILOMETERS_PER_HOUR"
#           },
#           "gust": {
#             "value": 18,
#             "unit": "KILOMETERS_PER_HOUR"
#           }
#         },
#         "cloudCover": 90,
#         "iceThickness": {
#           "thickness": 0,
#           "unit": "MILLIMETERS"
#         }
#       },
#       "nighttimeForecast": {
#         "interval": {
#           "startTime": "2025-09-24T11:00:00Z",
#           "endTime": "2025-09-24T23:00:00Z"
#         },
#         "weatherCondition": {
#           "iconBaseUri": "https://maps.gstatic.com/weather/v1/mostly_cloudy_night",
#           "description": {
#             "text": "Mostly cloudy",
#             "languageCode": "en"
#           },
#           "type": "MOSTLY_CLOUDY"
#         },
#         "relativeHumidity": 74,
#         "uvIndex": 0,
#         "precipitation": {
#           "probability": {
#             "percent": 25,
#             "type": "RAIN"
#           },
#           "snowQpf": {
#             "quantity": 0,
#             "unit": "MILLIMETERS"
#           },
#           "qpf": {
#             "quantity": 0.4089,
#             "unit": "MILLIMETERS"
#           }
#         },
#         "thunderstormProbability": 40,
#         "wind": {
#           "direction": {
#             "degrees": 326,
#             "cardinal": "NORTHWEST"
#           },
#           "speed": {
#             "value": 8,
#             "unit": "KILOMETERS_PER_HOUR"
#           },
#           "gust": {
#             "value": 16,
#             "unit": "KILOMETERS_PER_HOUR"
#           }
#         },
#         "cloudCover": 100,
#         "iceThickness": {
#           "thickness": 0,
#           "unit": "MILLIMETERS"
#         }
#       },
#       "maxTemperature": {
#         "degrees": 34.6,
#         "unit": "CELSIUS"
#       },
#       "minTemperature": {
#         "degrees": 25.7,
#         "unit": "CELSIUS"
#       },
#       "feelsLikeMaxTemperature": {
#         "degrees": 39.4,
#         "unit": "CELSIUS"
#       },
#       "feelsLikeMinTemperature": {
#         "degrees": 28.5,
#         "unit": "CELSIUS"
#       },
#       "sunEvents": {
#         "sunriseTime": "2025-09-23T23:02:09.381702387Z",
#         "sunsetTime": "2025-09-24T11:08:24.618427749Z"
#       },
#       "moonEvents": {
#         "moonPhase": "WAXING_CRESCENT",
#         "moonriseTimes": [
#           "2025-09-24T00:34:32.140032053Z"
#         ],
#         "moonsetTimes": [
#           "2025-09-24T12:48:59.944127085Z"
#         ]
#       },
#       "maxHeatIndex": {
#         "degrees": 39.4,
#         "unit": "CELSIUS"
#       }
#     },
#     {
#       "interval": {
#         "startTime": "2025-09-24T23:00:00Z",
#         "endTime": "2025-09-25T23:00:00Z"
#       },
#       "displayDate": {
#         "year": 2025,
#         "month": 9,
#         "day": 25
#       },
#       "daytimeForecast": {
#         "interval": {
#           "startTime": "2025-09-24T23:00:00Z",
#           "endTime": "2025-09-25T11:00:00Z"
#         },
#         "weatherCondition": {
#           "iconBaseUri": "https://maps.gstatic.com/weather/v1/cloudy",
#           "description": {
#             "text": "Cloudy",
#             "languageCode": "en"
#           },
#           "type": "CLOUDY"
#         },
#         "relativeHumidity": 62,
#         "uvIndex": 3,
#         "precipitation": {
#           "probability": {
#             "percent": 20,
#             "type": "RAIN"
#           },
#           "snowQpf": {
#             "quantity": 0,
#             "unit": "MILLIMETERS"
#           },
#           "qpf": {
#             "quantity": 0.0508,
#             "unit": "MILLIMETERS"
#           }
#         },
#         "thunderstormProbability": 40,
#         "wind": {
#           "direction": {
#             "degrees": 181,
#             "cardinal": "SOUTH"
#           },
#           "speed": {
#             "value": 8,
#             "unit": "KILOMETERS_PER_HOUR"
#           },
#           "gust": {
#             "value": 14,
#             "unit": "KILOMETERS_PER_HOUR"
#           }
#         },
#         "cloudCover": 100,
#         "iceThickness": {
#           "thickness": 0,
#           "unit": "MILLIMETERS"
#         }
#       },
#       "nighttimeForecast": {
#         "interval": {
#           "startTime": "2025-09-25T11:00:00Z",
#           "endTime": "2025-09-25T23:00:00Z"
#         },
#         "weatherCondition": {
#           "iconBaseUri": "https://maps.gstatic.com/weather/v1/cloudy",
#           "description": {
#             "text": "Cloudy",
#             "languageCode": "en"
#           },
#           "type": "CLOUDY"
#         },
#         "relativeHumidity": 71,
#         "uvIndex": 0,
#         "precipitation": {
#           "probability": {
#             "percent": 20,
#             "type": "RAIN"
#           },
#           "snowQpf": {
#             "quantity": 0,
#             "unit": "MILLIMETERS"
#           },
#           "qpf": {
#             "quantity": 0.1016,
#             "unit": "MILLIMETERS"
#           }
#         },
#         "thunderstormProbability": 30,
#         "wind": {
#           "direction": {
#             "degrees": 137,
#             "cardinal": "SOUTHEAST"
#           },
#           "speed": {
#             "value": 8,
#             "unit": "KILOMETERS_PER_HOUR"
#           },
#           "gust": {
#             "value": 14,
#             "unit": "KILOMETERS_PER_HOUR"
#           }
#         },
#         "cloudCover": 100,
#         "iceThickness": {
#           "thickness": 0,
#           "unit": "MILLIMETERS"
#         }
#       },
#       "maxTemperature": {
#         "degrees": 33.4,
#         "unit": "CELSIUS"
#       },
#       "minTemperature": {
#         "degrees": 25.6,
#         "unit": "CELSIUS"
#       },
#       "feelsLikeMaxTemperature": {
#         "degrees": 38.5,
#         "unit": "CELSIUS"
#       },
#       "feelsLikeMinTemperature": {
#         "degrees": 28.3,
#         "unit": "CELSIUS"
#       },
#       "sunEvents": {
#         "sunriseTime": "2025-09-24T23:01:53.587611229Z",
#         "sunsetTime": "2025-09-25T11:07:58.687129499Z"
#       },
#       "moonEvents": {
#         "moonPhase": "WAXING_CRESCENT",
#         "moonriseTimes": [
#           "2025-09-25T01:18:18.203830400Z"
#         ],
#         "moonsetTimes": [
#           "2025-09-25T13:31:21.584476275Z"
#         ]
#       },
#       "maxHeatIndex": {
#         "degrees": 38.5,
#         "unit": "CELSIUS"
#       }
#     },
#     {
#       "interval": {
#         "startTime": "2025-09-25T23:00:00Z",
#         "endTime": "2025-09-26T23:00:00Z"
#       },
#       "displayDate": {
#         "year": 2025,
#         "month": 9,
#         "day": 26
#       },
#       "daytimeForecast": {
#         "interval": {
#           "startTime": "2025-09-25T23:00:00Z",
#           "endTime": "2025-09-26T11:00:00Z"
#         },
#         "weatherCondition": {
#           "iconBaseUri": "https://maps.gstatic.com/weather/v1/isolated_tstorms",
#           "description": {
#             "text": "Scattered thunderstorms",
#             "languageCode": "en"
#           },
#           "type": "SCATTERED_THUNDERSTORMS"
#         },
#         "relativeHumidity": 59,
#         "uvIndex": 5,
#         "precipitation": {
#           "probability": {
#             "percent": 45,
#             "type": "RAIN"
#           },
#           "snowQpf": {
#             "quantity": 0,
#             "unit": "MILLIMETERS"
#           },
#           "qpf": {
#             "quantity": 3.1928,
#             "unit": "MILLIMETERS"
#           }
#         },
#         "thunderstormProbability": 70,
#         "wind": {
#           "direction": {
#             "degrees": 156,
#             "cardinal": "SOUTH_SOUTHEAST"
#           },
#           "speed": {
#             "value": 8,
#             "unit": "KILOMETERS_PER_HOUR"
#           },
#           "gust": {
#             "value": 14,
#             "unit": "KILOMETERS_PER_HOUR"
#           }
#         },
#         "cloudCover": 100,
#         "iceThickness": {
#           "thickness": 0,
#           "unit": "MILLIMETERS"
#         }
#       },
#       "nighttimeForecast": {
#         "interval": {
#           "startTime": "2025-09-26T11:00:00Z",
#           "endTime": "2025-09-26T23:00:00Z"
#         },
#         "weatherCondition": {
#           "iconBaseUri": "https://maps.gstatic.com/weather/v1/cloudy",
#           "description": {
#             "text": "Cloudy",
#             "languageCode": "en"
#           },
#           "type": "CLOUDY"
#         },
#         "relativeHumidity": 81,
#         "uvIndex": 0,
#         "precipitation": {
#           "probability": {
#             "percent": 45,
#             "type": "RAIN"
#           },
#           "snowQpf": {
#             "quantity": 0,
#             "unit": "MILLIMETERS"
#           },
#           "qpf": {
#             "quantity": 2.6645,
#             "unit": "MILLIMETERS"
#           }
#         },
#         "thunderstormProbability": 60,
#         "wind": {
#           "direction": {
#             "degrees": 111,
#             "cardinal": "EAST_SOUTHEAST"
#           },
#           "speed": {
#             "value": 6,
#             "unit": "KILOMETERS_PER_HOUR"
#           },
#           "gust": {
#             "value": 11,
#             "unit": "KILOMETERS_PER_HOUR"
#           }
#         },
#         "cloudCover": 100,
#         "iceThickness": {
#           "thickness": 0,
#           "unit": "MILLIMETERS"
#         }
#       },
#       "maxTemperature": {
#         "degrees": 34.2,
#         "unit": "CELSIUS"
#       },
#       "minTemperature": {
#         "degrees": 25.4,
#         "unit": "CELSIUS"
#       },
#       "feelsLikeMaxTemperature": {
#         "degrees": 39.3,
#         "unit": "CELSIUS"
#       },
#       "feelsLikeMinTemperature": {
#         "degrees": 28.2,
#         "unit": "CELSIUS"
#       },
#       "sunEvents": {
#         "sunriseTime": "2025-09-25T23:01:37.940921569Z",
#         "sunsetTime": "2025-09-26T11:07:32.930123477Z"
#       },
#       "moonEvents": {
#         "moonPhase": "WAXING_CRESCENT",
#         "moonriseTimes": [
#           "2025-09-26T02:04:07.235556425Z"
#         ],
#         "moonsetTimes": [
#           "2025-09-26T14:16:18.725001791Z"
#         ]
#       },
#       "maxHeatIndex": {
#         "degrees": 39.3,
#         "unit": "CELSIUS"
#       }
#     }
#   ],
#   "timeZone": {
#     "id": "Asia/Kuala_Lumpur"
#   }
# }