import requests
import json

url = "http://localhost:8001/api/route-analysis/"
data = {
    "source": "Chennai",
    "destination": "Coimbatore",
    "via": ""
}

try:
    response = requests.post(url, json=data, timeout=200)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except Exception as e:
    print(f"Error: {e}")
