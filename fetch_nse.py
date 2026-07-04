import requests
import json

def fetch_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    session = requests.Session()
    session.headers.update(headers)

    # 1. Ping the homepage to establish a session and get cookies
    try:
        session.get("https://www.nseindia.com", timeout=15)
    except Exception as e:
        print(f"Error connecting to NSE: {e}")

    # 2. Update headers for API requests
    session.headers.update({'Accept': 'application/json, text/javascript, */*; q=0.01'})

    # 3. Fetch FII/DII Data
    fiidii_url = "https://www.nseindia.com/api/fiidiiTradeNse"
    fiidii_res = session.get(fiidii_url, timeout=10)
    
    # 4. Fetch Advance/Decline Data
    adv_url = "https://www.nseindia.com/api/live-analysis-advance"
    adv_res = session.get(adv_url, timeout=10)

    # 5. Compile the data
    data = {}
    if fiidii_res.status_code == 200:
        data['fiidii'] = fiidii_res.json()
    else:
        data['fiidii'] = {"error": f"Failed with status {fiidii_res.status_code}"}

    if adv_res.status_code == 200:
        data['advance_decline'] = adv_res.json()
    else:
        data['advance_decline'] = {"error": f"Failed with status {adv_res.status_code}"}

    # 6. Save to JSON file
    with open("nse_data.json", "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    fetch_data()
