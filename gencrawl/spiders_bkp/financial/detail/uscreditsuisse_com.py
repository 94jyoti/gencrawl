from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
from datetime import datetime
import datetime
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
from gencrawl.util.statics import Statics
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem

class UscreditsuisseComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_uscreditsuisse_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        fund_url_temp = items[0]['fund_url'].rsplit("&")
        fund_url_temp.remove(fund_url_temp[len(fund_url_temp)-1])
        url="&".join(fund_url_temp)+"&tab=3"
        print("dsdsvdvdvdfvfdvfdvdfvdfvdfvdfvdfvfdvdfv",items)
        meta = response.meta
        meta['items'] = items
        #print(gross_url)
        yield self.make_request(url, callback=self.parse_performance, meta=meta,method=Statics.CRAWL_METHOD_SELENIUM)

    def parse_performance(self, response):
        items = response.meta['items']
        temp_net_assets=response.xpath("//td[contains(text(),'Net Assets')]//following-sibling::td//text()").extract()
        print(temp_net_assets)

        for item in range(len(items)):
            items[item]['total_net_assets']=temp_net_assets[item]
            items[item]['total_net_assets_date']=response.xpath("//i[contains(text(),'Last Update')]//text()").extract()[0].split(":")[-1].strip()
        #return items
            yield self.generate_item(items[item], FinancialDetailItem)