import bs4
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import requests
import os
import pandas as pd

base_url = 'https://www.bilbasen.dk/'
fuel = ["Hybrid (Benzin + El)" ,"El", "Benzin", "Diesel"]


def setup_url():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0")

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    driver.get(base_url)
    driver.implicitly_wait(3)
    
    try:
        deny = driver.find_element_by_id("onetrust-reject-all-handler")
        deny.click()
        return driver
    except Exception as e:
        return driver
        print(e)
    return driver


def search(fuel,driver):
    driver.implicitly_wait(10)
    cwd = os.getcwd()
    path = cwd + "/" + fuel
    
    filename = path + ".csv"
    
    dd = driver.find_elements_by_class_name("form-control.bb-select")
    

    select = Select(dd[8])
    select.select_by_visible_text('Kontant')
    
    ss = Select(dd[3])
    ss.select_by_visible_text(fuel)
    
    search = driver.find_element_by_class_name("react-autosuggest__input")
    search.send_keys("Audi")
    search.send_keys(Keys.RETURN)
    
    
    count=0
    counter=0
    while True:

        get_cars(fuel,filename,driver)
       
        try:
            next = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.next')))
            next.click()
            driver.implicitly_wait(3)
        except TimeoutException:
            break
        

def get_cars(fuel,filename,driver):
    
    try:
        main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "srp-content"))
        )
        cars = main.find_elements_by_class_name("row.listing.listing-plus.bb-listing-clickable")
        for car in cars:
            make_car_df(car, fuel,filename,driver)
        
    
    except Exception as e:
        print("An exception occurred", e) 


def make_car_df(car,fuel,filename,driver):

        
    complete_car={}
    model = car.find_element_by_class_name("listing-heading.darkLink")
    header = car.find_elements_by_class_name("col-xs-2.listing-data")
    prices = car.find_element_by_class_name("col-xs-3.listing-price ")
    area = car.find_element_by_class_name("col-xs-2.listing-region ")
    Kms = header[1]
    year = header[2]
    

    complete_car['model'] = (model.text[:-2])
    complete_car['price'] = prices.text
    complete_car['km'] = (Kms.text)
    complete_car['location'] = area.text
    complete_car['year'] = int(year.text)
 
    
    print(complete_car)
    df = pd.DataFrame([complete_car])
    df.to_csv(
        path_or_buf=filename,
        sep=";",
        mode="a",
        header=(not os.path.exists(filename)),
        index=False,
        )


def scrap_all_fuels():
    for f in fuel:
        driver = setup_url()
        print(driver)
        search(f,driver)


scrap_all_fuels()