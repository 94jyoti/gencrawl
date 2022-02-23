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

class SfmcNetHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_sfmc_net_us'
    custom_settings={
    "HTTPCACHE_ENABLED":False
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta
        text = Selector(text=items[0]['address_raw'])
        text = ' '.join(text.xpath(".//text()").getall())
        text = text.replace('Medical Center Map','')
        if len(items[0]['practice_name'])>0:
            text = text.replace(items[0]['practice_name'][0],'')
        text = text.split('Get Directions')

        text = [s for s in text if len(s)>2]
        if len(text)>1:
            item_copy = copy.deepcopy(items[0])
            items.append(item_copy)
        
        for c,address in enumerate(text):
            temp_address = re.split('(\d+)',address)
            temp_address = [t for t in temp_address if len(t)>1]
            contains_digit = False
            for character in temp_address[0]:
                if character.isdigit():
                    contains_digit = True
            if contains_digit==False:
                items[c]['practice_name'] = temp_address[0]
                address = address.replace(temp_address[0],'')

            phone = address.split(" ")
            items[c]['address_raw'] = address
            items[c]['phone'] = phone[-2]


        for item in items:           
            yield self.generate_item(item, HospitalDetailItem)