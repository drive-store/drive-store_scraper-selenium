#!/usr/bin/python3
import re, datetime, time
import pymongo
from pymongo import MongoClient
from selenium import webdriver

list_stores = [
    "https://courses-en-ligne.carrefour.fr/set-store/1019?sectorZip=59000&sectorCity=LILLE",
    "https://courses-en-ligne.carrefour.fr/set-store/276?sectorZip=59000&sectorCity=Lille",
    "https://courses-en-ligne.carrefour.fr/set-store/106?sectorZip=59461&sectorCity=LOMME",
    "https://courses-en-ligne.carrefour.fr/set-store/109?sectorZip=59290&sectorCity=WASQUEHAL",
]

list_products = [
    "coca cola zero 1l",
    "jus citron bio carrefour",
    "litiere hygiene catsan",
]


def formatter_price(price):
    return "".join(price).replace("\u20ac", "").replace(" ", "")

def formatter_priceper(priceunit):
    return re.sub(r" \u20ac.*", "", priceunit).replace(" ", "")

def main():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36")
    try:
        driver = webdriver.Chrome('chromedriver', options=chrome_options, service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])
    except:
        driver.close()

    time.sleep(6)
    go_homepage(driver)
    #try:
    #    go_homepage(driver)
    #except:
    #    driver.close()
    
    driver.close()

def go_homepage(driver):
    #print("go_homepage")
    driver.get("https://courses-en-ligne.carrefour.fr")
    for store_url in list_stores:
        time.sleep(6)
        go_drive_location(driver, store_url)

def go_drive_location(driver, store_url):
    #print("go_drive_location")
    driver.get(store_url)
    time.sleep(6)
    driver.save_screenshot("carrefour_go_drive_location.png")

    for product_tags in list_products:
        go_search_product(driver, product_tags)

def go_search_product(driver, product_tags):
    #print("go_search_product")
    #try:
    #    driver.get("https://courses-en-ligne.carrefour.fr/search?q=" + product_tags)
    #    go_result_products(driver)
    #except:
    #    driver.close()
    #    pass
    try:
        driver.get("https://new.carrefour.fr/s?q=" + product_tags)
        time.sleep(6)
        go_result_products_through_new_website(driver)
    except:
        driver.close()
        #pass
    driver.save_screenshot("carrefour_go_search_product.png")

def go_result_products(driver):
    #print("go_result_products")
    product = {}
    
    PRODUCT_LOCATION_SELECTOR = './/span[@class="cd-HeaderShopInfosAdress"]'
    PRODUCT_NAME_SELECTOR = './/div[@class="cd-ProductInfos "]//h4[@class="label title"]'
    PRODUCT_DESC_SELECTOR = './/div[@class="cd-ProductInfos "]//div[@class="cd-ProductDescription"]'
    PRODUCT_PRICE_SELECTOR = './/div[@class="cd-ProductInfos "]//div[@class="cd-ProductPriceUnit "]'
    PRODUCT_PRICEPER_SELECTOR = './/div[@class="cd-ProductInfos "]//div[@class="cd-ProductPriceReference"]'
    
    product_location = driver.find_element_by_xpath(PRODUCT_LOCATION_SELECTOR).text
    product_name = driver.find_elements_by_xpath(PRODUCT_NAME_SELECTOR)[0].text
    product_desc = driver.find_elements_by_xpath(PRODUCT_DESC_SELECTOR)[0].text
    product_price = driver.find_elements_by_xpath(PRODUCT_PRICE_SELECTOR)[0].text
    product_priceper = driver.find_elements_by_xpath(PRODUCT_PRICEPER_SELECTOR)[0].text
    
    product = {
        'Date': datetime.datetime.now(),
        'Company': 'Carrefour',
        'Location': product_location,
        'Product': product_name+" "+product_desc,
        'Price': formatter_price(product_price),
        'Priceper': formatter_priceper(product_priceper),
    }

    print(product)
    db_save(product)

def go_result_products_through_new_website(driver):
    #print("go_result_products_through_new_website")
    product = {}
    
    PRODUCT_LOCATION_SELECTOR = './/span[@class="channel-head__right-content__title"]'
    PRODUCT_NAME_SELECTOR = './/ul[@class="product-list__grid"]//h2[@class="label title"]'
    PRODUCT_DESC_SELECTOR = './/ul[@class="product-list__grid"]//div[@class="label packaging"]'
    PRODUCT_PRICE_SELECTOR = './/ul[@class="product-list__grid"]//span[@class="product-pricing__main-price"]'
    PRODUCT_PRICEPER_SELECTOR = './/ul[@class="product-list__grid"]//span[@class="product-pricing__main-ppu"]'
    
    product_location = driver.find_element_by_xpath(PRODUCT_LOCATION_SELECTOR).text
    product_name = driver.find_elements_by_xpath(PRODUCT_NAME_SELECTOR)[0].text
    product_desc = driver.find_elements_by_xpath(PRODUCT_DESC_SELECTOR)[0].text
    product_price = driver.find_elements_by_xpath(PRODUCT_PRICE_SELECTOR)[0].text
    product_priceper = driver.find_elements_by_xpath(PRODUCT_PRICEPER_SELECTOR)[0].text
    
    product = {
        'Date': datetime.datetime.now(),
        'Company': 'Carrefour',
        'Location': product_location,
        'Product': product_name+" "+product_desc,
        'Price': formatter_price(product_price),
        'Priceper': formatter_priceper(product_priceper),
    }

    print(product)
    db_save(product)

def db_save(product):
    client = MongoClient("ds141872.mlab.com", 41872)
    db = client['auchan-products']
    db.authenticate("scrapy59", "scrapy59")
    collection = db['products']
    collection.insert_one(product)

if __name__ == '__main__':
    main()
