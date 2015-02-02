# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class District(scrapy.Item):
    name = scrapy.Field()
    code = scrapy.Field()

class VDC(scrapy.Item):
    name = scrapy.Field()
    code = scrapy.Field()
    district_code = scrapy.Field()
    district_name = scrapy.Field()

class School(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    school_type = scrapy.Field()
    school_levels = scrapy.Field()
    district = scrapy.Field()
    vdc = scrapy.Field()
    address = scrapy.Field()
    eco_belt = scrapy.Field()
    ward_no = scrapy.Field()
    account_no = scrapy.Field()
    locality = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    resource_center = scrapy.Field()
