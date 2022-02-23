from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics


class Midhusonregional_org_us(HospitalDetailSpider):
    name = 'hospital_detail_midhudsonregional_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        for item in items:
            if(item['raw_full_name'].replace(",","") in item['designation']):
                item['designation']=item['designation'].replace(item['raw_full_name'],"")
        yield self.generate_item(items[0], HospitalDetailItem)