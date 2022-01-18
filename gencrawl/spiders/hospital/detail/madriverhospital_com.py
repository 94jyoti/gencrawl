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

class MadriverhospitalComHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_madriverhospital_com_us'
    custom_settings={
    "HTTPCACHE_ENABLED":False
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta

        block = response.xpath("//h1[@id='page-title']/parent::header/following-sibling::div//div[@class='field-item even']/p[1] | //h1[@id='page-title']/parent::header/following-sibling::div//div[@class='field-item even']/p[2]")
        
        print("gggg:",block)

        status=False

        for b in block:
            data = [a.replace('\n\xa0','').replace('\n','') for a  in b.xpath(".//text()").getall() if len(a.replace('\n\xa0','').replace('\n',''))>0]
            print("bbbb:",data,len(data))

            starts_with_digit=False
            print("URL:",items[0]['doctor_url'])

            if "madriverhospital.com/william-carlson-md-faafp#overlay-context=randall-bass-md-ms" in items[0]['doctor_url']:
                starts_with_digit=True
            else:

                if len(data)>1:
                    starts_with_digit = re.match(r"^\d", data[1].strip()) is not None
                print(starts_with_digit)

            

            if starts_with_digit==True:
                status=True
                item_copy = copy.deepcopy(items[0])
                count=0
                starts_with_digit = False
                for c,d in enumerate(data):
                    #print(data.strip())
                    starts_with_digit = re.match(r"^\d", d.strip()) is not None
                    print(d,',',c,',',starts_with_digit)
                    if starts_with_digit==True:
                        count = count+1
                print("starts_with_digit:",starts_with_digit)  
                print("count1:",count)

                if count==0:
                    if "madriverhospital.com/william-carlson-md-faafp#overlay-context=randall-bass-md-ms" in items[0]['doctor_url']:
                        item_copy['address_raw'] = data[3:]
                        item_copy['practice_name'] = ''.join(data[:3])
                    else:
                        item_copy['address_raw'] = []
                    yield self.generate_item(item_copy, HospitalDetailItem)
                if count==1:
                    item_copy['address_raw'] = data
                    yield self.generate_item(item_copy, HospitalDetailItem)
                if count>1:
                    print("here")
                    print(data)
                    for c,d in enumerate(data):
                        #print(c,d)
                        starts_with_digit = re.match(r"^\d", d.strip()) is not None
                        print(d,',',c,',',starts_with_digit)
                        if starts_with_digit==True:
                            item_copy = copy.deepcopy(items[0])
                            print("sss:",data[c])
                            item_copy['address_raw'] = [data[c]]
                            item_copy['practice_name'] = [data[c-1]]
                            yield self.generate_item(item_copy, HospitalDetailItem)
            
        if status==False:
            yield self.generate_item(items[0], HospitalDetailItem)




        

