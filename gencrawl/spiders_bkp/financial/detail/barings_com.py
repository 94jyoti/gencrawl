from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics


class BaringsComDetail(FinancialDetailSpider):
    name = 'financial_detail_barings_com'
	
    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        item=items[0]
        item['share_class']=item['share_class'].replace("\n\t","").replace("\t","")
        share_class_temp=[i.replace("-Class","").strip() for i in response.xpath("//h2[contains(text(),'Expense Ratios')]/following::table[1]//tr[1]//td//text()").extract()]

        row_data=response.xpath("//h2[contains(text(),'Expense Ratios')]/following::table[1]//tr[position()>1]")
        for row in row_data:
        	gross=row.xpath(".//td[1]//text()").extract()[0]
        	if(item['share_class'].replace("Class","").strip() in share_class_temp):
        		index_share_class=share_class_temp.index(item['share_class'].replace("Class","").strip())
        		if("Gross" in gross):
        			item['total_expense_gross']=row.xpath(".//td["+str(index_share_class+2)+"]").extract_first()
        		if("Net" in gross):
        			item['total_expense_net']=row.xpath("./td["+str(index_share_class+2)+"]").extract_first()
        yield self.generate_item(item, FinancialDetailItem)