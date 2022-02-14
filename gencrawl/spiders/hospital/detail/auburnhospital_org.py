from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics
import scrapy
import json
import copy
from scrapy.selector import Selector

class AuburnhospitalOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_auburnhospital_org_us'
    custom_settings={
    "HTTPCACHE_ENABLED":False
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta
        address_block = response.xpath("//h2[contains(text(),'Location')]/following-sibling::p[contains(.,'Address')]//text()").getall()
        if address_block is not None:
            text = ','.join(address_block).strip()
        else:
            text = ""
        no_of_pincodes = re.findall(r'[A-Z][A-Z] (\d{5})|[A-Z][a-z]+, ([A-Z][A-Z])$|(\d+)$|([A-Z][A-Z])$',text)
        count=0
        if len(no_of_pincodes)==0:
            yield self.generate_item(items[0], HospitalDetailItem)
            return
        else:
            for b in no_of_pincodes:
                for p in b:
                    if len(p)>0:
                        count = count +1

        no_of_pincodes = count
        final_items = []

        if no_of_pincodes==1:
            items[0]['address_raw'] = address_block
            yield self.generate_item(items[0], HospitalDetailItem)
        if no_of_pincodes>1:
            starts_with_digit = False
            for c,element in enumerate(address_block):
                starts_with_digit = re.match(r"^\d", element.strip()) is not None
                if starts_with_digit==True:
                    count = count+1
                    item_copy = copy.deepcopy(items[0])
                    item_copy['address_raw'] = [address_block[c]+","+address_block[c+1]]
                    final_items.append(item_copy)

            phone_nos = response.xpath("//strong[contains(text(),'Phone:')]/following-sibling::text()").getall()
            for c,item in enumerate(final_items):
                if len(phone_nos)==1:
                        final_items[c]['phone'] = phone_nos[c]
                if len(phone_nos)==2:
                    for phone in phone_nos:
                        final_items[c]['phone'] = phone_nos[c].split(':')[-1]
                yield self.generate_item(item, HospitalDetailItem)