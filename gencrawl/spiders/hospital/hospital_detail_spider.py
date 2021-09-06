from gencrawl.spiders import BaseSpider
from gencrawl.util.statics import Statics
from gencrawl.items.hospital.hospital_detail_item import HospitalDetailItem
from gencrawl.util.utility import Utility


class HospitalDetailSpider(BaseSpider):
    crawl_domain = Statics.DOMAIN_HOSPITAL
    url_key = Statics.URL_KEY_HOSPITAL_DETAIL
    name = f'{crawl_domain}_{Statics.CRAWL_TYPE_DETAIL}'

    @classmethod
    def from_crawler(cls, crawler, config, *args, **kwargs):
        cls.crawl_type = Statics.CRAWL_TYPE_DETAIL
        return super().from_crawler(crawler, config, *args, **kwargs)

    def prepare_items(self, response, default_item=None):
        default_item = default_item or dict()
        parsed_items = []
        items = self.exec_codes(response, default_obj=default_item)
        for item in items:
            item.update(default_item)
            for key, value in item.items():
                if key in self.all_url_keys:
                    item[key] = response.urljoin(value)
            parsed_items.append(item)
        return parsed_items

    def get_items_or_req(self, response, default_item=None):
        default_item = default_item or dict()
        parsed_items = []
        for item in self.prepare_items(response, default_item):
            parsed_items.append(self.generate_item(item, HospitalDetailItem))
        return parsed_items

