from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics


class Meridianhs_Org_us(HospitalDetailSpider):
    name = 'hospital_detail_meridianhs_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        for item in items:
            if("iframe" in item['address_raw']):
                continue
            else:
                yield self.generate_item(item, HospitalDetailItem)