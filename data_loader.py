import yfinance as yf
import pandas as pd
import os
# 设置环境变量，让 yfinance 自动使用代理
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

def download_crypto_data(symbol='BTC-USD', start='2015-01-01', end='2024-01-01', interval='1d'):
    """
    下载加密货币的历史K线数据
    symbol: 币种代码（Yahoo Finance 格式，如 BTC-USD）
    start, end: 起止日期
    interval: K线周期（'1d' = 日线）
    """
    data = yf.download(symbol, start=start, end=end, interval=interval)
    data.dropna(inplace=True)
    data.reset_index(inplace=True)
    return data

if __name__ == '__main__': # 调试
    df = download_crypto_data()
    print(df.head())
