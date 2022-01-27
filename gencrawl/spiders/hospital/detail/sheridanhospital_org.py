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
        raw_full_name = items[0]['raw_full_name']
        raw_full_name =  re.split(',',raw_full_name)[:2]
        if len(raw_full_name)==3:
            items[0]['first_name']=raw_full_name[1]
            items[0]['last_name'] = raw_full_name[0]
            items[0]['middle_name'] = raw_full_name[2]

        if len(raw_full_name)==2:
            temp = re.split(r' ',raw_full_name[1].strip())
            if len(temp)==2:
                items[0]['first_name']=temp[0]
                items[0]['middle_name'] = temp[1]
                items[0]['last_name'] = raw_full_name[0]
            else:
                items[0]['first_name']=raw_full_name[1]
                items[0]['last_name'] = raw_full_name[0]


        meta = response.meta
        for item in items:
            if item['address_raw']==[]:
                text_content=""

                yield self.generate_item(item, HospitalDetailItem)
            else:

                sel = scrapy.Selector(text=item['address_raw'])
                text_content = sel.xpath("//text()").getall()
                text_content = '\n'.join(text_content)
                phone_nos = re.findall('\d{3}\.\d{3}\.\d{4}',text_content)
                addresses = re.split('\d{3}\.\d{3}\.\d{4}',text_content)
               
                temp_address = [address.strip() for address in addresses if len(address)>4]

                for c,address in enumerate(temp_address):
                    item_copy = copy.deepcopy(item)
                    item_copy['address_raw'] = address.split('\n')[1:] # ['444','address','city','zip']
                    item_copy['phone'] = phone_nos[c]
                    item_copy['practice_name'] = address.split('\n')[0]
                    yield self.generate_item(item_copy, HospitalDetailItem)

            
