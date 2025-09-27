import requests
import json

url = "https://jaycee-unushered-oligarchically.ngrok-free.dev/search"

params = {
    "place" : "Ipoh",
}

try:
    data = requests.get(url, params=params)
    if data.status_code == 200:
        print(data.json())
        with open("test.txt", "w") as f:
            new_data = data.json()
            clean = json.dumps(new_data, indent=2)
            f.write(f"{clean}")
    else:
        print("something wrong")
except requests.RequestException as err:
    print(err)