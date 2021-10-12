from gencrawl.spiders.hospital.hospital_detail_spider import HospitalDetailSpider
from gencrawl.util.statics import Statics
from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.util.utility import Utility


class HospitalDetailPhoneCustomSpider(HospitalDetailSpider):
    crawl_domain = Statics.DOMAIN_HOSPITAL
    url_key = Statics.URL_KEY_HOSPITAL_DETAIL
    name = f'{crawl_domain}_{Statics.CRAWL_TYPE_DETAIL}_phones_as_address'

    def get_items_or_req(self, response, default_item=None):
        items = super(HospitalDetailPhoneCustomSpider, self).get_items_or_req(response, default_item)
        return items

