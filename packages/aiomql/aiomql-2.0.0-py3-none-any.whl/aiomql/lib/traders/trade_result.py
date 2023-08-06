from ...result import Result
from ...order import OrderSendResult
from pprint import pprint as pp


class TradeResult(Result):
    def __init__(self, *, result: OrderSendResult, parameters: dict, name: str = ''):
        """
        Args:
            result:
            parameters:
            name:
        """
        self.result = result.get_dict(exclude={'retcode', 'retcode_external', 'request_id', 'request'})
        self.parameters = parameters.copy()
        name = name or self.parameters.get('name', '')
        super().__init__(name)
        print(self.name, self.parameters.get('symbol'))

    @property
    def data(self) -> dict:
        """
        Merge the result and parameters dict to return unified data dict.

        Returns: The data dict

        """
        self.parameters.pop('name') if 'name' in self.parameters else ...
        return self.parameters | self.result | {'actual_profit': 0, 'closed': False, 'win': False}
