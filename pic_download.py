# -*- encoding:utf-8 -*-
import re
import urllib
import urllib.request
from itertools import islice
__author__ = 'Crazycosin'
__date__ = '18-7-3 下午7:29'
import threading
import csv
import ssl
from urllib import request, error
import random

ssl._create_default_https_context = ssl._create_unverified_context#针对https安全访问
ua_list = [
    "Mozilla/5.0 (Windows NT 6.1; ) Apple.... ",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0)... ",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X.... ",
    "Mozilla/5.0 (Macintosh; Intel Mac OS... "
]
user_agent = random.choice(ua_list)

#线程1下载imageurl前一半
def thread_task1(image_list1):
    """
    先要读取前一半的内容,并且以copyright+location+calendar命名照片
    :return:
    """
    n=0
    for row in image_list1:  # 将csv 文件中的数据保存到birth_data中
        imageurl = row.get('url')
        img_name =row.get('name')
        # img_data = urllib.request.urlopen(imageurl).read()
        try:
            # request = urllib.request.Request(imageurl)
            #
            # # 也可以通过调用Request.add_header() 添加/修改一个特定的header
            # request.add_header("User-Agent", user_agent)
            # # 第一个字母大写，后面的全部小写
            # request.get_header("User-agent")
            #
            # response = urllib.request.urlopen(request)
            #
            # data = response.read()
            # imagefile = open(img_name,'wb')
            # imagefile.write(data)
            # imagefile.close()
            urllib.request.urlretrieve(imageurl, (r'D:\Bingpicture\{}.jpg'.format(img_name)).encode())
            n=n+1
            print("线程1第"+str(n)+"张，下载完成")
        except error.URLError as e:
            if hasattr(e, 'code'):
                print("HTTPError")
                print(e.code)
            elif hasattr(e, 'reason'):
                print("URLError")
                print(e.reason)

#线程2下载后一半
def thread_task2(image_list2):
    n=0
    for row in image_list2:  # 将csv 文件中的数据保存到birth_data中
        imageurl = row.get('url')
        img_name =row.get('name')
        # img_data = urllib.request.urlopen(imageurl).read()
        try:
            urllib.request.urlretrieve(imageurl, (r'D:\Bingpicture\{}.jpg'.format(img_name)).encode())
            n=n+1
            print("线程2第"+str(n)+"张，下载完成")
        except error.URLError as e:
            if hasattr(e, 'code'):
                print("HTTPError")
                print(e.code)
            elif hasattr(e, 'reason'):
                print("URLError")
                print(e.reason)


def main():
    with open('bing-ioliu.csv','r',encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        imageurl_list =[]
        for row in islice(csv_reader, 1, None):
            image_url = row[0]
            # image_name = row[1]+row[2].strip()+row[3]
            name = row[3].replace(' ', '').replace('/','&')
            date = row[2]
            image_name = date+","+name
            image_dic = dict(url = image_url,name = image_name)
            imageurl_list.append(image_dic)
        total_lenth = len(imageurl_list)
        imageurl_list1 = imageurl_list[:400]
        imageurl_list2 = imageurl_list[399:total_lenth]
        download_1 = threading.Thread(target=thread_task1,args=(imageurl_list1,))
        download_2 = threading.Thread(target=thread_task2,args=(imageurl_list2,))
        download_1.start()
        download_2.start()
        download_1.join()
        print("线程1结束")
        download_2.join()
        print("线程2结束")
    pass

if __name__ == '__main__':
    main()