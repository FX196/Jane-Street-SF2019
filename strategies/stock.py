from strategies.stats import *
import numpy as np

def trade(exchange):
    trades = []
    data = exchange.last_data
    delta_t_history = exchange.delta_t
    total_trade = exchange.t_now
    stocks = ['VALBZ', 'GS', 'MS', 'WFC']
    current_holding = exchange.holdings
    buy_price = {} # process buy price when purchase

    for stock in stocks: 
        if data['type'] == 'book' and data['symbol'] == stock:
            if len(delta_t_history) < 10 or len(total_trade) < 10:
                break
            # # comment out the following two
            # tradeOp_gradient = np.gradient(delta_t_history)[-1] # > 0 when concave up
            # value_gradient = np.gradient(total_trade)[-1]
            average = mean(total_trade)
            stand_dev = std(total_trade)
            ema = EMA(delta_t_history)

            print("EMA: ", ema, " average: ", average, " std ", stand_dev)
            # print("value_gradient: ", value_gradient, " tradeOp_gradient: ", tradeOp_gradient)
            
            if ema > 0 and total_trade[-1] > average + stand_dev * 0.5 and current_holding[stock] > 0:
                trades.append(('SELL', stock, int(average + stand_dev * 0.6), current_holding[stock]))
            elif ema > 0 and total_trade[-1] > average - stand_dev * 0.5: 
                trades.append(('BUY', stock, int(average - stand_dev * 0.4), 100))

            # # sell strategies#
            # if ema > 0 and total_trade[-1] > average + stand_dev * 1.1 and current_holding[stock] > 0 and buy_price[stock] < total_trade[-1]:
            #     trades.append(('SELL', stock, total_trade[-1] + tradeOp_gradient * delta_t_history[-1], current_holding[stock]))
            # elif ema > 0 and total_trade[-1] > average + stand_dev * 0.5 and current_holding[stock] > 0 and buy_price[stock] < total_trade[-1]:
            #     trades.append(('SELL', stock, total_trade[-1] + tradeOp_gradient * delta_t_history[-1], current_holding[stock] // 2))
            
            # elif ema > 0 and tradeOp_gradient > 0 and value_gradient > 0 and total_trade[-1] < average - stand_dev * 1.1: 
            #     trades.append(('BUY', stock, total_trade[-1] + tradeOp_gradient * delta_t_history[-1], 200))
            # elif ema > 0 and tradeOp_gradient > 0 and value_gradient > 0 and total_trade[-1] < average - stand_dev * 0.5: 
            #     trades.append(('BUY', stock, total_trade[-1] + tradeOp_gradient * delta_t_history[-1], 100))
    # if data['type'] == 'book' and data['symbol'] == 'BOND':
    #     bids = data['buy']
    #     for price, size in bids:
    #         if price > 1000:
    #             trades.append(('SELL', 'BOND', price, size))

    #     asks = data['sell']
    #     for price, size in asks:
    #         if price < 1000:
    #             trades.append(('BUY', 'BOND', price, size))
    return trades
