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

class MhsystemOrgHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_mhsystem_org_us'
    custom_settings={
    "HTTPCACHE_ENABLED":True
    }

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        meta = response.meta
        npi = response.url
        for item in items:
            item['npi'] = npi.split("NPI=")[-1].strip()
            yield self.generate_item(item, HospitalDetailItem)