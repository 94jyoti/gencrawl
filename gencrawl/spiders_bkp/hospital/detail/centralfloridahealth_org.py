from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
import re


class CentralFloridaHealthOrgUs(HospitalDetailSpider):

    name = 'hospital_detail_centralfloridahealth_org_us'

    def get_items_or_req(self, response, default_item=None):
        items = self.prepare_items(response, default_item)
        address_raw = list(set(re.findall(r'maps\.google\.com\/\?q\=(.*?)"',response.text)))
        phone_nos = list(set(response.xpath("//strong[contains(text(),'Phone')]/following-sibling::a[contains(@href,'tel')]/text()").extract()))
        fax_nos = list(set(response.xpath("//strong[contains(text(),'Fax')]/following::text()[1]").extract()))
        for i in range(len(address_raw)):
            new_item = deepcopy(items[0])
            try:
                new_item['address_raw'] = address_raw[i].replace('+',' ').replace('%2c','').strip()
            except:
                new_item['address_raw'] = ''
            try:
                new_item['phone'] = phone_nos[i]
            except:
                new_item['phone'] = ''
            try:
                new_item['fax'] = fax_nos[i]
            except:
                new_item['fax'] = ''
            yield self.generate_item(new_item, HospitalDetailItem)