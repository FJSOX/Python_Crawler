#_*_ coding:utf-8 _*_
#__author__='阳光流淌007'#but代码与20200929失效了，FJSOX对此代码进行了修改使其能够再次运行
#__date__='2018-01-21'
#爬取wallhaven上的的图片，支持自定义搜索关键词，自动爬取并该关键词下所有图片并存入本地电脑。
import os
import requests
import time
import random
from lxml import etree
from scrapy.selector import Selector

#keyWord = input(f"{'Please input the keywords that you want to download :'}")
keyWord="angel"
class Spider():
    #初始化参数
    def __init__(self):
        #headers是请求头，"User-Agent"、"Accept"等字段都是通过谷歌Chrome浏览器查找的！
        self.headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36",
        }
        #filePath是自定义的，本次程序运行后创建的文件夹路径，存放各种需要下载的对象。
        self.filePath = ('D:/mydir/wallpaper/'+ keyWord + '/')

    def creat_File(self):
        #新建本地的文件夹路径，用于存储网页、图片等数据！
        filePath = self.filePath
        #print(filePath)
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        #print(filePath)

    def get_pageNum(self):
        #用来获取搜索关键词得到的结果总页面数,用totalPagenum记录。由于数字是夹在形如：1,985 Wallpapers found for “dog”的string中，
        #所以需要用个小函数，提取字符串中的数字保存到列表numlist中，再逐个拼接成完整数字。。。
        total = ""
        url = ("https://wallhaven.cc/search?q={}&categories=110&purity=100&atleast=1920x1080&sorting=relevance&order=desc").format(keyWord)#categories=110中数字表示general，anime和people
        html = requests.get(url)
        html.encoding='utf-8'
        #html_text = bytes(bytearray(html.text, encoding='utf-8'))
        #print(html.content)
        selector = etree.HTML(html.text)
        pageInfo = selector.xpath('/html/body/main/header/h1/text()')
        string = str(pageInfo[0])
        numlist = list(filter(str.isdigit,string))#提取按个位分离的数字列表
        for item in numlist:
            total += item
        totalPagenum = int(total)
        #print(totalPagenum)
        return totalPagenum

    def main_fuction(self):
        #count是总图片数，times是总页面数
        self.creat_File()
        count = self.get_pageNum()
        print("We have found:{} images!".format(count))
        times = int(count/24 + 1)
        #j = 1
        #pagenum=input("Please input how many pages you want to download(betweens 1 to " + str(times) + "):")#输入想要下载到的页码
        beginpage=input("Please input begin page number which you want to download(betweens 1 to " + str(times) + "):")#开始页码
        pagenum=input("Please input how many pages that you want to download(betweens 1 to " + str(times) + "):")#页码数
        rg=range(times)#构建页码list
        for i in rg[int(beginpage)-1:int(beginpage)+int(pagenum)-1]:#从开始页码（beginpage）遍历页码数（pagenam）个页码，i+1为页码
            pic_Urls = self.getLinks(i+1)
            j=i*24+1#图片编号=（页码-1）*24+1
            for item in pic_Urls:
                self.download(item,j)
                j += 1

    def getLinks(self,number):
        #此函数可以获取给定numvber的页面中所有图片的链接，用List形式返回
        url = ("https://wallhaven.cc/search?q={}&categories=110&purity=100&atleast=1920x1080&sorting=relevance&order=desc&page={}").format(keyWord,number)
        try:
            html = requests.get(url)
            selector = etree.HTML(html.text)
            pic_Linklist = selector.xpath('//a[@class="jsAnchor thumb-tags-toggle tagged"]/@data-href')
        except Exception as e:
            print(repr(e))
        return pic_Linklist


    def download(self,url,count):
        #此函数用于图片下载。其中参数url是形如：https://alpha.wallhaven.cc/wallpaper/616442/thumbTags的网址
        #616442是图片编号，我们需要用strip()得到此编号，然后构造html，html是图片的最终直接下载网址。
        #https://wallhaven.cc/w/011m90
        #https://w.wallhaven.cc/full/ox/wallhaven-oxl5gl.jpg# ox是随机生成的啦！#其实并不是！是最后标识码的前两位！
        #//*[@id="wallpaper"]

        string = url.strip().split('/')[-1]
        html = 'https://w.wallhaven.cc/full/' + string[0:2] + '/wallhaven-' + string + '.jpg'#拼接下载地址
        html2 = 'https://w.wallhaven.cc/full/' + string[0:2] + '/wallhaven-' + string + '.png'#png备胎

        #res = requests.get(url)
        #res.encoding='utf-8'
        #selector = etree.HTML(res.text)
        #html = str(selector.xpath('/html/body/main/section/div[1]/img/@src')[0])#将获取的下载链接转化为str

        pic_path = (self.filePath + keyWord + str(count) + '.jpg' )
        try:
            pic = requests.get(html,headers = self.headers)
            if pic.status_code==404:#当图片为png格式时返回404，此时启用png备胎并将图片存为png格式
                pic = requests.get(html2,headers = self.headers)
                pic_path = (self.filePath + keyWord + str(count) + '.png' )
            f = open(pic_path,'wb')
            f.write(pic.content)
            f.close()
            print("Image:{} has been downloaded!".format(count))
            time.sleep(random.uniform(0,0.5))#下完后随机休眠0~0.5s以防服务器发现是爬虫
        except Exception as e:
            print(repr(e))


spider = Spider()
spider.main_fuction()