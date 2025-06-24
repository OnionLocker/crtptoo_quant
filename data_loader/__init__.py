# -*- coding: utf-8 -*-
# data_loader/__init__.py

from .yfinance_loader import load_yf_data
from .okx_loader import load_okx_data
import os

USE_PROXY = True  # 改成 True 才启用
if USE_PROXY:
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

def load_data(source='yfinance', symbol='BTC-USD', start=None, end=None, interval='1d'):
    if source == 'yfinance':
        return load_yf_data(symbol, start, end, interval)
    elif source == 'okx':
        return load_okx_data(symbol.replace('-', '/'), timeframe=interval)
    else:
        raise ValueError(f"数据源 {source} 暂不支持")
