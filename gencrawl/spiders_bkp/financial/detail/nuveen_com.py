from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse


class NuveenComDetail(FinancialDetailSpider):
    name = 'financial_detail_nuveen_com_us'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        item = items[0]
        print(items)
        cusip_id = item['cusip']
        print(cusip_id)
        item['share_class'] = item['fund_url'].split("=")[-1]
        fund_managers_list = []

        for i in item['temp_fund_managers']:
            data_dict = {"fund_manager": "", "fund_manager_years_of_experience_in_industry": "",
                         "fund_manager_firm": "", "fund_manager_years_of_experience_with_fund": "",
                         'fund_manager': i.strip()}
            fund_managers_list.append(data_dict)

        item['fund_managers'] = fund_managers_list
        # print(item['share_class'])
        meta = response.meta
        meta['items'] = item
        api_url = "https://api.nuveen.com/MF/ProductDetail/DistributionHistory/" +cusip_id
        item['api_url'] = api_url
        r = self.make_request(api_url, callback=self.parse_performance_response, meta=meta,dont_filter=True)
        return r

    def parse_performance_response(self, response):
        items = response.meta['items']
        response_json = json.loads(response.text)
        capital_gains_list = []
        dividend_history = []
        for i in response_json:
            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                          "record_date": "", "per_share": "", "reinvestment_price": ""}
            data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                          'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
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
        items['dividends'] = dividend_history
        yield self.generate_item(items, FinancialDetailItem)
