import numpy as np
def trade(exchange):
    trades=[]
    bond = exchange.t_now["BOND"]
    gs = exchange.t_now["GS"]
    ms = exchange.t_now["MS"]
    wfc = exchange.t_now["WFC"]
    xlf = exchange.t_now["XLF"][-1]
    if len(bond)<6 or len(gs)<6 or len(ms)<6 or len(wfc)<6:
        return trades
    ave = 3 * np.mean(bond[-5:]) + 2 * np.mean(gs[:-5]) + 3 * np.mean(ms[:-5]) + 2 * np.mean(wfc[:-5])
    if (xlf < ave):
        trades.append(("BUG", "XLF", ave, 30))
    else:
        trades.append(("SELL", "XLF", xlf, 30))
    return trades
