import json
import socket


class ExchangeConnection:
    def __init__(self, exchange, team_name='ALPHASTOCK'):
        if exchange in ("0", "1", "2"):
            host_name = "test-exch-alphastock"
            port = 25000 + int(exchange)

        else:
            host_name = "production"
            port = 25000

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host_name, port))
        self.stream = s.makefile('rw', 1)

        self.write({"type": "hello", "team": team_name})
        hello = self.read()
        assert hello['type'] == 'hello'
        self.holdings = {}
        for symbol_position_pair in hello["symbols"]:
            self.holdings[symbol_position_pair["symbol"]] = symbol_position_pair["position"]

        self.last_data = None

        self.filled_orders = []
        self.current_orders = []
        self.sent_orders = {}

        self.order_id = 0
        self.latest_books = {
            "BOND": [None, None],
            "VALBZ": [None, None],
            "VALE": [None, None],
            "GS": [None, None],
            "MS": [None, None],
            "WFC": [None, None],
            "XLF": [None, None]
        }
        self.time = 0

    def read(self, store_last=True):  # read from exchange
        data_str = self.stream.readline()
        if data_str == "":
            return None
        else:
            data = json.loads(data_str)
            if store_last:
                self.last_data = data
                msg_type = data["type"]
                if msg_type == "book":
                    self.latest_books[data["symbol"]] = [data["buy"], data["sell"]]
                elif msg_type == "ack":
                    # accepted, add to current_orders
                    order_id = data["order_id"]
                    self.current_orders.append(self.sent_orders.pop(order_id))
                elif msg_type == "fill":
                    for order in self.current_orders:
                        pass
        return data

        # else:
        #     data = json.loads(data)
        #     if store_last:
        #         self.last_data = data
        #         if data["type"] == "book":
        #             #self.latest_books[data["symbol"]][0] = data
        #             self.latest_books[data["symbol"]] = data, self.latest_books[data["symbol"]][0]
        #         if data['type'] == "fill":
        #             self.filled_orders.append(data)
        #             if data['dir'] == "BUY":
        #                 self.holdings[data["symbol"]] += data["size"]
        #                 self.holdings["USD"] -= int(data["price"]) * int(data['size'])
        #             elif data['dir'] == "SELL":
        #                 self.holdings[data["symbol"]] -= data["size"]
        #                 self.holdings["USD"] += int(data["price"]) * int(data['size'])
        #             print(self.holdings)
        #             print("Order", data["order_id"], "filled:", data["dir"], data["size"], data["symbol"], "at price",
        #                   data["price"])
        #             print("Current order id", self.order_id)
        #     return data

    def write(self, data):  # write to exchange
        json.dump(data, self.stream)
        self.stream.write("\n")

    def trade(self, *args):
        if args[0] != "CONVERT":
            buysell, symbol, price, size = args
            trade = {'type': 'add', 'order_id': self.order_id, 'symbol': symbol,
                     'dir': buysell, 'price': price, 'size': size}
            self.sent_orders[self.order_id] = (self.order_id, buysell, symbol, price, size)
            self.order_id += 1
            # print(trade)
            self.write(trade)
        else:
            self.convert(*args[1:])

    def cancel(self, order_id):
        cancel = {'type': 'cancel', 'order_id': order_id}
        self.write(cancel)

    def trade_batch(self, trades):
        for buysell, symbol, price, size in trades:
            if buysell and size != 0:
                self.trade(buysell, symbol, price, size)
        if self.order_id % 10 == 0:
            print(self.current_orders)

    def convert(self, buysell, symbol, size):
        trade = {'type': 'convert', 'order_id': self.order_id,
                 'symbol': symbol, 'dir': buysell, 'size': size}
        self.order_id += 1
        # print(trade)
        self.write(trade)
