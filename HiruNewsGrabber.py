import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
sites = ['https://www.hirunews.lk/local-news.php?pageID=1','https://www.hirunews.lk/local-news.php?pageID=2','https://www.hirunews.lk/local-news.php?pageID=3','https://www.hirunews.lk/international-news.php','https://www.hirunews.lk/international-news.php?pageID=2','https://www.hirunews.lk/international-news.php?pageID=3']
driver = webdriver.Chrome('C:\\SeleniumDriver\\chromedriver')
today = datetime.now().date()
addresses = []
news_list = []
working_directory = os.getcwd()

def grabSite(url):
    driver.get(url)
    driver.implicitly_wait(3)
    elements = driver.find_elements(By.XPATH, "//div[@class='column middle']/a")
    for element in elements:
        address = element.get_attribute('href')
        addresses.append(address)
    for address in addresses:
        driver.get(address)
        news = driver.find_element_by_id("article-phara").text
        news_list.append(news)

if __name__ == '__main__':
    print(today)
    for site in sites:
        addresses = []
        grabSite(site)
    driver.quit()
    with open('G:/FYP/FYP_Approches/Sinhala_News/HiruNews/hiru_news_' + str(today) + '.txt', 'w',encoding='utf-8', errors='ignore') as a_file:
        json.dump(news_list,a_file)
