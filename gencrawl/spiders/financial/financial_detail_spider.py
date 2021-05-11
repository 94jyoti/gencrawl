from gencrawl.spiders import BaseSpider
from gencrawl.util.statics import Statics
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from gencrawl.util.utility import Utility


class FinancialDetailSpider(BaseSpider):
    crawl_domain = Statics.DOMAIN_FINANCIAL
    name = f'{crawl_domain}_{Statics.CRAWL_TYPE_DETAIL}'

    @classmethod
    def from_crawler(cls, crawler, config, *args, **kwargs):
        cls.crawl_type = Statics.CRAWL_TYPE_DETAIL
        return super().from_crawler(crawler, config, *args, **kwargs)

    def prepare_items(self, response, default_item={}):
        parsed_items = []
        items = self.exec_codes(response)
        for item in items:
            item.update(default_item)
            parsed_items.append(item)
        return parsed_items

    def get_items_or_req(self, response, default_item={}):
        parsed_items = []
        for item in self.prepare_items(response, default_item):
            parsed_items.append(self.generate_item(item, FinancialDetailItem))
        return parsed_items

