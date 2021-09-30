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
import traceback

class EmeraldfundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_emeraldfunds_com'
    custom_settings = {
        "RETRY_TIMES": 5,
        "CRAWLERA_ENABLED": True,
        "COOKIES_ENABLED": True,
        "COOKIES_DEBUG": True,
        "CRAWLERA_ENABLED": True
    }
    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        url_list=[]
        #for item in items:
         #   temp_ticker=item['nasdaq_ticker']
        headers={'Connection': 'keep-alive',
                     'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE2MzE3OTExNTUsImp0aSI6IjcxMkMxMTRGLTY5QUEtNDA5OC1BOTI4LUExMTRDNjgyQURDRCIsImlzcyI6Ind3dy5lbWVyYWxkbXV0dWFsZnVuZHMuY29tIiwic3ViIjoiaHR0cHM6XC9cL2Nzc2VjdXJlLmFscHNpbmMuY29tXC9hcGlcL3YxXC8iLCJuYmYiOjE2MzE3OTExNTUsImV4cCI6MTYzMTg3NzU1NX0.gq61J6yljp44U6WZfDYjK9XRIOPwl7IIxkGtnrkhUar9DDKWa9ZN8foRPIR-84YJjFvIYwOlEH7kD6PJvVrUSA",'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'}
        url="https://secure.alpsinc.com/MarketingAPI/api/v1/Dividend/HSPCX"
            #url_list.append(url)
            #item['capital_gains'] = []
            #item['dividends'] = []
        meta = response.meta
        meta['items'] = items
        for item in items:
            url = "https://secure.alpsinc.com/MarketingAPI/api/v1/Dividend/"+ item['nasdaq_ticker']
            headers = {"Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8","Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE2MzIyMTgwNjEsImp0aSI6IjU1QkI4Qzg2LTMxN0UtNDhFRi1BMkU4LTVGM0NBMDFBRkE1RSIsImlzcyI6Ind3dy5lbWVyYWxkbXV0dWFsZnVuZHMuY29tIiwic3ViIjoiaHR0cHM6XC9cL2Nzc2VjdXJlLmFscHNpbmMuY29tXC9hcGlcL3YxXC8iLCJuYmYiOjE2MzIyMTgwNjEsImV4cCI6MTYzMjMwNDQ2MX0.EO0VZMPODtRC4trkCUySsX5cUOW-g6ALc5CtMMu1jtv-9Su8rzYSv-aYhpBjyD8yMMpr4fYNc_kqeeXyGXHnDg","Connection": "keep-alive", "Host": "secure.alpsinc.com", "Origin": "https://www.emeraldmutualfunds.com", "Referer": "https://www.emeraldmutualfunds.com/","User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"}
            yield scrapy.Request(url, headers=headers, callback=self.parse_dividends, meta=meta,method="GET", dont_filter=True)

    def parse_dividends(self, response):
        items = response.meta['items']
        print("i am here")
        file = open("emerland.html", "w")
        file.write(response.text)
        file.close()
        json_data = json.loads(response.text)
        print(json_data)
        for item in items:

            capital_gain_list = []
            dividend_list = []
            if (item['nasdaq_ticker'] == json_data[0]['symbol']):
                print("isnide ififififiiffifii")
                # data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "", "record_date": "", "per_share": "", "reinvestment_price": ""}
                # data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
                for i in json_data:
                    data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                                  "record_date": "", "per_share": "", "reinvestment_price": ""}
                    data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                                  'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
                    print("iiiiiiiiiiiiiii--------------", i)
                    data_dict1['ex_date'] = i['exdate'].split("T")[0]
                    data_dict1['record_date'] = i['recorddate'].split("T")[0]
                    data_dict1['pay_date'] = i['payabledate'].split("T")[0]
                    data_dict1['ordinary_income'] = i['ord']
                    data_dict2['short_term_per_share'] = i['stcg']
                    data_dict2['long_term_per_share'] = i['ltcg']
                   # data_dict2['total_per_share'] = i['total']
                    capital_gain_list.append(data_dict2)
                    print("capitalllll-------------", capital_gain_list)
                    dividend_list.append(data_dict1)
                    print("dividendndnddndndndn", dividend_list)
                item['capital_gains'] = capital_gain_list
                item['dividends'] = dividend_list

                yield self.generate_item(item, FinancialDetailItem)