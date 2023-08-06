import logging
from datetime import datetime

from ...utils import dict_to_string
from ...trader import Trader
from ...core.constants import OrderType

from .trade_result import TradeResult

logger = logging.getLogger()


class DealTrader(Trader):

    async def create_order(self, order: OrderType, points: float):
        """
        Using the number of target pips determines the lot size
        Args:
            order (OrderType): Type of order
            points (float): Number of pips

        Returns:

        """
        await self.account.refresh()
        amount = self.account.margin_free * self.account.risk
        sl, tp, volume = await self.symbol.get_sl_tp_volume(amount=amount, risk_to_reward=self.account.risk_to_reward,
                                                            points=points)
        self.order.volume = volume
        self.order.type = order
        await self.set_order_limits(sl, tp)

    async def set_order_limits(self, sl, tp):
        tick = await self.symbol.info_tick()
        if self.order.type == OrderType.BUY:
            self.order.sl, self.order.tp = tick.ask - sl, tick.ask + tp
            self.order.price = tick.ask
        else:
            self.order.sl, self.order.tp = tick.bid + sl, tick.bid - tp
            self.order.price = tick.bid

    async def place_trade(self, order: OrderType, points: float, params):
        try:
            await self.create_order(order=order, points=points)
            check = await self.order.check()
            if check.retcode != 0:
                logger.warning(f"Symbol: {self.order.symbol}\nResult:\n{dict_to_string(check.get_dict(include={'comment', 'retcode'}), multi=True)}")
                return

            result = await self.order.send()
            if result.retcode != 10009:
                logger.warning(f"Symbol: {self.order.symbol}\nResult:\n{dict_to_string(result.get_dict(include={'comment', 'retcode'}), multi=True)}")
                return

            params['date'] = (date := datetime.utcnow())
            params['time'] = date.timestamp()
            logger.info(f"Symbol: {self.order.symbol}\nOrder: {dict_to_string(result.dict, multi=True)}\n")
            self.order.set_attributes(**result.get_dict(include={'price', 'volume'}))
            result.profit = await self.order.calc_profit()
            await TradeResult(result=result, parameters=params).save()
            # await results.save()
            return

        except Exception as err:
            logger.error(f"{err}. Symbol: {self.order.symbol}\n {self.__class__.__name__}place trade")
