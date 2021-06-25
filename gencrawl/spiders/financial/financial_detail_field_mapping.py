from gencrawl.spiders import BaseSpider
from gencrawl.util.statics import Statics
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from gencrawl.util.utility import Utility
from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from copy import deepcopy


class FinancialDetailFieldMapSpider(FinancialDetailSpider):
    crawl_domain = Statics.DOMAIN_FINANCIAL
    url_key = Statics.URL_KEY_FINANCIAL_DETAIL
    name = f'{crawl_domain}_{Statics.CRAWL_TYPE_DETAIL}_field_mapping'

    def map_fields(self, index, total_len, item, fields_to_map):
        for field in fields_to_map:
            val_list = item.get(field)
            if val_list:
                item[field] = val_list[index] if len(val_list) == total_len else None
        return item

    def prepare_mapped_items(self, response, items):
        parsed_mapped_items = []
        ext_codes = {k: v for k, v in self.ext_codes.items() if v.get("return_type") == Statics.RETURN_TYPE_LIST_MAP}
        # the fields that has return-type as `list-map`
        fields_to_map = ext_codes.keys()
        for index, item in enumerate(items):
            parsed_mapped_items.append(self.map_fields(index, len(items), item, fields_to_map))
        return parsed_mapped_items

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        parsed_items = self.prepare_mapped_items(response, items)
        return parsed_items

