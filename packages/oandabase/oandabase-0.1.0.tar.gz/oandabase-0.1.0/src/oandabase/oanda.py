
import requests
import json
from decouple import config
import logging
# create logger
logger = logging.getLogger()
# set minimum output level
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
# set minimum output level
ch.setLevel(logging.INFO)
# create formatter
formatter = logging.Formatter('[%(levelname)s] -'
                              ' %(asctime)s - '
                              '%(name)s : %(message)s')
# add formatter
ch.setFormatter(formatter)
# add a handler to logger
logger.addHandler(ch)


class Oanda(object):
    """Sets up access to an Oanda account and the market data stream for the chosen
     asset e.g. currency pair or commodity.

        Args:
            token (str, required):
                The Oanda API token. Defaults to env variables.
            account (str, required):
                The Oanda account number. Defaults to env variables.
            practice (bool, required):
                Use the Oanda practice stream or go live with real money.
                 Defaults to True. pair (str, required):
                Which asset to trade. Defaults to 'EUR_USD'.
        """

    def __init__(self, token=config('PRACTICE_TOKEN'),
                 account=config('PRACTICE_ACCOUNT'),
                 practice=True, pair='EUR_USD',
                 **kwargs):

        super().__init__(**kwargs)
        self.logger = logging.getLogger(__name__)
        self.token = token
        self.account = account
        self.practice = practice
        self.pair = pair
        self.base_url = self.set_base_url()
        self.headers = self.set_headers()

    def set_base_url(self):
        if self.practice:
            return 'https://api-fxpractice.oanda.com'
        else:
            return 'https://stream-fxtrade.oanda.com'

    def set_headers(self):
        return {'Authorization': 'Bearer ' + self.token}


class Account(Oanda):
    """Gets the current account status and attributes.
    Subclass of Oanda.
    """
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.get_account()
        self.get_account_properties()

    def get_account_properties(self):
        """Unpack the data returned by get_account"""
        self.account_currency = self.account_info['account']['currency']
        self.balance = self.account_info['account']['balance']
        self.marginRate = self.account_info['account']['marginRate']
        self.marginAvailable = self.account_info['account']['marginAvailable']
        self.trades = self.account_info['account']['trades']
        self.unrealizedPL = self.account_info['account']['unrealizedPL']
        self.NAV = self.account_info['account']['NAV']
        self.marginUsed = self.account_info['account']['marginUsed']
        self.marginAvailable = self.account_info['account']['marginAvailable']
        self.positionValue = self.account_info['account']['positionValue']

        self.marginCloseoutPercent =\
            self.account_info['account']['marginCloseoutPercent']

        self.openTradeCount = self.account_info['account']['openTradeCount']

        self.openPositionCount =\
            self.account_info['account']['openPositionCount']

        self.pendingOrderCount =\
            self.account_info['account']['pendingOrderCount']

        self.pl = self.account_info['account']['pl']
        self.orders = self.account_info['account']['orders']

    def set_account_properties(self):
        """Used to refresh the account properties"""
        self.get_account()
        self.get_account_properties()

    def get_account(self):
        try:
            url = self.base_url + '/v3/accounts/' + self.account
            r = requests.get(url, headers=self.headers)
            data = r.json()

            if data:
                self.logger.info("Account connected ok!")
                self.account_info = data
            else:
                self.logger.exception("OANDA API ERROR - Account.get_account -"
                                      " failed to retrieve data")
        except Exception:
            self.logger.exception("OANDA API ERROR - Account.get_account -"
                                  "failed to retrieve data")


