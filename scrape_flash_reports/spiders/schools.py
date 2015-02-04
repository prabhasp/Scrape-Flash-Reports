import scrapy
from scrape_flash_reports.items import District, VDC, School

BASE_URL = 'http://202.70.77.75:8080/flash/schoolreport'
BASE_LIST_URL = BASE_URL + '/reportprebe.php'
BASE_SHOW_URL = BASE_URL + '/reportshow.php'
YEARS = range(2064, 2071)

def val(sel):
    return sel.extract()[0].strip()

class SchoolistSpider(scrapy.Spider):
    name = "schools"
    allowed_domains = ["202.70.77.75"]
    start_urls = [BASE_LIST_URL + "?req=distlist"]

    def parse(self, response):
        options = response.css('option')
        # The first option is -Select District-, so we ignore it
        # and only use [1:] of the options
        for o in options[1:]:
            district = District()
            district['name'] = o.xpath('text()').extract()
            district['code'] = o.xpath('@value').extract()
            vdc_list_url = BASE_LIST_URL + '?req=vdclist&distcode=' + district['code'][0]
            request = scrapy.Request(vdc_list_url, callback=self.parse_vdc)
            request.meta['district'] = dict(district)
            yield request

    def parse_vdc(self, response):
        options = response.css('option')
        # The first option is -Select VDC-, so we ignore it
        # and only use [1:] of the options
        for o in options[1:]:
            district = response.meta['district']
            vdc = VDC()
            vdc['name'] = o.xpath('text()').extract()
            vdc['code'] = o.xpath('@value').extract()
            vdc['district_code'] = district['code']
            vdc['district_name'] = district['name']
            for y in YEARS:
                school_list_url = BASE_LIST_URL + '?req=schoollist&distcode=' + district['code'][0] + \
                                  '&vdccode=' + vdc['code'][0] + '&y=2070'
            request = scrapy.Request(school_list_url, callback=self.parse_school_list)
            request.meta['vdc'] = dict(vdc)
            yield request

    def parse_school_list(self, response):
        options = response.css('option')
        # The first option is -All Schools-, so we ignore it
        # and only use [1:] of the options
        for o in options[1:]:
            vdc = response.meta['vdc']
            school = School()
            school_code = o.xpath('@value').extract()[0]
            school_name = o.xpath('text()').extract()[0].split(' - ')[1]
            for y in YEARS:
                school_page_url = BASE_SHOW_URL + '?d=' + vdc['district_code'][0] + \
                                              '&v=' + vdc['code'][0] + \
                                              '&s=' + school_code + \
                                              '&yr=' + str(y)
                yield scrapy.Request(school_page_url, callback=self.parse_school_page)
                
    def parse_school_page(self, response):
        with open("scrape_log.txt", "a") as f:
            try:
                ## If no data for a school, just write that out and be done
                if len(response.xpath('/html/body/table')) == 0:
                    f.write('No data for: ' + response.url + '\n')
                school = School()
                name_code = response.xpath('/html/body/table/tr/td/table[1]/tr/td[2]/h2/text()').extract()
                school['url'] = response.url
                school['name'] = name_code[0].split(': ')[1].strip() # School: School Name
                school['code'] = name_code[1].split(': ')[1].strip() # Code: 123456789
                school['development_region'] = val(response.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[2]/td[2]/text()'))
                school['eco_belt'] =  val(response.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[3]/td[2]/text()'))
                school['zone'] = val(response.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[5]/td[2]/text()'))
                school['district'] = val(response.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[5]/td[2]/text()'))
                school['vdc'] = val(response.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[6]/td[2]/text()'))
                school['address'] = val(response.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[7]/td[2]/text()'))
                school['ward_no'] = val(response.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[8]/td[2]/text()'))
                school['account_no'] = val(response.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[9]/td[2]/text()'))
                school['locality'] = val(response.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[10]/td[2]/text()'))
                school['phone'] = val(response.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[11]/td[2]/text()'))
                school['email'] = val(response.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[12]/td[2]/text()'))
                school['resource_center'] = val(response.xpath('/html/body/table/tr/td/table[2]/tr/td[1]/table/tr[13]/td[2]/text()'))
            except Exception as e:
                f.write('Error parsing url: '  + response.url + '\n')
                f.write('Exception: ' + str(e) + '\n')
        yield school
