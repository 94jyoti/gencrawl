from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import json
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics


class funds_1920ComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_1920funds_com'
    custom_settings = {
        "RETRY_TIMES": 5,
        "CRAWLERA_ENABLED": True,
        "COOKIES_ENABLED": True,
        "COOKIES_DEBUG": True,
        "CRAWLERA_ENABLED": True
    }
    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        meta = response.meta
        meta['items'] = items
        for item in items:
            api_url="https://secure.alpsinc.com/MarketingAPI/api/v1/Dividend/"+item['nasdaq_ticker']
            headers={"Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8","Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE2MzIyMTM4NjYsImp0aSI6IkJBMEQxMzU1LUU5NTItNDVBRC1BNkU1LUEzQ0RGQURGQTE1NCIsImlzcyI6Ind3dy4xMjkwZnVuZHMuY29tIiwic3ViIjoiaHR0cHM6XC9cL2Nzc2VjdXJlLmFscHNpbmMuY29tXC9hcGlcL3YxXC8iLCJuYmYiOjE2MzIyMTM4NjYsImV4cCI6MTYzMjMwMDI2Nn0.IHh83ijzf41U8m0YJ76deucA_5lN1NVElONVKnnCuH-y0F9g2SGVRMtKrVOoQTEs-Iuuclimf_-wu2ApmIEycA","Connection": "keep-alive","Host": "secure.alpsinc.com","Origin": "http://www.1290funds.com","Referer": "http://www.1290funds.com/","User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"}
            yield self.make_request(api_url, headers=headers,callback=self.parse_dividends, meta=meta, method=Statics.CRAWL_METHOD_GET,dont_filter=True)

    def parse_dividends(self,response):
        items = response.meta['items']
        print("i am here")
        file = open("1290_div.html", "w")
        file.write(response.text)
        file.close()
        json_data=json.loads(response.text)
        print(json_data)


        for item in items:

            capital_gain_list = []
            dividend_list = []
            if(item['nasdaq_ticker']==json_data[0]['symbol']):
                print("isnide ififififiiffifii")
                #data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "", "record_date": "", "per_share": "", "reinvestment_price": ""}
                #data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
                for i in json_data:
                    data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "","record_date": "", "per_share": "", "reinvestment_price": ""}
                    data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
                    print("iiiiiiiiiiiiiii--------------",i)
                    data_dict1['ex_date']=i['exdate'].split("T")[0]
                    data_dict1['record_date']=i['recorddate'].split("T")[0]
                    data_dict1['pay_date']=i['payabledate'].split("T")[0]
                    data_dict1['ordinary_income']=i['ord']
                    data_dict2['short_term_per_share']=i['stcg']
                    data_dict2['long_term_per_share']=i['ltcg']
                    data_dict2['total_per_share']=i['total']
                    capital_gain_list.append(data_dict2)
                    print("capitalllll-------------",capital_gain_list)
                    dividend_list.append(data_dict1)
                    print("dividendndnddndndndn",dividend_list)
                item['capital_gains']=capital_gain_list
                item['dividends']=dividend_list
                
                yield self.generate_item(item, FinancialDetailItem)









