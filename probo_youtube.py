import requests
import time


def getViews():
    youtubeBroadcastId = "6GxXehkPyBs"
    youtubeAccessToken = "AIzaSyA5agtIvha5x2gEMiuo-TkFpZ8msaUBkB4"
    data = requests.get(
        f"https://youtube.googleapis.com/youtube/v3/videos?part=statistics%2C%20status&id={youtubeBroadcastId}&key=AIzaSyA5agtIvha5x2gEMiuo-TkFpZ8msaUBkB4",
        {
            "headers": {
                "Content-Type": "application/json",
            },
        },
    )
    data = data.json()
    # print(data)
    views = data["items"][0]["statistics"]["viewCount"]
    print(views)


while True:
    getViews()
    time.sleep(1)


def getAllEvents():
    headers = {
        "accept": "*/*",
        "accept-language": "en",
        "appid": "in.probo.pro",
        "authorization": "Bearer E62wjcYhBaP+6jF1sjXeA55QEp/HbkgjfVMzRupq0AE=",
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
    body = {
        "categoryIds": [],
        "topicIds": [452],
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
        events = data["data"]["records"]["events"]
        event_ids = [i["id"] for i in events]
        print(event_ids)
    except:
        print("Error")

# getAllEvents()
