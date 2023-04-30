from pandas import Series

class Strategy:
    # def __init__(self):
    #     # TODO : Complete 
    #     ...

    """
    Determines when it's the right time to buy
    \return     A boolean deciding whether it's the right time to buy or not
    """
    def should_buy(self, infos: Series) -> bool:
        # TODO : Complete
        return False

    """
    Determines when it's the right time to sell
    \return     A boolean deciding whether it's the right time to sell or not
    """
    def should_sell(self, infos: Series) -> bool:
        # TODO : Complete
        return False