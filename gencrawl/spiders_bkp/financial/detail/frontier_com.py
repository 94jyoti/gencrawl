from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
import scrapy
import re
from gencrawl.util.statics import Statics

class FrontierComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_frontier_com'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        file=open("frontier.html","w")
        file.write(response.text)
        file.close()
        print("endwekfncekfckndknvkn---------------------------------------------------",len(items))
        for item in range(len(items)):
        	if(items[item]['other_expenses']==[]):
        		other_expense_temp=response.xpath("//th[text()='Other Expenses']/following-sibling::td/text()").extract()
        		print(other_expense_temp)
        		items[item]['other_expenses']=other_expense_temp[item]
        		print("ayyagxcbdicdkcdbkcbdckd")
        	print(items[item]['redemption_fee'])
        	r_fees=items[item]['redemption_fee']
        	print(r_fees)
        	print("tayayabxjascxbsjc")
        	items[item]['redemption_fee']=re.findall(r'\d*\.?\d+%', r_fees)[0]
        	print(items[item]['redemption_fee'])
        	print("dcccc")
        		
        return items


