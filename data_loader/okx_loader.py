# -*- coding: utf-8 -*-
# data_loader/okx_loader.py

import ccxt
import pandas as pd
from datetime import datetime

okx = ccxt.okx({
    'enableRateLimit': True
})

def load_okx_data(symbol='BTC/USDT', timeframe='1d', since_days=180):
    okx = ccxt.okx()
    since = okx.milliseconds() - since_days * 24 * 60 * 60 * 1000

    print(f"正在从 OKX 获取 {symbol} 的数据...")

    ohlcv = okx.fetch_ohlcv(symbol, timeframe=timeframe, since=since)
    df = pd.DataFrame(ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)

    return df
