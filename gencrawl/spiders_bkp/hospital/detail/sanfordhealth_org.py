from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics
import scrapy
import json
import copy

class SanfordhealthOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_sanfordhealth_org_us'
    custom_settings={
    "HTTPCACHE_ENABLED":True
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta
        primary_address = response.xpath("(//h3[contains(text(),'Primary Location')]/../parent::div)[1]")
        item_copy = copy.deepcopy(items[0])
        item_copy['address_raw'] = primary_address.get()
        item_copy['phone'] = ''.join(response.xpath("(//a[@class='btn btn-small-font'])[1]/text()").getall())
        items.append(item_copy)
        
        for item in items:
            print("sss:",item['address_raw'])
            if item['address_raw']!=[]:

                yield self.generate_item(item, HospitalDetailItem)

