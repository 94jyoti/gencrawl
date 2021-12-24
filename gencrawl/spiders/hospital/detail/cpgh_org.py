from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics

class CpghOrg(HospitalDetailSpider):

    name = 'hospital_detail_cpgh_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        meta = response.meta
        meta['items'] = items
        try:
            items[0]['speciality'] = items[0]['speciality'].replace(';',' ').replace(',',' ').strip()
            cleaned_add_raw =  re.sub(r'<.*?>',' ',items[0]['address_raw']).strip()
            practice_name = re.findall(r'(^[a-zA-Z]+.*?)\d+',cleaned_add_raw)
            if practice_name:
                final_practice_name = practice_name[0].\
                                    replace('POBox','').replace('PO Box','').strip()
            else:
                final_practice_name = ''
            items[0]['practice_name'] = final_practice_name
        except:
            items[0]['practice_name'] = ''
        yield self.generate_item(items[0], HospitalDetailItem)

    
    
    