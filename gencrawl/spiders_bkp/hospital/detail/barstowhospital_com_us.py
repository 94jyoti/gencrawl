from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics


class BarstowHospital_Com_Us(HospitalDetailSpider):
    name = 'hospital_detail_barstowhospital_com_us'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        for item in items:
            item['address_raw']=item['address_raw'].replace("Attn:","")
            yield self.generate_item(item, HospitalDetailItem)