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

class GlensfallshospitalOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_glensfallshospital_org_us'
    custom_settings={
    "HTTPCACHE_ENABLED":True
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta

        for item in items:
            if item['address_raw']!=[]:
                text = re.split('(\d+)',item['address_raw'])
                if 'Glens Falls' in text[0]:
                    temp_text = re.split('(Glens Falls)',text[0])
                    item['practice_name']=temp_text[0].strip()
                    temp_text_2 = temp_text[1:]+ text[1:]
                    item['address_raw'] = ''.join(temp_text_2)
                else:
                    contains_digit = False
                    for character in text[0]:
                        if character.isdigit():
                            contains_digit = True
                    
                    if contains_digit ==False:
                        item['practice_name']=text[0]
                        item['address_raw']=''.join(text[1:])
                    if contains_digit ==True:
                        item['address_raw']=text
                        item['practice_name'] = []    
            yield self.generate_item(item, HospitalDetailItem)