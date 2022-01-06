from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics
import scrapy
import json
import copy

class DoctorsAdventisthealthOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_doctors_adventisthealth_org_us'
    custom_settings={
    "HTTPCACHE_ENABLED":True
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta

        addresses = response.xpath("//div[@id='provider-details-locations']//div[@itemprop='address']/div[2]")
        
        if len(addresses)>1:
            item_copy = copy.deepcopy(items[0])
            items.append(item_copy)

        for item in items:
            
            yield self.generate_item(item, HospitalDetailItem)

        
            

            

