from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import pandas as pd
from copy import deepcopy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
class Forester2ComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_forester2_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        #xprint(len(items))
        #print(items[0])
        if(response.xpath("//strong[contains(text(),'Portfolio Manager')]//following::text()[1]").extract()):
        	temp_fund_manager=response.xpath("//strong[contains(text(),'Portfolio Manager')]//following::text()[1]").extract()[0]
        elif(response.xpath("//span[contains(text(),'Portfolio Manager')]//following::text()[1]").extract()):
        	temp_fund_manager=response.xpath("//span[contains(text(),'Portfolio Manager')]//following::text()[1]").extract()[0]
        else:
        	temp_fund_manager=response.xpath("//p[contains(text(),'Portfolio Manager')]//text()").extract()[0]
        print(temp_fund_manager)
        for item in range(len(items)):
        	if("and" in temp_fund_manager):
        		fund_manager_temp=temp_fund_manager.replace(":","").split("and")
        	elif("," in temp_fund_manager):
        		fund_manager_temp=temp_fund_manager.replace(":","").split(",")
        	else:
        		if("Portfolio Manager" in temp_fund_manager):
        			fund_manager_temp=[temp_fund_manager.split(":")[-1]]
        		else:
        			fund_manager_temp=[temp_fund_manager]
        			print("dwkbdbcb",fund_manager_temp)
        	fund_manager_list=[]
        	for i in fund_manager_temp:
        		data_dict={"fund_manager": ""}
        		data_dict['fund_manager']=i
        		fund_manager_list.append(data_dict)
        	items[item]['fund_managers']=fund_manager_list
        	print(items[0])
        	yield self.generate_item(items[item], FinancialDetailItem)