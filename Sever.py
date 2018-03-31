#coding:utf-8
import multiprocessing  #分布式进程
import multiprocessing.managers #分布式进程管理器
import random,time  #随机数，时间
from queue import Queue #队列

import pymongo
import selenium
import selenium.webdriver
import time
import lxml
import lxml.etree


task_queue=Queue() #任务
result_queue=Queue() #结果

def  return_task(): #返回任务队列
    return task_queue
def return_result(): #返回结果队列
    return   result_queue

def getData(html):
    myTree = lxml.etree.HTML(html)
    liList = myTree.xpath('//ul[@id="normal_user_container"]//li')
    girlList = []
    for li in liList[1:]:
        imgUrl = li.xpath('./div//div[1]//a[@class="openBox os_stat"]/img/@src')[0]
        name = li.xpath('./div//div[2]//a[@class="os_stat"]/text()')[0]
        age = li.xpath('./div//p[@class="user_info"]/text()')[0][:2]
        tall = li.xpath('./div//p[@class="zhufang"]/span/text()')[0]
        address = li.xpath('./div//p[1]/text()')[0][-2:]
        girlDict = {'imgUrl':imgUrl,'name':name,'fAge':age,'tall':tall,'address':address}
        girlList.append(girlDict)
    return girlList

def pushImgUrl():
    pass

class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass

if __name__=="__main__":
    multiprocessing.freeze_support()#开启分布式支持
    QueueManger.register("get_task",callable=return_task)#注册函数给客户端调用
    QueueManger.register("get_result", callable=return_result)
    manger=QueueManger(address=("127.0.0.1",8848),authkey=123456) #创建一个管理器，设置地址与密码
    manger.start() #开启
    task,result=manger.get_task(),manger.get_result() #任务，结果

    myCon = pymongo.MongoClient(host='127.0.0.1', port=27017)
    db = myCon['zhenaiwang']
    coll = db['data']

    url = 'http://login.jiayuan.com/?'
    driver = selenium.webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(10)

    driver.find_element_by_id('login_email').send_keys('17512067801')
    driver.find_element_by_id('login_password').send_keys('plj0801')
    time.sleep(2)

    driver.find_element_by_id('login_btn').click()
    time.sleep(2)

    driver.get('http://search.jiayuan.com/v2/')
    for i in range(50):
        print('----------'+str(i))
        time.sleep(3)
        html = driver.page_source
        girlList = getData(html)
        for girl in girlList:
            task.put(girl)
        driver.execute_script("getSearchResult('next')")

    print ("waitting for------")

    for  i  in range(100000):
        res=result.get(timeout=100)
        coll.insert(res)
        print ("get data",res)

    manger.shutdown()#关闭服务器

