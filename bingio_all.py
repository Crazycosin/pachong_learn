# -*- encoding:utf-8 -*-
import csv

__author__ = 'Crazycosin'
__date__ = '18-7-3 下午12:31'
# urllib2_urlopen.py

# 导入urllib2 库
import urllib.request
import random
import re
import threading

def getHtml(page):
    # 向指定的url发送请求，并返回服务器响应的类文件对象
    url = "https://bing.ioliu.cn/?p="+str(page)
    ua_list = [
        "Mozilla/5.0 (Windows NT 6.1; ) Apple.... ",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0)... ",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X.... ",
        "Mozilla/5.0 (Macintosh; Intel Mac OS... "
    ]

    user_agent = random.choice(ua_list)
    request = urllib.request.Request(url)

    #也可以通过调用Request.add_header() 添加/修改一个特定的header
    request.add_header("User-Agent", user_agent)

    # 第一个字母大写，后面的全部小写
    request.get_header("User-agent")
    response = urllib.request.urlopen(request)

    # 类文件对象支持 文件对象的操作方法，如read()方法读取文件全部内容，返回字符串
    html = response.read().decode('utf-8')

    return html


def getItem(html):
    #获取每页中图片存在的item标签(<font>((?!</?font>).)*</font>)	)*	</font>
    item_pattern = re.compile('<div class="item">(.*?)</div>*</div>')
    item_list = re.findall(item_pattern,html)
    return item_list


def getImage_detail(item):

    #正则匹配<h3>标签中间的图片copyright
    copyright_pattern =re.compile('<h3>(.*?)</h3>')
    copyright_list = re.findall(copyright_pattern,item)[0]

    #正则匹配图片上传时间
    imagecalendar_pattern = re.compile('<i class="icon icon-calendar"></i><em class="t">(.*?)</em>')
    imagecalendar_list = re.findall(imagecalendar_pattern,item)[0]

    #图片拍摄地址
    imagelocation_pattern = re.compile('<i class="icon icon-location"></i><em class="t">(.*?)</em>')
    imagelocation_list = re.findall(imagelocation_pattern,item)
    print(imagelocation_list)
    #判断是否为空，设置默认值，避免取值越界
    if imagelocation_list:
        imagelocation_list = imagelocation_list[0]
    else:
        imagelocation_list = "地球"
        print("赋值成功")
    print(imagelocation_list)

    #图片下载地址
    imageurl_pattern = re.compile('<a .*class="ctrl download"? href=(.*?)target')
    imageurl_list = "https://bing.ioliu.cn"+re.findall(imageurl_pattern,item)[0].strip('" ')


    return copyright_list,imagecalendar_list,imagelocation_list,imageurl_list


#将数据写入csv文件中,保存copyright,calendar,拼接好的图片下载地址,图片拍摄地址
def imageDetail_Csv(image_list):
    headers = ['image_url', 'image_location', 'image_calendar', 'image_copyright']
    with open('bing-ioliu.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile,headers)
        writer.writeheader()
        writer.writerows(image_list)
        csvfile.close()


def main():
    index = urllib.request.urlopen('https://bing.ioliu.cn/').read().decode('utf-8')
    totalpage_pattern = re.compile('<div class="page">.*<span>(.*?)</span>.*</div>')#获取总页数
    totalpage_list = re.findall(totalpage_pattern,index)
    totalpage = int(str(totalpage_list).split('/')[1].split("'")[0])
    image_list = []
    # page应该是从第一页到71页
    for page in range(1,totalpage+1):
        html = getHtml(page)
        item_list = getItem(html)
        page_index ='正抓取第' +str(page)+'页'
        print(page_index)
        for item in item_list:
            image_copyright,image_calendar,image_location,image_url = getImage_detail(item)
            image_dic = dict(image_copyright=image_copyright,
                             image_calendar=image_calendar,
                             image_location=image_location,
                             image_url=image_url)  # 构建图片信息的字典，便于转换成json对象
            image_list.append(image_dic)
    print("抓取结束")
    imageDetail_Csv(image_list)


if __name__ == '__main__':
    main()