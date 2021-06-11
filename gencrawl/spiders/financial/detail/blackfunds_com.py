from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse


class NuveenComDetail(FinancialDetailSpider):
    name = 'financial_detail_black_funds_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        item = items[0]

        # https://www.blackrock.com/us/individual/products/227557/blackrock-high-yield-bondinstitutional-class-fund/1464253357804.ajax?tab=distributions&fileType=json&subtab=all.table
       # print("rdwydvwcbskjcbsckl", response.xpath('//*[@id="distroAllTable"]//@data-ajaxuri').extract()[0])
        api_url = "https://www.blackrock.com" + response.xpath('//*[@class="fund-component"]//@data-ajaxuri').extract()[
            0]+"&subtab=all.table"
        print(api_url)
        # https://www.blackrock.com/us/individual/products/298415/fund/1464253357804.ajax?tab=distributions&fileType=json&subtab=table
        meta = response.meta
        meta['items'] = item
        # api_url = "https://api.nuveen.com/MF/ProductDetail/DistributionHistory/" + cusip_id
        item['api_url'] = api_url
        r = self.make_request(api_url, callback=self.parse_performance_response, meta=meta)
        return r

    def parse_performance_response(self, response):
        print("inside")
        print(response.text)
        items = response.meta['items']
        response_json = json.loads(response.text)
        capital_gains_list = []
        dividend_history = []
        print(response.text=="{}")
        '''
        if (response.text =="{}"):
            api_url = "https://www.blackrock.com"+response.xpath('//*[@id="distroAllTable"]//@data-ajaxuri').extract()[0]
            meta = response.meta
            meta['items'] = item
            r = self.make_request(api_url, callback=self.parse_performance_response1, meta=meta)
'''
        for i in response_json['all.table']['aaData']:
                
            print(i[0]['display'])
            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                              "record_date": "", "per_share": "", "reinvestment_price": ""}
            data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                              'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
            data_dict1['record_date'] = i[0]['display']
            data_dict1['ex_date'] = i[2]['display']
            data_dict1['per_share'] = i[3]['display']
            data_dict1['pay_date'] = i[1]['display']
            data_dict1['ordinary_income'] = i[4]['display']
            dividend_history.append(data_dict1)
            data_dict2['long_term_per_share'] = i[6]['display']
            data_dict2['cg_ex_date'] = i[2]['display']
            data_dict2['cg_record_date'] = i[0]['display']
            data_dict2['short_term_per_share'] = i[5]['display']
            data_dict2['total_per_share'] = i[3]['display']
            data_dict2['cg_pay_date'] = i[1]['display']
            capital_gains_list.append(data_dict2)

        items['capital_gains'] = capital_gains_list
        items['dividends'] = dividend_history
        yield self.generate_item(items, FinancialDetailItem)

'''
    def parse_performance_response1(self, response):
        print("inside1")


        print(response.text)
        items = response.meta['items']
        response_json = json.loads(response.text)
        capital_gains_list = []
        dividend_history = []

        for i in response_json['table']['aaData']:
            print(i[0]['display'])
            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                          "record_date": "", "per_share": "", "reinvestment_price": ""}
            data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                          'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
            data_dict1['record_date'] = i[0]['display']
            data_dict1['ex_date'] = i[2]['display']
            data_dict1['per_share'] = i[3]['display']
            data_dict1['pay_date'] = i[1]['display']
            data_dict1['ordinary_income'] = i[4]['display']
            dividend_history.append(data_dict1)
            data_dict2['long_term_per_share'] = i[6]['display']
            data_dict2['cg_ex_date'] = i[2]['display']
            data_dict2['cg_record_date'] = i[0]['display']
            data_dict2['short_term_per_share'] = i[5]['display']
            data_dict2['total_per_share'] = i[3]['display']
            data_dict2['cg_pay_date'] = i[1]['display']
            capital_gains_list.append(data_dict2)
        items['capital_gains'] = capital_gains_list
        items['dividends'] = dividend_history
        yield self.generate_item(items, FinancialDetailItem)
        
        '''