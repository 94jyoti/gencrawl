from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics

class AspirusOrg(HospitalDetailSpider):

    name = 'hospital_detail_aspirus_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        meta = response.meta
        meta['items'] = items
        loc_urls_list = response.xpath("//div/a[contains(@href,'find-a-location')]/@href").extract()
        for item in loc_urls_list:
            location_url = 'https://www.aspirus.org/'+item
            yield self.make_request(location_url, callback=self.parse_locations, meta=meta, dont_filter=True)
    
    
    def parse_locations(self, response):
        items = response.meta['items']
        try:
            items[0]['address_line_1'] = response.xpath("//h3[span[contains(text(),'Find Us')]]/following-sibling::ul/li[1]/text()[1]").extract()[0]
        except:
            items[0]['address_line_1'] = ''

        try:
            items[0]['practice_name'] = items[0]['address_line_1']
        except:
            items[0]['practice_name'] = ''
        
        try:
            items[0]['address_line_2'] = ''.join(response.xpath("//h3[span[contains(text(),'Find Us')]]/following-sibling::ul/li[1]/p//text()").extract())
        except:
            items[0]['address_line_2'] = ''
        try:
            items[0]['address'] = items[0]['address_line_1'] + ' ' + items[0]['address_line_2']
        except:
            items[0]['address'] = ''
        try:
            items[0]['zip'] = items[0]['address_line_2'].split()[-1]
        except:
            items[0]['zip'] = ''
        try:
            items[0]['phone'] = response.xpath("//strong[contains(text(),'Main Phone')]/following-sibling::a[1]/text()").extract()[0]
        except:
            items[0]['phone'] = ''
        try:
            items[0]['fax'] = response.xpath("//strong[contains(text(),'Fax')]/following-sibling::a[1]/text()").extract()[0]
        except:
            items[0]['fax'] = ''
        
        yield self.generate_item(items[0], HospitalDetailItem)