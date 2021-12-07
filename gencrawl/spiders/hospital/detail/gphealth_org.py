from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics

class GpHealthOrg(HospitalDetailSpider):

    name = 'hospital_detail_gphealth_org_us'

    def get_items_or_req(self, response, default_item=None):
        items = self.prepare_items(response, default_item)
        meta = response.meta
        meta['items'] = items
        try:
            practice = items[0]['address_raw'].split('cui-accordion-item title="')[1].split('"')[0].strip()
        except:
            practice = ''
        if 'location' in practice.lower():
            practice = ''
        items[0]['practice_name'] = practice
        yield self.generate_item(items[0], HospitalDetailItem)
    