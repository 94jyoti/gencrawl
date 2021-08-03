from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics

class CommerceComDetail(FinancialDetailSpider):
    name = 'financial_detail_commerce_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        main_url = "https://www.commercefunds.com/fund-information/mutual-funds"
        meta = response.meta
        meta['items'] = items
        yield self.make_request(main_url, callback=self.dividends, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)

    def dividends(self, response):
        items = response.meta['items']
        nasdaq_ticker_temp=response.xpath("//tbody//tr")
        for row in nasdaq_ticker_temp:
        	nasdaq_ticker_main=row.xpath(".//td[1]//text()").extract_first()
        	if(items[0]['nasdaq_ticker'].strip()==nasdaq_ticker_main.strip()):
        		items[0]['dividend_frequency']=row.xpath(".//td[4]//text()").extract_first()
        yield self.generate_item(items[0], FinancialDetailItem)