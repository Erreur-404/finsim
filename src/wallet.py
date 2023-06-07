from utils import clamp, debug_print

"""
The class that contains all your assets during the simulation, such as your
stocks and your cash.
"""
class Wallet:
    def __init__(self, initial_cash: int, verbosity: int = 0):
        self.__cash = initial_cash
        self.__shares = dict()
        self.__verbosity = verbosity


    """
    Buy a stock
    \param      ticker: The Ticker of the stock to buy
    \param      amount: The amount of stock to buy
    \param      price_per_share: The price of a share at the time of the trade
    """
    def buy(self, ticker: str, amount: int, price_per_share: float) -> bool:
        if amount <= 0:
            return False

        if self.__cash < amount * price_per_share:
            return self.buy(ticker, self.__cash // price_per_share, price_per_share)

        debug_print('[+] Buying {} shares of {} at {:.2f}$'.format(int(amount), ticker, price_per_share), self.__verbosity, 1)
        self.__cash -= amount * price_per_share
        self.__cash = clamp(self.__cash)
        debug_print('[+] Cash is now at {:.2f}$\n'.format(self.__cash), self.__verbosity, 2)
        try:
            self.__shares[ticker] += amount
        except KeyError:
            self.__shares[ticker] = amount
        return True


    """
    Sell a stock
    \param      ticker: The Ticker of the stock to sell
    \param      amount: The amount of stock to sell
    \param      price_per_share: The price of a share at the time of the trade
    """
    def sell(self, ticker: str, amount: int, price_per_share: float) -> bool:
        if amount <= 0 or ticker not in self.__shares:
            return False

        if ticker in self.__shares and self.__shares[ticker] < amount:
            return self.sell_all(ticker, price_per_share)

        debug_print('[+] Selling {} shares of {} at {:.2f}$'.format(int(amount), ticker, price_per_share), self.__verbosity, 1)
        self.__cash += amount * price_per_share
        self.__shares[ticker] -= amount
        self.__shares[ticker] = clamp(self.__shares[ticker])
        debug_print('[+] Cash is now at {:.2f}$\n'.format(self.__cash), self.__verbosity, 2)
        return True


    """
    Sell all shares of a stock. Usually called at the end of the simulation.
    \param      ticker: The Ticker of the stock to sell
    \param      price_per_share: The price of a share at the time of the sell
    """
    def sell_all(self, ticker: str, price_per_share: float) -> bool:
        if ticker in self.__shares and self.__shares[ticker] > 0:
            self.sell(ticker, self.__shares[ticker], price_per_share)
            return True
        return False


    """
    Get the amount of cash in the wallet
    \return     The __cash attribute
    """
    @property
    def cash(self) -> float:
        return self.__cash


    """
    Get the owned amount of shares of a given stock
    \return     The amount of shares
    """
    def get_shares(self, ticker: str) -> int:
        return self.__shares[ticker] if ticker in self.__shares else 0
