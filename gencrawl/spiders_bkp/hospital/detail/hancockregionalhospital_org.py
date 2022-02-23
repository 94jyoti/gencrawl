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

class HancockregionalhospitalOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_hancockregionalhospital_org_us'
    custom_settings={
    "HTTPCACHE_ENABLED":True
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta
        raw_full_name = items[0]['raw_full_name'].split(',')[0].strip()
        primary_address = response.xpath("//div[@class='doctor-location-address']//p")
        if len(primary_address)==0 or len(primary_address)>2:
            if len(primary_address)==0:
                primary_address = response.xpath("//div[@class='doctor-location']//text()").getall()
                item_copy = copy.deepcopy(items[0])
                item_copy['address_raw'] = primary_address
                yield self.generate_item(item_copy, HospitalDetailItem)
            else:
                for p_address in primary_address:
                    temp_address = [p.strip() for p in p_address.xpath(".//text()").getall()]
                    if len(temp_address)>1:
                        item_copy = copy.deepcopy(items[0])
                        item_copy['address_raw'] = temp_address
                        yield self.generate_item(item_copy, HospitalDetailItem)

        if len(primary_address)==2:
            isaddress = []
            address_list = []
            for address_block in response.xpath("//div[@class='doctor-location-address']//p"):
                address_text = address_block.xpath(".//text()").getall()
                address_list.append(re.split(r',|\n',''.join(address_text)))
                temp = re.findall(r'([A-Z][A-Z]\s{1,2}\d{5})',''.join(address_text))
                if len(temp)>0:
                    isaddress.append(True)
                else:
                    isaddress.append(False)

            if False in isaddress:
                item_copy = copy.deepcopy(items[0])
                item_copy['address_raw'] = address_list[0]+address_list[1]
                yield self.generate_item(item_copy, HospitalDetailItem)

            else: 
                for c,l in enumerate(address_list):
                    item_copy = copy.deepcopy(items[0])
                    item_copy['address_raw'] = address_list[c]
                    yield self.generate_item(item_copy, HospitalDetailItem)

        additional_locations = response.xpath("//div[contains(text(),'Additional Locations')]/following-sibling::div/div")
        if len(additional_locations)>0:
            for address in additional_locations:
                item_copy = copy.deepcopy(items[0])
                item_copy['address_raw'] = address.xpath(".//text()").getall()
                yield self.generate_item(item_copy, HospitalDetailItem)