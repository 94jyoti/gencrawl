from gencrawl.spiders import BaseSpider
from gencrawl.util.statics import Statics
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from gencrawl.util.utility import Utility


class FinancialDetailSpider(BaseSpider):
    crawl_domain = Statics.DOMAIN_FINANCIAL
    name = f'{crawl_domain}_{Statics.TYPE_DETAIL}'

    @classmethod
    def from_crawler(cls, crawler, config, *args, **kwargs):
        cls.crawl_type = Statics.TYPE_DETAIL
        return super().from_crawler(crawler, config, *args, **kwargs)

    def prepare_items(self, response, default_item={}):
        item = self.exec_codes(response)
        item.update(default_item)
        # item = self.generate_item(obj, ProductItem)
        return [item]

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        for item in items:
            yield item
