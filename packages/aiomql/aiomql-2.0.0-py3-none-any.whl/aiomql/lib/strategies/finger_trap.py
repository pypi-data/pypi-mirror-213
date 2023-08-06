import asyncio
import logging
from dataclasses import dataclass

from ..traders.simple_deal_trader import DealTrader
from ... import Symbol
from ...strategy import Strategy
from ...core.constants import TimeFrame, OrderType
from ...candle import Candle, Candles

logger = logging.getLogger()


class FTCandle(Candle):
    def ema_crossover(self):
        return self.open < self.ema < self.close

    def ema_cross_under(self):
        return self.open > self.ema > self.close


class FTCandles(Candles):
    candle = FTCandle

    def get_swing_high(self) -> Candle | None:
        for candle in reversed(self):
            if self.is_swing_high(candle):
                return candle

    def get_swing_low(self) -> Candle | None:
        for candle in reversed(self):
            if self.is_swing_low(candle):
                return candle

    def is_swing_high(self, candle: Candle) -> bool:
        try:
            return self[candle.Index - 1].high < candle.high > self[candle.Index + 1].high
        except Exception as exe:
            return False

    def is_swing_low(self, candle: Candle):
        try:
            return self[candle.Index - 1].low > candle.low < self[candle.Index + 1].low
        except Exception as exe:
            return False


@dataclass
class Entry:
    """
    A helper class for capturing entry positions.

    Attributes:
        snooze (float): Time of the bar

        trend (str): The trend of the chart. Can be either of "notrend", "uptrend", "downtrend".

        new (bool): Shows if an entry position has been seen before.

        type (OrderType): OrderType for placing trade order

        points (float): points to trade.
    """
    snooze: float = 0
    bullish: bool = False
    bearish: bool = False
    ranging: bool = False
    trend_candle: Candle = Candle(close=0, open=0, high=0, low=0, Index=0, time=0)
    entry_candle: Candle = Candle(close=0, open=0, high=0, low=0, Index=0, time=0)
    new: bool = True
    order_type: OrderType | None = None
    points: float = 0

    def update(self, **kwargs):
        fields = self.__dict__
        for key in kwargs:
            if key in fields:
                setattr(self, key, kwargs[key])


class FingerTrap(Strategy):
    trend_time_frame: TimeFrame = TimeFrame.M30
    entry_time_frame: TimeFrame = TimeFrame.M5
    trend: int = 4
    fast_period: int = 8
    slow_period: int = 34
    Candle = FTCandle
    Candles = FTCandles
    prices: FTCandles
    name = "FingerTrap"
    default = {
        "name": name,
        "fast_period": fast_period,
        "slow_period": slow_period,
        "trend_time": trend_time_frame,
        "entry_time": entry_time_frame,
        "trend": trend
    }

    def __init__(self, *, symbol: Symbol, params: dict | None = None):
        super().__init__(symbol=symbol, params=params)
        self.trader = DealTrader(symbol=self.symbol)
        self.current_time = 0
        self.parameters |= self.default
        self.entry: Entry = Entry(snooze=self.trend_time_frame.time)

    async def check_trend(self):
        try:
            fast: FTCandles
            slow: FTCandles
            fast, slow = await asyncio.gather(self.get_ema(time_frame=self.trend_time_frame, period=self.fast_period),
                                              self.get_ema(time_frame=self.trend_time_frame, period=self.slow_period))

            fast = fast[-self.trend:]
            slow = slow[-self.trend:]
            current = fast[-1]
            if not (new := current > self.entry.trend_candle):
                self.entry.update(new=new, order_type=None)
                return

            self.entry.update(trend_candle=current, new=new)
            bullish = all((s.ema < f.ema < f.close) for f, s in zip(fast, slow))
            if bullish:
                self.entry.update(bullish=bullish, snooze=self.entry_time_frame.time,
                                  ranging=False, bearish=False)
                return

            bearish = all((s.ema > f.ema > f.close) for f, s in zip(fast, slow))
            if bearish:
                self.entry.update(bearish=bearish, snooze=self.entry_time_frame.time,
                                  ranging=False, bullish=False)
                return

            self.entry.update(snooze=self.trend_time_frame.time, ranging=True, order_type=None, bullish=False,
                              bearish=False)
        except Exception as exe:
            logger.error(f'{exe}. Error in {self.__class__.__name__}.check_trend')

    async def watch_market(self):
        await self.check_trend()
        if self.entry.ranging:
            return
        await self.confirm_trend()

    async def confirm_trend(self):
        try:
            entry_candles: FTCandles = await self.get_ema(time_frame=self.entry_time_frame, period=self.fast_period)
            entry_candle = entry_candles[-1]
            if not (new := entry_candle > self.entry.entry_candle):
                self.entry.update(new=new, order_type=None)
                return
            self.entry.update(entry_candle=entry_candle, new=new)
            if self.entry.bullish and entry_candle.ema_crossover() and (support_candle := entry_candles.get_swing_low()):
                self.entry.points = (entry_candle.close - support_candle.low) / self.symbol.point
                self.entry.order_type = OrderType.BUY
                print(entry_candle.high - support_candle.low, self.entry.points, entry_candle.high, entry_candle.low, 'bull', self.symbol)
                return

            if self.entry.bearish and entry_candle.ema_crossover() and (support_candle := entry_candles.get_swing_high()):
                self.entry.points = (support_candle.high - entry_candle.close) / self.symbol.point
                self.entry.order_type = OrderType.SELL
                print(support_candle.high - entry_candle.low, self.entry.points, support_candle.high, entry_candle.low, 'bear', self.symbol)
                return

            self.entry.update(order_type=None, snooze=self.entry_time_frame.time)
        except Exception as exe:
            logger.error(f'{exe}. Error in {self.__class__.__name__}.confirm_trend')

    async def trade(self):
        print(f'Trading {self.symbol}')
        while True:
            try:
                await self.watch_market()
                if not self.entry.new:
                    await asyncio.sleep(0.5)
                    continue

                if self.entry.order_type is None:
                    await self.sleep(self.entry.snooze)
                    continue

                print(self.entry.points, 'points')
                await self.trader.place_trade(order=self.entry.order_type, points=self.entry.points, params=self.parameters)
                await self.sleep(self.entry.snooze)
            except Exception as err:
                logger.error(f"Error: {err}\t Symbol: {self.symbol} in {self.__class__.__name__}.trade")
                await self.sleep(self.trend_time_frame.time)
                continue
