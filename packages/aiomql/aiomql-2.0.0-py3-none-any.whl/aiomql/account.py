from logging import getLogger

from .core.models import AccountInfo, SymbolInfo
from .terminal import Terminal


logger = getLogger()


class Account(AccountInfo):
    """
    Properties and methods of the current trading account. A Subclass of AccountInfo.
    This is a singleton class so you can only use one account at a time.
    
    Args:
        kwargs: Arguments for AccountInfo attributes

    Attributes:
        risk (float): Percentage of account to risk
        risk_to_reward (float): ratio of risk to reward
        connected (float):

    Notes:
        Other Account properties are defined in the AccountInfo Object
        Since bot can only use one account at a time use the account class as a module style singleton object by
        importing the account object declared
        in this module instead of creating a new object.
    """
    risk: float = 0.05
    risk_to_reward: float = 2
    connected: bool
    terminal = Terminal()
    symbols = set()
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        acc_info = self.config.account_info()
        kw = acc_info | kwargs
        super().__init__(**kw)

    async def refresh(self):
        """
        Update the account info object with the latest values from the terminal
        
        Returns:
            Account: The Account Object with updated properties

        """
        account_info = await self.mt5.account_info()
        acc = account_info._asdict()
        self.set_attributes(**acc)

    @property
    def account_info(self) -> dict:
        """
        Obtains a dictionary representing login details.

        Returns: a dict of login, server and password information

        """
        acc_info = self.get_dict(include={'login', 'server', 'password'})
        return acc_info

    async def sign_in(self):
        """
        Make sure account_number, password and server attributes have been initialized
        Returns: True if login was successful else False

        """
        self.connected = await self.mt5.login(**self.account_info)
        if self.connected:
            await self.refresh()
            self.symbols = await self.terminal.symbols_get()
            return self.connected
        await self.terminal.shutdown()

    def has_symbol(self, symbol):
        try:
            symbol = SymbolInfo(name=symbol) if isinstance(symbol, str) else symbol
            return symbol in self.symbols
        except Exception as err:
            logger.warning(f'Error: {err}; {symbol} not available in this market')
            return False

    async def initialize(self):
        """

        Returns:

        """
        await self.terminal.initialize()
        return await self.sign_in()


