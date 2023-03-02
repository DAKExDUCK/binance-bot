import asyncio
from datetime import datetime
import json
import os
import time

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import requests
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import \
    visibility_of_element_located as voel

from config import admin_id
from modules.bot import clear_MD, send
from modules.browser import Browser
from modules.logger import logger


class Binance:
    cookies: dict
    headers: dict

    def __init__(self, desired_price: float, max_price_for_order: float, balance: float, banks: list):
        self.balance = balance
        self.max_price_for_order = max_price_for_order
        self.desired_price = desired_price
        self.desired_banks = banks

        self.browser = Browser()

    def login_qr(self):
        def save_qr(qr):
            self.browser.driver.save_screenshot("qr.png")
            location = qr.location
            size = qr.size
            imgOpen = Image.open("qr.png")
            imgOpen = imgOpen.crop(
                (int(location['x']), int(location['y']),
                int(location['x']+size['width']),
                int(location['y']+size['height']))
            )
            imgOpen.save("qr.png")

        def show_qr():
            img = mpimg.imread('qr.png')
            plt.imshow(img)
            plt.axis('off')
            plt.show()

        self.browser.driver.get("https://accounts.binance.com/ru/login")
        
        os.system('cls' if os.name == 'nt' else 'clear')
        logger.info('Waiting closing QR window...')
        qr = self.browser.wait.until(voel((
            By.XPATH,
            '//div[contains(@class, "qr-code")]/div/canvas'
        )))
        save_qr(qr)
        show_qr()
        
        os.system('cls' if os.name == 'nt' else 'clear')
        logger.info('Waiting login...')
        while 1:
            time.sleep(0.5)
            if self.browser.driver.current_url == "https://www.binance.com/ru/my/dashboard":
                time.sleep(0.5)
                break
    
    def wait_p2p_page_orders(self, fiat="UAH"):
        while 1:
            time.sleep(0.2)
            if len(self.browser.driver.find_elements(
                By.XPATH,
                '//div[contains(@class, "css-ovjtyv")]'
            )) > 0:
                break
            if self.browser.driver.current_url == "https://p2p.binance.com/ru/trade/all-payments/USDT?fiat=LOCAL":
                self.browser.driver.get(f"https://p2p.binance.com/ru/trade/all-payments/USDT?fiat={fiat}")
            
    def accept_all(self):
        try:
            self.browser.driver.find_element(
                By.XPATH,
                '//*[@id="onetrust-accept-btn-handler"]'
            ).click()
        except:
            ...
        try:
            self.browser.driver.find_element(
                By.XPATH,
                '//*[contains(@class, "css-o78533")]',
            ).click()
        except:
            ...
        try:
            self.browser.driver.find_element(
                By.XPATH,
                '//*[contains(@class, "css-gyhchg")]'
            ).click()
        except:
            ...
        try:
            self.browser.driver.find_element(
                By.XPATH,
                '//*[contains(@class, "css-1v60uza")]'
            ).click()
        except:
            ...
        try:
            self.browser.driver.find_element(
                By.XPATH,
                '//*[contains(@class, "css-o78533")]',
            ).click()
        except:
            ...
        try:
            self.browser.driver.find_element(
                By.XPATH,
                '//*[contains(@class, "css-gyhchg")]'
            ).click()
        except:
            ...

    def p2p_ready_buy(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        logger.info('Waiting p2p page...')
        self.browser.driver.get("https://p2p.binance.com/ru/trade/all-payments/USDT?fiat=UAH")
        self.wait_p2p_page_orders()
        time.sleep(2)
        self.wait_p2p_page_orders()

        self.accept_all()

        self.browser.wait.until(voel((
            By.XPATH,
            '//*[@id="C2CofferList_btn_refresh"]'
        ))).click()
        
        self.accept_all()
        
        self.browser.wait.until(voel((
            By.XPATH,
            '//*[@id="__APP"]/div[2]/main/div[1]/div[3]/div[2]/div/div[6]/div/div[2]/div/div[2]'
        ))).click()

    def check_orders_buy(self, fiat: str, asset: str):
        status, data = self.get_orders(fiat, asset)
        
        if data['code'] != '000000' or status != 200:
            logger.error(data['message'])
            text = data['message']
            asyncio.run(send(admin_id, text))
            time.sleep(10)
            return

        logger.info('Checking orders...')

        for order in data['data']:
            order_id = order['adv']['advNo']
            order_merchant_name = order['advertiser']['nickName']
            order_asset = order['adv']['asset']
            order_fiat = order['adv']['fiatUnit']
            order_price = order['adv']['price']
            order_asset_amount = order['adv']['surplusAmount']
            order_max = order['adv']['dynamicMaxSingleTransAmount']
            order_min = order['adv']['minSingleTransAmount']
            order_trade_methods_name = [ trade_method['tradeMethodName'] for trade_method in order['adv']['tradeMethods'] ]

            if len(set(order_trade_methods_name) & set(self.desired_banks)) > 0:
                if float(order_price) < self.desired_price and float(order_min) < self.max_price_for_order:
                    payment_amount = 0.0
                    if self.max_price_for_order >= self.balance:
                        if self.balance > float(order_max):
                            temp_balance = self.balance - float(order_max)
                            payment_amount = float(order_max)
                        else:
                            temp_balance = self.balance - self.balance
                            payment_amount = self.balance
                    else:
                        if self.max_price_for_order < float(order_max):
                            temp_balance = self.balance - self.max_price_for_order
                            payment_amount = self.max_price_for_order
                        else:
                            temp_balance = self.balance - float(order_max)
                            payment_amount = float(order_max)
                    status, result = self.make_order(order_fiat, order_asset, order_id, order_price, payment_amount)
                    if result['code'] != '000000' or status != 200:
                        logger.error(result['message'])
                        text = result['message']
                        asyncio.run(send(admin_id, text))
                        time.sleep(30)
                        return

                    self.send_order_info_buy(order_price, order_fiat, order_asset_amount, order_asset, order_min, order_max, order_merchant_name, order_trade_methods_name)

                    self.balance = temp_balance
                    logger.info(f'Order maked | Balance={int(self.balance)} {order_fiat}')

    def get_orders(self, fiat: str, asset: str):
        logger.info('Getting orders...')
        json_data = {
            'proMerchantAds': False,
            'page': 1,
            'rows': 20,
            'payTypes': [],
            'countries': [],
            'publisherType': None,
            'asset': asset,
            'fiat': fiat,
            'tradeType': 'BUY',
        }

        response = requests.post(
            'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search',
            cookies=self.cookies,
            json=json_data,
        )
        try:
            return response.status_code, json.loads(response.text)
        except:
            return response.status_code, {
                'code': None,
                'message': 'Ошибка при запросе'
            }

    def get_order_info(self, id):
        response = requests.get(
            f'https://p2p.binance.com/bapi/c2c/v2/public/c2c/adv/selected-adv/{id}',
            cookies=self.cookies,
        )
        return response.status, json.loads(response.text)

    def make_order(self, fiat: str, asset: str, order_id: str, order_price: str, order_amount: int):
        logger.info('Making order...')
        json_data = {
            'advOrderNumber': order_id,
            'asset': asset,
            'matchPrice': order_price,
            'fiatUnit': fiat,
            'buyType': 'BY_MONEY',
            'totalAmount': order_amount,
            'tradeType': 'BUY',
            'origin': 'MAKE_TAKE',
        }

        response = requests.post(
            'https://p2p.binance.com/bapi/c2c/v2/private/c2c/order-match/makeOrder',
            cookies=self.cookies,
            headers=self.headers,
            json=json_data,
        )

        return response.status_code, json.loads(response.text)

    def send_order_info_buy(self, fiat_per_one, fiat, avlbl_asset, asset, limit_min, limit_max, merchant_name, banks):
        banks_list = f", ".join(banks)
        text = "Новый ордер\! *BUY*\n\n" \
                f"Продавец: *{clear_MD(merchant_name)}*\n" \
                f"Цена: *{clear_MD(fiat_per_one)} {clear_MD(fiat)}*\n" \
                f"Доступно: *{clear_MD(avlbl_asset)} {clear_MD(asset)}*\n" \
                f"Лимиты: *{clear_MD(int(float(limit_min)))} {clear_MD(fiat)}* \<\-\> *{clear_MD(int(float(limit_max)))} {clear_MD(fiat)}*\n" \
                f"Банки: *{banks_list}*\n" \
                f"Баланс: *{clear_MD(int(self.balance))} {clear_MD(fiat)}*"

        asyncio.run(send(admin_id, text))

    def len_of_active_orders(self):
        json_data = {
            'orderStatusList': [
                1,
            ],
            'page': 1,
            'rows': 999,
        }

        response = requests.post(
            'https://c2c.binance.com/bapi/c2c/v2/private/c2c/order-match/order-list',
            cookies=self.cookies,
            headers=self.headers,
            json=json_data
        )
        data = json.loads(response.text)
        try:
            return int(data['total'])
        except:
            return data