import pandas_ta as ta
from pandas import DataFrame
from wallet import Wallet

class Strategy:
    def __init__(self, ticker_data: DataFrame, wallet: Wallet):
        self.__wallet = wallet
        self.__ticker_data = ticker_data
        self.__buy_quantity = 100 # TODO : Adjust according to your strategy
        self.__sell_quantity = 100 # TODO : Adjust according to your strategy

        # Note : Feel free to add your own attributes and methods!
        self.rsi = ta.rsi(self.__ticker_data.get('Close'))


    """
    Determines when is the right time to buy. This method is called once per interval
    \return     A boolean deciding whether it's the right time to buy or not
    """
    def should_buy(self, i: int) -> bool:
        # TODO : Replace with your buying strategy
        return self.rsi.iloc[i] < 20


    """
    Determines when is the right time to sell
    \return     A boolean deciding whether it's the right time to sell or not
    """
    def should_sell(self, i: int) -> bool:
        # TODO : Replace with your selling strategy 
        return self.rsi.iloc[i] > 80
    
    def should_buy_bear(self, i: int) -> bool:
        return False

    def should_sell_bear(self, i: int) -> bool:
        return False

    """
    Gets the number of shares to buy on the next buy occasion
    \return     The __buy_quantity attribute
    """
    @property
    def buy_quantity(self) -> int:
        return self.__buy_quantity


    """
    Gets the number of shares to sell on the next sell occasion
    \return     The __sell_quantity attribute
    """
    @property
    def sell_quantity(self) -> int:
        return self.__sell_quantity
