# -*- coding: utf-8 -*-
import backtrader as bt

class MovingAverageCrossStrategy(bt.Strategy):
    params = (('short_window', 10), ('long_window', 30))

    def __init__(self):
        self.sma_short = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_window)
        self.sma_long = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_window)
        self.buy_signals = []
        self.sell_signals = []

    def next(self):
        # 如果尚未持仓，并且短期均线上穿长期均线 --> 买入
        if not self.position and self.sma_short[0] > self.sma_long[0] and self.sma_short[-1] <= self.sma_long[-1]:
            self.buy()
            self.buy_signals.append((self.data.datetime.datetime(0), self.data.close[0]))

        # 如果已经持仓，并且短期均线下穿长期均线 --> 卖出
        elif self.position and self.sma_short[0] < self.sma_long[0] and self.sma_short[-1] >= self.sma_long[-1]:
            self.sell()
            self.sell_signals.append((self.data.datetime.datetime(0), self.data.close[0]))

class MovingAverageRSIStrategy(bt.Strategy):
    params = (
        ('short_window', 10),
        ('long_window', 30),
        ('rsi_period', 14),
        ('rsi_buy_threshold', 70),
        ('rsi_sell_threshold', 30),
    )

    def __init__(self):
        self.sma_short = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_window)
        self.sma_long = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_window)
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        self.buy_signals = []
        self.sell_signals = []

    def next(self):
        if not self.position:
            if (
                self.sma_short[0] > self.sma_long[0] and
                self.sma_short[-1] <= self.sma_long[-1] and
                self.rsi[0] < self.params.rsi_buy_threshold
            ):
                self.buy()
                self.buy_signals.append((self.datas[0].datetime.datetime(0), self.datas[0].close[0]))
        else:
            if (
                self.sma_short[0] < self.sma_long[0] and
                self.sma_short[-1] >= self.sma_long[-1] and
                self.rsi[0] > self.params.rsi_sell_threshold
            ):
                self.sell()
                self.sell_signals.append((self.datas[0].datetime.datetime(0), self.datas[0].close[0]))


class MACDStrategy(bt.Strategy):
    def __init__(self):
        macd = bt.ind.MACD(self.data.close)
        self.macd_hist = macd.macd - macd.signal  # 即 dif - dea
        self.buy_signals = []
        self.sell_signals = []

    def next(self):
        if not self.position and self.macd_hist[0] > 0 and self.macd_hist[-1] <= 0:
            self.buy()
            self.buy_signals.append((self.data.datetime.datetime(0), self.data.close[0]))
        elif self.position and self.macd_hist[0] < 0 and self.macd_hist[-1] >= 0:
            self.sell()
            self.sell_signals.append((self.data.datetime.datetime(0), self.data.close[0]))

