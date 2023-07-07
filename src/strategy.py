import pandas_ta as ta
from pandas import DataFrame
from wallet import Wallet

class Strategy:
    def __init__(self, ticker_data: DataFrame, wallet: Wallet):
        self.__wallet = wallet
        self.__ticker_data = ticker_data
        self.__buy_quantity = 100000 # TODO : Adjust according to your strategy
        self.__sell_quantity = 100000 # TODO : Adjust according to your strategy

        # Note : Feel free to add your own attributes and methods!
        # self.rsi = ta.rsi(self.__ticker_data.get('Close'))
        self.stoch = ta.stoch(self.__ticker_data.get('High'), self.__ticker_data.get('Low'), self.__ticker_data.get('Close'))
        self.psar = ta.psar(self.__ticker_data.get('High'), self.__ticker_data.get('Low'), af0=0.02)
        self.bbands = ta.bbands(self.__ticker_data.get('Close'), 20)
        self.has_bought = False

        self.bought_price: float = 0.0

        self.ichimoku = ta.ichimoku(ticker_data.get('High'), ticker_data.get('Low'), ticker_data.get('Close'))
        # self.precedent_spanA = self.ichimoku[0].get('ISA_9')


    # TODO : Add param in doc
    """
    Determines when is the right time to buy. This method is called once per interval
    \return     A boolean deciding whether it's the right time to buy or not
    """
    def should_buy(self, i: int) -> bool:
        price = self.__ticker_data.iloc[i][3]

        ### Strategy 1 ###
        # try:
        #     return self.stoch.get('STOCHk_14_3_3').iloc[i-12] < 20
        # except:
        #     return False

        ### Strategy 2 ###
        # date = self.__ticker_data.index[i]
        # try:
        #     if price > span_a and price > span_b and self.stoch.get('STOCHk_14_3_3').iloc[i-12] < 20 and \
        #         10 <= date.hour and (date.hour <= 15 or date.hour == 15 and date.minutes < 30):
        #         self.bought_price = price
        #         return True
        #     else:
        #         return False
        # except:
        #     return False

        ### Strategy 3 ###
        # span_a = self.ichimoku[0].iloc[i][0]
        # span_b = self.ichimoku[0].iloc[i][1]
        # volume = self.__ticker_data.iloc[i][5]
        # precedent_volume = self.__ticker_data.iloc[i-1][5]
        # price = self.__ticker_data.iloc[i][3]
        # precedent_price = self.__ticker_data.iloc[i-1][3]
        # if i > 0 and \
        #     volume >= precedent_volume * 2 and \
        #     price < precedent_price:
        #     self.bought_price = price
        #     return True
        # else: 
        #     return False

        ### Strategy Test ###
        # if i == 0 or not self.has_bought and self.psar.get('PSARr_0.02_0.2').iloc[i]:
        #     self.has_bought = True
        #     return True
        # return False
        return True



    # TODO : Add param in doc
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
