import ccxt
import pandas as pd
import time
import requests
import os

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

def fetch_binance_ohlcv(symbol='BTC/USDT', timeframe='1d', since_days=365):
    binance = ccxt.binance()

    since_timestamp = binance.parse8601(
        (pd.Timestamp.now() - pd.Timedelta(days=since_days)).isoformat()
    )

    all_ohlcv = []
    limit = 500  # 最大一次获取 500 根K线
    while True:
        ohlcv = binance.fetch_ohlcv(symbol, timeframe, since=since_timestamp, limit=limit)
        if not ohlcv:
            break
        all_ohlcv += ohlcv
        since_timestamp = ohlcv[-1][0] + 1
        time.sleep(0.3)  # 避免被限流
        if len(ohlcv) < limit:
            break

    df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('datetime', inplace=True)
    return df

if __name__ == '__main__':
    df = fetch_binance_ohlcv()
    print(df.head())
