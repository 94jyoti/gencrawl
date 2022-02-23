from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics
import re

class TocquevilleComDetail(FinancialDetailSpider):
    name = 'financial_detail_tocqueville_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        url="https://www.tocquevillefunds.com/"+response.xpath("//a[contains(text(),'Performance')]//@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        yield self.make_request(url, callback=self.parse_performance, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)

    def parse_performance(self,response):
        gross=response.xpath("//h2[contains(text(),'Last Quarter')]//following::table//td[contains(text(),'Gross')]//text()").extract()
        items = response.meta['items']
        for i in gross:
            if("Gross" in i):
                items[0]['total_expense_gross']=re.findall(r'\d*\.?\d+', i)[0]
                items[0]['expense_waivers']="-"+re.findall(r'\d*\.?\d+', i)[1]
            if("after Fee Waiver" in i):
                items[0]['annual_fund_operating_expenses_after_fee_waiver']=re.findall(r'\d*\.?\d+', i)[0]
                items[0]['total_expense_net']=re.findall(r'\d*\.?\d+', i)[0]
        items[0]['benchmarks']=list(set(response.xpath("//h2[contains(text(),'Last Month')]//following::table[1]//tbody//tr[position()=last()]//td[1]//text()").extract()))
        yield self.generate_item(items[0], FinancialDetailItem)
