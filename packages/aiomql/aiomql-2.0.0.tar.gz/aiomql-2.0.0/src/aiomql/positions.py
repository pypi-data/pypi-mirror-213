import asyncio

from .core.meta_trader import MetaTrader
from .core.models import TradePosition
from .core.constants import TradeAction, OrderType
from .order import Order


class Positions:
    """
    Hold open positions related properties and objects

    Keyword Args:
        symbol (str): Financial instrument name
        group (str): The filter for arranging a group of necessary symbols. Optional named parameter. If the group is specified, the function returns
                     only positions meeting a specified criteria for a symbol name.
        ticket (int): Position ticket

    Attributes:
        symbol (str): Financial instrument name

        group (str): The filter for arranging a group of necessary symbols. Optional named parameter. If the group is specified, the function returns
                     only positions meeting a specified criteria for a symbol name.

        ticket (int): Position ticket

        positions (list[TradePosition]): A list of trade positions

        total_positions (int):
    """
    mt5: MetaTrader = MetaTrader()
    total_positions: int = 0
    positions: list[TradePosition] = []
    
    def __init__(self, *, symbol: str = "", group: str = "", ticket: int = 0):
        self.symbol = symbol
        self.group = group
        self.ticket = ticket

    async def positions_total(self) -> int:
        """
        Get open positions with the ability to filter by symbol or ticket.
        
        Returns (int): Return integer value

        """
        self.total_positions = await self.mt5.positions_total()
        return self.total_positions

    async def positions_get(self):
        """
        Get open positions with the ability to filter by symbol or ticket.
        
        Returns:
            list[TradePosition]: A list of open trade positions

        """
        positions = await self.mt5.positions_get(group=self.group, symbol=self.symbol, ticket=self.ticket)
        self.positions = [TradePosition(**pos._asdict()) for pos in positions]
        return self.positions

    async def close_all(self) -> int:
        """
        Close all open positions
        
        Returns (int): Return number of positions closed.
        """
        orders = [Order(action=TradeAction.DEAL, price=pos.price_current, position=pos.ticket,
                        type=OrderType(pos.type).opposite,
                        **pos.get_dict(include={'symbol', 'volume'})) for pos in (await self.positions_get())]

        results = await asyncio.gather(*[order.send() for order in orders])
        amount_closed = len([res for res in results if res.retcode == 10009])
        await self.positions_total()
        return amount_closed
