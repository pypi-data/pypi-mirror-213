from typing import NamedTuple
from logging import getLogger
from .core.models import TerminalInfo, Error, SymbolInfo

logger = getLogger()


class Terminal(TerminalInfo):

    """
    Terminal related functions and properties

    Keyword Args:
        mt5 (MetaTrader): The Meta trader object for connecting to the terminal. Default Keyword Argument
        
    Attributes:
        version: Namedtuple of terminal version values

    Notes:
        Other attributes are defined in the TerminalInfo Class
    """

    Version = NamedTuple("Version", (('version', str), ('build', int), ('release_date', str)))

    async def initialize(self) -> bool:
        """
        Establish a connection with the MetaTrader 5 terminal. There are three call options.
        Call without parameters. The terminal for connection is found automatically.
        Call specifying the path to the MetaTrader 5 terminal we want to connect to. word path as a keyword argument
        Call specifying the trading account path and parameters i.e login, password, server, as keyword arguments, path can be omitted.

        Returns:
            (bool): True if successful else False
        """
        self.connected = await self.mt5.initialize(**self.config.account_info())

        if not self.connected:
            err = await self.mt5.last_error()
            msg = f'Failed to initialize Terminal. Error Code: {err}'
            logger.critical(msg)
            raise SystemExit

        return self.connected

    async def shutdown(self):
        """
        Close the previously established connection to the MetaTrader 5 terminal.

        Returns: None
        """
        await self.mt5.shutdown()

    @property
    async def version(self):
        """
        Get the MetaTrader 5 terminal version.
        This method returns the terminal version, build and release date as a tuple of three values

        Returns:
            Version: version of tuple as Version object
        """
        res = await self.mt5.version()
        return self.Version(*res)

    async def info(self):
        """
        Get the connected MetaTrader 5 client terminal status and settings. gets terminal info in the form of a named tuple structure (namedtuple).
        Return None in case of an error. The info on the error can be obtained using last_error().

        Returns:
             (Terminal): Terminal status and settings as a terminal object.
        """
        info = await self.mt5.terminal_info()
        self.set_attributes(**info._asdict())
        return self

    async def symbols_total(self) -> int:
        """
        Get the number of all financial instruments in the MetaTrader 5 terminal.

        Returns:
            int: Total number of available symbols
        """
        return await self.mt5.symbols_total()

    async def symbols_get(self, group="") -> set[SymbolInfo]:
        """
        Get all financial instruments from the MetaTrader 5 terminal.
        Keyword Args:
            group (str): The filter for arranging a group of necessary symbols. Optional parameter. If the group is specified, the function returns
            only symbols meeting a specified criteria.

        Returns:
            Iterator[Symbol]: A set of available symbols.

        Notes: The group parameter allows sorting out symbols by name. '*' can be used at the beginning and the end of a string. The group parameter
            can be used as a named or an unnamed one. Both options work the same way. The named option (group="GROUP") makes the code easier to read.
            The group parameter may contain several comma separated conditions. A condition can be set as a mask using '*'. The logical negation
            symbol '!' can be used for an exclusion. All conditions are applied sequentially, which means conditions of including to a group should be
            specified first followed by an exclusion condition. For example, group="*, !EUR" means that all symbols should be selected first
            and the ones containing "EUR" in their names should be excluded afterwards.
        """
        syms = await self.mt5.symbols_get(group=group)
        return {SymbolInfo(name=sym.name) for sym in syms}

    async def last_error(self) -> Error:
        """
        Return data on the last error.

        Returns:
            ErrorCode: Last error as ErrorCode object
        """
        res = await self.mt5.last_error()
        return Error(*res)


terminal = Terminal()
