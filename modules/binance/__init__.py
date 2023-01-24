import asyncio
import os
import time

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import \
    visibility_of_element_located as voel
from modules.logger import logger
from modules.bot import clear_MD, send

from modules.browser import Browser
from config import admin_id


class Binance:
    def __init__(self, desired_price: float, balance: float, banks: list):
        self.balance = balance
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
            plt.show(block=False)

        def update_qr():
            self.browser.driver.get("https://accounts.binance.com/ru/login")
              
        self.browser.driver.get("https://accounts.binance.com/ru/login")
        while 1:
            os.system('cls||clear')
            qr = self.browser.wait.until(voel((
                By.XPATH,
                '//div[contains(@class, "qr-code")]/div/canvas'
            )))
            save_qr(qr)
            show_qr()
            choice = input("1. After scanning QR \n2. For update QR \n3. Quit\nEnter: ")
            # 1 Login
            # 2 Update
            # 3 Quit
            # else Quit
            if choice == "1":
                plt.close() 
                break
            elif choice == "2":
                plt.close() 
                update_qr()
            elif choice == "3":
                raise SystemExit
            else:
                raise SystemExit
        os.system('cls||clear')
        logger.info('Waiting login...')
        while 1:
            time.sleep(0.5)
            if self.browser.driver.current_url == "https://www.binance.com/ru/my/dashboard":
                time.sleep(0.5)
                break
    
    def wait_p2p_page_orders(self):
        while 1:
            time.sleep(0.2)
            if len(self.browser.driver.find_elements(
                By.XPATH,
                '//div[contains(@class, "css-ovjtyv")]'
            )) > 0:
                break

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
        os.system('cls||clear')
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

    def check_orders_buy(self):
        logger.info('Checking p2p page...')
        key_path_elems = [
            ['fiat_per_one_arr', '/html/body/div[1]/div[2]/main/div[1]/div[4]/div/div[2]/div/div[1]/div[2]/div/div/div[1]', None],
            ['avlbl_asset_arr', '/html/body/div[1]/div[2]/main/div[1]/div[4]/div/div[2]/div/div[1]/div[3]/div/div[1]/div[2]', None],
            ['limit_min_arr', '/html/body/div[1]/div[2]/main/div[1]/div[4]/div/div[2]/div/div[1]/div[3]/div/div[2]/div[2]/div[1]', None],
            ['limit_max_arr', '/html/body/div[1]/div[2]/main/div[1]/div[4]/div/div[2]/div/div[1]/div[3]/div/div[2]/div[2]/div[3]', None],
            ['merchant_name_arr', '/html/body/div[1]/div[2]/main/div[1]/div[4]/div/div[2]/div/div[1]/div[1]/div/div[1]/div/a', None],
            ['buy_button', '/html/body/div[1]/div[2]/main/div[1]/div[4]/div/div[2]/div/div[1]/div[5]/div/button', None],
        ]
        banks_arr = [[], [], [], [], [], [], [], [], [], []]

        for i in range(0, len(key_path_elems)):
            path = key_path_elems[i][1]
            key_path_elems[i][2] = self.browser.driver.find_elements(
                By.XPATH,
                path
            )

        for i in range(10):
            tmp_l = self.browser.driver.find_elements(
                By.XPATH,
                f'/html/body/div[1]/div[2]/main/div[1]/div[4]/div/div[2]/div[{i}]/div[1]/div[4]/div/div/a/div'
            )
            for b in tmp_l:
                banks_arr[i].append(b.text.lower())
        

        for fiat_per_one, avlbl_asset, limit_min, limit_max, merchant_name, buy_button, banks in zip(key_path_elems[0][2], key_path_elems[1][2], key_path_elems[2][2], key_path_elems[3][2], key_path_elems[4][2], key_path_elems[5][2], banks_arr):        
            if buy_button.get_attribute("class").replace(' ', '') == "css-s1iig6":
                if len([set(self.desired_banks) & set(banks)]) > 0:
                    fiat_per_one = float(fiat_per_one.text.replace(',', ''))
                    avlbl_asset, asset = [_.replace(',', '') for _ in avlbl_asset.text.split()]
                    avlbl_asset = float(avlbl_asset)
                    limit_min = float(limit_min.text.split()[1].replace(',', ''))
                    fiat, limit_max = [_.replace(',', '') for _ in limit_max.text.split()]
                    limit_max = float(limit_max)
                    merchant_name = merchant_name.text

                    if fiat_per_one < self.desired_price and limit_min < self.balance:
                        try:
                            self.reserve_order_buy(fiat_per_one, fiat, avlbl_asset, asset, limit_min, limit_max, merchant_name, buy_button, banks)
                            self.p2p_ready_buy()
                            self.wait_p2p_page_orders()
                        except:
                            ...
                        return 

    def reserve_order_buy(self, fiat_per_one, fiat, avlbl_asset, asset, limit_min, limit_max, merchant_name, buy_button, banks):
        logger.info('Reserving BUY order...')
        payment_amount = 0.0
        if self.balance > limit_max:
            temp_balance = self.balance - limit_max
            payment_amount = limit_max
        else:
            temp_balance = self.balance - self.balance
            payment_amount = self.balance

        buy_button.click()
        try:
            self.browser.wait.until(voel((
                By.XPATH,
                '//*[@id="C2CofferBuy_amount_input"]'
            ))).send_keys(payment_amount)
        except:
            if self.browser.driver.find_elements(
                By.XPATH,
                '//*[contains(@class,"css-18jinle")]'
            ) > 0:
                logger.error("Error while reserving order")
                return False
            
        self.browser.wait.until(voel((
            By.XPATH,
            '//*[@id="C2CofferBuy__btn_buyNow"]'
        ))).click()

        while 1:
            time.sleep(0.2)
            if len(self.browser.driver.find_elements(
                By.XPATH,
                '//*[@id="__APP"]/div[2]/main/div[3]/div/div[2]/div/div[2]/div/div[3]/div[1]/textarea'
            )) > 0:
                break
            if len(self.browser.driver.find_elements(
                By.XPATH,
                '//*[contains(@class,"css-18jinle")]'
            )) > 0:
                logger.error("Error while reserving order")
                return False

        self.balance = temp_balance

        url = self.browser.driver.current_url
        self.send_order_info_buy(fiat_per_one, fiat, avlbl_asset, asset, limit_min, limit_max, merchant_name, banks, url)
        return True

    def send_order_info_buy(self, fiat_per_one, fiat, avlbl_asset, asset, limit_min, limit_max, merchant_name, banks, url):
        # banks_list = f", ".join(banks)
        text = "Новый ордер\! *BUY*\n\n" \
                f"Продавец: *{clear_MD(merchant_name)}*\n" \
                f"Цена: *{clear_MD(fiat_per_one)}{clear_MD(fiat)}*\n" \
                f"Доступно: *{clear_MD(avlbl_asset)}{clear_MD(asset)}*\n" \
                f"Лимиты: *{clear_MD(limit_min)}{clear_MD(fiat)}* \<\-\> *{clear_MD(limit_max)}{clear_MD(fiat)}*\n"
                # f"Банки: {banks_list}"
        asyncio.run(send(admin_id, text, url))

    
