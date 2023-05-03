from pandas import DataFrame

class Strategy:
    def __init__(self, ticker_data: DataFrame):
        self.ticker_data = ticker_data
        self.__buy_quantity = 0
        self.__sell_quantity = 0

    """
    Determines when is the right time to buy
    \return     A boolean deciding whether it's the right time to buy or not
    """
    def should_buy(self, i: int) -> bool:
        # TODO : Complete
        return False

    """
    Determines when is the right time to sell
    \return     A boolean deciding whether it's the right time to sell or not
    """
    def should_sell(self, i: int) -> bool:
        # TODO : Complete
        return False

    """
    Returns the number of shares to buy on the next buy occasion
    \return     The __buy_quantity attribute
    """
    @property
    def buy_quantity(self):
        return self.__buy_quantity

    """
    Returns the number of shares to sell on the next sell occasion
    \return     The __sell_quantity attribute
    """
    @property
    def sell_quantity(self):
        return self.__sell_quantity