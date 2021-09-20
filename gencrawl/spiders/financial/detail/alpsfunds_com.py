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


class AlpsfundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_alpsfunds_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        url_list=[]
        for item in items:
            temp_ticker=item['nasdaq_ticker']
            url="https://www.alpsfunds.com/api/dbws/v1/distributions?identifier="+temp_ticker+"&limit=2000&_type=json"
            url_list.append(url)
            #item['capital_gains'] = []
            #item['dividends'] = []
        temp_rows=response.xpath("//table[contains(@summary,'distribution')]//tbody//tr")
        capital_gains_list = []
        dividend_history = []
        meta = response.meta
        meta['items'] = items
        hit_url=url_list[0]
        meta['url_list']=url_list[1:]
        yield self.make_request(hit_url, callback=self.dividends, meta=meta, method=Statics.CRAWL_METHOD_SELENIUM,dont_filter=True)

    def dividends(self, response):
        items = response.meta['items']
        url_list= response.meta.get('url_list')
        print(url_list)
        temp_data=re.findall("<html><head></head><body><pre .*?>(.*?)</pre></body></html",response.text)[0]
        json_data=json.loads(temp_data)
        temp_ticker=json_data['meta']['identifier']
        for item in items:
            if(item['nasdaq_ticker']==temp_ticker):
                dividend_history = []
                capital_gains_list = []
                for row in json_data['data']:
                    data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                                  "record_date": "", "per_share": "", "reinvestment_price": ""}
                    data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                                  'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
                    if("dividendPerShare" in row['dividend']):
                        data_dict1['ordinary_income']=row['dividend']['dividendPerShare']
                    else:
                        data_dict1['ordinary_income']="-"
                    if("exDivDate" in row['dividend']):
                        data_dict1['ex_date']=row['dividend']['exDivDate']
                    else:
                        data_dict1['ex_date']="-"
                    if("recordDate" in row['dividend']):
                        data_dict1['record_date'] = row['dividend']['recordDate']
                    else:
                        data_dict1['record_date'] = "-"

                    if ("payableDate" in row['dividend']):
                        data_dict1['pay_date'] = row['dividend']['payableDate']
                    else:
                        data_dict1['pay_date'] = "-"

                    if ("shortTermCapitalGain" in row['capitalGain']):
                        data_dict2['short_term_per_share'] = row['capitalGain']['shortTermCapitalGain']
                    else:
                        data_dict2['short_term_per_share'] = "-"
                    print("tetstinggngnnggng",row['capitalGain'])

                    if("longTermCapitalGain" in row['capitalGain']):
                        data_dict2['long_term_per_share'] = row['capitalGain']['longTermCapitalGain']
                    else:
                        data_dict2['long_term_per_share'] = "-"
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