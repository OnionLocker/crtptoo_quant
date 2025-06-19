# utils.py
# -*- coding: utf-8 -*-
import pandas as pd

def standardize_ohlcv_df(df):
    """
    通用K线数据清洗器：
    - 统一列名为 open, high, low, close, volume
    - 统一时间列为 datetime 并设为索引
    - 兼容 yfinance / ccxt / 其他交易所格式
    """

    # 1. 解开多级列名（如 yfinance）
    if isinstance(df.columns[0], tuple):
        df.columns = df.columns.get_level_values(0)

    # 2. 所有列名转小写字符串，避免 tuple 报错
    df.columns = [str(c).lower() for c in df.columns]

    # 3. 标准化列名
    rename_map = {
        'date': 'datetime',
        'timestamp': 'datetime',
        'ts': 'datetime',
        'o': 'open',
        'h': 'high',
        'l': 'low',
        'c': 'close',
        'v': 'volume',
        'adj close': 'close',  # yfinance 的特殊列
    }
    df = df.rename(columns=rename_map)

    # 4. 检查时间列
    if 'datetime' not in df.columns:
        raise ValueError("数据中找不到时间列 datetime，请检查源数据")

    # 5. 设置时间索引
    if not df.index.name == 'datetime':
        df.set_index('datetime', inplace=True)

    # 6. 只保留标准列
    keep_cols = ['open', 'high', 'low', 'close', 'volume']
    df = df[[col for col in keep_cols if col in df.columns]]

    return df
