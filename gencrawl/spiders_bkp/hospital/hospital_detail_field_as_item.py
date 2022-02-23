from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from gencrawl.util.statics import Statics
from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.util.utility import Utility
from copy import deepcopy


class HospitalDetailPhoneAsAddressSpider(HospitalDetailSpider):
    crawl_domain = Statics.DOMAIN_HOSPITAL
    url_key = Statics.URL_KEY_HOSPITAL_DETAIL
    name = f'{crawl_domain}_{Statics.CRAWL_TYPE_DETAIL}_field_as_item'
    address_fields = ['practice_name', 'address_raw', 'address', 'address_line_1', 'address_line_2', 'address_line_3',
                      'city', 'state', 'zip', 'phone', 'fax']

    # will create a new item for each phones found in phone_as_address
    def get_field_as_item(self, items):
        item = items[0]
        field_map = {"phone_as_item": "phone", "practice_as_item": "practice_name", "fax_as_item": "fax"}
        addresses_raw = []
        for item in items:
            addr_raw = item.get("address_raw")
            if addr_raw:
                if isinstance(addr_raw, list):
                    addr_raw = ' '.join(addr_raw)
                addresses_raw.append(addr_raw)
        addresses_raw = '___'.join(addresses_raw)

        for field in field_map:
            field_values = item.get(field)
            if field_values:
                if isinstance(field_values, str):
                    field_values = [field_values]
                for val in field_values:
                    if val and val.strip() in addresses_raw:
                        continue
                    item_replica = deepcopy(item)
                    for key in self.address_fields:
                        item_replica[key] = None
                    item_replica[field_map[field]] = val
                    items.append(item_replica)
        return items

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        items = self.get_field_as_item(items)
        return items

