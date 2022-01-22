from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics


class CedarParkRegional_org_us(HospitalDetailSpider):
    name = 'hospital_detail_cedarparkregional_com_us'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        for item in items:
            item['address_raw']=re.sub("ext. ([\\d]{5})",'',item['address_raw'])
        yield self.generate_item(items[0], HospitalDetailItem)