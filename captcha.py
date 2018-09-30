#!/usr/bin/python3
import re, datetime, time
import pymongo
from pymongo import MongoClient
from selenium import webdriver

list_stores = [
    "https://courses-en-ligne.carrefour.fr/set-store/276?sectorZip=59155&sectorCity=Faches-Thumesnil",
    #"https://courses-en-ligne.carrefour.fr/set-store/276?sectorZip=59000&sectorCity=Lille",
]

list_products = [
    "https://courses-en-ligne.carrefour.fr/5449000054227/soda-coca-cola",
]



def init_browser_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    try:
        driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options, service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
    except:
        driver.close()
    return driver


def save_mongo(product):
    client = MongoClient("ds141872.mlab.com", 41872)
    #client = MongoClient("localhost", 27017)
    db = client['auchan-products']
    db.authenticate("scrapy59", "scrapy59")
    collection = db['products']
    collection.insert(product)


def main():
    product = {}

    for store_url in list_stores:
        #PRODUCT_LOCATION_SELECTOR = './/span[@class="cd-HeaderShopInfosAdress"]'

        driver = init_browser_chrome()
        time.sleep(1)
        driver.get(store_url)
        print(driver.find_element_by_xpath("//*").get_attribute('outerHTML'))
        driver.save_screenshot("/tmp/screenshot01.png")
        time.sleep(3)
        driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))
        print(driver.find_element_by_xpath("//*").get_attribute('outerHTML'))
        driver.save_screenshot("/tmp/screenshot02.png")

        #product_location = driver.find_element_by_xpath(PRODUCT_LOCATION_SELECTOR).text #.split(" - ")[1]
        #print("Visit Auchan Drive %s" % (product_location))

        driver.close()


if __name__ == '__main__':
    main()
