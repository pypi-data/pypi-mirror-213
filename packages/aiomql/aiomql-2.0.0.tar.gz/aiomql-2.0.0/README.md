# aiomql
![GitHub](https://img.shields.io/github/license/ichinga-samuel/aiomql?style=plastic)
![GitHub issues](https://img.shields.io/github/issues/ichinga-samuel/aiomql?style=plastic)
![PyPI](https://img.shields.io/pypi/v/aiomql)


## Installation
```bash
pip install aiomql
```

## Key Features
- Asynchronous Python Library For MetaTrader 5
- Build bots for trading in different financial markets using a bot factory
- Use threadpool executors to run multiple strategies on multiple instruments concurrently
- Record and keep track of trades and strategies in csv files.
- Utility classes for using the MetaTrader 5 Library
- Sample Pre-Built strategies

## Simple Usage as an asynchronous MetaTrader5 Libray
```python
import asyncio

# import the class
from aiomql import MetaTrader, Account, TimeFrame, OrderType


async def main():
    # Assuming your login details are already defined in the aiomql.json somewhere in your project directory. 
    acc = Account()
    
    # if this is unsuccessful the program exits
    await acc.initialize()
    
    # print all available symbols
    print(acc.symbols)

asyncio.run(main())
```
## As a Bot Building FrameWork using a Sample Strategy
```python
from aiomql import Bot
from aiomql import ForexSymbol
from aiomql.lib import FingerTrap

# Create a bot instance
bot = Bot()

# Choose a Symbol to trade
symbol = ForexSymbol(name='EURUSD')

# Create a strategy
ft_eur_usd = FingerTrap(symbol=symbol)

# Add strategy to Bot
bot.add_strategy(ft_eur_usd)

# run the bot
bot.execute()
```

see [docs](https://github.com/Ichinga-Samuel/aiomql/tree/master/docs)
