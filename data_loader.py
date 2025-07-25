# -*- coding: utf-8 -*-
import yfinance as yf
import pandas as pd
import os
# 设置环境变量，让 yfinance 自动使用代理
USE_PROXY = True  # 改成 True 才启用

if USE_PROXY:
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

import yfinance as yf

def download_crypto_data(symbol='BTC-USD', start='2015-01-01', end='2024-01-01', interval='1d'):
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
    df = download_crypto_data()
    print(df.head())
