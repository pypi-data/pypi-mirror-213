import asyncio
from typing import Type, TypeVar, Generic

from pandas import DataFrame, Series

from .core.constants import TimeFrame


CandlesType = TypeVar('CandlesType', bound='Candles')  # A type representing the candles class


CandleType = TypeVar('CandleType', bound='Candle')  # A type representing the candle class


class Candle:
    """
    A class representing rates from the charts as Japanese Candlesticks.
    You can subclass this class for added customization.

    Attributes:
        Index (int): Position of the candle in the chart. Zero represents the most recent
        time (int): Period start time.
        open (int): Open price
        high (float): The highest price of the period
        low (float): The lowest price of the period
        close (float): Close price
        tick_volume (float): Tick volume
        real_volume (float): Trade volume
        spread (float): Spread
        ema (float, optional): ema

    Notes: All initialization arguments are assumed to be class attributes.
    """
    def __init__(self, *, time: int, open: float, high: float, low: float, close: float, tick_volume: float = 0,
                 real_volume: float = 0, spread: float = 0, Index: int = 0, ema: float = 0, **kwargs):
        self.time = time
        self.high = high
        self.low = low
        self.close = close
        self.real_volume = real_volume
        self.spread = spread
        self.open = open
        self.tick_volume = tick_volume
        self.Index = Index
        self.ema = ema
        [setattr(self, key, value) for key, value in kwargs.items()]

    def __eq__(self, other):
        return (self.open, self.close, self.low, self.high, self.time) == (other.open, other.close, other.low, other.high, other.time)

    def __lt__(self, other):
        return self.time < other.time

    def __gt__(self, other):
        return self.time > other.time

    def __hash__(self):
        return int(self.open*self.close*self.high*self.low*self.time)

    @property
    def mid(self) -> float:
        """
        The mid of open and close
        Returns: mid

        """
        return (self.open + self.close) / 2

    def is_bullish(self) -> bool:
        """
        Returns: True or False

        """
        return self.close > self.open

    def is_bearish(self) -> bool:
        """

        Returns: True or False

        """
        return self.open > self.close

    def is_hanging_man(self, ratio=1.5):
        return max((self.open - self.low), (self.high - self.close)) / (self.close - self.open) >= ratio

    def is_bullish_hammer(self, ratio=1.5):
        return max((self.close - self.low), (self.high - self.open)) / (self.open - self.close) >= ratio


class Candles(Generic[CandleType]):
    """
    A class representing a collection of rates as Candle Objects. Arranged chronologically,
    the Candles is an iterable container of candles from the oldest to the most recent.

    Args:
        data (DataFrame, tuple[tuple]): A pandas dataframe or a tuple of tuple as returned from the terminal

    Keyword Args:
        candle (Type(Candle)): A Candle class to be used for the rates.
        flip (bool): If flip is True reverse the chronological order of the candles.

    Attributes:
        data: Dataframe Object holding the rates
        Candle: Candle class for individual objects.
        Index (Series['int']): A pandas Series of the indexes of all candles in the object.
        time (Series['int']): A pandas Series of the time of all candles in the object.
        open (Series[float]): A pandas Series of the opening price of all candles in the object.
        high (Series[float]): A pandas Series of the high price of all candles in the object.
        low (Series[float]):  A pandas Series of the low price of all candles in the object.
        close (Series[float]):  A pandas Series of the closing price of all candles in the object.
        tick_volume (Series[float]):  A pandas Series of the tick volume of all candles in the object.
        real_volume (Series[float]): A pandas Series of the real volume of all candles in the object.
        spread (Series[float]): A pandas Series of the spread of all candles in the object.
        ema (Series[float], Optional): A pandas Series of the ema of all candles in the object if available.
    """
    Index: Series
    time: Series
    open: Series
    high: Series
    low: Series
    close: Series
    tick_volume: Series
    real_volume: Series
    spread: Series
    ema: Series
    candle: Type[Candle] = Candle
    
    def __init__(self, *, data: DataFrame | tuple[tuple], flip=False):
        data = DataFrame(data) if not isinstance(data, DataFrame) else data
        self._data = data.iloc[::-1] if flip else data
        tf = self.time[1] - self.time[0]
        self.timeframe = TimeFrame.get(abs(tf))

    def __len__(self):
        return self._data.shape[0]

    def __contains__(self, item: Candle):
        return item.time == self[item.Index].time

    def __getitem__(self, index) -> CandleType | CandlesType:
        if isinstance(index, slice):
            cls = self.__class__
            data = self._data.iloc[index]
            data.reset_index(drop=True, inplace=True)
            return cls(data=data)

        item = self._data.iloc[index]
        return self.candle(Index=index, **item)

    def __getattr__(self, item):
        if item in {'Index', 'time', 'open', 'high', 'low', 'close', 'tick_volume', 'real_volume', 'spread', 'ema'}:
            return self._data[item]
        raise AttributeError(f'Attribute {item} not defined on class {self.__class__.__name__}')

    def __iter__(self):
        return (self.candle(**row._asdict()) for row in self._data.itertuples())

    async def get_ema(self, *, period: int):
        asyncio.to_thread(self._data.ta.ema, length=period, append=True)
        self._data.rename(columns={f"EMA_{period}": 'ema'}, inplace=True)
        return self

    @property
    def data(self) -> DataFrame:
        return self._data
