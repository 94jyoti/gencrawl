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
        print("itemdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",item)
        
        # for manager in item["fund_managers"]:
            # for key,value in manager.iteritems():
                # manager[key]=
        cusip_id=item['cusip']
        meta = response.meta
        meta['items'] = item
        api_url="https://api.nuveen.com/MF/ProductDetail/DistributionHistory/"+cusip_id
        #api_url="https://www.nuveen.com/en-us/mutual-funds"
        print(api_url)
        item['api_url']=api_url
        r=self.make_request(api_url, callback=self.parse_performance_response, meta=meta)
        return r
        # request.append(r)
        #return response

    def parse_performance_response(self, response):
        print('wdwaaaaaaaaaaaddddddddddddddddddddddddd')
        items = response.meta['items']
        response_json = json.loads(response.text)
        #print("reso.....................................",response_json)
        #historical_data = response_json['Distributions']
        #try:
        #items = items[0]
        #except:
         #   print("done")
        capital_gains_list = []
        for i in response_json:
            data_dict = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                         'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': "","ordinary_income":""}
            data_dict['long_term_per_share'] = None
            data_dict['cg_ex_date'] = i['exdivdt']
            data_dict['cg_record_date'] = i['rcrddt']
            data_dict['cg_pay_date'] = i['paydt']
            data_dict['short_term_per_share'] = None
            data_dict['total_per_share'] = None
            data_dict['cg_reinvestment_price'] = None
            data_dict['ordinary_income'] = None
            capital_gains_list.append(data_dict)
 
        items['capital_gains'] = capital_gains_list
        print("bvbvvvvvvvvvvvvvvvvvvvvvvv",items)
        yield self.generate_item(items, FinancialDetailItem)
