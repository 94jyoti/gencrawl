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
    allowed_domains = ["secure.alpsinc.com"]
    custom_settings = {
        "HTTPCACHE_ENABLED": True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 4,
        "COOKIES_ENABLED": True,
        "COOKIES_DEBUG":True
    }

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        url_list=[]
        for item in items:
            temp_ticker=item['nasdaq_ticker']
            headers={'Connection': 'keep-alive',
                     'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpYXQiOjE2MzE3OTExNTUsImp0aSI6IjcxMkMxMTRGLTY5QUEtNDA5OC1BOTI4LUExMTRDNjgyQURDRCIsImlzcyI6Ind3dy5lbWVyYWxkbXV0dWFsZnVuZHMuY29tIiwic3ViIjoiaHR0cHM6XC9cL2Nzc2VjdXJlLmFscHNpbmMuY29tXC9hcGlcL3YxXC8iLCJuYmYiOjE2MzE3OTExNTUsImV4cCI6MTYzMTg3NzU1NX0.gq61J6yljp44U6WZfDYjK9XRIOPwl7IIxkGtnrkhUar9DDKWa9ZN8foRPIR-84YJjFvIYwOlEH7kD6PJvVrUSA",'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'}





            url="https://secure.alpsinc.com/MarketingAPI/api/v1/Dividend/"+item['nasdaq_ticker']
            url_list.append(url)
            #item['capital_gains'] = []
            #item['dividends'] = []
        meta = response.meta
        meta['items'] = items
        hit_url=url_list[0]
        meta['url_list']=url_list[1:]
        #yield self.make_request(hit_url, callback=self.dividends,headers=headers, meta=meta, method=Statics.CRAWL_METHOD_GET,dont_filter=True)
        params = {
            'grant_type': 'client_credentials',
            'client_id': '**********',
            'client_secret': '************'
        }

        yield scrapy.Request(url='https://secure.alpsinc.com/oauth2/token', method="POST", body=urllib.urlencode(params))

    def parse(self, response):
        print("iicdcparsee")
        print(response.text)

        # revoke access token from response object. and set Header according to Yelp docs.
        bearer_token = json.loads(response.text)['access_token']
        print(beared_token)
        headers = {'Authorization': 'Bearer %s' % bearer_token}

    def dividends(self, response):
        items = response.meta['items']
        url_list= response.meta.get('url_list')
        print(url_list)
        print(response.text)

        #temp_data=re.findall("<html><head></head><body><pre .*?>(.*?)</pre></body></html",response.text)[0]
        json_data=json.loads(response.text)


        temp_ticker=json_data[0]['symbol']
        for item in items:
            if(item['nasdaq_ticker']==temp_ticker):
                dividend_history = []
                capital_gains_list = []
                for row in json_data:
                    data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                                  "record_date": "", "per_share": "", "reinvestment_price": ""}
                    data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                                  'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
                    if("exdate" in row):
                        data_dict1['ex_date']=row['exdate'].split("T")[0]
                    else:
                        data_dict1['ex_date']="-"
                    if("recorddate" in row):
                        data_dict1['record_date']=row['recorddate'].split("T")[0]
                    else:
                        data_dict1['record_date']="-"
                    if("payabledate" in row):
                        data_dict1['pay_date'] = row['payabledate'].split("T")[0]
                    else:
                        data_dict1['pay_date'] = "-"

                    if ("stcg" in row):
                        data_dict2['short_term_per_share'] = row['stcg']
                    else:
                        data_dict2['short_term_per_share'] = "-"
                    print("tetstinggngnnggng",row['stcg'])

                    if("ltcg" in row):
                        data_dict2['long_term_per_share'] = row['ltcg']
                    else:
                        data_dict2['long_term_per_share'] = "-"
                    if ("qdi" in row):
                        data_dict1['ordinary_income'] = row['qdi']
                    else:
                        data_dict2['ordinary_income'] = "-"
                    #print(data_dict1)
                    #print(data_dict2)
                    dividend_history.append(data_dict1)
                    capital_gains_list.append(data_dict2)
                    #print(capital_gains_list)
                item['dividends']=dividend_history
                item['capital_gains']=capital_gains_list
                #print(item['capital_gains'])
            #print(items)
        if(len(url_list)!=0):
            hit_url=url_list[0]
            print(len(url_list))
            print(hit_url)
            meta = response.meta
            meta['items'] = items
            meta['url_list']=url_list[1:]
            yield self.make_request(hit_url, callback=self.dividends, meta=meta,method=Statics.CRAWL_METHOD_SELENIUM,dont_filter=True)
        else:
            #print("noting")
            for i in items:
                yield self.generate_item(i, FinancialDetailItem)







'''


        for row in temp_rows:
            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "","record_date": "", "per_share": "", "reinvestment_price": ""}
            data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
            data_dict2["cg_ex_date"]=row.xpath(".//th[contains(@class,'fds-th-date')]//text()").extract_first()
            data_dict2["cg_record_date"]=row.xpath(".//td[contains(@class,'record')]//text()").extract_first()
            data_dict2["cg_pay_date"]=row.xpath(".//td[contains(@class,'payable')]//text()").extract_first()
            data_dict2["short_term_per_share"]=row.xpath(".//td[@class='fds-td-fund']//text()").extract_first()
            data_dict2["long_term_per_share"]=row.xpath(".//td[@class='fds-td-fund2']//text()").extract_first()
            data_dict2["ordinary_income"]=row.xpath(".//td[@class='fds-td-income']//text()").extract_first()
            dividend_history.append(data_dict1)
            capital_gains_list.append(data_dict2)
        for item in items:

            yield self.generate_item(item, FinancialDetailItem)
'''