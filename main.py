import os
import time
import traceback
from modules.logger import logger
from modules.binance import Binance


def main():
    desired_price = float(input("Enter desired price (39.1): "))
    balance = float(input("Enter balance (4000.1): "))
    banks = [ bank.lower() for bank in input("Enter banks with comma ('Wise, Zen'): ").split(', ')]
    os.system('cls||clear')
    logger.info('Waiting browser...')

    bnc = Binance(desired_price=desired_price, balance=balance, banks=banks)
    try:
        bnc.login_qr()
        bnc.p2p_ready_buy()
        bnc.wait_p2p_page_orders()

        while 1:
            bnc.check_orders_buy()
            time.sleep(5)
    except Exception as exc:
        print(traceback.format_exc(exc))
        logger.info('Screenshot saved - error.png')
        bnc.browser.driver.save_screenshot("error.png")

    bnc.browser.driver.close()


if __name__ == "__main__":
    main()