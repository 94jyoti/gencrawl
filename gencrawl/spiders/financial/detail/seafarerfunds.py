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


class SeafarefundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_seafarefunds_com'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        #print(response.text)
        file=open("diercxion.html","w")
        file.write(response.text)
        file.close()
        meta = response.meta
        meta['items'] = items
        for item in items:
            print("sometognffff wrong")
            hit_url="https://www.seafarerfunds.com/data/distributions?"+item['nasdaq_ticker']
            print(hit_url)
            yield self.make_request(hit_url, callback=self.parse_dividends, meta=meta,method=Statics.CRAWL_METHOD_GET, dont_filter=True)

    def parse_dividends(self, response):
        items = response.meta['items']
        file = open("diercxion.html", "w")
        file.write(response.text)
        file.close()
        for item in items:
            temp_ticker=response.xpath('//h1[contains(text(),"Distributions")]//text()').extract()[0]
            if(item['nasdaq_ticker']==temp_ticker.replace("Distributions","").replace("(","").replace(")","").strip()):
                print("isnide if")
                capital_gain_list=[]
                dividend_list=[]
                temp_ticker=item['nasdaq_ticker']
                temp_data=response.xpath('//table//tbody//tr')
                for row in temp_data:
                    data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "","record_date": "", "per_share": "", "reinvestment_price": ""}
                    data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
                    data_dict1['ex_date']=row.xpath(".//td[1]//text()").extract_first()
                    data_dict1['reinvestment_price']=row.xpath(".//td[2]/text()").extract_first()
                    data_dict1['ordinary_income']=row.xpath(".//td[3]/text()").extract_first()
                    data_dict2['short_term_per_share']=row.xpath(".//td[4]/text()").extract_first()
                    data_dict2['long_term_per_share'] = row.xpath(".//td[5]/text()").extract_first()
                    data_dict2['total_per_share']=row.xpath(".//td[6]/text()").extract_first()
                    data_dict1['per_share']=row.xpath(".//td[7]//text()").extract_first()
                    capital_gain_list.append(data_dict2)
                    dividend_list.append(data_dict1)
                item['capital_gains']=capital_gain_list
                item['dividends']=dividend_list
                yield self.generate_item(item, FinancialDetailItem)



