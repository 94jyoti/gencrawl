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
import logging
import requests
from lxml import html
from scrapy.selector import Selector
import copy


class glafundsDetail(FinancialDetailFieldMapSpider):
    logging.basicConfig(filename="hsbc.log", level=logging.INFO)
    logging.info("InvestorFundsUSHSBCDetail")
    name = 'glafunds_com'

    
    def get_items_or_req(self, response, default_item={}):
        logging.info("InvestorFundsUSHSBCDetail...get_items_or_req")
        items = super().get_items_or_req(response, default_item)
        #print("Items:",len(items))

        #open('a.html','w',encoding='utf-8').write(response.text)

        meta = response.meta
        
        meta['items'] = items

        #open('gla.html','w',encoding='utf-8').write(response.text)
        selector = scrapy.Selector(text=response.text, type="html")

        share_classes = selector.xpath("//h3[contains(text(),'FUND BASICS')]/following-sibling::table/tbody/tr/td[2][contains(text(),'cusip')]//preceding-sibling::td/text()").getall()

        #print("share_classes:",share_classes)

        investment_block = selector.xpath("//strong[contains(text(),'Class')]//ancestor::table[1]//tr")

        #print(investment_block)

        temp = []

        for i in investment_block:
            share_class = i.xpath("./td[1]/text() | ./td[1]/strong/text()").get()
            min_investment = i.xpath("./td[2]/text() | ./td[2]/strong/text()").get()
            addl_investment = i.xpath("./td[3]/text() | ./td[3]/strong/text()").get()

            #Dict = {}

            

            temp.append([share_class,[min_investment,addl_investment]])


        #print(temp)

        for c,i in enumerate(temp):
            #if i[0]=='Regular Account':

            if temp[c][0]=='Regular Account':
                temp[c-1][1][0] = temp[c][1][0]
                temp[c-1][1][1] = temp[c][1][1]


            #print(c,temp[c][0])

        #print(temp)



        fee_expenses_block = selector.xpath("//td[contains(text(),'Management Fee')]//parent::tr//ancestor::table[1]//tr")

        td_count = len(selector.xpath("//td[contains(text(),'Management Fee')]//parent::tr//ancestor::table[1]//tr[1]/td"))

        print("td_count:",td_count)
        #print("fee_expenses_block:",fee_expenses_block)

        temp_fee_expense = []

        ttt=[]

        for f in fee_expenses_block:
            tt=[]
            for t in range(0,td_count):
                print("ttt:",t+1)
                heading = f.xpath("./td["+str(t+1)+"]/text() | ./td["+str(t+1)+"]/strong/text()").get()
                print(heading)

                tt.append(heading)
            print(tt)
            temp_fee_expense.append(tt)
        print("temp_fee_expense:",temp_fee_expense)


        fund_mgr = selector.xpath("//h3[contains(text(),'PORTFOLIO MANAGEMENT')]//following-sibling::p[@class='bold gla_blue_light']/text()").getall()

        print("fund_mgr:",fund_mgr)
        fund_mg_list = [fund_mgr[f-1] for f in range(1,len(fund_mgr),2)]
        print("fund_mg_list:",fund_mg_list)

        fund_managers_list = []

        Dict = {}
        for f in fund_mg_list:
            print("f:",f)
            Dict = dict([('fund_manager',f)])
            print("DICT:",Dict)
            fund_managers_list.append(Dict)



            
        #print(heading,ticker1,ticker2)
        #temp_fee_expense.append([heading,ticker1])

        #print("temp_fee_expense:",temp_fee_expense)

        print(temp_fee_expense[0],len(temp_fee_expense))

        temp_fee_dict = {}


           


        for i in meta['items']:
            print(i)


            #fund Managers
            i['fund_managers'] = fund_managers_list
            

            for j in temp:
                #print(j)
                if i['share_class'] in j[0]:


                    i['minimum_initial_investment'] = j[1][0]
                    i['minimum_additional_investment'] = j[1][1]
                    

                    #print(j)
            for j in range(1,len(temp_fee_expense[0])):
                print(j,temp_fee_expense[0][j],i['nasdaq_ticker'])


                if i['nasdaq_ticker'].strip()==temp_fee_expense[0][j].strip():
                    x = [f[1] for f in temp_fee_expense if 'Total Expense Ratio' in f]
                    print(x)
                    print("hello",j,i['nasdaq_ticker'],temp_fee_expense[4][j])

                    i['total_expense_gross'] = [f[1] for f in temp_fee_expense if 'Total Expense Ratio' in f][0]
                    i['management_fee'] = [f[1] for f in temp_fee_expense if 'Management Fee' in f][0]
                    i['fees_total_12b_1'] = [f[1] for f in temp_fee_expense if '12b-1 Distribution Fee' in f][0]
                    i['other_expenses'] = [f[1] for f in temp_fee_expense if 'Other Expenses' in f][0]
            
            yield self.generate_item(i, FinancialDetailItem)



       






    