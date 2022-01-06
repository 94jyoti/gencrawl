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


class WmhwebComHospitalDetail(HospitalDetailSpider):
    name = 'hospital_detail_wmhweb_com_us'

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta
        
        for item in items:
            print(item['address_raw'][0])
            #print(item)
            if item['address_raw'] == []:
                item['address_raw']=(response.xpath("//h1/following::p[position()>=1][not(contains(.,'Medical School') or contains(.,'Residency')) ]").extract()[0]).replace(item['speciality'],"")
                print(item['address_raw'])
            #print(item['address_raw'][1])
            if(item['address_raw'].replace("<p>","").startswith('Phone')):
                del item
                continue
            #print("jebflejwbwbevjwjb",re.findall('<p>(.*?)</p>', item['address_raw']))
            if("\xa0" in re.findall('<p>(.*?)</p>',item['address_raw'])):
                del item
                continue

            item['address_raw'] = item['address_raw'].replace("Phone", "").replace(":", "")



            #if item['address_raw'] == []:


            yield self.generate_item(item, HospitalDetailItem)