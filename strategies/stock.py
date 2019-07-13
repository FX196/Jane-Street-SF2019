from strategies.stats import *
import numpy as np

def trade(exchange):
    trades = []
    data = exchange.last_data
    delta_t_history = exchange.delta_t
    total_trade = exchange.t_now
    stocks = ['GS', 'MS', 'WFC']
    current_holding = exchange.holdings
    buy_price = {} # process buy price when purchase

    for stock in stocks: 
        if data['type'] == 'book' and data['symbol'] == stock:
            if len(delta_t_history[stock]) < 100 or len(total_trade[stock]) < 100:
                break
            # comment out the following two
            tradeOp_gradient = np.gradient(delta_t_history[stock])[-1] # > 0 when concave up
            value_gradient = np.gradient(total_trade[stock])[-1]
            average = np.average(total_trade[stock])
            stand_dev = np.std(total_trade[stock])
            ema = EMA(delta_t_history[stock])

            if stock not in buy_price:
                buy_price[stock] = -1
            if stock not in current_holding: 
                current_holding[stock] = -1 
            # print("EMA: ", ema, " average: ", average, " std ", stand_dev)
            # print("value_gradient: ", value_gradient, " tradeOp_gradient: ", tradeOp_gradient)
            
            # # for bot
            if ema > 0 and total_trade[stock][-1] > average + stand_dev*0.5 and current_holding[stock] > 0:
                if current_holding[stock] == 1: 
                    trades.append(('SELL', stock, int(average + stand_dev*0.3), 1))    
                    current_holding[stock] -= 1
                else:
                    trades.append(('SELL', stock, int(average + stand_dev*0.3), 2))
                    current_holding[stock] -= 2
                if current_holding[stock] == 0:
                    buy_price[stock] = -1 
            elif ema > 0 and total_trade[stock][-1] > average and current_holding[stock] > 0:
                if current_holding[stock] == 1: 
                    trades.append(('SELL', stock, int(average), 1))    
                    current_holding[stock] -= 1
                else:
                    trades.append(('SELL', stock, int(average), 2))
                    current_holding[stock] -= 2
                if current_holding[stock] == 0:
                    buy_price[stock] = -1 
            # if ema < 0 and total_trade[stock][-1] > average + stand_dev and current_holding[stock] > 0 and buy_price[stock] != -1:
            #     trades.append(('SELL', stock, int(average + stand_dev * 0.9), current_holding[stock]))
            #     current_holding[stock] = 0
            # elif ema < 0 and total_trade[stock][-1] > average + stand_dev * 0.5 and buy_price[stock] != -1 and current_holding[stock] > 0:
            #     trades.append(('SELL', stock, int(average + stand_dev * 0.3), current_holding[stock] // 2))
            #     current_holding[stock] = 0
            # elif ema < 0 and total_trade[stock][-1] > average + stand_dev * 0.3: 
            #     trades.append(('SELL', stock, int(average), current_holding[stock]))
            #     current_holding[stock] = 0
            elif ema < 0 and total_trade[stock][-1] < average - stand_dev * 0.5: 
                trades.append(('BUY', stock, int(average - stand_dev * 0.3), 2))
                buy_price[stock] = int(average - stand_dev * 0.3)
                current_holding[stock] += 2
            elif ema < 0 and total_trade[stock][-1] < average - stand_dev: 
                trades.append(('BUY', stock, int(average - stand_dev * 0.9), 2))   
                buy_price[stock] = int(average - stand_dev * 0.9) 
                current_holding[stock] += 2

            # # # sell strategies#
            # if ema > 0 and total_trade[stock][-1] > average + stand_dev * 1.1 and current_holding[stock] > 0 and buy_price[stock] < total_trade[stock][-1]:
            #     trades.append(('SELL', stock, total_trade[stock][-1] + tradeOp_gradient * delta_t_history[-1], current_holding[stock]))
            # elif ema > 0 and total_trade[stock][-1] > average + stand_dev * 0.5 and current_holding[stock] > 0 and buy_price[stock] < total_trade[stock][-1]:
            #     trades.append(('SELL', stock, total_trade[stock][-1] + tradeOp_gradient * delta_t_history[-1], current_holding[stock] // 2))
            
            # elif ema > 0 and tradeOp_gradient > 0 and value_gradient > 0 and total_trade[stock][-1] < average - stand_dev * 1.1: 
            #     trades.append(('BUY', stock, total_trade[stock][-1] + tradeOp_gradient * delta_t_history[stock][-1], 200))
            # elif ema > 0 and tradeOp_gradient > 0 and value_gradient > 0 and total_trade[stock][-1] < average - stand_dev * 0.5: 
            #     trades.append(('BUY', stock, total_trade[stock][-1] + tradeOp_gradient * delta_t_history[stock][-1], 100))
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
