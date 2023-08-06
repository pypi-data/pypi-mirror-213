from datetime import datetime
from logging import getLogger
from .core.constants import TimeFrame, CopyTicks
from .core.models import SymbolInfo, BookInfo
from .ticks import Tick, Ticks
from .candle import Candles
from .account import Account
logger = getLogger()


class Symbol(SymbolInfo):
    """
    Helper class with general properties and methods of a financial instrument.
    You can inherit from this class and add your own properties and methods.
    This class subclass of SymbolInfo which contains all symbol properties.
    All methods of this class accept keyword only arguments.

    Keyword Args:
        mt5: Platform, defaults to the MetaTrader5 class.

    Attributes:
        tick (Tick): Price tick object for instrument

    Notes:
        Full properties are on the SymbolInfo Object.
        Make sure Symbol is always initialized with a name argument
    """
    tick: Tick
    account = Account()

    async def info_tick(self, *, name: str = "") -> Tick | None:
        """
        Get Price Tick of the financial instrument
        Args:
            name: if name is supplied get price tick of that financial instrument

        Returns:
            Tick: Returns a Custom Tick Object
        """
        tick = await self.mt5.symbol_info_tick(name or self.name)

        if tick is None:
            err = await self.mt5.last_error()
            logger.warning(f'Could not get tick for {name or self.name}. Error Code: {err}')
            return

        tick = Tick(**tick._asdict())
        setattr(self, 'tick', tick) if not name else ...
        return tick

    async def symbol_select(self, *, enable: bool = True) -> bool:
        """
        Select a symbol in the MarketWatch window or remove a symbol from the window.
        Update the select property

        Args:
            enable (bool): Switch. Optional unnamed parameter. If 'false', a symbol should be removed from the MarketWatch window.
                Otherwise, it should be selected in the MarketWatch window. A symbol cannot be removed if open charts with this symbol are currently
                present or positions are opened on it.

        Returns:
            bool: True if successful, otherwise – False.
        """
        self.select = await self.mt5.symbol_select(self.name, enable)
        return self.select

    async def info(self) -> SymbolInfo | None:
        """
        Get data on the specified financial instrument and update the symbol object properties

        Returns:
            (SymbolInfo | None): SymbolInfo if successful else None
        """
        
        info = await self.mt5.symbol_info(self.name)
        if info:
            self.set_attributes(**info._asdict())
            return SymbolInfo(**info._asdict())

        err = await self.mt5.last_error()
        raise ValueError(f'{err}. Unable to obtain info for {self.name}.')

    async def init(self) -> bool:
        """
        Initialized the symbol by pulling properties from the terminal

        Returns:
             bool: Returns True if symbol info was successful initialized
        """
        try:
            if await self.symbol_select():
                await self.book_add()
                await self.info()
                return True

            logger.warning(f'Unable to initialized symbol {self}')
            return False
        except Exception as err:
            logger.warning(err)
            return False

    async def book_add(self) -> bool:
        """
        Subscribes the MetaTrader 5 terminal to the Market Depth change events for a specified symbol.
        If the symbol is not in the list of instruments for the market, This method will return False

        Args:
            symbol (str): financial instrument name

        Returns: True if successful, otherwise – False.

        """
        return await self.mt5.market_book_add(self.name)

    async def book_get(self) -> BookInfo:
        """
        Returns a tuple from BookInfo featuring Market Depth entries for the specified symbol.

        Keyword Args:
            symbol (str): financial instrument name

        Returns (BookInfo | None): Returns the Market Depth content as a BookInfo Object else None

        """
        info = await self.mt5.market_book_get(self.name)
        return BookInfo(**info._asdict())

    async def book_release(self) -> bool:
        """
        Cancels subscription of the MetaTrader 5 terminal to the Market Depth change events for a specified symbol.
        Args:
            symbol: financial instrument name

        Returns:
            bool: True if successful, otherwise – False.

        """
        return await self.mt5.market_book_release(self.name)

    async def currency_conversion(self, *, amount: float, base: str, quote: str) -> float:
        """
        Convert from one currency to the other.
        Args:
            amount: amount to convert given in terms of the quote currency
            base: The base currency of the pair
            quote: The quote currency of the pair

        Returns: Amount in terms of the quote currency or None if it failed to convert
        Raises: ValueError if conversion is impossible
        """
        pair = f'{base}{quote}'
        if self.account.has_symbol(pair):
            tick = await self.info_tick(name=pair)
            if tick is not None:
                return amount / tick.ask

        pair = f'{quote}{base}'
        if self.account.has_symbol(pair):
            tick = await self.info_tick(name=pair)
            if tick is not None:
                amount = amount * tick.bid
                return amount
        logger.warning(f'Currency conversion failed: Unable to convert {amount} in {quote} to {base}')

        raise ValueError('Currency Conversion Failed')

    @property
    def pip(self) -> float:
        """

        Returns:

        """
        if self.digits == 5:
            return self.point * 10
        else:
            return self.point

    async def copy_rates_from(self, *, timeframe: TimeFrame, date_from: datetime | int, count: int) -> Candles | None:
        """
        Get bars from the MetaTrader 5 terminal starting from the specified date.

        Args:
            timeframe (TimeFrame): Timeframe the bars are requested for. Set by a value from the TimeFrame enumeration. Required unnamed parameter.

            date_from (datetime | int): Date of opening of the first bar from the requested sample. Set by the 'datetime' object or as a number
                of seconds elapsed since 1970.01.01. Required unnamed parameter.

            count (int): Number of bars to receive. Required unnamed parameter.

        Returns:
            Candles: Returns a Candles class object as a collection of rates ordered chronologically.
            None: Return None if there is an error
        """
        rates = await self.mt5.copy_rates_from(self.name, timeframe, date_from, count)
        return Candles(data=rates) if rates is not None else None

    async def copy_rates_from_pos(self, *, timeframe: TimeFrame, count: int = 500, start_position: int = 0) -> Candles | None:
        """
        Get bars from the MetaTrader 5 terminal starting from the specified index.

        Args:
            timeframe (TimeFrame): TimeFrame value from TimeFrame Enum. Required keyword only parameter

            count (int): Number of bars to return. Keyword argument defaults to 500

            start_position (int): Initial index of the bar the data are requested from. The numbering of bars goes from present to past.
                Thus, the zero bar means the current one. Keyword argument defaults to 0.

        Returns:
             Candles: Returns a Candles class object as a collection of rates ordered chronologically.
             None: Return None if there is an error
        """
        rates = await self.mt5.copy_rates_from_pos(self.name, timeframe, start_position, count)
        return Candles(data=rates) if rates is not None else None

    async def copy_ticks_from(self, *, date_from: datetime | int, count: int = 100, flags: CopyTicks = CopyTicks.ALL) -> Ticks | None:
        """
        Get ticks from the MetaTrader 5 terminal starting from the specified date.

        Args: date_from (datetime | int): Date the ticks are requested from. Set by the 'datetime' object or as a
        number of seconds elapsed since 1970.01.01.

            count (int): Number of requested ticks. Defaults to 100

            flags (CopyTicks): A flag to define the type of the requested ticks from CopyTicks enum. INFO is the default

        Returns:
             Ticks: Returns a Ticks class object as a collection of ticks ordered chronologically.
             None: Return None if there is an error
        """
        ticks = await self.mt5.copy_ticks_from(self.name, date_from, count, flags)
        return Ticks(data=ticks) if ticks is not None else None

    async def copy_rates_range(self, *, timeframe: TimeFrame, date_from: datetime | int, date_to: datetime | int) -> Candles | None:
        """
        Get bars in the specified date range from the MetaTrader 5 terminal.

        Args:
            timeframe (TimeFrame): Timeframe the bars are requested for. Set by a value from the TimeFrame enumeration. Required unnamed parameter.

            date_from (datetime | int): Date the bars are requested from. Set by the 'datetime' object or as a number of seconds
                elapsed since 1970.01.01. Bars with the open time >= date_from are returned. Required unnamed parameter.

            date_to (datetime | int): Date, up to which the bars are requested. Set by the 'datetime' object or as a number of
                seconds elapsed since 1970.01.01. Bars with the open time <= date_to are returned. Required unnamed parameter.

        Returns:
            Candles: Returns a Candles class object as a collection of rates ordered chronologically.
            None: Return None if there is an error
        """
        rates = await self.mt5.copy_rates_range(symbol=self.name, timeframe=timeframe, date_from=date_from, date_to=date_to)
        return Candles(data=rates) if rates is not None else None

    async def copy_ticks_range(self, *, date_from: datetime | int, date_to: datetime | int, flags: CopyTicks = CopyTicks.ALL) -> Ticks | None:
        """
        Get ticks for the specified date range from the MetaTrader 5 terminal.
        Args:
            date_from: Date the bars are requested from. Set by the 'datetime' object or as a number of seconds elapsed since 1970.01.01. Bars with
                the open time >= date_from are returned. Required unnamed parameter.

            date_to: Date, up to which the bars are requested. Set by the 'datetime' object or as a number of seconds elapsed since 1970.01.01. Bars
                with the open time <= date_to are returned. Required unnamed parameter.
                
            flags (CopyTicks):

        Returns:
            Ticks: Returns a Ticks class object as a collection of ticks ordered chronologically.
            None: Return None if there is an error
        """
        ticks = await self.mt5.copy_ticks_range(self.name, date_from, date_to, flags)
        return Ticks(data=ticks) if ticks is not None else None
