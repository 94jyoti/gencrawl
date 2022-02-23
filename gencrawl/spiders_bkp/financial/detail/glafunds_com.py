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
    name = 'glafunds_com'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        meta = response.meta
        meta['items'] = items
        selector = scrapy.Selector(text=response.text, type="html")

        share_classes = selector.xpath("//h3[contains(text(),'FUND BASICS')]/following-sibling::table/tbody/tr/td[2][contains(text(),'cusip')]//preceding-sibling::td/text()").getall()
        investment_block = selector.xpath("//strong[contains(text(),'Class')]//ancestor::table[1]//tr")
        temp = []

        for i in investment_block:
            share_class = i.xpath("./td[1]/text() | ./td[1]/strong/text()").get()
            min_investment = i.xpath("./td[2]/text() | ./td[2]/strong/text()").get()
            addl_investment = i.xpath("./td[3]/text() | ./td[3]/strong/text()").get()
            temp.append([share_class,[min_investment,addl_investment]])

        for c,i in enumerate(temp):
            if temp[c][0]=='Regular Account':
                temp[c-1][1][0] = temp[c][1][0]
                temp[c-1][1][1] = temp[c][1][1]

        fee_expenses_block = selector.xpath("//td[contains(text(),'Management Fee')]//parent::tr//ancestor::table[1]//tr")

        td_count = len(selector.xpath("//td[contains(text(),'Management Fee')]//parent::tr//ancestor::table[1]//tr[1]/td"))
        temp_fee_expense = []
        for f in fee_expenses_block:
            tt=[]
            for t in range(0,td_count):
                heading = f.xpath("./td["+str(t+1)+"]/text() | ./td["+str(t+1)+"]/strong/text()").get()
                tt.append(heading)

            temp_fee_expense.append(tt)

        fund_mgr = selector.xpath("//h3[contains(text(),'PORTFOLIO MANAGEMENT')]//following-sibling::p[@class='bold gla_blue_light']/text()").getall()
        fund_mg_list = [fund_mgr[f-1] for f in range(1,len(fund_mgr),2)]
        fund_managers_list = []

        for f in fund_mg_list:
            Dict = dict([('fund_manager',f)])
            fund_managers_list.append(Dict)

        for i in meta['items']:
            i['fund_managers'] = fund_managers_list

            for j in temp:
                if i['share_class'] in j[0]:
                    i['minimum_initial_investment'] = j[1][0]
                    i['minimum_additional_investment'] = j[1][1]
                    
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



       






    