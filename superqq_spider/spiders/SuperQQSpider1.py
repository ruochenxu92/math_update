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
    urls += ['http://arxiv.org/list/math.AG/new',
'http://arxiv.org/list/math.AT/new',
'http://arxiv.org/list/math.AP/new',
'http://arxiv.org/list/math.CT/new',
'http://arxiv.org/list/math.CA/new',
'http://arxiv.org/list/math.CO/new',
'http://arxiv.org/list/math.AC/new',
'http://arxiv.org/list/math.CV/new',
'http://arxiv.org/list/math.DG/new',
'http://arxiv.org/list/math.DS/new',
'http://arxiv.org/list/math.FA/new',
'http://arxiv.org/list/math.GM/new',
'http://arxiv.org/list/math.GN/new',
'http://arxiv.org/list/math.GT/new',
'http://arxiv.org/list/math.GR/new',
'http://arxiv.org/list/math.HO/new',
'http://arxiv.org/list/math.IT/new',
'http://arxiv.org/list/math.KT/new',
'http://arxiv.org/list/math.LO/new',
'http://arxiv.org/list/math.MP/new',
'http://arxiv.org/list/math.MG/new',
'http://arxiv.org/list/math.NT/new',
'http://arxiv.org/list/math.NA/new',
'http://arxiv.org/list/math.OA/new',
'http://arxiv.org/list/math.OC/new',
'http://arxiv.org/list/math.PR/new',
'http://arxiv.org/list/math.QA/new',
'http://arxiv.org/list/math.RT/new',
'http://arxiv.org/list/math.RA/new',
'http://arxiv.org/list/math.SP/new',
'http://arxiv.org/list/math.ST/new',
'http://arxiv.org/list/math.SG/new',]
    return reversed(urls)

class CS499Spider(Spider):
    hostname = 'http://arxiv.org'
    name = 'cs_update'
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
            try:
                item['urllink'] = prefix + sel.xpath('span/a[1]/@href').extract()[0]
                item['pdflink'] = prefix + sel.xpath('span/a[2]/@href').extract()[0]
                item['category'] = response.xpath('//*[@id="dlpage"]/h1/text()').extract()[0]
                seeMore = item['urllink']
                request = scrapy.Request(seeMore, callback=self.parseMovieDetails)
                request.meta['item'] = item
                i += 1
                yield request
            except:
                print 'urllink parse error'

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
        try:
            str1 = (response.xpath('//*[@id="abs"]/div[2]/div[3]/text()').extract()[0])
            def parse_string(str1):
                st = str1.replace('(Submitted on ', '')
                right = -1
                for i in range(len(st)):
                    if st[i:i + 3] == '201':
                          right = i
                          break
                return st[:right] + st[right + 2:right + 4]
            temp = datetime.datetime.strptime(parse_string(str1),'%d %b %y')
            item['date'] = str(temp.year) + '-' + str(temp.month) + '-' + str(temp.day)
        except:
            item['date'] = '2015-01-01'
            print(str1)
            print "time parsing error"
        return item