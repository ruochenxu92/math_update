# -*- coding: utf-8 -*-

# Scrapy settings for superqq_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'superqq_spider'

SPIDER_MODULES = ['superqq_spider.spiders']
NEWSPIDER_MODULE = 'superqq_spider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'superqq_spider (+http://www.yourdomain.com)'
ITEM_PIPELINES = {
    'superqq_spider.pipelines.JsonWriterPipeline': 2,
}

from random import randint
DOWNLOAD_DELAY = randint(1, 120)

#禁Cookie防ban
COOKIES_ENABLED =False
#使用变化的UserAgent防ban
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'superqq_spider.useragent.UserAgentPoolMiddleware': 400
}
CONCURRENCY_REQUESTS = 10
