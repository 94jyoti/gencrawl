from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
from gencrawl.util.statics import Statics
import re
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
import json

class BrownadvisoryDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_brownadvisory_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        url="https://www.brownadvisory.com/mf"
        meta = response.meta
        meta['items'] = items
        yield self.make_request(url, callback=self.parse_mainpage, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)
    def parse_mainpage(self, response):
        items = response.meta['items']
        fund_name = None
        for block in response.xpath("//tr[contains(@class, 'fund-row')]"):
                fund_name = block.xpath(".//td[1]//a//text()").extract_first() or fund_name
                if (fund_name not in items[0]['instrument_name']):
                    continue
                ticker = block.xpath('.//td[4]//text()').extract_first()
                share_class = block.xpath('.//td[3]//text()').extract_first()
                for item in items:
                    if(item['share_class']==share_class):
                        item['nasdaq_ticker']=ticker
        for item in items:
            yield self.generate_item(item, FinancialDetailItem)
