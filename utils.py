# utils.py
# -*- coding: utf-8 -*-
import pandas as pd

def standardize_ohlcv_df(df):
    df = df.copy()

    # 如果是多重列名，提前剥离
    if isinstance(df.columns[0], tuple):
        df.columns = [col[0] for col in df.columns]

    # 重命名
    rename_map = {
        'Date': 'datetime',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Adj Close': 'adj_close',
        'Volume': 'volume'
    }
    df.rename(columns=rename_map, inplace=True)

    # 检查是否有 datetime 列
    if 'datetime' not in df.columns:
        raise ValueError("数据中找不到时间列 datetime，请检查源数据")

    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)

    # 确保所有列都是小写
    df.columns = [str(col).lower() for col in df.columns]

    # 仅保留常用字段
    keep_cols = ['open', 'high', 'low', 'close', 'volume']
    df = df[keep_cols]

    return df