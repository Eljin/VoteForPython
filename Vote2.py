# -*- coding: utf-8 -*-

import requests
import random
from lxml import etree


def get_proxies_from_site():
    url = 'http://www.89ip.cn/tiqu.php?sxb=&tqsl=500&ports=&ktip=&xl=on&submit=%CC%E1++%C8%A1'
    xpath = '/html/body/a/[last()]/text()'

    r = requests.get(url)
    tree = etree.HTML(r.text)

    results = tree.xpath(xpath)
    print results
    proxies = [line.strip() for line in results]

    return proxies

#使用http://lwons.com/wx网页来测试代理主机是否可用
def get_valid_proxies(proxies, count):
    url = 'http://lwons.com/wx'
    results = []
    cur = 0
    for p in proxies:
        proxy = {'http': 'http://' + p}
        succeed = False
        try:
            r = requests.get(url, proxies=proxy)
            if r.text == 'default':
                succeed = True
        except Exception, e:
            print 'error:', p
            succeed = False
        if succeed:
            print 'succeed:', p
            results.append(p)
            cur += 1
            if cur >= count:
                break

def req_post():
    url = "http://web.etiantian.com/learnInEtiantian/ajaxVote.jsp"
    req_header = {
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; MyIE9; BTRS123646; .NET CLR 2.0.50727; .NET CLR 31.01.4506.2152; .NET CLR 3.5.30729)',
    'Accept':'text/html;q=0.9,*/*;q=0.8',
     'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
     'Accept-Encoding':'gzip',
     'Connection':'Keep-Alive',
     'Referer':'http://web.etiantian.com/learnInEtiantian/show.jsp?userId=2796501', #注意如果依然不能抓取的话，这里可以设置抓取网站的host
     'Cookie': 'ss',
     'CLIENT-IP':'139.196.0.31',
     'X-FORWARDED-FOR':'139.196.0.31'
      }
    a = random.random()
    b = str(a)
    postData = {'userId':'2796501','rdm':b+'05827'}
    r = requests.post(url,data=postData,headers=req_header)
    # print r.headers
    print '=='+r.text



if __name__ == '__main__':
    #print 'get ' + str(len(get_valid_proxies(get_proxies_from_site(), 20))) + ' proxies'
    # req_post()
    print get_proxies_from_site()