# strategy_runner.py
# -*- coding: utf-8 -*-
import backtrader as bt
from analyzers import analyze_results
from utils import standardize_ohlcv_df

class StrategyRunner:
    def __init__(self, strategy_cls, df):
        self.strategy_cls = strategy_cls
        self.df = standardize_ohlcv_df(df)

    def run(self):
        cerebro = bt.Cerebro()
        data = bt.feeds.PandasData(
            dataname=self.df,
            datetime=None,
            open='open',
            high='high',
            low='low',
            close='close',
            volume='volume',
            openinterest=-1
        )
        cerebro.adddata(data)
        cerebro.addstrategy(self.strategy_cls)
        cerebro.broker.setcash(100000)
        cerebro.broker.setcommission(commission=0.001)

        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='tradeanalyzer')
        cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')

        strategies = cerebro.run()
        strat = strategies[0]
        final_value = cerebro.broker.getvalue()

        results = {'final_value': final_value}
        return analyze_results(results, strat.analyzers, self.strategy_cls.__name__)