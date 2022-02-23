from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics
import scrapy
import json

class ClevelandClinicOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_clevelandclinic_org_us'
    custom_settings={
    "HTTPCACHE_ENABLED":False
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta
        #meta['items'] = items

        print("ddd:",response.url)

        raw_full_name = response.xpath("//h1/text()").get()
        address_raw = response.xpath("//div[@class='bio--locations-specialties__wrapper clearfix']//div[@class='l-1col ']/div/text()").get()

        for item in items:
    
            #print("xxx:",item)
            item['raw_full_name'] = raw_full_name
            #item['address_raw'] = address_raw

            yield self.generate_item(item, HospitalDetailItem)
