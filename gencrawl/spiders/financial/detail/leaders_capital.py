from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider

from datetime import datetime
import datetime
import urllib.parse
import re
from gencrawl.util.statics import Statics
# import urllib
import itertools


class LeadersComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_leaders_com'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        #print(items)
        inception_date_text=response.xpath("//p[contains(text(),'Inception')]//text()").extract()[0]
        print(inception_date_text)
        inception_date_temp=inception_date_text.replace("Inception Date -","").split(",")
        print(inception_date_temp)
        for i in items:
        	#i['share_class']=i['share_class'].split("(")[0].strip()
        	print(response.xpath("//td[contains(text(),'CUSIP')]//text()").extract()[0])
        	print(i['share_class'] in response.xpath("//td[contains(text(),'CUSIP')]//text()").extract()[0].replace("CUSIP -","").replace("Share Class","").strip())
        	print(i['share_class'])
        	if(i['share_class'] in response.xpath("//td[contains(text(),'CUSIP')]//text()").extract()[0] ):
        		i['cusip']=response.xpath("//td[contains(text(),'CUSIP')]//following-sibling::td//text()").extract()[0]
        		print("cusisssoxsoppckdpcdkcdpcdk",i['cusip'])
        	for date in inception_date_temp:
        		print(i['nasdaq_ticker'] in date)
        		if(i['nasdaq_ticker'] in date):
        			print(date)
        			i['share_inception_date']=date.split(":")[-1]
        for i in items:
        	yield self.generate_item(i, FinancialDetailItem)