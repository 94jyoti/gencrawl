from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse


class VolumetricComDetail(FinancialDetailSpider):
    name = 'financial_detail_volumetric_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        portfolio_managers_url = response.xpath("//li//a[contains(text(),'PORTFOLIO MANAGERS')]//@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        yield self.make_request(portfolio_managers_url, callback=self.portfolio_manager, meta=meta)

    def portfolio_manager(self, response):
        items = response.meta['items']
        fund_manager_temp=response.xpath("//*[contains(@id,'comp-jbt')]//h6[1]//text()").extract()
        fund_manager_list=[]
        for i in fund_manager_temp:
        	data_dict={"fund_manager": ""}
        	data_dict['fund_manager']=i
        	fund_manager_list.append(data_dict)
        items[0]['fund_managers']=fund_manager_list
        yield self.generate_item(items[0], FinancialDetailItem)