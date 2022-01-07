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

class BellevuehospitalComHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_bellevuehospital_com_us'
    custom_settings={
    "HTTPCACHE_ENABLED":True
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta
        for item in items:

            if item['address_raw']!=[]:
                contains_digit = False
                for character in item['address_raw'][1]:
                    if character.isdigit():
                        contains_digit = True
                if contains_digit ==False:
                    item['practice_name']=item['address_raw'][1]
                    item['address_raw']=item['address_raw'][2:]
                if contains_digit ==True:
                    item['address_raw']=item['address_raw'][1:]
                    item['practice_name'] = []
                
            yield self.generate_item(item, HospitalDetailItem)