import asyncio
from abc import ABC, abstractmethod
import csv
from logging import getLogger

from .core.config import Config

logger = getLogger()


class Result(ABC):
    """
    An abstract base Class for handling trade results and strategy parameters for record keeping and reference purpose
        result (OrderSendResult): OrderSendResult object of an executed trade
        request (Order | dict): Order object or a dict of trade order request properties
        parameters (dict): The parameters of the strategy placing the trade
        time (float): Timestamp of when order was placed
        name: Name  of strategy or any desired name for the result csv file
    Attributes:
        config: The configuration object
        name: Any desired name for the result csv file

    Notes:
        To enable saving trades as csv file. Make sure that config.record_trades is True
    """
    config = Config()

    def __init__(self, name: str):
        self.name = name

    @property
    @abstractmethod
    def data(self) -> dict:
        """
        A dict representing data to be saved in the csv file.
        Returns (dict): A dict of data to be saved
        """

    async def to_csv(self):
        """
        Record trade results and associated parameters as a csv file
        """
        try:
            file = self.config.records_dir / f"{self.name}.csv"
            exists = file.exists()
            with open(file, 'a', newline='') as fh:
                writer = csv.DictWriter(fh, fieldnames=sorted(list(self.data.keys())), extrasaction='ignore', restval=None)
                if not exists:
                    writer.writeheader()
                writer.writerow(self.data)
        except Exception as err:
            logger.error(f'Error: {err}. Unable to save trade results')

    async def save(self):
        loop = asyncio.get_running_loop()
        asyncio.run_coroutine_threadsafe(self.to_csv(), loop)
