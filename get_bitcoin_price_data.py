import os
import requests
import datetime
import concurrent.futures
import json

API_KEY = "e471405e501d405ced14457f2554c1e080328f4c1796a63a5ae56eba42a0b46a"
days = 1  # We want to download the last 100 days
current_ts = datetime.datetime.now().timestamp()
end = int(current_ts - current_ts % (60 * 60 * 24 * 1000))
start = end - 1000 * 60 * 60 * 24 * days
days_str = []

def getUrl(endTime):
    url = f'https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=USDT&toTs={endTime}&limit=1916&api_key={API_KEY}'
    return url


def download_day_data():
    end = 1723996200
    url_to_call = getUrl(end)
    response = requests.get(url_to_call)

    if response.status_code == 200:
        response_json = response.json()
        data_field = response_json.get('Data')
        if data_field:
            with open(f'./data/cryptocompare_BTC_USDT_{end}.json', 'w', encoding='utf8') as file:
                json.dump(data_field, file, ensure_ascii=False, indent=4)
        else:
            print(f"No 'Data' field found in the response for {end}")
            print(response_json)
    else:
        print(f"Failed to download data for {end}: {response.status_code}")

# Ensure the data directory exists
os.makedirs('./data', exist_ok=True)

# Use ThreadPoolExecutor to handle asynchronous requests
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     executor.map(download_day_data, days_str)

download_day_data()