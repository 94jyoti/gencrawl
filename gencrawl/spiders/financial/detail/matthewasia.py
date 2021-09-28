from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics

class MatthewasiaComDetail(FinancialDetailSpider):
    name = 'financial_detail_matthewasia_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        meta = response.meta
        meta['items'] = items
        file=open("matheasia.html","w")
        file.write(response.text)
        file.close()
        table_data = response.xpath("(//table[@class='funds distributions_table'])[1]//tr")
        for item in items:
            capital_gain_list = []
            dividend_list = []
            print("inside item")
            for row in table_data:
                print("inside fir")
                print(row)
                data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                          "record_date": "", "per_share": "", "reinvestment_price": ""}
                data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                          'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
                print(row.xpath(".//td[1]/text()[1]").extract_first())
                data_dict1['record_date'] = (row.xpath(".//td[1][not(contains(@colspan,'1'))]//text()[1]").extract_first())
                if(data_dict1['record_date']==None):
                    continue

                data_dict1['ex_date'] = row.xpath(".//td[2]/text()").extract_first()
                data_dict1['pay_date'] = row.xpath(".//td[2]/text()").extract_first()
                data_dict1['ordinary_income'] = row.xpath(".//td[3]/text()").extract_first()
                data_dict2['short_term_per_share'] = row.xpath(".//td[4]/text()").extract_first()
                data_dict2['long_term_per_share'] = row.xpath(".//td[5]/text()").extract_first()
                data_dict1['per_share'] = row.xpath(".//td[6]/text()").extract_first()
                capital_gain_list.append(data_dict2)
                dividend_list.append(data_dict1)
            item['capital_gains'] = capital_gain_list
            item['dividends'] = dividend_list
            yield self.generate_item(item, FinancialDetailItem)
''''
        print(table_data)
        #print("here")
        #print(table_data.xpath("//td[1][not(contains(@colspan,'1'))]//text()[1]").extract())
            for item in items:
                capital_gain_list = []
            dividend_list = []
            print("inside item")
            for row in table_data:
                print("inside fir")
            print(row)
            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                          "record_date": "", "per_share": "", "reinvestment_price": ""}
            data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                          'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
            print(row.xpath(".//td[1]/text()[1]").extract_first())
            data_dict1['record_date'] = row.xpath(".//td[1][not(contains(@colspan,'1'))]//text()[1]").extract_first()
            data_dict1['ex_date'] = row.xpath(".//td[2]/text()").extract_first()
            data_dict1['pay_date'] = row.xpath(".//td[2]/text()").extract_first()
            data_dict1['ordinary_income'] = row.xpath(".//td[3]/text()").extract_first()
            data_dict2['short_term_per_share'] = row.xpath(".//td[4]/text()").extract_first()
            data_dict2['long_term_per_share'] = row.xpath(".//td[5]/text()").extract_first()
            data_dict1['per_share'] = row.xpath(".//td[6]/text()").extract_first()
            capital_gain_list.append(data_dict2)
            dividend_list.append(data_dict1)
            item['capital_gains'] = capital_gain_list
            item['dividends'] = dividend_list
            # yield self.generate_item(item, FinancialDetailItem)

        #file=open("matthew.html","w")
        #file.write(response.text)
        #file.close()
        
        for item in items:
            capital_gain_list = []
            dividend_list = []
            print("inside item")
            for row in table_data:
                print("inside fir")
                print(row)
                data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "", "record_date": "", "per_share": "", "reinvestment_price": ""}
                data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
                print(row.xpath(".//td[1]/text()[1]").extract_first())
                data_dict1['record_date']=row.xpath(".//td[1][not(contains(@colspan,'1'))]//text()[1]").extract_first()
                data_dict1['ex_date']=row.xpath(".//td[2]/text()").extract_first()
                data_dict1['pay_date']=row.xpath(".//td[2]/text()").extract_first()
                data_dict1['ordinary_income']=row.xpath(".//td[3]/text()").extract_first()
                data_dict2['short_term_per_share']=row.xpath(".//td[4]/text()").extract_first()
                data_dict2['long_term_per_share']=row.xpath(".//td[5]/text()").extract_first()
                data_dict1['per_share']=row.xpath(".//td[6]/text()").extract_first()
                capital_gain_list.append(data_dict2)
                dividend_list.append(data_dict1)
            item['capital_gains']=capital_gain_list
            item['dividends']=dividend_list
            #yield self.generate_item(item, FinancialDetailItem)
            '''