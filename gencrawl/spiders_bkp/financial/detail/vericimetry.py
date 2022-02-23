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


class VericimetryComDetail(FinancialDetailSpider):
    name = 'financial_detail_vericimetry_com'
    allowed_domains = ['www.vericimetry.com','hosting.umb.com']
    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        url=response.xpath("//iframe//@src").extract()[0]
        print(url)
        meta = response.meta
        meta['items'] = items
        yield self.make_request(url, callback=self.parse_performance, meta=meta)
        #yield self.generate_item(item, FinancialDetailItem)
    def parse_performance(self,response):
        print("performance")
        items = response.meta['items']
        instrument_name=response.xpath("//h1[@class='entry-title']//text()").extract()[0]
        print(instrument_name)
        benchmark=response.xpath("//table[2]//tr/td[contains(text(),'Index')]/text()").extract()
        items[0]['instrument_name']=instrument_name
        items[0]['benchmarks']=benchmark
        meta = response.meta
        meta['items'] = items
        url="https://www.vericimetry.com/vysvx/team.php"
        yield self.make_request(url, callback=self.parse_team, meta=meta)
        #yield self.generate_item(items[0], FinancialDetailItem)
    def parse_team(self,response):
        print("isnideeeei")
        items = response.meta['items']
        fund_manager_list=[]
        manager=response.xpath("// strong[contains(text(), 'Investment Team')] / ancestor::h3 // following::p / strong / a[@class ='fancybox'][contains(text(), 'PhD') or contains(text(), 'Berman')] // text()").extract()
        for i in manager:
            data_dict1={"fund_manager": ""}
            data_dict1['fund_manager']=i
            fund_manager_list.append(data_dict1)
        items[0]['fund_managers']=fund_manager_list
        yield self.generate_item(items[0], FinancialDetailItem)