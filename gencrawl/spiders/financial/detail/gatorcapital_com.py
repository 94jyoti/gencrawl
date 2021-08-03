from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
import scrapy
import re
from gencrawl.util.statics import Statics
class GatorComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_gator_com'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        print(len(items))
        
        fund_manager_url = "https://gatorcapital.com/"+response.xpath("//a[contains(text(),'Overview')]//@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        print("yahan tk aya")
        print(fund_manager_url)
        yield self.make_request(fund_manager_url, callback=self.fund_manager, meta=meta)

    def fund_manager(self, response):
        items = response.meta['items']
        file=open("gator.html","w")
        file.write(response.text)
        file.close()
        print("response aagya")
        objective=response.xpath("//h2[1]/following::p[1]/text()").extract()[0]
        print(objective)
        strategy=response.xpath("//h2[2]/following::p[1]/text()").extract()[0]
        print(strategy)
        fund_manager_list=[]
        
        fund_manager_temp=response.xpath("//div[@class='left']/h4//text()").extract()
        print(fund_manager_temp)
        for i in fund_manager_temp:
        	data_dict={"fund_manager": ""}
        	data_dict['fund_manager']=i
        	print(data_dict)
        	fund_manager_list.append(data_dict)
        for item in items:
        	item['fund_managers']=fund_manager_list
        	item['investment_objective']=objective
        	item['investment_strategy']=strategy
        				
        return items


