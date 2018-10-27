#!/usr/bin/python3
import re, datetime
import pymongo
from pymongo import MongoClient
from selenium import webdriver

list_stores = [
    "https://courses-en-ligne.carrefour.fr/set-store/276?sectorZip=59155&sectorCity=Faches-Thumesnil",
    #"https://courses-en-ligne.carrefour.fr/set-store/276?sectorZip=59000&sectorCity=Lille",
]

list_products = [
    "https://courses-en-ligne.carrefour.fr/5449000133328/soda-zero-sucres-coca-cola-zero",
    "https://courses-en-ligne.carrefour.fr/5000112611762/soda-zero-sucres-coca-cola",
]



def init_browser_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")
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
        PRODUCT_LOCATION_SELECTOR = './/span[@class="cd-HeaderShopInfosAdress"]'

        driver = init_browser_chrome()
        driver.get(store_url)

        product_location = driver.find_element_by_xpath(PRODUCT_LOCATION_SELECTOR).text #.split(" - ")[1]
        print("Visit Carrefour Drive %s" % (product_location))
        #driver.save_screenshot("carrefour_"+product_location+".png")

        for product_url in list_products:
            PRODUCT_NAME_SELECTOR = '//span[@class="cd-ProductPageTitle cd-span-h1"]'
            PRODUCT_PRICE_SELECTOR = '//div[@class="cd-ProductPriceUnit"]'
            PRODUCT_PRICEPER_SELECTOR = '//div[@class="cd-ProductPriceReference"]'

            driver.get(product_url)
            # Prevent to Not found product in Store
            #  Products URL are different by store
            if len(driver.find_elements_by_xpath('//p[@class="MiscPage-description"]')):
                print("Error in location '%s' for url '%s'" % (product_location, product_url))
                continue

            product_name = driver.find_element_by_xpath(PRODUCT_NAME_SELECTOR).text
            product_price = "".join(driver.find_element_by_xpath(PRODUCT_PRICE_SELECTOR).text).replace("\u20ac", "").replace(" ", "")
            product_priceper = re.sub(r" \u20ac.*", "", driver.find_element_by_xpath(PRODUCT_PRICEPER_SELECTOR).text).replace(" ", "")
            print("%s - %s - %s" % (product_name, product_price, product_priceper))
            product_data = {
                'Date': datetime.datetime.now(),
                'Company': 'Carrefour',
                'Location': product_location,
                'Product': product_name,
                'Price': product_price,
                'Priceper': product_priceper,
            }
            #driver.save_screenshot("carrefour_"+product_location+"_"+product_name+".png")

            save_mongo(product_data)

        driver.close()


if __name__ == '__main__':
    main()
