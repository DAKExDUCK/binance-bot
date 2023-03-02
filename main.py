import asyncio
import os
import time
from modules.bot import send
from modules.logger import logger
from modules.binance import Binance
from config import admin_id


def main():
    fiat = input("Enter Fiat (UAH): ")
    desired_price = float(input("Enter desired price (39.1): "))
    max_price_for_order = float(input("Enter max price for order (2000.1): "))
    balance = float(input("Enter balance (4000.1): "))
    banks = [ bank for bank in input("Enter banks with comma ('Wise, PUMB'): ").split(', ')]
    os.system('cls' if os.name == 'nt' else 'clear')
    logger.info('Waiting browser...')

    bnc = Binance(desired_price=desired_price, max_price_for_order=max_price_for_order, balance=balance, banks=banks)
    bnc.login_qr()
    os.system('cls' if os.name == 'nt' else 'clear')
    logger.info('Loading p2p page...')
    bnc.browser.driver.get(f"https://p2p.binance.com/ru/trade/all-payments/USDT?fiat={fiat}")
    logger.info('Waiting p2p page...')
    bnc.wait_p2p_page_orders(fiat)
    bnc.cookies = bnc.browser.get_cookies_data()
    bnc.headers = bnc.browser.get_headers()

    start = time.time()
    while 1:
        try:
            bnc.check_orders_buy(fiat=fiat, asset='USDT')
        except Exception as exc:
            logger.error(exc)
            text = f"Error: {exc}"
            asyncio.run(send(admin_id, text))
            

        if time.time() - start > 600:
            try:
                logger.info('Waiting p2p page...')
                bnc.browser.driver.get(f"https://p2p.binance.com/ru/trade/all-payments/USDT?fiat={fiat}")
                bnc.wait_p2p_page_orders(fiat)
                bnc.cookies = bnc.browser.get_cookies_data()
                bnc.headers = bnc.browser.get_headers()
                start = time.time()
            except Exception as exc:
                logger.error(exc, exc_info=True)
                logger.error('Error while updating cookies')
                text = 'Error while updating cookies'
                asyncio.run(send(admin_id, text))
                break
            
    bnc.browser.driver.close()


if __name__ == "__main__":
    main()