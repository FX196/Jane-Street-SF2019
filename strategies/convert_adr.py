from strategies.stats import *


def trade(exchange):
    trades = []
    try:
        ori_buy, ori_sell = exchange.latest_books["VALE"]
        adr_buy, adr_sell = exchange.latest_books["VALBZ"]
    except:
        return []

    ori_estimate = fair_price_estimate(ori_buy, ori_sell)
    adr_estimate = fair_price_estimate(adr_buy, adr_sell)

    if not ori_estimate or not adr_estimate:
        return []

    if exchange.counter % 100 != 0:
        return []

    diff = adr_estimate - ori_estimate
    if diff > 10:
        size = 1
        trades.append(("BUY", "VALBZ", int(EMA(exchange.trade_prices["VALBZ"])), size))
        trades.append(("CONVERT", "BUY", "VALE", size))
        trades.append(("SELL", "VALE", int(EMA(exchange.trade_prices["VALE"])), size + exchange.holdings["VALE"]))
    elif diff < 10:
        size = 1
        trades.append(("SELL", "VALBZ", int(EMA(exchange.trade_prices["VALBZ"])), size + exchange.holdings["VALBZ"]))
        trades.append(("CONVERT", "SELL", "VALE", size))
        trades.append(("BUY", "VALE", int(EMA(exchange.trade_prices["VALE"])), size))
    return trades


def fair_price_estimate(buy, sell):
    buy = np.array(buy)
    sell = np.array(sell)
    if not weighted_mean(buy) or not weighted_mean(sell):
        return None
    return (weighted_mean(buy) + weighted_mean(sell)) / 2


def weighted_mean(a):
    if a is None:
        return None
    try:
        return np.sum((a[:, 0] * a[:, 1]) / np.sum(a[:, 1]))
    except:
        print("Handling None")
        return None
