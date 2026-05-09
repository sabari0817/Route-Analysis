import requests
import json

def test_api():
    url = "http://localhost:8000/api/route-analysis/"
    payload = {
        "source": "Chennai",
        "destination": "Coimbatore",
        "via": ""
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_api()
