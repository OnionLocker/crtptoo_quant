# -*- coding: utf-8 -*-
# optimizer.py
import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from strategy import MovingAverageCrossStrategy
from utils import standardize_ohlcv_df

class StrategyWithParams(bt.Strategy):
    params = (
        ('short_window', 10),
        ('long_window', 30),
    )

    def __init__(self):
        sma_short = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_window)
        sma_long = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_window)
        self.crossover = bt.ind.CrossOver(sma_short, sma_long)

    def next(self):
        if not self.position and self.crossover > 0:
            self.buy()
        elif self.position and self.crossover < 0:
            self.sell()

def run_optimization(df, short_range, long_range):
    results = []
    total = sum(1 for s in short_range for l in long_range if s < l)
    with tqdm(total=total, desc="参数组合测试中") as pbar:
        for short in short_range:
            for long in long_range:
                if short >= long:
                    continue
                if len(df) < long + 10:
                    pbar.update(1)
                    continue  # 数据不足以计算长期均线，跳过

                cerebro = bt.Cerebro()
                data = bt.feeds.PandasData(dataname=df, datetime=None, open='open', high='high',
                                           low='low', close='close', volume='volume', openinterest=-1)
                cerebro.adddata(data)
                cerebro.addstrategy(StrategyWithParams, short_window=short, long_window=long)
                cerebro.broker.setcash(100000)
                cerebro.broker.setcommission(commission=0.001)
                try:
                    cerebro.run()
                    final_value = cerebro.broker.getvalue()
                    roi = (final_value - 100000) / 100000
                    results.append({'short': short, 'long': long, 'roi': roi})
                except Exception as e:
                    print(f"组合 ({short}, {long}) 出错: {e}")
                pbar.update(1)

    results_df = pd.DataFrame(results)
    results_df.sort_values(by='roi', ascending=False, inplace=True)
    return results_df

def plot_roi_heatmap(results_df):
    pivot = results_df.pivot(index='short', columns='long', values='roi')
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, fmt=".2%", cmap="RdBu_r", center=0)
    plt.title("均线参数组合收益率热力图")
    plt.xlabel("长期均线")
    plt.ylabel("短期均线")
    plt.tight_layout()
    plt.show()
