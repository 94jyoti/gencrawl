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

    def map_fields(self, index, total_len, item, fields_to_map, response=None):
        for field in fields_to_map:
            val_list = item.get(field)
            if val_list:
                item[field] = val_list[index] if len(val_list) == total_len else None
        return item

    def prepare_mapped_items(self, response, items):
        ext_codes = {k: v for k, v in self.ext_codes.items() if v.get("return_type") == Statics.RETURN_TYPE_LIST_MAP}
        if ext_codes:
            # the fields that has return-type as `list-map`
            fields_to_map = ext_codes.keys()
            parsed_mapped_items = []
            for index, item in enumerate(items):
                parsed_mapped_items.append(self.map_fields(index, len(items), item, fields_to_map, response=response))
            return parsed_mapped_items
        else:
            return items

    def get_items_or_req(self, response, default_item=None):
        default_item = default_item or dict()
        parsed_items = []
        for item in self.prepare_items(response, default_item):
            parsed_items.append(self.generate_item(item, HospitalDetailItem))
        return self.prepare_mapped_items(response, parsed_items)

