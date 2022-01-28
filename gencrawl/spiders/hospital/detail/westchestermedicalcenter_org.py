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

class WestchestermedicalcenterOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_westchestermedicalcenter_org_us'
    custom_settings={
    "HTTPCACHE_ENABLED":True
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        
        practice_names_list = []
        practice_names = response.xpath("//h2[contains(text(),'Locations')]//following::p[@class='location-info']/preceding-sibling::p[@class='location-name']")

        for practice_name in practice_names:
            temp = ''.join(practice_name.xpath(".//text()").getall()).split(",")
            practice_names_list.append(temp)
        temp_name1 = ','.join(items[0]['raw_full_name'])
        temp_name = re.findall(r"(.*) Surgical Oncologist|(.*) MD|(.*) Provider|(.*) Attending|(.*),Assistant",temp_name1 ,flags=re.IGNORECASE)
        temp_name = [t for t in temp_name[0] if len(t)>0]
        first_name = temp_name[0].split(",")[1].strip().replace(",","")
        first_name = re.sub(r'\([a-zA-Z]+\)','',first_name)
        last_name = temp_name[0].split(",")[0].strip().replace(",","")
        middle_name = " "
        temp_name2 = temp_name1.replace(first_name," ").replace(last_name," ").replace(middle_name," ").strip()
        designation = re.split(r',',temp_name2)
        final_designation = []
        for d in designation:
            if len(d)>0 and 'Avi' not in d:
                final_designation.append(d.strip())
        
        temp = first_name.split()
        if len(temp)==2:
            first_name = temp[0]
            middle_name = temp[1]
        
        for c,item in enumerate(items):
            body = item['address_raw']
            temp_address = Selector(text=body).xpath('.//text()').getall()
            try:
                final_address = practice_names_list[c]+temp_address
            except:
                 final_address = temp_address
            items[c]['address_raw'] = final_address
            item['first_name']= first_name
            item['last_name'] = last_name
            item['middle_name'] = middle_name
            item['raw_full_name'] = first_name + " " + item['middle_name'] + " " + last_name +" "+', '.join(final_designation)
            item['designation'] = final_designation
            yield self.generate_item(item, HospitalDetailItem)
            
