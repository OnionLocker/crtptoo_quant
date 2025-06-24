# -*- coding: utf-8 -*-
from data_loader import load_data
from strategy import MovingAverageCrossStrategy, MovingAverageRSIStrategy, MACDStrategy
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import warnings
setattr(mdates, 'warnings', warnings)
import backtrader as bt
import os
from utils import standardize_ohlcv_df
from datetime import datetime
from optimizer import run_optimization, plot_roi_heatmap
import pandas as pd
plt.style.use('seaborn-v0_8-darkgrid')

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文黑体
plt.rcParams['axes.unicode_minus'] = False   # 解决负号显示问题

# 下载数据
df = download_crypto_data()

# 解开多重列名
df.columns = df.columns.get_level_values(0)
df = standardize_ohlcv_df(df)

# 转为 backtrader 数据格式
data = bt.feeds.PandasData(
    dataname=df,
    datetime=None,
    open='open',
    high='high',
    low='low',
    close='close',
    volume='volume',
    openinterest=-1
)

strategy_name = "macd"  # 或者 "ma", "rsi" 

# 创建 backtrader 引擎
cerebro = bt.Cerebro()
cerebro.adddata(data)
if strategy_name == "ma":
    cerebro.addstrategy(MovingAverageCrossStrategy)
elif strategy_name == "rsi":
    cerebro.addstrategy(MovingAverageRSIStrategy)
elif strategy_name == "macd":
    cerebro.addstrategy(MACDStrategy)

# 添加风控分析器
# 添加风险分析器和统计器
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe', timeframe=bt.TimeFrame.Days)
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='timereturn')  # 资金曲线
initial_cash = 100000
cerebro.broker.setcash(initial_cash)
result = cerebro.run()



final_cash = cerebro.broker.getvalue()

# 计算收益率
roi = (final_cash - initial_cash) / initial_cash * 100
print(f"回测起始资金: {initial_cash:.2f}")
print(f"回测结束资金: {final_cash:.2f}")
print(f"策略收益率: {roi:.2f}%")

# 提取策略结果
strategy = result[0]
buy_dates, buy_prices = zip(*strategy.buy_signals) if strategy.buy_signals else ([], [])
sell_dates, sell_prices = zip(*strategy.sell_signals) if strategy.sell_signals else ([], [])

# 输出风险指标
# 输出风险与统计指标
sharpe = strategy.analyzers.sharpe.get_analysis().get('sharperatio', 'N/A')
drawdown = strategy.analyzers.drawdown.get_analysis()
returns = strategy.analyzers.returns.get_analysis()
trades = strategy.analyzers.trades.get_analysis()

max_dd = drawdown.max.drawdown if drawdown else 'N/A'
annual_return = returns.get('rnorm100', 'N/A')

total_trades = trades.total.closed if 'total' in trades and 'closed' in trades.total else 'N/A'
won_trades = trades.won.total if 'won' in trades and 'total' in trades.won else 'N/A'
win_rate = (won_trades / total_trades * 100) if total_trades and total_trades != 0 else 'N/A'

print(f"夏普比率: {sharpe}")
print(f"最大回撤: {max_dd:.2f}%")
print(f"年化收益率: {annual_return:.2f}%")
print(f"总交易次数: {total_trades}")
print(f"胜率: {win_rate:.2f}%")

# 绘图
plt.figure(figsize=(14, 8))
plt.plot(df.index, df['close'], label='Close Price', color='black', linewidth=1)

# 画买入信号点
if buy_dates:
    plt.scatter(buy_dates, buy_prices, marker='^', color='green', label='Buy', zorder=5)
# 画卖出信号点
if sell_dates:
    plt.scatter(sell_dates, sell_prices, marker='v', color='red', label='Sell', zorder=5)

plt.title("回测价格与交易信号图")
plt.xlabel("日期")
plt.ylabel("价格")
plt.legend()
plt.grid(True)
plt.tight_layout()

# # 自动构建保存路径
# timestamp = datetime.now()
# date_str = timestamp.strftime('%Y%m%d')
# time_str = timestamp.strftime('%Y-%m-%d_%H-%M-%S')

# folder_path = os.path.join(os.path.dirname(__file__), 'images', date_str)
# os.makedirs(folder_path, exist_ok=True)

# filename = f'report_{time_str}.png'
# save_path = os.path.join(folder_path, filename)

# plt.savefig(save_path, dpi=300)
# print(f'图像已保存为 {save_path}')

# === 提取资金曲线并绘制 ===
returns_series = pd.Series(strategy.analyzers.timereturn.get_analysis())
cum_returns = (1 + returns_series).cumprod()

plt.figure(figsize=(12, 6))
plt.plot(cum_returns, label='资金净值曲线')
plt.title("策略资金曲线")
plt.xlabel("时间")
plt.ylabel("净值")
plt.grid(True)
plt.legend()

# 资金曲线图
date_str = pd.Timestamp.now().strftime('%Y%m%d')
output_dir = os.path.join('output', date_str)
os.makedirs(output_dir, exist_ok=True)
plt.savefig(os.path.join(output_dir, 'equity_curve.png'), dpi=300)
plt.show()

# 盈亏比 = 平均盈利 / 平均亏损
total_win = trades.won.pnl.get('total', 0)
count_win = trades.won.total if trades.won else 0

total_loss = abs(trades.lost.pnl.get('total', 0))
count_loss = trades.lost.total if trades.lost else 0

avg_win = total_win / count_win if count_win > 0 else 0
avg_loss = total_loss / count_loss if count_loss > 0 else 0

profit_factor = avg_win / avg_loss if avg_loss != 0 else 'N/A'
print(f"盈亏比（Profit Factor）: {profit_factor}")


# 热点图
# results = run_optimization(df, short_range=range(5, 21, 5), long_range=range(25, 61, 5))
# print(results.head().to_string(index=False))
# plot_roi_heatmap(results)