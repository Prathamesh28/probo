import csv
from datetime import datetime
import json
import pandas as pd
import pytz
import requests
import time
from probo import Probo
import numpy as np
import pickle

# defining key/request url
key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
model_filename = 'grid_search_gradient_boosting_classifier.pkl'

with open(model_filename, 'rb') as file:
    loaded_model = pickle.load(file)


# requesting data from url
# prev = 26857.61
# while True:
def getBitcoinPrice():
    data = requests.get(key)
    data = data.json()
    print(f"{data['symbol']} price is {data['price']}")

    return float(data['price'])


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





def makeTradeNewEvent(bitcoin_prices):
    pastEvents = getAllEvents()
    eventID = sorted(pastEvents)[1]
    # while True:
    #     currEvents = getAllEvents()
    #     for eventID in currEvents:
    #         if eventID not in pastEvents:
    event = Probo(eventID)
    X = np.array(bitcoin_prices)
    X = X - event.target_price
    X = X.reshape(1,2)
    print(X)

    # Use the loaded model to make predictions

    y_proba = loaded_model.predict_proba(X)

    threshold = 0.55
    print(y_proba)
    if y_proba[0][0] >= threshold or y_proba[0][1] >= threshold:
        prediction = 1 if y_proba[0][1] >= 0.5 else 0
        print(prediction)
        if prediction == 1:
            # order_id = event.buy_yes(1,5)
            # time.sleep(1)
            # event.exit_order(order_id,5.5)
            print("Yes order placed")
        else:
            # order_id = event.buy_no(1,5)
            # time.sleep(1)
            # event.exit_order(order_id,5.5)
            print("No order placed")
        # pastEvents = currEvents
        return {"prediction" : prediction, "price" : event.getBestPrice(prediction)}
    else:
        return None
        # time.sleep(0.5)
        


def save_prev_event(prev_events):
    while True:
        curr_events = getAllEvents()
        for event_id in prev_events:
            if event_id not in curr_events:
                data = get_event_data(event_id)
                if data:
                    prev_events = curr_events
                    print(data)
                    return data, prev_events
        time.sleep(0.5)

past_events = []

def execute_model_strategy(previous_event):
    curr_btc_price = getBitcoinPrice()
    bitcoin_prices = [curr_btc_price]
    data, prev_events = save_prev_event(previous_event)
    global score, max_loss, max_profit
    print("Got prev data")
    print(data)
    # if previous_value == data[3]:
    #     score = score + 4
    # else:
    #     score = score - 5
    if len(past_events) > 1 and past_events[-2] != None:
        previous_value = 1 if data[3] == "Yes" else 0
        if past_events[-2]["prediction"]  == previous_value:
            score = score + (10 - past_events[-2]["price"])*0.8
        else:
            score = score - past_events[-2]["price"]

    max_profit = max(max_profit, score)
    max_loss = min(max_loss, score)


    print("Executed the event data script")
    with open('traded_data.csv', 'a') as csvfile:
        writer_object = csv.writer(csvfile)
        writer_object.writerow(data)
        csvfile.close()

    while True:
        if (datetime.now().minute)%5 == 0 and datetime.now().second == 59 :
            curr_btc_price = getBitcoinPrice()
            bitcoin_prices.append(curr_btc_price)

            event = makeTradeNewEvent(bitcoin_prices)
            past_events.append(event)
            break
        time.sleep(0.5)


if __name__ == '__main__':
    # Initialize the score
    score = 0
    max_profit = 0
    max_loss = 0
    # Apply the strategy
    previous_value = "Yes"

    # es = getAllEvents()
    # e = Probo(es[1])
    # print(e.getBestPrice(0))

    # bitcoin_prices = [2837,63492.00000000]
    while True:
        traded = 0
        # while True:
        #     if datetime.now().second == 0:
        #         curr_btc_price = getBitcoinPrice()
        #         bitcoin_prices.append(curr_btc_price)
        #         if (datetime.now().minute+1)%5 == 0:
        #             break
        #         else:
        #             time.sleep(58)

        while True:
            if (datetime.now().minute+1)%5 == 0 and datetime.now().second == 57 :
                previous_event = getAllEvents()
                execute_model_strategy(previous_event)

                print(f"The final score for the date {datetime.now()} is: {score}. Max Profit : {max_profit}, Max Loss : {max_loss}")
                traded = 1
            if traded:
                print("Trade completed successfully")
                break
            time.sleep(0.5)
        

                        
    # makeTradeNewEvent()

