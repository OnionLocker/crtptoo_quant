# -*- coding: utf-8 -*-
# compare_strategies.py

import pandas as pd
from data_loader import download_crypto_data
from strategy import MACDStrategy, MovingAverageRSIStrategy, MovingAverageCrossStrategy
from strategy_runner import StrategyRunner

# 下载并标准化数据
df = download_crypto_data()

# 处理 yfinance 多层列名
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# 重命名列
df = df.rename(columns={
    'Date': 'datetime',
    'Open': 'open',
    'High': 'high',
    'Low': 'low',
    'Close': 'close',
    'Volume': 'volume'
})
df.columns = [str(c).lower() for c in df.columns]

# 转换为 datetime 类型，并设为索引
df['datetime'] = pd.to_datetime(df['datetime'])
df.set_index('datetime', inplace=True)

# 策略列表
strategies = [
    MACDStrategy,
    MovingAverageRSIStrategy,
    MovingAverageCrossStrategy,
]

# 回测并打印结果
for strat_cls in strategies:
    print(f"正在回测: {strat_cls.__name__}")
    runner = StrategyRunner(strat_cls, df)
    res = runner.run()
    print(f"\n策略: {strat_cls.__name__}")
    print("起始资金:", res['start_value'])
    print("最终资金:", res['end_value'])
    print("收益率: %.2f%%" % (res['roi'] * 100))
    print("年化收益率: %.2f%%" % (res['annual_return'] * 100))
    print("最大回撤: %.2f%%" % (res['max_drawdown'] * 100))
    print("夏普比率:", res['sharpe_ratio'])
    print("总交易次数:", res['total_trades'])
    print("胜率: %.2f%%" % (res['win_rate'] * 100))
    print("盈亏比 (Profit Factor): %.2f" % res['profit_factor'])
    print("-" * 40)
