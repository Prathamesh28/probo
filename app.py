import csv
from datetime import datetime
import json
import pandas as pd
import pytz
import requests
import time
from probo import Probo

# defining key/request url
key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

# requesting data from url
# prev = 26857.61
# while True:
def getBitcoinPrice():
    data = requests.get(key)
    data = data.json()
    # curr = float(data["price"])
    # if curr - prev > 1:
    #     print("Sell")
    # if prev - curr > 1:
    #     print("Buy")
    print(f"{data['symbol']} price is {data['price']}")
    return float(data['price'])
    # prev = curr
    # time.sleep(0.5)


headers = {
        "accept": "*/*",
        "accept-language": "en",
        "appid": "in.probo.pro",
        "authorization": "Bearer 1YXyfRlW9aW3UAUMeXiDxfcOIhuIXHGfuv1UoSFx8uc=",
        "content-type": "application/json",
        "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-device-os": "ANDROID",
        "x-version-name": "10",
        "Referer": "https://trading.probo.in/",
        "Referrer-Policy": "strict-origin-when-cross-origin",
    }

def getAllEvents():
    
    body = {
        "categoryIds": [],
        "topicIds": [2449],
        "eventIds": [],
        "followedOnly": "false",
        "page": 1,
        "filter": {},
    }
    try:
        data = requests.post(
            "https://prod.api.probo.in/api/v1/product/arena/events/v2",
            json=body,
            headers=headers,
        )
        data = data.json()
        # print(data)
        events = data["data"]["records"]["events"]
        event_ids = [i["id"] for i in events]
        print(event_ids)
        return event_ids
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)



def convert_to_IST(utc_time):
    utc_time = datetime.strptime(utc_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    utc_zone = pytz.utc
    ist_zone = pytz.timezone('Asia/Kolkata')
    utc_time = utc_zone.localize(utc_time)
    ist_time = utc_time.astimezone(ist_zone)
    ist_time_str = ist_time.strftime('%Y-%m-%dT%H:%M:%S%z')

    return ist_time_str



def load_event_data(filename):
    event_data = pd.read_csv(filename)
    event_data['start_time'] = pd.to_datetime(event_data['start_time'])
    event_data['end_time'] = pd.to_datetime(event_data['end_time'])
    return event_data



def get_event_data(event_id):
    data = requests.get(
        f"https://prod.api.probo.in/api/v1/product/events/{event_id}",
        headers=headers,
    )
    data = data.json()
    data = data["data"]
    # print(data)
    # print(data)
    # print(data["disable_text"])
    if(len(data["tags"]) > 0 and  data["tags"][0]["value"] in ["Bitcoin"] and "disable_text" in data and data["disable_text"] != "Result Awaited"):
        event_name = data["tags"][0]["value"]
        if event_name == "Bitcoin":
            target_price = float(data["name"].split()[5])
            start_time = convert_to_IST(data["start_date"])
            end_time = convert_to_IST(data["end_date"])
            settled_as = data["disable_text"].split()[2]
            event_details = [start_time, end_time, target_price, settled_as]
            
            return event_details
    return None





def makeTradeNewEvent():
    pastEvents = getAllEvents()
    while True:
        currEvents = getAllEvents()
        for eventID in currEvents:
            if eventID not in pastEvents:
                event = Probo(eventID)
                if event.target_price <= getBitcoinPrice():
                    # order_id = event.buy_yes(1,5)
                    time.sleep(1)
                    # event.exit_order(order_id,5.5)
                    print("Yes order placed")
                else:
                    # order_id = event.buy_no(1,5)
                    time.sleep(1)
                    # event.exit_order(order_id,5.5)
                    print("No order placed")
                pastEvents = currEvents
                return event
        time.sleep(0.5)
        


def save_prev_event():
    prev_events = getAllEvents()
    while True:
        curr_events = getAllEvents()
        for event_id in prev_events:
            if event_id not in curr_events:
                data = get_event_data(event_id)
                if data:
                    prev_events = curr_events
                    print(data)
                    return data
        time.sleep(0.5)

def extract_features_from_last_events(current_event_start_time, curr_target_price, event_data):
    # Filter events up to the current event start time
    past_events = event_data[event_data['start_time'] < current_event_start_time]
    
    if len(past_events) < 3:
        return None  # Not enough past events to extract features
    
    # Get the last 3 events
    last_3_events = past_events.tail(3)
    
    # Extract features
    features = {}
    for i, (idx, event) in enumerate(last_3_events.iterrows()):
        features[f'event_{i+1}_outcome'] = 1 if event['settled_as'] == 'Yes' else 0
        # Target price deviation
        features[f'target_{i+1}_price_deviation'] = (event["bitcoin_price"] - event['target_price']) 
    
    bitcoin_price = getBitcoinPrice()

    features['target_price_deviation'] = (bitcoin_price - curr_target_price) 

    return features

past_events = []
def execute_model_strategy():
    event_data = load_event_data()

    data = save_prev_event()
    print("Got prev data")
    data.append(past_events[-1].curr_price)
    last_event_data = {
        'start_time': [pd.to_datetime(data[0])],
        'end_time': [pd.to_datetime(data[1])],
        'target_price': [data[2]],
        'settled_as': [1 if data[3] == 'Yes' else 0],
        'bitcoin_price': [past_events[-1].curr_price]
    }
    last_event_df = pd.DataFrame(last_event_data)

    # Combine historical event data with the last event data
    combined_event_data = pd.concat([event_data, last_event_df], ignore_index=True)

    # Extract features for the last event
    current_event_start_time = pd.to_datetime(data[0])
    features = extract_features_from_last_events(current_event_start_time, event, combined_event_data)


    event = makeTradeNewEvent()
    past_events.append(event)

    print("Executed the event data script")
    with open('traded_data.csv', 'a') as csvfile:
        writer_object = csv.writer(csvfile)
        writer_object.writerow(data)
        csvfile.close()

if __name__ == '__main__':
    getAllEvents()
    # while True:
    #     traded = 0
    #     while True:
    #         if (datetime.now().minute+1)%5 == 0 and datetime.now().second == 58:
    #             execute_model_strategy()
    #             traded = 1
    #         if traded:
    #             print("Trade completed successfully")
    #             break
    #         time.sleep(1)
    #     time.sleep(295)
        
    # makeTradeNewEvent()

