import yfinance as yf
from argparse import ArgumentParser
from wallet import Wallet
from strategy import Strategy

"""
Sets the argument parser to interface with the CLI
"""
def set_args():
    arg_parser = ArgumentParser(
    prog = 'finsim',
    usage = '%(prog) TODO')
    
    arg_parser.add_argument('--ticker', '-t',
                            help='The ticker on which the simulation will be executed',
                            required=True)

    arg_parser.add_argument('--period', '-p',
                            help='The period of the simulation. Possible values: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max',
                            default='1mo',
                            required=False)

    # TODO : Complete

"""
Perform the simulation
"""
def simulate():
    initial_cash = 100000
    wallet = Wallet(initial_cash)
    print('[*] Downloading MSFT data...') # TODO : Replace MSFT
    ticker_data = yf.download(tickers="MSFT", period="1d", interval="1m", prepost=False, repair=True) # TODO : Adjust according to the command line parameters
    strategy = Strategy(ticker_data)
    print('[*] Simulating...')
    for i in range(len(ticker_data.index)):
        if strategy.should_buy(i): # TODO : Send date instead of Series
            wallet.buy("MSFT", 100, 12) # TODO : Determine how much
        elif strategy.should_sell(i):
            wallet.sell("MSFT", 100, 12) # TODO : Determine how much
    # TODO : Sell all remaining assets (or find a way to show them in the final output)
    final_cash = wallet.cash
    print('[+] Simulation done')
    print(f'[+] Profits: {100 * (1 - initial_cash / final_cash)}%') # TODO : Format (xxx.xx% instead of xxx.xxxxxx%)
    print(f'[+] If you had invested {initial_cash}$, you would now have {final_cash}$ using this method over the given period.') # TODO : Adjust period to be dynamic and format


if __name__ == '__main__':
    set_args()
    simulate()
