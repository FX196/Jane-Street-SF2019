import numpy as np 
from ..stats import *

def trade(exchange):
    data = exchange.last_data
    delta_t_history = exchange.delta_t
    total_trade = exchange.t_now
    stocks = ['VALBZ', 'GS', 'MS', 'WFC']
    current_holding = exchange.holdings
    for stock in stocks: 
        if data['type'] == 'book' and data['symbol'] == stock:
            tradeOp_gradient = np.gradient(delta_t_history)[-1]
            value_gradient = np.gradient(total_trade)[-1]
            average = mean(total_trade)
            stand_dev = std(total_trade)
            ema = EMA(delta_t_history)
            
            if total_trade[-1] > average + stand_dev:

            
    
    if data['type'] == 'book' and data['symbol'] == 'BOND':
        bids = data['buy']
        for price, size in bids:
            if price > 1000:
                trades.append(('SELL', 'BOND', price, size))

        asks = data['sell']
        for price, size in asks:
            if price < 1000:
                trades.append(('BUY', 'BOND', price, size))
    return trades
