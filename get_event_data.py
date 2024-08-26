import requests
from datetime import datetime
import pytz
import json
import time
import csv
events_data = []


def convert_to_IST(utc_time):
    utc_time = datetime.strptime(utc_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    utc_zone = pytz.utc
    ist_zone = pytz.timezone('Asia/Kolkata')
    utc_time = utc_zone.localize(utc_time)
    ist_time = utc_time.astimezone(ist_zone)
    ist_time_str = ist_time.strftime('%Y-%m-%dT%H:%M:%S%z')

    return ist_time_str


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
        for event_id in range(2899424, 2918353, 1):
            # print(event_id)
            data = requests.get(
                f"https://prod.api.probo.in/api/v1/product/events/{event_id}",
                headers=headers,
            )
            data = data.json()
            data = data["data"]
            # print(data)
            # print(data)
            # print(data["disable_text"])
            if(len(data["tags"]) > 0 and  data["tags"][0]["value"] in ["Bitcoin", "Youtube"] and "disable_text" in data and data["disable_text"] != "Result Awaited") and len(data["disable_text"].split()) == 3:
                event_name = data["tags"][0]["value"]
                if event_name == "Bitcoin":
                    target_price = float(data["name"].split()[5])
                    start_time = convert_to_IST(data["start_date"])
                    end_time = convert_to_IST(data["end_date"])
                    settled_as = data["disable_text"].split()[2]
                    event_details = [start_time, end_time, target_price, settled_as]
                    with open('bitcoin_data.csv', 'a') as csvfile:

                        writer_object = csv.writer(csvfile)


                        writer_object.writerow(event_details)

                        csvfile.close()
                    with open('bitcoin_event_ids.csv', 'a') as csvfile:

                        writer_object = csv.writer(csvfile)

                        writer_object.writerow([event_id])

                        csvfile.close()
                    print(event_id)
                elif (event_name == "Youtube" and data["disable_text"] != "Result Awaited"):
                    target_views = data["name"].split()[-5]
                    video_name = data["name"].split("\'")[1]
                    start_time = convert_to_IST(data["start_date"])
                    end_time = convert_to_IST(data["end_date"])
                    settled_as = data["disable_text"].split()[2]
                    event_details = [start_time, end_time, target_views, settled_as, video_name]
                    with open('youtube_data.csv', 'a') as csvfile:

                        writer_object = csv.writer(csvfile)

                        writer_object.writerow(event_details)
                        csvfile.close()
                    with open('youtube_event_ids.csv', 'a') as csvfile:

                        writer_object = csv.writer(csvfile)

                        writer_object.writerow([event_id])

                        csvfile.close()
                    print(event_id)

    
                    



    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    
getEventsData(2764594)
# 2753000 - 2836646
# 2836646 - 2839514
# 2839514 - 2844611
# 2844611 - 2850750
# 2850750 - 2918352