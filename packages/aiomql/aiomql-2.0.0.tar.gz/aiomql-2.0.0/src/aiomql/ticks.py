from typing import Union, TypeVar

from pandas import DataFrame, Series

from .core.constants import TickFlag


Self = TypeVar('Self', bound='Ticks')


class Tick:
    """
    Price Tick of a Financial Instrument or symbol.

    Notes: All initialization arguments are assumed to be class attributes.
    """
    def __init__(self, *, time: int, bid: float, ask: float, last: float, volume: float, time_msc: int, flags: TickFlag,
                 volume_real: float, Index: int = 0, **kwargs):
        self.time = time
        self.bid = bid
        self.ask = ask
        self.last = last
        self.volume = volume
        self.time_msc = time_msc
        self.flags = flags
        self.volume_real = volume_real
        self.Index = Index
        [setattr(self, key, value) for key, value in kwargs.items()]


class Ticks:
    """
    Container data class for price ticks. Arrange in chronological order.
    Supports iteration, slicing and assignment

    Args:
        data (DataFrame | tuple[tuple]): Dataframe of price ticks or a tuple of tuples

    Keyword Args:
        flip (bool): If flip is True reverse data argument.

    Attributes:
        data: Dataframe Object holding the ticks
    """
    time: Series
    bid: Series
    ask: Series
    last: Series
    volume: Series
    time_msc: Series
    flags: Series
    volume_real: Series
    Index: Series

    def __init__(self, *, data: DataFrame | tuple[tuple], flip=False):
        data: DataFrame = DataFrame(data) if not isinstance(data, DataFrame) else data
        self._data = data.iloc[::-1] if flip else data

    def __len__(self):
        return self._data.shape[0]

    def __contains__(self, item: Tick) -> bool:
        return item.time_msc == self[item.Index].time_msc

    def __getattribute__(self, item):
        if item in {'time', 'bid', 'ask', 'last', 'volume', 'time_msc', 'flags', 'volume_real', 'Index'}:
            return self._data[item]
        return super(Ticks, self).__getattribute__(item)

    def __getitem__(self, index) -> Tick | Self:
        if isinstance(index, slice):
            cls = self.__class__
            data = self._data.iloc[index]
            data.reset_index(drop=True, inplace=True)
            return cls(data=data)

        item = self._data.iloc[index]
        return Tick(Index=index, **item)

    def __iter__(self):
        return (Tick(**row._asdict()) for row in self._data.itertuples())

    @property
    def data(self) -> DataFrame:
        return self._data
