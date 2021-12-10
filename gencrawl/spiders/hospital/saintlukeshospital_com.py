from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics
import scrapy
import json
import copy

class SaintlukeshospitalComHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_saintlukeshospital_com_us'
    custom_settings={
    "HTTPCACHE_ENABLED":False
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta
        for item in items:
            address_raw = ''.join(item['address_raw'])
            temp_address = re.findall('[A-Z].*[A-Z][A-Z] \d{5}',address_raw,re.DOTALL)
            temp_address = ''.join(temp_address)
            temp_address = re.split('\d{3}-\d{3}-\d{4}',temp_address)
            for i in temp_address:
                if len(i)>10:
                    item_copy = copy.deepcopy(item)
                    item_copy['address_raw'] = i.split('\n')
                    yield self.generate_item(item_copy, HospitalDetailItem)
