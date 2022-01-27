from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics


class LabettehealthCom(HospitalDetailSpider):
    name = 'hospital_detail_labettehealth_com_us'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        for item in items:
            address_raw = item.get("address_raw")
            if address_raw:
                address_raw = address_raw.replace("LLC.", "LLC,")
                address_line_1 = re.search('class="accordion">\s*<h2>(.*?)</h2>', address_raw, re.S)
                if address_line_1:
                    address_line_1 = address_line_1.group(1)
                    if ',' not in address_line_1:
                        practice_name = re.search(r'(.*?)\d+', address_line_1)
                        if practice_name:
                            practice_name = practice_name.group(1)
                            address_raw = address_raw.replace(practice_name, practice_name+",")
                item['address_raw'] = address_raw
        return items

