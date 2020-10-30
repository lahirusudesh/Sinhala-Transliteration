
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
sites = ['http://sinhala.adaderana.lk/']
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
def getDate1(date):
    months = ['january','february','march','aprial','may','june','july','august','september','october','november','december']
    month = months.index(date[1].lower())+1
    day = int(date[2].split(',')[0])
    year = int(date[3])
    x = datetime(year,month,day).date()
    return x

def grabSite(url):
    driver.get(url)
    driver.implicitly_wait(3)
    titles = ['උණුසුම් පුවත්','වෙනත් පුවත්','ක්‍රීඩා පිට්ය','සයුරෙන් එතෙර']
    #titles = ['උණුසුම් පුවත්']
    for title in titles:
        print(title)
        driver.find_element(By.XPATH, '//a[@title =\''+title+'\']').click()
        elements = driver.find_elements(By.XPATH, "//h2/a")
        for element in elements:
            addr = element.get_attribute("href")
            addresses.append(addr)
    for address in addresses:
        driver.get(address)
        news = driver.find_element_by_xpath("//div[@class='news-content']").text
        news_list.append(news)


if __name__ == '__main__':
    print(today)
    for site in sites:
        grabSite(site)
    driver.quit()
    a_file = open('G:/FYP/FYP_Approches/Sinhala_News/AdaDerana/adaderana_news_'+str(today)+'.txt', 'w', encoding='utf-8', errors='ignore')
    a_file.write(str(news_list))
    a_file.close()
