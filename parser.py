from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from time import sleep

import pandas as pd


url = 'https://rabota.by/search/vacancy?text=%D0%A1%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D1%81%D1%82+%D0%BF%D0%BE+%D0%BA%D0%B8%D0%B1%D0%B5%D1%80%D0%B1%D0%B5%D0%B7%D0%BE%D0%BF%D0%B0%D1%81%D0%BD%D0%BE%D1%81%D1%82%D0%B8&salary=&ored_clusters=true&excluded_text=&area=1002&page=1&search'

options = webdriver.ChromeOptions()


def opt():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 MyAwesomeBot/1.0"
    options.add_argument(f"--user-agent={my_user_agent}")

def get_driver():
    options = opt()
    driver = webdriver.Chrome(options=options)
    return driver

def get_page(url:str, driver:webdriver.Chrome) -> webdriver.Chrome:
    driver.get(url)
    return driver

def parser_list(url, time_wait:int, driver:webdriver.Chrome) -> list:
    answer = []
    driver = get_page(url, driver)
    sleep(time_wait)
    list_divs = driver.find_elements(By.CLASS_NAME, 'vacancy-info--ieHKDTkezpEj0Gsx')
    sleep(time_wait)
    for div in list_divs:
        href = div.find_element(By.TAG_NAME, 'a').get_attribute('href')
        answer.append(href)
    
def parser_vacancy(vacancy:str, time_wait, driver:webdriver.Chrome):
    driver = get_page(vacancy,driver)
    sleep(time_wait)
    



def main():
    driver = get_driver()
    print(parser_list(url, 3, driver))

if __name__ == '__main__':
    main()








