from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics


class Bchealth_Org_us(HospitalDetailSpider):
    name = 'hospital_detail_bchealth_org_us'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        for item in items:
            temp_full_name=item['raw_full_name'].split(" ")
            for i in temp_full_name:
                if(i in item['designation']):
                    item['designation']=item['designation'].replace(i,"")
            item['designation']=item['designation'].replace(",","")
            designation_data = item['designation'].split(" ")
            print(designation_data)
            while '' in designation_data:
                designation_data.remove('')
            item['designation']=",".join(designation_data)

            yield self.generate_item(item, HospitalDetailItem)