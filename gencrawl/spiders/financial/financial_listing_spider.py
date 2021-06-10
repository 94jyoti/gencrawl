from gencrawl.spiders import BaseSpider
from gencrawl.util.statics import Statics
from gencrawl.items.financial.financial_listing_item import FinancialListingItem
from gencrawl.util.utility import Utility


class FinancialListingSpider(BaseSpider):
    crawl_domain = Statics.DOMAIN_FINANCIAL
    url_key = Statics.URL_KEY_FINANCIAL_LISTING
    name = f'{crawl_domain}_{Statics.CRAWL_TYPE_LISTING}'

    @classmethod
    def from_crawler(cls, crawler, config, *args, **kwargs):
        cls.crawl_type = Statics.CRAWL_TYPE_LISTING
        return super().from_crawler(crawler, config, *args, **kwargs)

    def prepare_items(self, response, default_item=None):
        default_item = default_item or dict()
        parsed_items = []
        items = self.exec_codes(response)
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
            print(item)
            parsed_items.append(self.generate_item(item, FinancialListingItem))
        return parsed_items

