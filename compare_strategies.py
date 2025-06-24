# compare_strategies.py
# -*- coding: utf-8 -*-
import pandas as pd
from data_loader import load_data
from strategy import MACDStrategy, MovingAverageRSIStrategy, MovingAverageCrossStrategy
from strategy_runner import StrategyRunner

# # 下载数据（不设为索引，让标准化函数处理）
# df = load_data(source='okx', symbol='BTC-USD', start="2014-01-01", end="2024-01-01", interval='1d')

# df['datetime'] = pd.to_datetime(df['datetime'])

# # 回测多个策略
# # 策略列表
# strategies = [
#     MACDStrategy,
#     MovingAverageRSIStrategy,
#     MovingAverageCrossStrategy,
# ]

# for strat_cls in strategies:
#     print(f"正在回测: {strat_cls.__name__}")
#     runner = StrategyRunner(strat_cls, df)
#     res = runner.run()
#     print("回测结果:")
#     for k, v in res.items():
#         print(f"{k}: {v}")
#     print("-" * 40)

# import requests
# print(requests.get("https://www.okx.com").text[:200])

import ccxt
import os
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

okx = ccxt.okx({
    'enableRateLimit': True,
    'timeout': 10000,
})

markets = okx.load_markets()
print("成功加载市场数量：", len(markets))
