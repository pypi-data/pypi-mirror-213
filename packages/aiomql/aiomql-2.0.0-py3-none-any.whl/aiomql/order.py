from .core.models import TradeRequest, OrderSendResult, OrderCheckResult, TradeOrder
from .core.constants import TradeAction, OrderTime, OrderFilling


class Order(TradeRequest):
    """
    Trade order related functions and properties. Subclass of TradeRequest.

    Keyword Args:
        kwargs: Arguments for initializing the order object

    Attributes:
        action (TradeAction): Trading operation type from TradeAction Enum

        type_time (OrderTime):  Order type by expiration from OrderTime

        type_filling (OrderFilling): Order filling type from OrderFilling Enum

    Notes:
        Other order properties are defined in the TradeRequest Object
    """
    action: TradeAction = TradeAction.DEAL
    type_time: OrderTime = OrderTime.SPECIFIED_DAY
    type_filling: OrderFilling = OrderFilling.FOK
    total: int = 0
    orders: list[TradeOrder]

    async def orders_total(self):
        """
        Get the number of active orders. Update the total property

        Returns:
            int: Number of active orders
        """
        self.total = await self.mt5.orders_total()
        return self.total

    async def orders_get(self, *, symbol="", group="", ticket=0):
        """
        Get active orders with the ability to filter by symbol or ticket. There are three call options.
        Call without parameters. Return active orders on all symbols

        Keyword Args:
            symbol (str): Symbol name. Optional named parameter. If a symbol is specified, the ticket parameter is ignored.

            group (str): The filter for arranging a group of necessary symbols. Optional named parameter. If the group is specified, the function
                returns only active orders meeting a specified criteria for a symbol name.

            ticket (int): Order ticket (ORDER_TICKET). Optional named parameter.

        Returns:
            list[TradeOrder]: A list of active trade orders as TradeOrder objects

        """
        orders = await self.mt5.orders_get(group=group, ticket=ticket, symbol=symbol)
        self.orders = [TradeOrder(**order._asdict()) for order in orders]
        return self.orders

    async def check(self) -> OrderCheckResult:
        """
        Check funds sufficiency for performing a required trading operation

        Returns:
            (OrderCheckResult): Returns OrderCheckResult object
        """
        res = await self.mt5.order_check(self.dict)
        return OrderCheckResult(**res._asdict())

    async def send(self) -> OrderSendResult:
        """
        Send a request to perform a trading operation from the terminal to the trade server.

        Returns:
             OrderSendResult: Returns OrderSendResult object
        """
        res = await self.mt5.order_send(self.dict)
        return OrderSendResult(**res._asdict())

    async def calc_margin(self) -> float | None:
        """
        Return margin in the account currency to perform a specified trading operation.

        Returns:
            float: Returns float value if successful
            None: If not successful
        """
        return await self.mt5.order_calc_margin(self.type, self.symbol, self.volume, self.price)

    async def calc_profit(self) -> float | None:
        """
        Return profit in the account currency for a specified trading operation.
        Returns:
            float: Returns float value if successful
            None: If not successful
        """
        return await self.mt5.order_calc_profit(self.type, self.symbol, self.volume, self.price, self.tp)
