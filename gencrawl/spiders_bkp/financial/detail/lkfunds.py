from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics


class LkfundsfundsComDetail(FinancialDetailSpider):
    name = 'financial_detail_lkfunds_com'
    custom_settings = {
        "RETRY_TIMES": 5,
        "CRAWLERA_ENABLED": True,
        "DOWNLOAD_DELAY": 4
    }

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        meta = response.meta
        meta['items'] = items
        url = "http://www.lkfunds.com/"+response.xpath("//a[contains(text(),'Overview')]/@href").extract()[0]
        print(url)
        yield self.make_request(url, callback=self.overview, meta=meta,method=Statics.CRAWL_METHOD_SELENIUM)
    def overview(self,response):
        items = response.meta['items']
        print("here")

        for item in items:
            item['investment_objective']=response.xpath("//li//span[contains(text(),'Objective')]//following::text()[1]").extract()[0]
        yield self.generate_item(items[0], FinancialDetailItem)


