# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Field, Item
class Paper(Item):
    urllink = Field()
    pdflink = Field()
    category= Field()
    authors= Field()
    title = Field()
    subjects = Field()
    abstract = Field()
    date = Field()
    # ref = Field()