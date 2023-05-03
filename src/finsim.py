import yfinance as yf
from argparse import ArgumentParser
from wallet import Wallet
from strategy import Strategy


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

    # TODO : Complete
    arguments = arg_parser.parse_args()
    arguments.ticker = arguments.ticker.upper()
    return arguments


"""
Perform the simulation
\param      cli_args : The command line arguments that were supplied by the user
"""
def simulate(cli_args):
    initial_cash = 100000
    wallet = Wallet(initial_cash)

    print(f'[*] Downloading {cli_args.ticker} data...')
    ticker_data = yf.download(tickers=cli_args.ticker, 
                                period=cli_args.period, 
                                interval=cli_args.interval, 
                                prepost=False, 
                                repair=True)
    if ticker_data.empty:
        exit()
    strategy = Strategy(ticker_data)

    print('[*] Simulating...')
    for i in range(len(ticker_data.index)):
        if strategy.should_buy(i): # TODO : Send date instead of Series
            wallet.buy(cli_args.ticker, strategy.buy_quantity, 12) # TODO : Determine how much
        elif strategy.should_sell(i):
            wallet.sell(cli_args.ticker, strategy.sell_quantity, 12) # TODO : Determine how much
    last_price_per_share = ticker_data.iloc[-1][3]
    wallet.sell_remaining_shares(cli_args.ticker, last_price_per_share)
    final_cash = wallet.cash

    print('[+] Simulation done')
    print('[+] Profits: {:.2f}%'.format(100 * (1 - initial_cash / final_cash)))
    print('[+] If you had invested {:.2f}$, you would now have {:.2f}$ using this method over a period of {}.'.format(initial_cash, final_cash, cli_args.period))


if __name__ == '__main__':
    args = set_args()
    simulate(args)
