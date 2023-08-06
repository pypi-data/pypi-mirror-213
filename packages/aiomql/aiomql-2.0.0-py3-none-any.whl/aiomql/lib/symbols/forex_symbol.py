from math import ceil, log10

from ...symbol import Symbol


class ForexSymbol(Symbol):
    async def get_sl_tp_volume(self, *, amount: float, risk_to_reward: float, points: float):
        """

        Args:
            amount: Amount in account currency
            risk_to_reward: The risk to reward ratio
            points:

        Returns:

        """
        if (base := self.currency_profit) != (quote := self.account.currency):
            amount = await self.currency_conversion(amount=amount, base=base, quote=quote)

        vpp = amount / points  # value per point
        volume = vpp / (self.point * 1e5)
        step = ceil(abs(log10(self.volume_step)))
        volume = round(volume, step)

        if (volume < self.volume_min) or (volume > self.volume_max):
            raise ValueError(f'Incorrect Volume. Computed Volume: {volume}; Symbol Max Volume: {self.volume_max}; '
                             f'Symbol Min Volume: {self.volume_min}')

        rsl = self.point * points
        stop_loss, take_profit = rsl, rsl * risk_to_reward
        return stop_loss, take_profit, volume
