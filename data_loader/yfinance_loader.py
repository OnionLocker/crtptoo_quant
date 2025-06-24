# -*- coding: utf-8 -*-
import yfinance as yf
import pandas as pd

def load_yf_data(symbol='BTC-USD', start='2015-01-01', end='2024-01-01', interval='1d'):
    data = yf.download(symbol, start=start, end=end, interval=interval)
    data.dropna(inplace=True)
    data.reset_index(inplace=True)  # 保留 Date 列为普通列
    data.columns = data.columns.get_level_values(0)  # 解决多重列名问题
    data.rename(columns={
        'Date': 'datetime',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume'
    }, inplace=True)
    return data

if __name__ == '__main__': # 调试
    df = load_yf_data()
    print(df.head())
