from webbrowser import Chrome
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
sites = ['http://sinhala.adaderana.lk/']
driver = webdriver.Chrome('C:\\SeleniumDriver\\chromedriver')
today = datetime.now().date()
addresses = []
news_list = []
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
    #titles = ['උණුසුම් පුවත්','වෙනත් පුවත්','ක්‍රීඩා පිට්ය','සයුරෙන් එතෙර']
    titles = ['උණුසුම් පුවත්']
    for title in titles:
        print(title)
        driver.find_element(By.XPATH, '//a[@title =\''+title+'\']').click()
        elements = driver.find_elements(By.XPATH, "//h2/a")
        for element in elements:
            addr = element.get_attribute("href")
            addresses.append(addr)
    for address in addresses:
        driver.get(address)
        date  = driver.find_element_by_xpath('//p[@class="news-datestamp english-font"]').text
        date = str(date).split(' ')
        if getDate(date) == today:
            news = driver.find_element_by_xpath("//div[@class='news-content']").text
            news_list.append(news)


if __name__ == '__main__':
    print(today)
    for site in sites:
        grabSite(site)
    #getDate(['|', 'October', '23,', '2020', '', '9:33', 'am'])
    driver.quit()
    a_file = open('news_updated.txt', 'w', encoding='utf-8', errors='ignore')
    a_file.write(str(news_list))
