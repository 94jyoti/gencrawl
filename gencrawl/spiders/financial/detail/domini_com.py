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
class DominiComDetail(FinancialDetailSpider):
    name = 'financial_detail_domini_com'
	
    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        for item in items:
        	try:
        		if("annual turnover" in item['turnover_rate_date'].lower()):
        			item['turnover_rate_date']=response.xpath("//strong[contains(text(),'Portfolio Statistics')]/following::text()[1]").extract()[0].replace("as of","").strip()
        	except:
        		pass
        	
        	try:
        		temp=response.xpath("//td[contains(text(),'SEC')]//text()").extract()[0].lower()
        		if("sec 30" in temp):
        			sec30_data_list=response.xpath("//td[contains(text(),'SEC')]//text()").extract()
        			for i in sec30_data_list:
        				if(item['share_class'].replace("\n","").strip() in i):
        					index_sec=sec30_data_list.index(i)
        					item['sec_yield_30_day']=response.xpath("//td[contains(text(),'SEC 30-Day Yield ("+item['share_class'].replace('\n','').strip()+")')]/following-sibling::td[1]//text()").extract()[0]
        					sec_date=response.xpath("//h2[contains(text(),'Characteristic')]//parent::div//following::em[contains(text(),'as of')]//text()").extract()[0]
        					item['sec_yield_date_30_day']=re.findall("\d+/\d+/\d+",sec_date)[0]
        	except:
        		pass
        yield self.generate_item(item, FinancialDetailItem)