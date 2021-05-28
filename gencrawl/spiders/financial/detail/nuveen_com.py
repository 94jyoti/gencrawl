from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse


class NuveenComDetail(FinancialDetailSpider):
    name = 'financial_detail_nuveen_com'
    #allowed_domains = ['api.nuveen.com','www.nuveen.com']
    
    def get_items_or_req(self, response, default_item={}):
        
        # request = []
        items = self.prepare_items(response, default_item)
        item=items[0]
        '''
        bench_mark = []
        for benchmark in range(len(temp_class_benchmark)-1):
            bench_mark.append(temp_class_benchmark[benchmark])
        item['benchmarks'] = bench_mark
        '''
        # for manager in item["fund_managers"]:
            # for key,value in manager.iteritems():
                # manager[key]=
        cusip_id=item['cusip']
        item['share_class']=item['fund_url'].split("=")[-1]
        fund_managers_list=[]
        
        for i in item['temp_fund_managers']:
        	data_dict={"fund_manager": "", "fund_manager_years_of_experience_in_industry": "", "fund_manager_firm": "","fund_manager_years_of_experience_with_fund": ""}
        	data_dict['fund_manager']=i.strip()
        	fund_managers_list.append(data_dict)
        	
        item['fund_managers']=fund_managers_list
        #print(item['share_class'])
        meta = response.meta
        meta['items'] = item
        api_url="https://api.nuveen.com/MF/ProductDetail/DistributionHistory/"+cusip_id
        #api_url="https://www.nuveen.com/en-us/mutual-funds"
        #print(api_url)
        item['api_url']=api_url
        r=self.make_request(api_url, callback=self.parse_performance_response, meta=meta)
        return r
        # request.append(r)
        #return response

    def parse_performance_response(self, response):
        #print('wdwaaaaaaaaaaaddddddddddddddddddddddddd')
        items = response.meta['items']
        response_json = json.loads(response.text)
        #print("reso.....................................",response_json)
        #historical_data = response_json['Distributions']
        #try:
        #items = items[0]
        #except:
         #   print("done")
        capital_gains_list = []
        dividend_history=[]
        for i in response_json:
            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "", "record_date": "", "per_share": "", "reinvestment_price": ""}
            data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
            data_dict1['qualified_income'] = None
            data_dict1['ex_date'] = i['exdivdt']
            data_dict1['record_date'] = i['rcrddt']
            data_dict1['pay_date'] = i['paydt'].split("T")[0]
            data_dict1['per_share'] = None
            data_dict1['reinvestment_price'] = None
            data_dict1['ordinary_income'] = i['ordinaryincome']
            dividend_history.append(data_dict1)
            data_dict2['long_term_per_share'] = i['longgain']
            data_dict2['cg_ex_date'] = i['exdivdt']
            data_dict2['cg_record_date'] = i['rcrddt']
            data_dict2['cg_pay_date'] = i['paydt'].split("T")[0]
            data_dict2['short_term_per_share'] = None
            data_dict2['total_per_share'] = None
            data_dict2['cg_reinvestment_price'] = None
            capital_gains_list.append(data_dict2)
        items['capital_gains'] = capital_gains_list
        items['dividends']=dividend_history
        
        
        
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
        #print("bvbvvvvvvvvvvvvvvvvvvvvvvv",items)
        yield self.generate_item(items, FinancialDetailItem)
