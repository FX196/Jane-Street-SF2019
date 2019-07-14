def trade(exchange):
    trades = []
    ori_buy, ori_sell = exchange.latest_books["VALBZ"]
    adr_buy, adr_sell = exchange.latest_books["VALE"]

    try:
        b_adr = max(adr_buy, key=lambda x: x[0])[0]
        s_adr = min(adr_sell, key=lambda x: x[0])[0]

        b_ori = max(ori_buy, key=lambda x: x[0])[0]
        s_ori = min(ori_sell, key=lambda x: x[0])[0]
    except:
        print("Handling None")
        return []

    if s_adr - b_ori > 10:
        size = 1
        trades.append(("BUY", "VALBZ", b_ori, size))
        trades.append(("CONVERT", "BUY", "VALE", size))
        trades.append(("SELL", "VALE", s_adr, size + exchange.holdings["VALE"]))
    elif s_ori - b_adr > 10:
        size = 1
        trades.append(("SELL", "VALBZ", s_ori, size + exchange.holdings["VALBZ"]))
        trades.append(("CONVERT", "SELL", "VALE", size))
        trades.append(("BUY", "VALE", b_adr, size))

    return trades
