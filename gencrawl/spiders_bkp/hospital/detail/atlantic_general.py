from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
import re
from copy import deepcopy


class AtlanticGeneralComHospitalDetail(HospitalDetailSpider):

    name = 'hospital_detail_atlanticgeneral_org_us'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        for item in items:
                item['address_raw']=item['address_raw'].replace("  "," ")
                yield self.generate_item(item, HospitalDetailItem)