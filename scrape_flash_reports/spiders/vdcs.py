import scrapy
from scrape_flash_reports.items import District, VDC

BASE_URL = 'http://202.70.77.75:8080/flash/schoolreport/reportprebe.php?'
class DistrictListSpider(scrapy.Spider):
    name = "vdcs"
    allowed_domains = ["http://202.70.77.75:8080/", "202.70.77.75"]
    start_urls = [BASE_URL + "req=distlist"]

    def parse(self, response):
        options = response.css('option')
        # The first option is -Select District-, so we ignore it
        # and only use [1:] of the options
        for o in options[1:]:
            district = District()
            district['name'] = o.xpath('text()').extract()
            district['code'] = o.xpath('@value').extract()
            vdc_list_url = BASE_URL + 'req=vdclist&distcode=' + district['code'][0]
            request = scrapy.Request(vdc_list_url, callback=self.parse_vdc)
            request.meta['district'] = dict(district)
            yield request

    def parse_vdc(self, response):
        options = response.css('option')
        # The first option is -Select District-, so we ignore it
        # and only use [1:] of the options
        for o in options[1:]:
            district = response.meta['district']
            vdc = VDC()
            vdc['name'] = o.xpath('text()').extract()
            vdc['code'] = o.xpath('@value').extract()
            vdc['district_code'] = district['code']
            vdc['district_name'] = district['name']
            yield vdc
