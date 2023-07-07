import yfinance as yf
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from wallet import Wallet
from strategy import Strategy
from utils import read_constants
from pandas import DataFrame

# TODO : Place finsim.py in root folder
# TODO : Update README.md


"""
Sets the argument parser to interface with the CLI
"""
def set_args():
    arg_parser = ArgumentParser(prog='finsim',
                                usage='finsim TICKER [options]',
                                exit_on_error = True)
    
    arg_parser.add_argument('ticker',
                            help='The ticker on which the simulation will be executed')

    arg_parser.add_argument('--period', '-p',
                            help='The period of the simulation. Possible values: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max',
                            default='1mo')

    arg_parser.add_argument('--interval', '-i',
                            help='The interval between two timestamps. Possible values: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo',
                            default='1d')

    arg_parser.add_argument('--bear', '-b',
                            help="If active, the strategy will buy the bear version of the given stock (even if it doesn't exist) when you sell the bull and vice versa",
                            action='store_true',
                            default=False)

    arg_parser.add_argument('--graph', '-g',
                            help='Whether a graph should be displayed at the end of the simulation',
                            action='store_true',
                            default=False)

    arg_parser.add_argument('--verbose', '-v',
                            help='The verbose level. Can be supplied multiple times to increase verbosity',
                            action='count',
                            default=0)

    arguments = arg_parser.parse_args()
    arguments.ticker = arguments.ticker.upper()
    return arguments


"""
Generate a graph showing the moments were the strategy would have bought or sold shares
of the given stock over the given period
\param      data: The stock data
\param      buy_moments: A list of tuples with information about moments of buy
            buy_moments[0]: Moment of buy
            buy_moments[1]: Price at moment of buy
\param      sell_moments: A list of tuples with information about moments of sell
            sell_moments[0]: Moment of sell
            sell_moments[1]: Price at moment of sell
"""
def generate_graph(data: DataFrame, buy_moments: list, sell_moments: list, period: str):
        print('[*] Generating graph...')
        plt.plot(data.index, data.get('Close'))
        plt.plot([i[0] for i in sell_moments], [i[1] for i in sell_moments], '.r', label='Sell moments', markersize=8)
        plt.plot([i[0] for i in buy_moments], [i[1] for i in buy_moments], '.g', label='Buy moments', markersize=8)
        plt.legend()
        plt.suptitle(f'Application of the strategy over a period of {period}')
        plt.xlabel('Timestamp')
        plt.ylabel('Price')
        plt.show()


"""
Perform the simulation
\param      cli_args : The command line arguments that were supplied by the user
"""
def simulate(cli_args):
    initial_cash = 100000
    wallet = Wallet(initial_cash, cli_args.verbose)

    print(f'[*] Downloading {cli_args.ticker} data...')
    ticker_data = yf.download(tickers=cli_args.ticker, 
                                period=cli_args.period, 
                                interval=cli_args.interval, 
                                prepost=False, 
                                repair=True)
    bear_bought_price = 0.0
    bull_bought_price = 0.0
    if ticker_data.empty:
        exit()

    strategy = Strategy(yf.download(cli_args.ticker,
                                period=cli_args.period, 
                                interval=cli_args.interval, 
                                prepost=False, 
                                repair=True),
                        wallet)

    print('[*] Simulating...')
    buy_moments = list()
    sell_moments = list()
    for i in range(len(ticker_data.index)):
        if strategy.should_buy(i):
            price = ticker_data.iloc[i][CONSTANTS['CLOSE']]

            if cli_args.bear and strategy.should_sell_bear(i):
                bear_price = bear_bought_price + (bear_bought_price - price)
                if wallet.sell(cli_args.ticker, strategy.sell_quantity, bear_price):
                    bear_bought_price = 0.0

            if wallet.buy(cli_args.ticker, strategy.buy_quantity, price):
                buy_moments.append((ticker_data.index[i], price))
                bull_bought_price = price

        elif strategy.should_sell(i):
            price = ticker_data.iloc[i][CONSTANTS['CLOSE']]

            if wallet.sell(cli_args.ticker, strategy.sell_quantity, price):
                sell_moments.append((ticker_data.index[i], price))
                bull_bought_price = 0.0

            if cli_args.bear and strategy.should_buy_bear(i):
                bear_price = price
                if wallet.buy(cli_args.ticker, strategy.buy_quantity, bear_price):
                    bear_bought_price = price

    last_bull_price = ticker_data.iloc[-1][CONSTANTS['CLOSE']]
    if bear_bought_price != 0.0:
        bear_price = bear_bought_price + (bear_bought_price - last_bull_price)
        wallet.sell_all(cli_args.ticker, bear_price)
    else:
        wallet.sell_all(cli_args.ticker, last_bull_price)
    final_cash = wallet.cash
    print('[+] Simulation done')

    print('[+] Profits: {:.2f}%'.format(100 * (final_cash / initial_cash - 1)))
    print('[+] If you had invested {:.2f}$, you would now have {:.2f}$ using this method over a period of {}.'.format(initial_cash, final_cash, cli_args.period))

    if cli_args.graph:
        generate_graph(ticker_data, buy_moments, sell_moments, cli_args.period)


CONSTANTS = read_constants()

if __name__ == '__main__':
    args = set_args()
    simulate(args)
