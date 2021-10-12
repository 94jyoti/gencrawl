from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from gencrawl.util.statics import Statics
from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.util.utility import Utility
from copy import deepcopy


class HospitalDetailPhoneAsAddressSpider(HospitalDetailSpider):
    crawl_domain = Statics.DOMAIN_HOSPITAL
    url_key = Statics.URL_KEY_HOSPITAL_DETAIL
    name = f'{crawl_domain}_{Statics.CRAWL_TYPE_DETAIL}_phone_as_item'
    address_fields = ['address_raw', 'address', 'address_line_1', 'address_line_2', 'address_line_3',
                      'city', 'state', 'zip', 'phone', 'fax']

    # will create a new item for each phones found in phone_as_address
    def get_phones_as_items(self, items):
        item = items[0]
        phone_as_address = item.get("phone_as_item")
        if phone_as_address:
            if isinstance(phone_as_address, str):
                phone_as_address = [phone_as_address]
                for phone in phone_as_address:
                    item_replica = deepcopy(item)
                    for key in self.address_fields:
                        item_replica[key] = None
                    item_replica['phone'] = phone
                    items.append(item_replica)
        return items

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        items = self.get_phones_as_items(items)
        return items

