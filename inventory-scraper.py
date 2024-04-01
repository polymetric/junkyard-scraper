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

headless = False

os.system('killall chromium')

#display = Display(backend="xvfb", visible=1, size=(800, 800))
#display.start()
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
chrome_options.add_argument("user-data-dir=selenium")
#chrome_options.add_argument('headless')
chrome_options.add_argument('--disable-gpu')

#specify the path to chromedriver.exe (download and save on your computer)
driver = webdriver.Chrome(options=chrome_options)

def scroll_down(f=None):
    print('scrolling')
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        if f != None:
            if f():
                return
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        print('i')

print('loading page')
driver.get("https://www.lkqpickyourpart.com/inventory/orlando-1134/")

print('scrolling down')
scroll_down()
print('done scrolling')

cars={}
if os.path.exists('cars.json'):
    f=open('cars.json', 'r')
    cars = json.loads(f.read())
    f.close()
print(f'loaded {len(cars)} existing cars')
before_len = len(cars)

print('scraping inventory')
cars_e = driver.find_elements(By.XPATH, "//div[@class='pypvi_resultRow']")
cars = []

for car_e in tqdm(cars_e):
    try:
        print(car_e.text)
        car = {}
        r = re.compile("(\d{4}) ([\w\-]*) ([\w\- ]*).*\nColor")
        car['year'] = r.search(car_e.text).group(1)
        car['make'] = r.search(car_e.text).group(2)
        car['model'] = r.search(car_e.text).group(3)
        car['vin'] = re.search("VIN: (\w*)", car_e.text).group(1)
        car['color'] = re.search("Color: (\w*)", car_e.text).group(1)
        car['section'] = re.search("Section: ([\w\/]*)", car_e.text).group(1)
        car['row'] = re.search("Row: (\w*)", car_e.text).group(1)
        car['space'] = re.search("Space: (\w*)", car_e.text).group(1)
        car['stock #'] = re.search("Stock #: (\w*.\w)", car_e.text).group(1)
        car['available'] = re.search("Available: (\w*)", car_e.text).group(1)
        car['image_url'] = car_e.find_element(By.XPATH, "./a[1]/img[1]").get_attribute("src")
        cars.append(car)
    except Exception as e:
        # TODO handle these individually so we don't throw out the whole entry 
        print(e)
#    print(f"{car['year']} {car['make']} {car['model']} {car['vin']} {car['image_url']}")

print(f'found {len(cars)} cars')

with open('cars.json', 'w') as f:
    f.write(json.dumps(cars, indent=4))
    f.close()

