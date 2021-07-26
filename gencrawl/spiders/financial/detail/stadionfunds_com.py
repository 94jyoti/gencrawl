from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import pandas as pd


class StadionComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_stadion_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        #print(len(items))
        inception_date_list=(items[0]['share_inception_date']).split("Class")
        while("" in inception_date_list) :
            inception_date_list.remove("")
        for item in items:
        	for i in inception_date_list:
        		print("iiiiiii",i)
        		if(item['share_class'] in i ):
        			item['share_inception_date']=(re.search(r'(\d+/\d+/\d+)',i)).group()
        			print(item['share_inception_date'])
        print(inception_date_list)
        return items