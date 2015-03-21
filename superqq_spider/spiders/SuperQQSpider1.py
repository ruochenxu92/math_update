__author__ = 'Xiaomin'

from scrapy.spider import Spider
from scrapy.utils.response import open_in_browser
import scrapy
import os
from superqq_spider.items import Paper
import datetime
import json

from superqq_spider.utils import utils

tool = utils()
def getUrls():
    urls = []
    urls += ['http://arxiv.org/list/cs/1501?show=1302', 'http://arxiv.org/list/cs/1502?show=1480', 'http://arxiv.org/list/cs/1503?show=1075']
    return urls

class CS499Spider(Spider):
    hostname = 'http://arxiv.org'
    name = 'xxu461'
    #allowed_domains = ['http://cs.illinois.edu']
    start_urls = getUrls()

    def __init__(self):
        self.count = 0

    def parse(self, response):
        i = 1
        # print response.xpath('//*[@id="dlpage"]/dl/dd[1]/div/div[1]/text()').extract()[0]
        prefix = 'http://arxiv.org'
        for sel in response.xpath('//*[@id="dlpage"]/dl[1]/dt'):
            item = Paper()
            item['urllink'] = prefix + sel.xpath('span/a[1]/@href').extract()[0]
            item['pdflink'] = prefix + sel.xpath('span/a[2]/@href').extract()[0]
            item['category'] = response.xpath('//*[@id="dlpage"]/h1/text()').extract()[0]
            seeMore = item['urllink']
            request = scrapy.Request(seeMore, callback=self.parseMovieDetails)
            request.meta['item'] = item
            i += 1
            yield request


    def parseMovieDetails(self,response):
        item = response.meta['item']
        buffer = ''
        for content in response.xpath('//*[@id="abs"]/div[2]/div[2]/a'):
            buffer += content.xpath('text()').extract()[0] + ', '
        item['authors'] = buffer[:-1]
        item['title']= response.xpath('//*[@id="abs"]/div[2]/h1/text()').extract()[0]
        item['subjects']= response.xpath('//*[@class="primary-subject"]/text()').extract()[0]
        abstract = response.xpath('//*[@id="abs"]/div[2]/blockquote').extract()[0]
        item['abstract']= tool.once_clean(abstract[80:-13])
        str1 = (response.xpath('//*[@id="abs"]/div[2]/div[3]/text()').extract()[0])[-12:-1]
        li = str1.split()
        li[2] = li[2][2:]
        str1 = ' '.join(li)
        temp = datetime.datetime.strptime(str1,'%d %b %y')
        item['date'] = str(temp.year) + '-' + str(temp.month) + '-' + str(temp.day)
        return item