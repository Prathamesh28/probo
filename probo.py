import requests
import time
from datetime import datetime
import pytz

def convert_to_IST(utc_time):
    utc_time = datetime.strptime(utc_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    utc_zone = pytz.utc
    ist_zone = pytz.timezone('Asia/Kolkata')
    utc_time = utc_zone.localize(utc_time)
    ist_time = utc_time.astimezone(ist_zone)
    ist_time_str = ist_time.strftime('%Y-%m-%dT%H:%M:%S%z')

    return ist_time_str

key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"


def getBitcoinPrice():
    data = requests.get(key)
    data = data.json()
    print(f"{data['symbol']} price is {data['price']}")
    return float(data['price'])

class Probo:
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

    def __init__(self, eventID):
        self.orderIds = {}
        self.eventID = eventID
        self.target_price = self.getTargetPrice(eventID)
        self.curr_price = getBitcoinPrice()

    def getTargetPrice(self, event_id):
        data = requests.get(
            f"https://prod.api.probo.in/api/v1/product/events/{event_id}",
            headers=self.headers,
        )
        data = data.json()
        data = data["data"]
        target_price = float(data["name"].split()[5])
        start_time = convert_to_IST(data["start_date"])
        end_time = convert_to_IST(data["end_date"])

        return target_price
        
    def buy_yes(self, quantity, price):
        body = {
            "event_id": self.eventID,
            "offer_type": "buy",
            "order_type": "LO",
            "l1_order_quantity": quantity,
            "l1_expected_price": price,
        }
        data = requests.post(
            "https://prod.api.probo.in/api/v1/oms/order/initiate",
            headers=self.headers,
            json=body,
        )
        data = data.json()
        order_id = data["data"]["id"]
        print(
            f"Order ID : {order_id} , YES order placed for {self.eventID} of {quantity} unit at price {price}"
        )
        self.orderIds[order_id] = {"price": price, "quantity": quantity}
        return order_id

    def buy_no(self, quantity, price):
        body = {
            "event_id": self.eventID,
            "offer_type": "sell",
            "order_type": "LO",
            "l1_order_quantity": quantity,
            "l1_expected_price": price,
        }
        data = requests.post(
            "https://prod.api.probo.in/api/v1/oms/order/initiate",
            headers=self.headers,
            json=body,
        )

        data = data.json()
        order_id = data["data"]["id"]
        print(
            f"Order ID : {order_id} , NO order placed for {self.eventID} of {quantity} unit at price {price}"
        )
        self.orderIds[order_id] = {"price": price, "quantity": quantity}

        return order_id

    def exit_order(self, orderID, exitPrice):
        body = {"exit_params": [{"exit_price": exitPrice, "order_id": orderID}]}

        data = requests.post(
            "https://prod.api.probo.in/api/v2/oms/order/exit",
            headers=self.headers,
            json=body,
        )
        data = data.json()

        print(
            f"Exited Order ID {orderID}  at price {exitPrice} with profit of {(exitPrice - self.orderIds[orderID]['price'])*self.orderIds[orderID]['quantity']}"
        )
        print(data)
        del self.orderIds[orderID]

    def cancel_order(self, orderID):
        data = requests.put(
            f"https://prod.api.probo.in/api/v1/oms/order/cancel/{orderID}?eventId={self.eventID}",
            headers=self.headers,
            json={},
        )
        print(f"Canceled Order ID {orderID} of event ID {self.eventID}")
        del self.orderIds[orderID]

    def getBestPrice(self, buy):
        data = requests.get(
            f"https://prod.api.probo.in/api/v3/tms/trade/bestAvailablePrice?eventId={self.eventID}&requestType=availableQuantities",
            headers=self.headers,
        )
        data = data.json()
        buy_prices = data["data"]["available_qty"]["buy"]
        sell_prices = data["data"]["available_qty"]["sell"]
        i = 0.5
        best_buy_price = 10
        best_sell_price = 10
        while i < 10:
            if buy_prices[str(i)] > 0:
                best_buy_price = min(best_buy_price, i)

            if sell_prices[str(i)] > 0:
                best_sell_price = min(best_sell_price, i)
            i += 0.5
        # buy_prices = buy_prices.values()
        # print(f"YES price : {buy_prices} | NO Price : {sell_prices}")
        print(f"YES price : {best_buy_price} | NO Price : {best_sell_price}")
        if buy:
            return best_buy_price
        return best_sell_price


