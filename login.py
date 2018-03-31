#coding:utf-8
#! ‪C:\Developer\python36\python3.exe
import selenium
import selenium.webdriver
import time

url = 'http://login.jiayuan.com/?'
driver = selenium.webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)
time.sleep(5)
driver.find_element_by_id('login_email').send_keys('17512067801')
driver.find_element_by_id('login_password').send_keys('plj0801')
time.sleep(2)
#
driver.find_element_by_id('login_btn').click()
#
time.sleep(2)
#
driver.get('http://search.jiayuan.com/v2/')

time.sleep(2)

driver.execute_script("getSearchResult('next')")
html = driver.page_source

# time.sleep(2)

# driver.execute_script("getSearchResult('next')")
#
driver.execute_script("window.scrollBy(0, 700)")
time.sleep(2)

# driver.execute_script("getSearchResult('next')")
#
time.sleep(20)

