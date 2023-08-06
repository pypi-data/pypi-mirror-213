import asyncio
from typing import Type, Iterable, TypeVar
import logging

from .executor import Executor
from .account import Account
from .symbol import Symbol as _Symbol
from .strategy import Strategy as _Strategy

logger = logging.getLogger()
Strategy = TypeVar('Strategy', bound=_Strategy)
Symbol = TypeVar('Symbol', bound=_Symbol)


class Bot:
    """
    Bot builder class

    Attributes:
        account (Account): Account Object.
        executor: The default thread executor.
        symbols (set[Symbols]): A set of symbols for the trading session
    """
    account: Account = Account()
    executor = Executor()
    symbols = set()

    async def start(self):
        await self.account.initialize()
        logger.info("Login Successful")
        await self.init_symbols()
        self.executor.remove_workers(*self.symbols)

    def execute(self):
        asyncio.run(self.start())
        self.executor.execute()

    def add_strategy(self, strategy: Strategy):
        """
        Add a strategy to the executor. Will only be successfully if the symbol is in the list of successfully
        initialized symbols
        
        Args:
            strategy: Strategy to run on bot

        Returns:
            Notes: Make sure the symbol has been added to the market

        """
        self.symbols.add(strategy.symbol)
        self.executor.add_worker(strategy)

    def add_strategies(self, strategies: Iterable[Strategy]):
        """
        Add multiple strategies at the same time
        
        Args:
            strategies: A list of strategies

        Returns:
        """
        [self.add_strategy(strategy) for strategy in strategies]

    def add_strategy_all(self, *, strategy: Type[Strategy], params: dict | None = None):
        """
        Use this to run a strategy on all available instruments in the market using the default parameters i.e one set
        of parameters for all trading symbols

        Keyword Args:
            strategy: Strategy class

            params: A dictionary of parameters for the strategy

        Returns:

        """
        [self.add_strategy(strategy(symbol=symbol, params=params)) for symbol in self.symbols]

    async def init_symbols(self):
        """
        Initialize the symbols for the current trading session

        Returns: None
        """
        syms = [self.init_symbol(symbol) for symbol in self.symbols]
        await asyncio.gather(*syms, return_exceptions=True)

    async def init_symbol(self, symbol: Symbol) -> Symbol:
        """
        Initialize symbol before the beginning of a trading sessions

        Args:
            symbol: Symbol object to be initialized

        Returns:
            symbol: if successfully initialized

        """
        if self.account.has_symbol(symbol):
            init = await symbol.init()
            if init:
                return symbol
            self.symbols.remove(symbol)
            logger.warning(f'Unable to initialize symbol {symbol}')

        self.symbols.remove(symbol)
        logger.warning(f'{symbol} not a available for this market')
