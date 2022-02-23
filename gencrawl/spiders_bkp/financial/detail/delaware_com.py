from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
import re


class EatonvanceComDetail(FinancialDetailSpider):
    name = 'financial_detail_delaware_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        item = items[0]
        # item['share_class'] = item['fund_url'].split("=")[-1]
        file=open("eatonjson.html","w")
        file.write(response.text)
        file.close()
        print("-----------------------------------------------------")
        print(item['fund_url'])
        yield self.generate_item(item, FinancialDetailItem)

    def parse_performance_response(self, response):
        print('wdwaaaaaaaaaaaddddddddddddddddddddddddd')
        items = response.meta['items']
        distribution_history = response.xpath('//tr[@class="tableView"]//td//text()').extract()
        print(distribution_history)
        # file = open("jsonnuveen.txt", "w")
        # file.write(response.text)
        # file.close()
        file = open("eaton.txt", "w")
        file.write(response.text)
        file.close()
        # print("reso.....................................",response_json)
        # historical_data = response_json['Distributions']
        # try:
        # items = items[0]
        # except:
        #   print("done")

        #capital_gains_list = []
        dividend_history = []
        
        for dis in range(0, len(distribution_history), 3):
            print(dis)
            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                      "record_date": "", "per_share": "", "reinvestment_price": ""}
            data_dict1['ex_date'] = distribution_history[dis]
            data_dict1['reinvestment_price'] = distribution_history[dis + 2]
            data_dict1['ordinary_income'] = distribution_history[dis + 1]
            dividend_history.append(data_dict1)
        # items['capital_gains'] = capital_gains_list
        items['dividends'] = dividend_history

        '''

        capital_gains_list = []
        for i in response_json:
            data_dict = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                         'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': "","ordinary_income":""}
            data_dict['long_term_per_share'] = 
            data_dict['cg_ex_date'] = i['exdivdt']
            data_dict['cg_record_date'] = i['rcrddt']
            data_dict['cg_pay_date'] = i['paydt']
            data_dict['short_term_per_share'] = None
            data_dict['total_per_share'] = None
            data_dict['cg_reinvestment_price'] = None
            data_dict['ordinary_income'] = None
            capital_gains_list.append(data_dict)

        items['capital_gains'] = capital_gains_list
        '''
        # print("bvbvvvvvvvvvvvvvvvvvvvvvvv",items)
        yield self.generate_item(items, FinancialDetailItem)
