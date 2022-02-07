from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from datetime import datetime
from gencrawl.util.statics import Statics
import scrapy
import json
#import xmltodict
import copy
from bs4 import BeautifulSoup
import re
import logging


class AccesstocareVaGovHospitalDetail(HospitalDetailSpider):
    name = 'hospital_detail_accesstocare_va_gov_us'
    logging.basicConfig(filename="accesstocare.log", level=logging.INFO)

    def parse(self,response):
        items = self.prepare_items(response, default_item=self.get_default_item(response))
        
        meta = response.meta

        search_url = items[0]['search_url']
        print("search_url:",search_url)
        p=re.findall(r'p=(\d+)',search_url)[0]
        s=re.findall(r's=(\d+)',search_url)[0]

        meta['specialty_code'] = s

        print("dd:",p,s)

        static_url = "https://www.accesstocare.va.gov/api/SearchResults?e="+str(0)+"&p="+str(p)+"&s="+str(s)+"&"

        yield scrapy.Request(static_url, callback=self.parse_information, dont_filter=True,meta=meta)

    def parse_information(self,response):
        #print("xx:",response.text)
        meta = response.meta
        specialty_code = meta['specialty_code']
        items = self.prepare_items(response, default_item=self.get_default_item(response))
        loaded_json = json.loads(response.text)
        records_count = int(loaded_json['c'])

        print("records_count:",records_count)

        static_url = "https://www.accesstocare.va.gov/api/SearchResults?p="+str(records_count)+"&s="+str(specialty_code)+"&"
        yield scrapy.Request(static_url, callback=self.parse_information2, dont_filter=True,meta=meta)

    def parse_information2(self,response):
        items = self.prepare_items(response, default_item=self.get_default_item(response))
        #print(response.text)
        meta = response.meta

        loaded_json = json.loads(response.text)
        #print(loaded_json['r'])
        for data in loaded_json['r']:
            #print("ddd:",data)
            item_copy = copy.deepcopy(items[0])
            item_copy['first_name'] = data['f']
            item_copy['last_name'] = data['l']
            item_copy['practice_name'] = data['v']
            item_copy['address_line_1'] = data['a']
            item_copy['city'] = data['y']
            item_copy['state'] = data['t']
            item_copy['zip'] = data['z']
            item_copy['speciality'] = data['o']
            item_copy['raw_full_name'] = data['f'] + " " +data['l']
            #item_copy['doctor_url'] = count

            
            yield self.generate_item(item_copy, HospitalDetailItem)


        



       


                             