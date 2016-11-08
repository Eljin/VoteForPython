# -*- coding: utf-8 -*-

import urllib2
import random
from threading import Thread
from time import time
import re
from lxml import etree
import codecs
import requests
import sys

#ip代理网站
#http://www.daili666.net/ 购买的可用率90%，免费的可用率很底  舍得花钱建议买这个
#http://www.89ip.cn 可用率不是很稳定
#http://www.xicidaili.com/  可用率不是很稳定

class Vote(Thread):
    def __init__(self, proxy):
        Thread.__init__(self)
        self.proxy = proxy
        self.url = 'http://web.etiantian.com/learnInEtiantian/ajaxVote.jsp?userId=2796501'  #2796501,,,1781105
        self.timeout = 10
        
    def run(self):
        enable_proxy = True
        # print  r'proxy http://%s' % self.proxy + '\t'
        proxy_handle = urllib2.ProxyHandler({"http": r'http://%s' % self.proxy})
        null_proxy_handle = urllib2.ProxyHandler({})
        # httpHandler = urllib2.HTTPHandler(debuglevel=1)
        if enable_proxy:
            opener = urllib2.build_opener(proxy_handle)
            # opener = urllib2.build_opener(proxy_handle,httpHandler)
        else:
            opener = urllib2.build_opener(null_proxy_handle)

        urllib2.install_opener(opener)
        try:
            a = random.random()
            b = str(a)
            Headers={'User-Agent': 'Mozilla/5.0 ','Cookie': 'JSESSIONID=4D'+b+'79652-n1.tomcat4'}
            req = urllib2.urlopen(urllib2.Request(self.url,headers=Headers),timeout=self.timeout)
            result = req.read().lstrip().decode('utf-8')
            # print result
            pos = result.find(u'成功')
            if pos > 1:
                print result
                addnum()
            else:
                pass
        except Exception, e:
            # e.info()  e.read() e.reason e.geturl()
            # print 'error : ' , e
            # print e,',error'
            pass


def addnum():
    global n
    n += 1

def shownum():
    return n

n = 0

threads = []
results = []

# 读取代理配置文件获取代理ip
def get_proxies_from_local():
    global threads
    proxylist = open('proxy.txt', 'r')
    regex = re.compile("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\:\d{1,4})?")
    i=0
    threads=[]
    for proxy in proxylist:
        ip = re.findall(regex, proxy)
        if len(ip) > 0 :
            t = Vote(ip[0])
            threads.append(t)
            i +=1
    # proxylist.close()
    print i

# 从代理api获取代理ip  :one  
def get_proxies_from_sit(count=100):
    global threads , results , n

    if len(results)==0 :
        xpath = "/html/body/div[@class='mass']/br/following-sibling::text()"
        url = 'http://www.89ip.cn/api/?&tqsl='+str(count)+'&sxa=&sxb=&tta=&ports=&ktip=&cf=1'
        print ' get proxy sit %s' %url

        content = requests.get(url).text
        # print content
        tree = etree.HTML(content)
        results = tree.xpath(xpath)
        results.pop()   # 删除最后一个无用元素
        print '=uccess get sit proxis, size== %s' %len(results)
    threads = []
    for k in results:
        t = Vote(k)
        threads.append(t)
    print "=threads size==%s" %len(threads)
    
# 从代理api获取代理ip  :two
def get_proxies_from_sit2(count=1):
    global threads,results
    # xpath="/descendant::table[@id='ip_list']/tbody/tr[@class='odd']/td[position()==2]/text()/following-sibling::td/text()"
    xpath="/descendant::table[@id='ip_list']/tr[@class='odd']/td[position()=2]/text()"
    xpath_post="/descendant::table[@id='ip_list']/tr[@class='odd']/td[position()=3]/text()"
    url = "http://www.xicidaili.com/nn/"+str(count)
    reqheaders={'Content-type':'application/x-www-form-urlencoded',  
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Host':'www.xicidaili.com', 
    'Origin':'http://www.xicidaili.com',  'Referer':'http://www.xicidaili.com',  
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'}
    content=requests.get(url,None,headers=reqheaders,allow_redirects=False).text
    # content = requests.get(url).text

    # url = 'xxx.html'
    # f = codecs.open(url,'r','UTF-8')
    # content = f.read()
    # f.close()

    # print content
    tree = etree.HTML(content)
    results = tree.xpath(xpath)
    results_post = tree.xpath(xpath_post)

    # print results,results_post

    threads = []
    for i in range(len(results)):
        # print results[i]+':'+results_post[i]
        t = Vote(results[i]+':'+results_post[i])
        threads.append(t)
    print "=threads size==%s" %len(threads)

# 从代理api获取代理ip  :three
def get_proxies_from_sit3(num=10):
    global threads,results
    if len(results)==0 :
        url = "http://qsrdk.daili666api.com/ip/?tid=558881954209756&num=%s" %num;
        content = requests.get(url).text
        # print content
        regex = re.compile("(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\:\d{1,4})?")
        results = re.findall(regex, content)
        print "get proxy ips %s" %len(results)
        
    threads=[]
    for ip in results:
        t = Vote(ip)
        threads.append(t)
    

def do_process(cycle,proxy_count):
     for ii in range(cycle):
        get_proxies_from_local()
        # get_proxies_from_sit(proxy_count)
        # get_proxies_from_sit2(cycle)
        # get_proxies_from_sit3(proxy_count)
        
        start_time = time()
        for i in threads:
            i.start()
        for i in threads:
            i.join()
        print '\n %s votes have been voted successfully using %s seconds,cycle count %s' % (shownum(), time()-start_time,ii+1)


if __name__ == '__main__':
    cycle,proxy_count,targetVote=2,10,-1

    cycle = len(sys.argv) > 1 and int(sys.argv[1]) or cycle
    proxy_count = len(sys.argv) > 2 and sys.argv[2] or proxy_count
    targetVote = len(sys.argv) > 3 and int(sys.argv[3]) or targetVote

    while targetVote > 0 and shownum()<targetVote:
      results=[]
      do_process(cycle,proxy_count)
      print '显示是否满足目标投票数bool=',shownum()<targetVote
      