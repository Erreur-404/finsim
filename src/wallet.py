"""
The class that contains all your assets during the simulation, such as your
stocks and your cash.
"""
class Wallet:
    def __init__(self, initial_cash):
        self.__cash = initial_cash
        self.__shares = dict()

    """
    Buy a stock
    \param      ticker: The Ticker of the stock to buy
    \param      amount: The amount of stock to buy
    \param      price_per_share: The price of a share at the time of the trade
    """
    def buy(self, ticker, amount, price_per_share):
        self.__cash -= amount * price_per_share
        self.__cash = clamp(self.__cash)
        try:
            self.__shares[ticker] += amount
        except KeyError:
            self.__shares[ticker] = amount

    """
    Sell a stock
    \param      ticker: The Ticker of the stock to sell
    \param      amount: The amount of stock to sell
    \param      price_per_share: The price of a share at the time of the trade
    """
    def sell(self, ticker, amount, price_per_share):
        self.__cash += amount * price_per_share
        try:
            self.__shares[ticker] -= amount
        except KeyError:
            print('ERROR: Trying to sell unpossessed shares')
            print('ABORTING')
            exit()
        self.__shares = clamp(self.__shares)

    def sell_remaining_shares(self, ticker, price_per_share):
        self.sell(ticker, self.__shares[ticker], price_per_share)

    @property
    def cash(self):
        return self.__cash

"""
Clamp the parameter so that it does not go below 0.
\param      attrib: The value to clamp
"""
def clamp(attrib):
    return 0 if attrib < 0 else attrib
