#!/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException
import time
from pyvirtualdisplay import Display
from tqdm import tqdm
import re
import json
import os
import arrow
import traceback

os.system('killall chromium 2>/dev/null')

#display = Display(backend="xvfb", visible=1, size=(800, 800))
#display.start()
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
chrome_options.add_argument("user-data-dir=selenium")
chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-gpu')

#specify the path to chromedriver.exe (download and save on your computer)
driver = webdriver.Chrome(options=chrome_options)
#driver.maximize_window()

print('loading page')
driver.get("https://centralfloridapickandpay.com/vehicle-inventory/")

cars=[]
#if os.path.exists('cars.json'):
#    f=open('cars.json', 'r')
#    cars = json.loads(f.read())
#    f.close()
#print(f'loaded {len(cars)} existing cars')
#before_len = len(cars)
#newcars = 0

print('scraping inventory')
page_count = int(driver.find_elements(By.XPATH, "//li[@class='paginate_button page-item ']/a")[-1].get_attribute('innerHTML'))
for page in tqdm(range(page_count)):
    cars_e = driver.find_elements(By.XPATH, "//table[@id='vehicles']/tbody/tr")
    
    def findcar(cars, vin):
        for car in cars:
            if car['vin'] == vin:
                return car
    
    for car_e in cars_e:
        try:
    #        print(car_e.text)
            car = {}
    
    #        car['vin'] = re.search("VIN: (\w*)", car_e.text).group(1)
    
            # check if car has already been scraped
    #        existing_car = findcar(cars, car['vin']) 
    #        if existing_car != None:
    #            existing_car['last_seen'] = arrow.utcnow().isoformat()
    #            continue;
    
            car['year'] = car_e.find_element(By.XPATH, "./td[@data-label='Year']").get_attribute('innerHTML')
            car['make'] = car_e.find_element(By.XPATH, "./td[@data-label='Make']").get_attribute('innerHTML')
            car['model'] = car_e.find_element(By.XPATH, "./td[@data-label='Model']").get_attribute('innerHTML')
            car['color'] = car_e.find_element(By.XPATH, "./td[@data-label='Color']").get_attribute('innerHTML')
            car['engine'] = car_e.find_element(By.XPATH, "./td[@data-label='Engine']").get_attribute('innerHTML')
            car['row'] = car_e.find_element(By.XPATH, "./td[@data-label='Row']").get_attribute('innerHTML')
            car['arrived'] = car_e.find_element(By.XPATH, "./td[@data-label='Arrived']").get_attribute('innerHTML')
            car['vin'] = car_e.find_element(By.XPATH, "./td[@data-label='vin']").get_attribute('innerHTML')
#            print(car)
    
    #        r = re.compile("(\d{4}) ([\w\-]*) ([\w\- ]*).*\nColor")
    #        getparam('year', r, 1)
    #        car['year'] = int(car['year'])
    #        getparam('make', r, 2)
    #        getparam('model', r, 3)
    #        getparam('color', "Color: (\w*)", 1)
    #        getparam('section', "Section: ([\w\/]*)", 1)
    #        getparam('row', "Row: (\w*)", 1)
    #        getparam('space', "Space: (\w*)", 1)
    #        getparam('stock #', "Stock #: (\w*.\w)", 1)
    #        getparam('available_date', "Available: ([\d/]*)", 1)
    #        car['image_url'] = car_e.find_element(By.XPATH, "./a[1]/img[1]").get_attribute("src")
    #        car['first_seen'] = arrow.utcnow().isoformat()
    #        car['last_seen'] = arrow.utcnow().isoformat()
    #        car['available'] = "true"
            cars.append(car)
    #        newcars+=1
    #        print(f"{car['year']} {car['make']} {car['model']} {car['vin']} {car['image_url']}")
        except Exception:
            print(traceback.format_exc())

    nextbutton = driver.find_element(By.XPATH, "//li[@id='vehicles_next']/a")
    driver.execute_script("arguments[0].scrollIntoView(true);", nextbutton);
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(nextbutton))
    for i in range(10):
        try:
            nextbutton.click()
            break
        except:
            pass
    
# TODO check for cars that aren't there any more

#print(f'prev {before_len}, new total {len(cars)}, with {newcars} new cars found')
print(f'{len(cars)} cars found')

with open('cars_cfpnp.json', 'w') as f:
    f.write(json.dumps(cars, indent=4))
    f.close()

