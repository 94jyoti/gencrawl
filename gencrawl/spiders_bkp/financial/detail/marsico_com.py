from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics

class MarsicoComDetail(FinancialDetailSpider):
    name = 'financial_detail_marsico_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        main_url = "https://www.marsicofunds.com/"+response.xpath("//a[contains(text(),'Manager Bios')]//@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        yield self.make_request(main_url, callback=self.parse_manager, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)

    def parse_manager(self, response):
        items = response.meta['items']
        fund_manager_list=[]
        fund_manager_temp=response.xpath("//input[contains(@id,'Managers')]/following-sibling::h2//text()").extract()
        print(fund_manager_temp)
        for i in fund_manager_temp:
            data_dict={"fund_manager": ""}
            data_dict['fund_manager']=i
            fund_manager_list.append(data_dict)
        print(fund_manager_list)


        items[0]['fund_managers']=fund_manager_list
        yield self.generate_item(items[0], FinancialDetailItem)