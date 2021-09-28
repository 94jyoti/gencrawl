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

class ThrivenComDetail(FinancialDetailSpider):
    name = 'financial_detail_thriven_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        file=open("thriven.html","w")
        file.write(response.text)
        file.close()
        item=items[0]
        capital_gain_list=[]
        dividends_list=[]
        table_data=response.xpath("//h2[text()='Dividend Distributions & Price History']/following::table[1]//tbody//tr[contains(@class,'main')]")
        for row in table_data:

            data_dict2 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "","record_date": "", "per_share": "", "reinvestment_price": ""}
            data_dict2['record_date']=row.xpath(".//td[1]//text()").extract_first()
            data_dict2['per_share']=row.xpath(".//td[2]//text()").extract_first()
            dividends_list.append(data_dict2)

        table_data1 = response.xpath("//h2[text()='Dividend Distributions & Price History']/following::table[2]//tbody//tr[contains(@class,'main')]")
        for row1 in table_data1:
            #print(row1.xpath(".//td[2]//text()").extract()[0])
            data_dict1 = {"cg_ex_date": "", "cg_record_date": "", "cg_pay_date": "", "short_term_per_share": "", "long_term_per_share": "", "total_per_share": "", "cg_reinvestment_price": ""}
            data_dict1['cg_record_date'] = row1.xpath(".//td[1]//text()").extract_first()
            data_dict1['short_term_per_share'] = row1.xpath(".//td[2]//text()").extract_first()
            print(data_dict1['short_term_per_share'] )
            data_dict1['long_term_per_share'] = row1.xpath(".//td[3]//text()").extract_first()
            data_dict1['total_per_share'] = row1.xpath(".//td[4]//text()").extract_first()
            capital_gain_list.append(data_dict1)
        item['capital_gains']=capital_gain_list
        item['dividends']=dividends_list
        yield self.generate_item(item, FinancialDetailItem)