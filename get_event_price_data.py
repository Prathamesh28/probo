
import pandas as pd
import os
import requests
from datetime import datetime
import pytz
import json
import time
import csv
events_data = []



def process_api_response(response, event_id):
    data = response['Data']
    df = pd.DataFrame(data)
    df['event_id'] = event_id
    df['time'] = pd.to_datetime(df['time'], unit='ms').dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
    return df

def save_to_parquet(dfs, filename):
    if os.path.exists(filename):
        existing_df = pd.read_parquet(filename)
        combined_df = pd.concat([existing_df] + dfs, ignore_index=True)
    else:
        combined_df = pd.concat(dfs, ignore_index=True)
    
    combined_df.to_parquet(filename, index=False)
    print(f"Data saved to {filename}")


def getEventsData(curr_event_id):
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
    try:
        bitcoin_data = []
        youtube_data = []
        event_ids = pd.read_csv("bitcoin_event_ids.csv").to_numpy().flatten()
        for event_id in event_ids:
            data = requests.get(
                f"https://prod.api.probo.in/api/v1/tms/trade/eventGraphData?eventId={event_id}",
                headers=headers,
            )
            data = data.json()
            data = data["data"]
            # print(data)
            # print(data)
            # print(data["disable_text"])
            # if(len(data["tags"]) > 0 and  data["tags"][0]["value"] in ["Bitcoin","Youtube"] and "disable_text" in data and data["disable_text"] != "Result Awaited") and len(data["disable_text"].split()) == 3:
            # event_name = data["tags"][0]["value"]
            # if event_name == "Bitcoin":
            df = process_api_response(data, event_id)
            bitcoin_data.append(df)
            
            # Save all the data to a Parquet file
                # with open('bitcoin_event_ids.csv', 'a') as csvfile:

                #     writer_object = csv.writer(csvfile)

                #     writer_object.writerow([event_id])

                #     csvfile.close()
                # print(event_id)
                # elif (event_name == "Youtube" and data["disable_text"] != "Result Awaited"):
                    # df = process_api_response(data, event_id)
                    # bitcoin_data.append(df)
                
                    # with open('youtube_event_ids.csv', 'a') as csvfile:

                    #     writer_object = csv.writer(csvfile)

                    #     writer_object.writerow([event_id])

                    #     csvfile.close()
                    # print(event_id)
        save_to_parquet(bitcoin_data, 'bitcoin_events_price.parquet')
        # save_to_parquet(youtube_data, 'youtube_events_price.parquet')



    
                    



    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    
getEventsData(2764594)
# 2809521 - 2824591

