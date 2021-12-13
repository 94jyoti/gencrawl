from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics

class RussellCaresCom(HospitalDetailSpider):

    name = 'hospital_detail_russellcares_com_us'

    def get_items_or_req(self, response, default_item=None):
        items = self.prepare_items(response, default_item)
        meta = response.meta
        meta['items'] = items
        try:
            add_block = items[0]['address_raw']
            if 'Address:' in add_block:
                final_add = add_block.split('Address:')[1].replace('</p>','').replace('</strong>','').strip()
            else:
                final_add = ''
        except:
            final_add = ''
        items[0]['address'] = final_add
        yield self.generate_item(items[0], HospitalDetailItem)
    