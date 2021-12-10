from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics

class LittleTonHealthCareOrg(HospitalDetailSpider):

    name = 'hospital_detail_littletonhealthcare_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        meta = response.meta
        meta['items'] = items
        add_raw = items[0]['address_raw'].replace('\r',' ').replace('\n',' ').replace('\t',' ').replace('<br>',' ').replace('<p>',' ').strip()
        total_add_blocks = re.findall(r'(.*?\(\d+\)\s*\d+\-\d+)',add_raw)
        if not total_add_blocks:
            total_add_blocks = re.findall(r'(.*?\d+\.\d+\.\d+)',add_raw)
        if len(total_add_blocks) > 1 and total_add_blocks[1].strip().startswith('Fax:'):
            total_add_blocks.pop(1)
        for item in total_add_blocks:
            item = item.replace('Currently seeing patients in:','').strip()
            items[0]['address'] = item
            items[0]['address_raw'] = add_raw
            
            try:
                items[0]['phone'] = re.findall(r'(\(\d+\)\s*\d+\-\d+)',item)[0]
            except:
                items[0]['phone'] = re.findall(r'(\d+\.\d+\.\d+)',item)[0]
            try:
                items[0]['practice_name'] = re.findall(r'(.*?)\d+\s',item)[0].strip()
            except:
                items[0]['practice_name'] = ''
            try:
                items[0]['address_line_1'] = re.findall(r'(\s\d+\s.*?)\w+\,',item)[0]
                if len(items[0]['address_line_1'].split()) == 1:
                    items[0]['address_line_1'] = re.findall(r'(\d+\s.*?)\w+\,',item)[0]
            except:
                items[0]['address_line_1'] = ''
            yield self.generate_item(items[0], HospitalDetailItem)
    
    
    