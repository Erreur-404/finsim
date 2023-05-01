from pandas import Dataframe

class Strategy:
    def __init__(self, ticker_data: Dataframe):
        self.ticker_data = ticker_data

    """
    Determines when it's the right time to buy
    \return     A boolean deciding whether it's the right time to buy or not
    """
    def should_buy(self, i: int) -> bool:
        # TODO : Complete
        return False

    """
    Determines when it's the right time to sell
    \return     A boolean deciding whether it's the right time to sell or not
    """
    def should_sell(self, i: int) -> bool:
        # TODO : Complete
        return False