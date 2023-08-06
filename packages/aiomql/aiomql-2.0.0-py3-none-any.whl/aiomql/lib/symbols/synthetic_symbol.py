from math import ceil, log10

from ...symbol import Symbol


class SyntheticSymbol(Symbol):
    async def get_sl_tp_volume(self, *, amount: float, risk_to_reward: float, points: float):
        """
        Calculate the required stop_loss, take_profit and volume given an amount, a risk to reward factor and the
        desired points to capture.

        Keyword Args:
            amount (float):
            risk_to_reward:
            points:

        Returns:

        """
        volume = (points * self.point) / amount
        step = ceil(abs(log10(self.volume_step)))
        volume = round(volume, step)

        if (volume < self.volume_min) or (volume > self.volume_max):
            raise ValueError(f'Incorrect Volume. Computed Volume: {volume}; Symbol Max Volume: {self.volume_max}; '
                             f'Symbol Min Volume: {self.volume_min}')

        return (sl := amount / volume), sl * risk_to_reward, volume
