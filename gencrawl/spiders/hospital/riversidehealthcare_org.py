from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics
import scrapy
import json
import copy

class RiversidehealthcareOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_riversidehealthcare_org_us'
    custom_settings={
    "HTTPCACHE_ENABLED":False
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta
        addresses_block = response.xpath("//*[@class='IH_DynamicPageZones hidden-xs ng-isolate-scope']//div[@class='form-group ih-field-locationaddress']")
        if len(addresses_block)==1:
            for address in addresses_block:
                practice_name = address.xpath("./parent::div/parent::div/div[1]/div/div/text()").get()
                items[0]['practice_name'] = practice_name
            yield self.generate_item(items[0], HospitalDetailItem)

        if len(addresses_block)>1:
            for c,address in enumerate(addresses_block):
                practice_name = address.xpath("./parent::div/parent::div/div[1]/div/div/text()").get()
                item_copy = copy.deepcopy(items[0])
                item_copy['address_raw'] = address.getall()[0]
                item_copy['practice_name'] = practice_name
                if c>0:
                    item_copy['phone']=''
                    item_copy['fax']=''

                yield self.generate_item(item_copy, HospitalDetailItem)
