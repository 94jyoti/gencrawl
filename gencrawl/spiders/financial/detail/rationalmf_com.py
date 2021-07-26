from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import bs4 as bs
import pandas as pd

class RationalmfDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_rationalmf_com'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        try:
        	maximum_sales_charge=response.xpath("//em[contains(text(),'maximum sales')]//text()").extract()[0]
        except:
        	maximum_sales_charge=response.xpath("//em[contains(text(),'Maximum sales')]//text()").extract()[0]
        for i in items:
        	try:
        		i['portfolio_consultant']=re.findall('Rational Advisors, Inc',i['portfolio_consultant'])[0]
        	except:
        		pass
        	try:
        		if("A" in i['share_class']):
        			try:
        				i['initial_sales_charge']=re.findall(r'.*? maximum sales charge for Class “A” .*? (\d*\.?\d+%)', maximum_sales_charge)[0]
        			except:
        				i['initial_sales_charge']=re.findall(r'Maximum sales charge for Class A shares.*?(\d*\.?\d+%)', maximum_sales_charge)[0]
        	except:
        		pass
        	try:
        		if("C" in i['share_class']):
        			i['contingent_deferred_sales_charge']=re.findall(r'.*? (\d*\.?\d+%) CDSC.*?', maximum_sales_charge)[0]
        	except:
        		pass
        return items