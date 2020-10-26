from webbrowser import Chrome
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
# Look to the path of your current working directory

from selenium.webdriver.common.keys import Keys
from time import sleep
sites = ['https://www.citizen.lk/category/8']
driver = webdriver.Chrome('C:\\SeleniumDriver\\chromedriver')
today = datetime.now().date()
addresses = []
news_list = []
working_directory = os.getcwd()

def getDate(date):
    months = ['january','february','march','aprial','may','june','july','august','september','october','november','december']
    month = months.index(date[0].lower())+1
    day = int(date[1].split(',')[0])
    year = int(date[2])
    x = datetime(year,month,day).date()
    return x

def grabSite(url):
    driver.get(url)
    driver.implicitly_wait(3)
    elements = driver.find_elements(By.XPATH, '//h3/a')
    for element in elements:
        addr = element.get_attribute("href")
        addresses.append(addr)
    for address in addresses:
        driver.get(address)
        news = driver.find_element_by_xpath("//div[@class='single-blog-wrapper']").text
        news_list.append(news)


if __name__ == '__main__':
    print(today)
    for site in sites:
        grabSite(site)
    driver.quit()
    a_file = open('G:/FYP/FYP_Approches/Sinhala_News/Citizen/citizen_news_'+str(today)+'.txt', 'w', encoding='utf-8', errors='ignore')
    a_file.write(str(news_list))
