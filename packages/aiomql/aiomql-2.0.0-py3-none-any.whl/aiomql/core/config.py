import os
from pathlib import Path
from sys import _getframe
from typing import Iterator
import json
from logging import getLogger

logger = getLogger()


class Config:
    """
    Set config variables for your bot
    Keyword Args:
        file (str): config file
        record_trades (bool): If true record trade in a csv file defaults to True
        filename (str): Name of config file, defaults to "mt5.json"
        records_dir(str): Name of directory for saving trades, defaults to trade records
        win_percentage (float): Percentage of expected profit that counts as a win
        base_dir (str | Path): Base directory for saving outputs.

    Attributes:
        file (str):
        record_trades (bool):
        filename (str):
        records_dir (str):
        win_percentage (float):
        base_dir (str | Path):
        account_number (int): Broker account number for
        password (str): Broker password
        server (str): Broker server
        path (str): Path to terminal file
    """
    login: int = 0
    password: str = ""
    server: str = ""
    path: str = ""
    timeout: int = 60000
    record_trades: bool = True
    filename: str = "aiomql.json"
    file = None
    win_percentage: float = 0.85
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, **kwargs):
        self.set_attributes(**kwargs)
        self.records_dir = Path.home() / 'Documents' / 'Aiomql' / 'Trade Records'
        self.records_dir.mkdir(parents=True, exist_ok=True)
        self.load_config()
    
    @staticmethod
    def walk_to_root(path: str) -> Iterator[str]:
        
        if not os.path.exists(path):
            raise IOError('Starting path not found')
        
        if os.path.isfile(path):
            path = os.path.dirname(path)
        
        last_dir = None
        current_dir = os.path.abspath(path)
        while last_dir != current_dir:
            yield current_dir
            parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
            last_dir, current_dir = current_dir, parent_dir
    
    def find_config(self):
        current_file = __file__
        frame = _getframe()
        while frame.f_code.co_filename == current_file:
            if frame.f_back is None:
                return None
            frame = frame.f_back
        frame_filename = frame.f_code.co_filename
        path = os.path.dirname(os.path.abspath(frame_filename))
        
        for dirname in self.walk_to_root(path):
            check_path = os.path.join(dirname, self.filename)
            if os.path.isfile(check_path):
                return check_path
        return None
    
    def load_config(self, file: str = None):
        if (file := (file or self.find_config())) is None:
            logger.warning('No Config File Found')
            return
        fh = open(file, mode='r')
        data = json.load(fh)
        fh.close()
        [setattr(self, key, value) for key, value in data.items()]

    def account_info(self) -> dict['login', 'password', 'server']:
        """
           Returns Account Info as found in the config object if available

           Returns (dict): A dictionary of account properties
        """
        return {'login': self.login, 'password': self.password, 'server': self.server}
    
    def set_attributes(self, **kwargs):
        """
        Add attributes to the config object
        Args:
            **kwargs: Set attributes as keyword arguments

        Returns:

        """
        [setattr(self, i, j) for i, j in kwargs.items()]
