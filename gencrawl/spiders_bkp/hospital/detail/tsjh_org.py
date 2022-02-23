from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from copy import deepcopy


class TsjhOrg(HospitalDetailSpider):
    name = "hospital_detail_tsjh_org_us"

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        items = deepcopy(items[0])

        if items["address_raw"]:
            address_raw = items.get('address_raw')
            address_raw = address_raw.replace('.', '')
            items['address_raw'] = address_raw

        yield self.generate_item(items, HospitalDetailItem)
