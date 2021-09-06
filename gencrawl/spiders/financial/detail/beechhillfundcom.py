from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics


class BeechhillfundComDetail(FinancialDetailSpider):
    name = 'financial_detail_beechhillfund_com'

    def get_items_or_req(self, response, default_item=None):
        items = self.prepare_items(response, default_item)
        file=open("beechhil.html","w")
        file.write(response.text)
        file.close()
        url=response.xpath("//h2[contains(text(),'At a Glance')]//following::iframe[1]//@src").extract()[0]
        items[0]['performance_url']=response.xpath("//h2[contains(text(),'Fund Performance')]//following::iframe[1]//@src").extract()[0]
        meta = response.meta
        meta['items'] = items
        return self.make_request(url, callback=self.parse_iframe, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)
    def parse_iframe(self,response):
        items = response.meta['items']
        items[0]['nasdaq_ticker']=response.xpath("//span[contains(text(),'Ticker')]//parent::td//parent::tr//following::tr/td[1]//text()").extract()[0]
        #url = response.xpath("//h2[contains(text(),'Fund Performance')]//following::iframe[1]//@src").extract()[0]
        url=items[0]['performance_url']
        meta = response.meta
        meta['items'] = items
        return self.make_request(url, callback=self.parse_performance, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)

    def parse_performance(self,response):
        items = response.meta['items']
        items[0]['benchmarks']=response.xpath("//table[@class='performance-table']//tbody//tr//td[contains(@class,'header')]//text()[contains(.,'Index') or contains(.,'INDEX')]").extract()
        yield self.generate_item(items[0], FinancialDetailItem)



