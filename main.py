import os
import time
import traceback
from modules.logger import logger
from modules.binance import Binance


def main():
    desired_price = float(input("Enter desired price (39.1): "))
    balance = float(input("Enter balance (4000.1): "))
    banks = [ bank.lower() for bank in input("Enter banks with comma ('Wise, Zen'): ").split(', ')]
    os.system('cls' if os.name == 'nt' else 'clear')
    logger.info('Waiting browser...')

    bnc = Binance(desired_price=desired_price, balance=balance, banks=banks)
    bnc.login_qr()
    os.system('cls' if os.name == 'nt' else 'clear')
    logger.info('Waiting p2p page...')
    bnc.browser.driver.get("https://p2p.binance.com/ru/trade/all-payments/USDT?fiat=UAH")
    bnc.wait_p2p_page_orders()
    bnc.cookies = bnc.browser.get_cookies_data()
    bnc.headers = bnc.browser.get_headers()
    bnc.browser.driver.close()

    while 1:
        bnc.check_orders_buy()
        time.sleep(5)



if __name__ == "__main__":
    main()