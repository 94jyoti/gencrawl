from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics
import scrapy
import json
import copy

class ButlerhealthsystemOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_butlerhealthsystem_org_us'
    custom_settings={
    "HTTPCACHE_ENABLED":True
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta

        phone_fax = response.xpath("//strong[@class='phone-link']/text()").getall()
        for item in items:

            if len(phone_fax)==1:
                item['phone'] = phone_fax[0]
            if len(phone_fax)>1:
                item['fax'] = phone_fax[1]
            yield self.generate_item(item, HospitalDetailItem)

        