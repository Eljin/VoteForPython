# -*- coding: utf-8 -*-

import requests
import random
from lxml import etree


def get_proxies_from_site():
    url = 'http://web.etiantian.com/learnInEtiantian/'
    # requests.encoding = "utf-8"
    r = requests.get(url)
    tree = etree.HTML(r.text)

    name = tree.xpath("//strong[@id=2731423]/../../p[@class='one']/text()")[0].encode('utf-8')
    vote = tree.xpath("//strong[@id=2731423]/text()")[0]
    name1 = tree.xpath("//strong[@id=2796501]/../../p[@class='one']/text()")[0].encode('utf-8')
    vote1 = tree.xpath("//strong[@id=2796501]/text()")[0]

    print "%s【2731423】=(%s),%s【2796501】=(%s)" %(name,vote,name1,vote1)

if __name__ == '__main__':
    get_proxies_from_site()