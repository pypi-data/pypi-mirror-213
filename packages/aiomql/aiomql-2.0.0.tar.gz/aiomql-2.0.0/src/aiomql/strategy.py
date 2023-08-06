import asyncio
import time
from typing import Type, TypeVar
from abc import ABC, abstractmethod

import pandas_ta as ta

from .core.constants import TimeFrame
from .candle import Candles, Candle
from .symbol import Symbol as _Symbol
from .account import Account


Symbol = TypeVar('Symbol', bound=_Symbol)


class Strategy(ABC):
    """
    The base class for creating strategies.

    Keyword Args:
        symbol (Symbol): The Financial Instrument as a Symbol Object

        params (dict): Configurable parameters for running the strategy

    Attributes:
        Candle (Type[Candle]): Can be a subclass of the Candle class specific to the strategy and analysis carried out on it.

        Candles (Type[Candles]): Candles class for the strategy can be the same or a subclass of the "candle.Candles" class.

        name (str): A name for the strategy.

        symbol (Symbol): The Financial Instrument as a Symbol Object
    """
    Candle: Type[Candle] = Candle
    Candles: Type[Candles] = Candles
    name:  str = ""
    account = Account()

    def __init__(self, *, symbol: Symbol, params: dict = None):
        self.symbol = symbol
        self.parameters = params or {}
        self.parameters['symbol'] = symbol.name

    def __repr__(self):
        return f"{self.name}({self.symbol!r})"

    async def get_ema(self, *, time_frame: TimeFrame, period: int, count: int = 500) -> type(Candles):
        """
        Helper method that gets the ema of the bars.

        Keyword Args:
            time_frame (TimeFrame): Timeframe of the bars returned

            period (int): Period of the ema

            count (int): Number of objects to be returned

        Returns: A Candles Object
        """
        rates = await self.symbol.copy_rates_from_pos(timeframe=time_frame, count=count)
        await asyncio.to_thread(rates.data.ta.ema, length=period, append=True)
        rates.data.rename(columns={f"EMA_{period}": 'ema'}, inplace=True)
        return self.Candles(data=rates.data)

    @staticmethod
    async def sleep(secs: float):
        """
        Sleep for the needed amount of seconds between requests to the terminal
        Args:
            secs (float): The time period of the requests, eg. when trading on the 5 minute time frame the value will be 300 secs

        Returns: None.

        """
        mod = time.time() % secs
        secs = secs - mod if mod != 0 else mod
        await asyncio.sleep(secs)

    @abstractmethod
    async def trade(self):
        """
        Place trades using this method
        Returns:

        """
