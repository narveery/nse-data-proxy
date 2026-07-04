import requests
import json

def fetch_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    session = requests.Session()
    session.headers.update(headers)

    # 1. Ping homepage to get cookies
    try:
        session.get("https://www.nseindia.com", timeout=15)
    except Exception as e:
        print(f"Error connecting to NSE: {e}")

    # 2. Define the endpoints
    endpoints = {
        "fiidii": "https://www.nseindia.com/api/fiidiiTradeNse",
        "advance_decline": "https://www.nseindia.com/api/live-analysis-advance",
        "all_indices": "https://www.nseindia.com/api/allIndices"
    }

    data = {}

    # 3. Fetch all endpoints and store the JSON
    for key, url in endpoints.items():
        try:
            res = session.get(url, timeout=10)
            if res.status_code == 200:
                data[key] = res.json()
            else:
                data[key] = {"error": f"Failed with status {res.status_code}"}
        except Exception as e:
            data[key] = {"error": str(e)}

    # 4. Save to JSON file
    with open("nse_data.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    fetch_data()
