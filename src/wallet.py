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
        if self.__cash < amount * price_per_share:
            self.buy(ticker, self.__cash // price_per_share, price_per_share)
            return

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
        if self.__shares[ticker] < amount:
            self.sell_all(ticker, price_per_share)
            return

        self.__cash += amount * price_per_share
        try:
            self.__shares[ticker] -= amount
        except KeyError:
            print('ERROR: Trying to sell unpossessed shares')
            print('ABORTING')
            exit()
        self.__shares[ticker] = clamp(self.__shares[ticker])

    """
    Sell all shares of a stock. Usually called at the end of the simulation.
    \param      ticker: The Ticker of the stock to sell
    \param      price_per_share: The price of a share at the time of the sell
    """
    def sell_all(self, ticker, price_per_share):
        if ticker in self.__shares and self.__shares[ticker] > 0:
            self.sell(ticker, self.__shares[ticker], price_per_share)

    """
    Get the amount of cash in the wallet
    \return     The __cash attribute
    """
    @property
    def cash(self):
        return self.__cash

    """
    Get the owned amount of shares of a given stock
    \return     The amount of shares
    """
    def get_shares(self, ticker):
        return self.__shares[ticker] if ticker in self.__shares else 0

"""
Clamp the parameter so that it does not go below 0.
\param      attrib: The value to clamp
"""
def clamp(attrib):
    return 0 if attrib < 0 else attrib
