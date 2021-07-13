from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re

class VirtusComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_virtus_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        #print("tetstttacfascvscvsdhcc",items[0]['minimum_initial_investment'])
        print(items)
        
        test=(response.xpath("//h3[contains(text(),'Sales Charge and Expenses')]//following-sibling::div//text()").extract()[0]).split("%")
        print(test)
        for i in test:
        	print(i)
        	try:
        		if("maximum sales charge" in i.lower()):
        		
        			print("isnid eiifii")
        			items[0]['maximum_sales_charge_full_load']=(re.search('(\d*\.?\d+)', i).group(0))+"%"
        		print(items[0]['maximum_sales_charge_full_load'])
        		if("contingent deferred sales charge" in i.lower()):
        			items[0]['contingent_deferred_sales_charge']=(re.search('(\d*\.?\d+)', i).group(0))+"%"
        	except:
        		 print("fsefs")
        try:
        	gross=(response.xpath('//h3[contains(text(),"Sales Charge and Expenses")]//parent::div//p[1]//text()').extract()[0]).split("%")
        
        	for i in gross:
        		print(i)
        	try:
        		if("gross expense" in i.lower()):
        			items[0]['total_expense_gross']=(re.search('(\d*\.?\d+)', i).group(0))+"%"
        		if("net expense" in i.lower()):
        			items[0]['total_expense_net']=(re.search('(\d*\.?\d+)', i).group(0))+"%"
        	except:
        		print("dgd")
        except:
        	print("nothing")
        return items
