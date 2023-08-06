from abc import ABC, abstractmethod
from typing import TypeVar

from .order import Order
from .symbol import Symbol as _Symbol
from .account import Account

Symbol = TypeVar('Symbol', bound=_Symbol)


class Trader(ABC):
    """
    Helper class for creating a Trader object. Handles the initializing of an order and the placing of trades
    Args:
        symbol (Symbol): Financial instrument

    Attributes:

        symbol (Symbol): Financial instrument class Symbol class or any subclass of it.

        account (Account): Trading account

        order (Order): Trade order
    """

    def __init__(self, *, symbol: Symbol):
        self.symbol = symbol
        self.order = Order(symbol=symbol)
        self.account = Account()

    @abstractmethod
    async def create_order(self, *args, **kwargs):
        """
        Create an order, and update the order object initialized
        Args:
            *args:
            **kwargs:

        Returns:

        """

    @abstractmethod
    async def place_trade(self, *args, **kwargs):
        """
        Send trade to server
        Args:
            *args:
            **kwargs:
        """
