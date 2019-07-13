from strategies.stats import *


def trade(exchange):
    trades = []
    try:
        ori_newest = exchange.t_now["VALBZ"][-10:]
        adr_newest = exchange.t_now["VALE"][-10:]
    except:
        return []


    ori_estimate = EMA(ori_newest)
    adr_estimate = EMA(adr_newest)

    if exchange.counter % 100 != 0:
        return []

    diff = adr_estimate - ori_estimate
    if diff > 0:
        size = min(int((diff / 0.1) * 2), 5)
        trades.append(("BUY", "VALBZ", int(ori_estimate + 1), size))
        trades.append(("CONVERT", "BUY", "VALE", size))
        trades.append(("SELL", "VALE", int(adr_estimate - 1), size))
    elif diff < 0:
        size = min(int((-diff / 0.1) * 2), 5)
        trades.append(("SELL", "VALBZ", int(ori_estimate + 1), size))
        trades.append(("CONVERT", "SELL", "VALE", size))
        trades.append(("BUY", "VALE", int(adr_estimate - 1), size))
    return trades
