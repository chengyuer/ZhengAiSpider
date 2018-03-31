#coding:utf-8
#! ‪C:\Developer\python36\python3.exe

import selenium
import selenium.webdriver
import time
import lxml
import lxml.etree

url = 'http://login.jiayuan.com/?'
driver = selenium.webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)
time.sleep(5)
driver.find_element_by_id('login_email').send_keys('17512067801')
driver.find_element_by_id('login_password').send_keys('plj0801')
time.sleep(2)

driver.find_element_by_id('login_btn').click()

time.sleep(2)

driver.get('http://search.jiayuan.com/v2/')

time.sleep(2)

html = driver.page_source
myTree = lxml.etree.HTML(html)
liList = myTree.xpath('//ul[@id="normal_user_container"]//li')
print(liList)
for li in liList[1:]:
    imgUrl = li.xpath('./div//div[1]//a[@class="openBox os_stat"]/img/@src')[0]
    name = li.xpath('./div//div[2]//a[@class="os_stat"]/text()')[0]
    age = li.xpath('./div//p[@class="user_info"]/text()')[0][:2]
    tall = li.xpath('./div//p[@class="zhufang"]/span/text()')[0]
    address = li.xpath('./div//p[1]/text()')[0][-2:]

    print(imgUrl)
    print(name)
    print(age)
    print(tall)
    print(address)

# file = open('zhenai.txt')
# file.write(driver.page_source.encode('utf-8'))
# html = file.read()

# print(html)

# file.close()