class Order(Account):
    """A class to hold details of current open positions, place orders,
    check current orders and to notify the user when orders are placed
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.order = None
        self.get_open_positions()
        self.get_open_trades()

    def get_open_positions(self):
        try:
            url = self.base_url + '/v3/accounts/' + self.account +\
                 '/openPositions'
            r = requests.get(url, headers=self.headers)
            data = r.json()
            self.open_positions = data
        except Exception:
            self.logger.exception("OANDA API ERROR - Order.get_open_positions"
                                  " failed to get any data")

    def get_open_trades(self):
        try:
            url = self.base_url + '/v3/accounts/' +\
                 self.account + '/openTrades'
            r = requests.get(url, headers=self.headers)
            data = r.json()
            self.open_trades = data
        except Exception:
            self.logger.exception("OANDA API ERROR - Order.get_open_trades"
                                  " failed to get any data")

    def find_matching_trades(self):
        # TODO add args instrument
        new_list = []
        for item in self.open_trades['trades']:
            if item['instrument'] == self.pair:
                new_list.append(item)
        return sorted(new_list, key=lambda i: i['id'])

    def get_orders(self):
        try:
            url = self.base_url + '/v3/accounts/' + self.account + '/orders'
            r = requests.get(url, headers=self.headers)
            data = r.json()
            return data
        except Exception:
            self.logger.exception("OANDA DATA ERROR - Order.get_orders"
                                  " failed to return any orders")

    def get_pending_orders(self):
        try:
            url = self.base_url + '/v3/accounts/' + self.account +\
                 '/pendingOrders'
            r = requests.get(url, headers=self.headers)
            data = r.json()
            return data
        except Exception:
            self.logger.exception("OANDA DATA ERROR - Order.get_pending_orders"
                                  " failed to return any pending orders")

    def buy_market(self, units, instrument):
        try:
            url = self.base_url + '/v3/accounts/' + self.account + '/orders'
            data = {
                "order": {
                    "units": units,
                    "instrument": instrument,
                    "timeInForce": "FOK",
                    "type": "MARKET",
                    "positionFill": "DEFAULT"
                }
            }
            r = requests.post(url, headers=self.headers, json=data)
            self.notify_order(r.json())
        except Exception:
            self.logger.exception("OANDA DATA ERROR - Order.buy_market"
                                  " failed to send the order")

    def sell_market(self, units, instrument):
        try:
            url = self.base_url + '/v3/accounts/' + self.account + '/orders'
            data = {
                "order": {
                    "units": -units,
                    "instrument": instrument,
                    "timeInForce": "FOK",
                    "type": "MARKET",
                    "positionFill": "DEFAULT"
                }
            }
            r = requests.post(url, headers=self.headers, json=data)
            self.notify_order(r.json())
        except Exception:
            self.logger.exception("OANDA DATA ERROR - Order.sell_market"
                                  " failed to send the order")

    def notify_order(self, order):
        self.order = order
        if 'orderCancelTransaction' in self.order:
            print('Order Transaction Canceled:')
            msg = (f"{order['orderCancelTransaction']['type']},"
                   f"{order['orderCancelTransaction']['reason']}")
            print(msg)
            self.logger.exception(f"OANDA ORDER ERROR - {msg}")

        print('\n')
        if 'orderFillTransaction' in self.order:
            time = order["orderFillTransaction"]["time"]
            orderID = order["orderFillTransaction"]["orderID"]
            instrument = order["orderFillTransaction"]["instrument"]
            units = order["orderFillTransaction"]["units"]
            price = order["orderFillTransaction"]["price"]
            reason = order["orderFillTransaction"]["reason"]
            pl = order["orderFillTransaction"]["pl"]
            msg = (f"*** ORDER FULFILLED ***\n"
                   f"Time: {time}\n"
                   f"Type: {reason}\n"
                   f"Order Id: {orderID}\nInstrument: {instrument}\n"
                   f"Units: {units}\n"
                   f"Price: {price}\n"
                   f"P/L: ${pl}")
            self.logger.warning(f"OANDA ORDER SUCCESSFUL - {msg}")

    def close_trade(self, order_id):
        try:
            url = self.base_url + '/v3/accounts/' + self.account +\
                 '/trades/' + order_id + '/close'
            r = requests.put(url, headers=self.headers)
            self.notify_order(r.json())
        except Exception:
            self.logger.exception("OANDA DATA ERROR - Order.close_trade"
                                  " failed to send the order")


class DataFeed(Order):
    """Handles the streaming data from Oanda

    Args:
        backfill (bool, optional):
            Get the last 500 candles?. Defaults to True.
    """

    def __init__(self, backfill=True, **kwargs):
        super().__init__(**kwargs)
        self.backfill = backfill
        self.data0 = self.set_init_data0()
        self.stream_url = self.set_stream_url()

    def set_init_data0(self):
        try:
            # TODO allow the setting of different params
            params = {'granularity': 'M1', 'count': 1, 'price': 'BA'}
            if self.backfill:
                params['count'] = 500
            url = self.base_url + '/v3/instruments/' + self.pair + '/candles?'
            r = requests.get(url, headers=self.headers, params=params)
            data = r.json()
            bars = data['candles'][::-1]
            return bars
        except Exception:
            self.logger.exception("OANDA DATA ERROR - "
                                  "Datastream.set_init_data0 -"
                                  " did not get any data")

    def rebuild_data(self, latest_bar):
        latest_bar_time = latest_bar['time']
        last_bar_time = self.data0[0]['time']
        if latest_bar_time != last_bar_time:
            self.data0.insert(0, latest_bar)
            if len(self.data0) > 500:  # Only keeps the last 500 bars in memory
                self.data0.pop()

    def refresh_data(self):
        try:
            url = self.base_url + '/v3/instruments/' + self.pair +\
                 '/candles?count=1&price=BA'
            # TODO allow the setting of different params
            params = {'granularity': 'M1'}
            r = requests.get(url, headers=self.headers, params=params)
            data = r.json()
            latest_bar = data['candles'][::-1][0]
            self.rebuild_data(latest_bar)
            self.get_open_trades()
        except Exception:
            self.logger.exception("OANDA DATA ERROR - "
                                  "Datastream.refresh_data - "
                                  "did not get any data")

    def set_stream_url(self):
        """Set the stream url based on use of
         the practice or live stream account
         """
        if self.practice:
            return ('https://stream-fxpractice.oanda.com/v3/accounts/' +
                    self.account + "/pricing/stream")
        else:
            return ('https://stream-fxtrade.oanda.com/v3/accounts/' +
                    self.account + "/pricing/stream")

    def connect_to_stream(self):
        """
        Gets the stream response
        """
        try:
            s = requests.Session()
            params = {'instruments': self.pair}
            req = requests.Request('GET', self.stream_url,
                                   headers=self.headers, params=params)
            pre = req.prepare()
            resp = s.send(pre, stream=True, verify=True)
            return resp
        except Exception:
            self.logger.exception('Failed to connect to stream')

    def stream(self, console_output=True):
        """Handles the full stream json e.g.
            {"type":"PRICE",
            "time":"2021-05-13T22:00:43.020656828Z",
            "bids":[{"price":"1.20804","liquidity":10000000}],
            "asks":[{"price":"1.20828","liquidity":10000000}],
            "closeoutBid":"1.20804","closeoutAsk":"1.20828",
            "status":"tradeable",
            "tradeable":true,
            "instrument":"EUR_USD"}
        """
        response = self.connect_to_stream()
        print(response.status_code)
        if response.status_code != 200:
            self.logger.debug("Bid stream bad response status {}"
                              .format(response.status))
        else:
            self.logger.debug("Stream connected OK")
        lines = response.iter_lines()
        next(lines)
        for line in lines:
            line = line.decode('utf-8')
            msg = json.loads(line)

            if "instrument" in msg or "tick" in msg:
                self.full_stream = msg
                if console_output:
                    print('\n' + line)

    def bid_stream(self, console_output=True):
        """Extracts the current bid price from the connected stream
        Updates instance.bid as a float value, which can then be used by
        trading bots to monitor price
        """
        response = self.connect_to_stream()
        # print(response.status_code)
        if response.status_code != 200:
            self.logger.debug("Bid stream bad response status {}"
                              .format(response.status))

        lines = response.iter_lines()

        next(lines)
        for line in lines:
            line = line.decode('utf-8')
            msg = json.loads(line)
            if 'bids' in msg:
                self.bid = float(msg['bids'][0]['price'])
                if console_output:
                    print(self.bid)

    def ask_stream(self, console_output=True):
        """Extracts the current ask price from the connected stream
        Updates instance.ask as a float value, which can then be used by
        trading bots to monitor price
        """
        response = self.connect_to_stream()
        # print(response.status_code)
        if response.status_code != 200:
            self.logger.debug("Bid stream bad response status {}"
                              .format(response.status))
        lines = response.iter_lines()
        next(lines)
        for line in lines:
            line = line.decode('utf-8')
            msg = json.loads(line)
            if 'asks' in msg:
                self.ask = float(msg['asks'][0]['price'])
                if console_output:
                    print(self.ask)


if __name__ == "__main__":

    feed = DataFeed()
