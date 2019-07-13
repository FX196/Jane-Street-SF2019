from ..stats import *


def trade(exchange):
    trades = []
    ori_newest = exchange.t_now["VALBZ"][-10:]
    adr_newest = exchange.t_now["VALE"][-10:]

    ori_estimate = EMA(ori_newest)
    adr_estimate = EMA(adr_newest)

    diff = adr_estimate - ori_estimate
    if diff > 0:
        size = (diff / 0.1) * 2
        trades.append(("BUY", "VALBZ", ori_estimate + 1, size))
        trades.append(("CONVERT", "BUY", "VALE", size))
        trades.append(("SELL", "VALE", adr_estimate - 1, size))
    elif diff < 0:
        size = (diff / 0.1) * 2
        trades.append(("SELL", "VALBZ", ori_estimate + 1, size))
        trades.append(("CONVERT", "SELL", "VALE", size))
        trades.append(("BUY", "VALE", adr_estimate - 1, size))
    return trades