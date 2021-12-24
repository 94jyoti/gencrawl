from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics
import scrapy
import json
import copy

class SheridanhospitalOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_sheridanhospital_org_us'
    custom_settings={
    "HTTPCACHE_ENABLED":False
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta
        for item in items:
            print("xx:",item['address_raw'])
            if item['address_raw']==[]:
                text_content=""
                yield self.generate_item(item, HospitalDetailItem)
            else:

                sel = scrapy.Selector(text=item['address_raw'])
                text_content = sel.xpath("//text()").getall()
                text_content = '\n'.join(text_content)
            
                print("dd:",text_content)
                
                phone_nos = re.findall('\d{3}\.\d{3}\.\d{4}',text_content)
                print("phone_nos:",phone_nos)
                addresses = re.split('\d{3}\.\d{3}\.\d{4}',text_content)
               
                temp_address = [address.strip() for address in addresses if len(address)>4]
                print("temp_address:",temp_address)

                for c,address in enumerate(temp_address):
                    print("fff:",address.split('\n')[1:])
                    print("hhh:",address.split('\n')[0])
                    
                    item_copy = copy.deepcopy(item)
                    item_copy['address_raw'] = '\n'.join(address.split('\n')[1:]) # ['444','address','city','zip']
                    item_copy['phone'] = phone_nos[c]
                    item_copy['practice_name'] = address.split('\n')[0]
                    yield self.generate_item(item_copy, HospitalDetailItem)

            
