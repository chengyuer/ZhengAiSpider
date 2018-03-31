#coding:utf-8
import multiprocessing  #分布式进程
import multiprocessing.managers #分布式进程管理器
import random,time  #随机数，时间
from queue import Queue #队列
import threading
import gevent
import gevent.monkey
import aip
from aip import AipNlp
from aip import AipFace
import urllib
import urllib.request

APP_ID = '10253494'
API_KEY = 'NAh5KkgrKTPyxzUBewCAakvm'
SECRET_KEY = 'nTrHzPhh0CQP9H9Idz3jftsji9NgVdvF'

aipFace = AipFace(APP_ID, API_KEY, SECRET_KEY)
class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def getAgeBeauty(filePath):

    options = {
        'max_face_num': 1,
        'face_fields': "age,beauty",
    }
    # 调用人脸属性检测接口
    result = aipFace.detect(get_file_content(filePath), options)
    try:
        data = {'age':str(int(result['result'][0]['age'])),'beauty':str(result['result'][0]['beauty'])}
        return data
    except:
        pass

def downImg(filePath,imgUrl):
    url = imgUrl
    urllib.request.urlretrieve(url, filename=filePath)


def checkImg(data,result):
    name = data['name']
    imgUrl = data['imgUrl']
    fAge = data['fAge']
    tall = data['tall']
    address = data['address']
    fileName = name+'_'+address+'.jpg'
    filePath = './girlImgs/'+fileName
    downImg(filePath, imgUrl)
    print('download:'+name)
    time.sleep(2)
    aiData = getAgeBeauty(filePath)
    aiAge = aiData['age']
    beauty = aiData['beauty']
    girlDict = {'name':name,'herAge':fAge,'aiAge':aiAge,'beauty':beauty,'tall':tall,'address':address,'img':filePath}
    result.put(girlDict)



if __name__=="__main__":
    QueueManger.register("get_task")  # 注册函数调用服务器
    QueueManger.register("get_result")
    manger=QueueManger(address=("127.0.0.1",8848),authkey=123456)
    manger.connect()  #链接服务器
    task= manger.get_task()
    result =manger.get_result()  # 任务，结果


    for  i  in range(10000):
        data = task.get()
        checkImg(data,result)


