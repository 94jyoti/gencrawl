from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
from copy import deepcopy
import re

class RiverparkfundsDetail(FinancialDetailSpider):
    name = 'financial_detail_riverparkfunds_com'
    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        temp_items=[]
        gross_net_temp=response.xpath("//div[@class='performance-disclosure']//p[contains(text(),'Expense Ratio')]//text()").extract()[0].split(",")
        share_class_temp=response.xpath("//h3[contains(text(),'DAILY')]/parent::div//table//tr//td[1]//text()").extract()
        nasdaq_temp=items[0]['nasdaq_ticker'].replace("(","").replace(")","").split("/")
        for i in range(len(nasdaq_temp)):
        	temp_items.append(deepcopy(items[0]))
        for item in range(len(temp_items)):
        	temp_items[item]['nasdaq_ticker']=nasdaq_temp[item]
        	for share in share_class_temp:
        		if(temp_items[item]['nasdaq_ticker'] in share):
        			temp_items[item]['share_class']=share.split("(")[0].strip()
        	for gross_net in gross_net_temp:
        		if(temp_items[item]['share_class'] in gross_net):
        			gross_temp=gross_net.split("and")
        			for i in gross_temp:
        				if("gross" in i):
        					temp_items[item]['total_expense_gross']=re.findall(r'\d*\.?\d+%', i)[0]
        				elif("net" in i):
        					temp_items[item]['total_expense_net']=re.findall(r'\d*\.?\d+%', i)[0]
        for item in temp_items:
        	yield self.generate_item(item, FinancialDetailItem)