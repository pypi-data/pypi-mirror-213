import asyncio
from datetime import datetime
from pathlib import Path
import csv

from .history import History
from .core.config import Config


class Records:
    """
    This utility class read trade records from csv files, and update them based on their closing positions

    Keyword Args:
        records_dir (Path): Path to directory containing record of placed trades.

    Attributes:
        config: Config object

        records_dir(Path): Path to directory containing record of placed trades, If not given takes the default from the config
    """
    config: Config = Config()
    
    def __init__(self, records_dir: Path = ''):
        self.records_dir = records_dir or self.config.records_dir

    async def get_records(self):
        """
        get trade records from records_dir folder
        Returns:

        """
        for file in self.records_dir.iterdir():
            if file.is_file() and file.name.endswith('.csv'):
                yield file

    async def read_update(self, file: Path):
        """
        Read and update trade records

        Args:
            file: Trade record file

        Returns:

        """
        fr = open(file, mode='r', newline='')
        reader = csv.DictReader(fr)
        rows = [row for row in reader]
        rows = await self.update_rows(rows)
        fr.close()
        fw = open(file, mode='w', newline='')
        writer = csv.DictWriter(fw, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        fw.close()

    async def update_rows(self, rows: list[dict]) -> list[dict]:
        """
        Update the trade records with historical records
        Args:
            rows: A list of dictionaries from the dictionary writer object of the csv file.

        Returns:

        """
        start = float(min(rows, key=lambda r: r['time'])['time'])
        end = datetime.utcnow().timestamp()
        his = History(date_from=start, date_to=end)
        await his.init(orders=False)
        deals = {str(deal.position_id): deal.profit for deal in his.deals}
        for row in rows:
            if (deal := row['order']) in deals:
                profit = deals[deal]
                row.update(actual_profit=profit, win=profit > 0)
        return rows

    async def update_records(self):
        """
        Update trade records
        Returns:
        """
        records = [self.read_update(record) async for record in self.get_records()]
        await asyncio.gather(*records)

    async def update_record(self, file: Path | str):
        """
        Returns:

        """
        await self.read_update(file)
