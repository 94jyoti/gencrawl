from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re


class SoafundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_soafunds_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        meta = response.meta
        meta['items'] = items
        fund_manager_url=response.xpath("//p[contains(text(),'MANAGEMENT TEAM')]//ancestor::a//@href").extract()[0]
        return self.make_request(fund_manager_url, callback=self.fund_manager, meta=meta,dont_filter=True)
    
    def fund_manager(self, response):
        items = response.meta['items']
        fund_manager_list=[]
        fund_since_temp=[]
        fund_since=response.xpath("//*[contains(text(),'Industry since')]/text() | //span[contains(text(),'Portfolio Manager')]//br[1]//following-sibling::text()").extract()
        for i in fund_since:
        	if(re.findall(r'\d*\.?\d+', i)!=[]):
        		fund_since_temp.append(re.findall(r'\d*\.?\d+', i)[0])
        fund_manager_temp=response.xpath('//*[contains(text(),"Management Team")]//following::span[contains(text(),"Portfolio Manager")]//preceding::span[1]//text()').extract()
        for i in range(len(fund_manager_temp)):
        	data_dict = {"fund_manager": "", "fund_manager_years_of_experience_in_industry": "","fund_manager_firm": "", "fund_manager_years_of_experience_with_fund": ""}
        	data_dict['fund_manager']=fund_manager_temp[i]
        	data_dict['fund_manager_years_of_experience_in_industry']=fund_since_temp[i]
        	fund_manager_list.append(data_dict)
        items[0]['fund_managers']=fund_manager_list
        return items