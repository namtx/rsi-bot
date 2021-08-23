from binance import Client
from app import app
from fastapi import Request
import talib
import os
import requests
import numpy as np
import pandas as pd

@app.get('/indicators')
async def indicators(symbol: str, interval: str = '1d', limit: int = 100):
    client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

    print(parse_symbol(symbol))

    klines = client.get_historical_klines(parse_symbol(symbol), interval, get_start_time(interval))
    df = pd.DataFrame(np.array(klines),
                columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quoute_asset_volume', 'ignmore'],
                dtype='float64')

    cl = df['close']

    rsi = talib.RSI(cl.values, timeperiod=14)
    
    return {
        "rsi": rsi[-1]
    }

def parse_symbol(symbol):
    return ''.join(list(map(lambda x: x.upper(), symbol.split('/'))))

def get_start_time(interval):
    switcher = {
        '1m': '1 day ago UTC',
        '3m': '1 day ago UTC',
        '5m': '1 day ago UTC',
        '15m': '1 day ago UTC',
        '30m': '1 day ago UTC',
        '1h': '2 week ago UTC',
        '2h': '2 week ago UTC',
        '4h': '2 week ago UTC',
        '6h': '2 week ago UTC',
        '8h': '1 month ago UTC',
        '12h': '1 month ago UTC',
        '1d': '1 month ago UTC',
        '3d': '1 month ago UTC',
        '1w': '1 year ago UTC',
        '1M': '2 year ago UTC',
    }

    return switcher.get(interval, 'Invalid interval')
