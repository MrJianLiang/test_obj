import requests
from lxml import html
from io import BytesIO
import base64
import re
import random
from fontTools.ttLib import TTFont
import time


def clear_area(AreaString):
    return re.sub('\s', '', AreaString)

def ran_time():
    ran_int = random.uniform(5,10)
    print('等待时间为:',ran_int)
    return ran_int


def headers():
    # 随机更换user-agents
    agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.2.1000 Chrome/39.0.2146.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 QQBrowser/9.4.7658.400',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.12150.8 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0',
    ]
    Agent = random.choice(agents)
    headers = {
    "User-Agent": Agent,
    }
    return headers


def clear_data(string):
    lone = map(lambda x:x.strip(),string)
    return lone



def get_page_info(url):
    req = requests.get(url=url,headers=headers())

    # 获取当前网页字体
    font = re.findall(r"charset=utf-8;base64,(.*?)'",req.text)[0]
    # print(font)
    time.sleep(ran_time())

    select = html.fromstring(req.text)

    title = select.xpath("//ul[@class='listUl']/li/div[@class='des']/h2/a/text()")

    # 价格
    price = select.xpath("//div[@class='listliright']/div[@class='money']/b/text()")

    title = clear_data(title)
    title = list(title)
    print(len(list(title)))
    print(len(price))
    # print(title)

    # 面积
    # area1 = select.xpath("//div[@class='des']/p/text()")
    # area2 = clear_area(area1)
    # area3 = crack_num(font,area2)
    # print(area3)



    # t1 = crack_num(font,title[0])
    # print("标题：",t1)
    # a = crack_num(font,price[0])
    # print('price:',a)

    # return font,title,price
    # 保存到文件中
    for i in range(len(price)):
        with open('test房价.csv','a',encoding='utf8') as f:
            f.write('标题:'+crack_num(font,title[i])+'     '+crack_num(font,price[i])+'\n')
            print(crack_num(font,title[i]))


# 像解密函数中传递两个参数 字体 和 需要解密的文字
def crack_num(base64String,string):
    # 解析为base64字节形式字符串
    bin_data = base64.decodebytes(base64String.encode())
    # print(bin_data)
    # 将得到的 base64 字符串当做文件 在内存中操作
    font = TTFont(BytesIO(bin_data))
    # 得到xml文件中 对应的字体
    utf8_code = font.getBestCmap()
    # print(utf8_code)

    # 进行字体转换  定义一个列表 传入函数的值  进行转换完成后 添加进列表
    num_list = []

    for char in string:
        # 如果要解析的字在 xml 文件中
        # ord() 函数返回的是 一个 ascii 的编码节点
        decode_num = ord(char)
        # 如果解密出来的字体在 xml文件中 则进行解密
        if decode_num in utf8_code:
            num = utf8_code[decode_num]
            # print(num1)
            num = int(num[-2:]) -1
            # print(num)
            num_list.append(num)
        else:
            # 如果是正常字体则添加到列表中
            num_list.append(char)
    # 定义个字符串
    ret_str_show = ''
    for num in num_list:
        ret_str_show +=str(num)


    return ret_str_show

if __name__ == '__main__':
    for i in range(71):
    # url = 'https://sh.58.com/chuzu/'
        print('开始爬取58同城出租第%s页'%i)
    # url = 'https://sh.58.com/chuzu/pn3/'
    #     url = 'https://sh.58.com/ershoufang/0/pn%s/'%str(i)
        url = 'https://sh.58.com/chuzu/sub/0/pn%s/'%str(i)
        get_page_info(url)