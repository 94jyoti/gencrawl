from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy
from datetime import datetime
import re
from gencrawl.util.statics import Statics

class BeebehealthcareorghospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_beebehealthcare_org_us'

    def get_items_or_req(self, response, default_item={}):

        items = self.prepare_items(response, default_item)
        for item in items:
            try:
                remove_from_address=re.findall('<span class="m-0 address">[\w].* Department.*?</span>',item['address_raw'].replace("\n",""))[0]
                item['address_raw']=item['address_raw'].replace("\n","").replace(remove_from_address,"")
            except:
                pass

            yield self.generate_item(item, HospitalDetailItem)