import scrapy
from flash_scrape.items import District, VDC

BASE_URL = 'http://202.70.77.75:8080/flash/schoolreport/reportprebe.php?'
class DistrictListSpider(scrapy.Spider):
    name = "DistrictLister"
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
            yield district
