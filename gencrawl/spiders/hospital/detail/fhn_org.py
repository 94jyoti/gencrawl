from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics

class FhnOrg(HospitalDetailSpider):

    name = 'hospital_detail_fhn_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        location_url = 'https://fhn.org/'+response.xpath("//b[contains(text(),'Location')]/following-sibling::a[1]/@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        yield self.make_request(location_url, callback=self.parse_locations, meta=meta, dont_filter=True)
    

    def parse_locations(self, response):
        items = response.meta['items']
        try:
            items[0]['address_line_1'] = response.xpath("//h2[contains(text(),'Contact Us')]/following::text()[1]").extract()[0]
        except:
            items[0]['address_line_1'] = ''
        try:
            items[0]['address_line_2'] = response.xpath("//h2[contains(text(),'Contact Us')]/following::text()[2]").extract()[0]
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

        if not items[0]['phone']:
            try:
                items[0]['phone'] = response.xpath("//div[h2[contains(text(),'Contact Us')]]//a[contains(@href,'tel')]/text()").extract()[0]
            except:
                items[0]['phone'] = ''
        if not items[0]['fax']:
            try:
                items[0]['fax'] = response.xpath("//div[h2[contains(text(),'Contact Us')]]//strong[contains(text(),'Fax')]/following::text()[1]").extract()[0]
            except:
                items[0]['fax'] = ''
        yield self.generate_item(items[0], HospitalDetailItem)