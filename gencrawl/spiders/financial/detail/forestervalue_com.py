from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import pandas as pd
from copy import deepcopy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
class ForesterComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_forester_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        print(items)
        #return items
        length_nasdaq=len(items[0]['nasdaq_ticker'].split("/"))
        final_item =[]
        for i in range(len(items[0]['nasdaq_ticker'].split("/"))):
            final_item.append(deepcopy(items[0]))
            #print(len(final_item))
        print(len(final_item))
        print("cdsvdsvssdv",len(final_item[0]['nasdaq_ticker'].split("/")))
        if(len(final_item)==2):
            counter=0
            
            for i in range(len(final_item)):
                
                #print("edfegvegwegwegew",final_item[i]['nasdaq_ticker'].split("/")[i])
                print(final_item[i]['nasdaq_ticker'])
                print("lkenfclekwfwelkfnewkfnefwelfkwnn")
                n=final_item[i]['nasdaq_ticker'].split("/")[i]
                print(n)
                final_item[i]['nasdaq_ticker']=n
                #final_item[i]['nasdaq_ticker']=nasdaq_ticker
                final_item[i]['cusip']=final_item[i]['cusip'].split("/")[i]
                final_item[i]['share_class']=final_item[i]['share_class'].split("/")[i].replace(")","")
                final_item[i]['total_expense_gross']=final_item[i]['total_expense_gross'].split("/")[i]
                final_item[i]['minimum_initial_investment']=final_item[i]['minimum_initial_investment'].split("/")[i]
				#counter=counter+1
        #print(final_item)   
        #print("efffff",len(final_item))
       # final_list={'nasdaq_ticker':items['nasdaq_ticker'].split("/"),'cusip':items['cusip'].split("/"),'share_class':items['share_class'].split("/"),'total_expense_gross':item['total_expense_gross'].split("/")}
        for i in final_item:
                yield self.generate_item(i, FinancialDetailItem)