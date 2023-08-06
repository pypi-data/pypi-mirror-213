from functools import cache
from typing import Mapping, Iterable
from logging import getLogger

from .config import Config
from .meta_trader import MetaTrader

logger = getLogger()


class Base:
    """
    Base class for data model with setup and data accessing functionalities.
    Attributes defined on the class body with type annotations help with type hinting and initializing the attribute.

    Args:
        **kwargs: Object attributes and values as keyword arguments

    Attributes:
        mt5 (ClassVar, MetaTrader): The MetaTrader Instance

        config (ClassVar, Config): Singleton class Variable
    """
    mt5: MetaTrader = MetaTrader()
    config = Config()

    def __init__(self, **kwargs):
        self.set_attributes(**kwargs)

    def __repr__(self):
        values = ', '.join(f"{name}={value!r}" for name, value in self.__dict__.items())
        return f"{self.__class__.__name__}({values})"

    def set_attributes(self, **kwargs):
        """
        Set keyword arguments as object attributes
        
        Args:
            **kwargs: Object attributes and values as keyword arguments

        Raises:
            AttributeError: When assigning an attribute that does not belong to the class or any parent class

        Notes:
            Only sets attributes that have been annotated on the class body.
        """
        for i, j in kwargs.items():
            try:
                setattr(self, i, self.annotations[i](j))
            except KeyError:
                logger.warning(f"Attribute {i} does not belong to class {self.__class__.__name__}")
                continue
            except Exception as exe:
                logger.warning(f'Did not set attribute {i} on class {self.__class__.__name__} due to {exe}')
                continue

    @property
    @cache
    def annotations(self) -> dict:
        """
        Returns annotations defined on the class body and it's parent classes as dictionary

        Returns:
            annotations (dict): dictionary of annotations

        """
        annots = {}
        for base in self.__class__.__mro__[-3::-1]:
            annots |= getattr(base, '__annotations__', {})
        return annots

    def get_dict(self, exclude: set = None, include: set = None) -> dict:
        """
        Returns class attributes as a dict, with the ability to filter

        Keyword Args:
            exclude: A set of attributes to be excluded
            include: Specific attributes to be returned

        Returns:
             dict: A dictionary of specified class attributes

        Notes:
            You can only set either of include or exclude.
            If you set both, include will take precedence

        """
        exclude, include = exclude or set(), include or set()
        filter_ = include or set(self.dict.keys()).difference(exclude)
        return {key: value for key, value in self.dict.items() if key in filter_}

    @property
    @cache
    def class_vars(self):
        """
        Annotated class attributes

        Returns:
            A dictionary of available class attributes

        """
        return {key: value for key, value in self.__class__.__dict__.items() if key in self.__class__.__annotations__}

    @property
    def dict(self) -> dict:
        """
        All instance and class attributes as a dictionary, except those in the "Config.except" set

        Returns:
            dict: A dictionary of instance and class attributes
        """
        try:
            return {key: value for key, value in (self.__dict__ | self.class_vars).items() if key not in self.Config.filter}
        except Exception as err:
            logger.warning(err)

    @dict.setter
    def dict(self, value: Mapping | Iterable[Iterable]):
        """
        Update the dict property
        Args:
            value (Mapping | Iterable[Iterable]): Value should be a mapping or iterable of key value pairs

        Returns:

        """
        self.dict.update(value)

    class Config:
        """
        Config Object of the class

        Attributes:
            exclude (set): A set of default attributes that will be excluded from the dict property
            include (set): A set of default attributes that should always be include
        """
        exclude = {'mt5', "Config"}
        include = set()
        
        @classmethod
        @property
        def filter(cls) -> set:
            """
            Returns:

            """
            return cls.exclude.difference(cls.include)
        