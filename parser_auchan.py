#!/usr/bin/python3
import re, datetime
import pymongo
from pymongo import MongoClient
from selenium import webdriver

list_stores = [
    "https://www.auchandrive.fr/drive/mag/update-924",
    "https://www.auchandrive.fr/drive/mag/update-823",
    "https://www.auchandrive.fr/drive/mag/update-36132",
    "https://www.auchandrive.fr/drive/mag/update-361",
]

list_products = [
    "https://www.auchandrive.fr/catalog/coca-cola-zero-1l-P762493",
    "https://www.auchandrive.fr/catalog/jardin-bio-jus-de-citron-de-sicile-25cl-P401977",
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
        PRODUCT_LOCATION_SELECTOR = './/div[@class="header__identity-pointOfService"]'

        driver = init_browser_chrome()
        driver.get(store_url)
        #try:
        #    driver.get(store_url)
        #except:
        #    driver.close()

        product_location = driver.find_element_by_xpath(PRODUCT_LOCATION_SELECTOR).text
        print("Visit Auchan Drive %s" % (product_location))

        for product_url in list_products:
            PRODUCT_NAME_SELECTOR = './/p[@class="pdp-infos__title"]'
            PRODUCT_PRICE_SELECTOR = './/p[@class="price-standard"]'
            PRODUCT_PRICEPER_SELECTOR = './/p[@class="price--per"]'

            driver.get(product_url)
            #try:
            #    driver.get(url)
            #except:
            #    driver.close()

            product_name = driver.find_element_by_xpath(PRODUCT_NAME_SELECTOR).text
            product_price = "".join(driver.find_element_by_xpath(PRODUCT_PRICE_SELECTOR).text).replace("\u20ac", "").replace(" ", "")
            product_priceper = re.sub(r" \u20ac.*", "", driver.find_element_by_xpath(PRODUCT_PRICEPER_SELECTOR).text).replace(" ", "")
            print("%s - %s - %s" % (product_name, product_price, product_priceper))
            product_data = {
                'Date': datetime.datetime.now(),
                'Company': 'Auchan',
                'Location': product_location,
                'Product': product_name,
                'Price': product_price,
                'Priceper': product_priceper,
            }

            save_mongo(product_data)

        driver.close()


if __name__ == '__main__':
    main()
