from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse


class EatonvanceComDetail(FinancialDetailSpider):
    name = 'financial_detail_eatonvance_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        item = items[0]
        #item['share_class'] = item['fund_url'].split("=")[-1]
        fund_managers_list = []
        fund_managers_temp = item['temp_fund_managers']
        data_dict = {"fund_manager": "", "fund_manager_years_of_experience_in_industry": "", "fund_manager_firm": "",
                     "fund_manager_years_of_experience_with_fund": ""}
        #print("sharreeeee..............--------------------------",item['share_class'])
        for i in range(len(fund_managers_temp)):
            if (i % 2 == 0):
                data_dict['fund_manager'] = fund_managers_temp[i].strip()
            else:
                data_dict['fund_manager_years_of_experience_with_fund'] = fund_managers_temp[i]
                fund_managers_list.append(data_dict)
        item['fund_managers'] = fund_managers_list
        capital_gain_list = []
        capital_gain_temp = item['temp_capital_gain']
        #print(capital_gain_temp)
        capital_data_dict = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                             'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
        for capital in range(0, len(capital_gain_temp), 4):
            capital_data_dict['cg_ex_date'] = capital_gain_temp[capital]
            capital_data_dict['short_term_per_share'] = capital_gain_temp[capital + 1]
            capital_data_dict['long_term_per_share'] = capital_gain_temp[capital + 2]
            capital_data_dict['cg_reinvestment_price'] = capital_gain_temp[capital + 3]
            capital_gain_list.append(capital_data_dict)
            print("capitaaaaaaaall.......................", capital)
        #print(capital_gain_list)
        meta = response.meta
        meta['items'] = item
        api_url ='https://funds.eatonvance.com/'+response.xpath('//table[@name="DIVIDENDHISTORY"]//tfoot//*[contains(text(),"View All")]//@href').extract()[0]
        print("cnldnckldncklnnnnlll")
        item['api_url'] = api_url
        r=self.make_request(api_url, callback=self.parse_performance_response, meta=meta)
        #request.append(r)
        return r
        # return response

    def parse_performance_response(self, response):
        print('wdwaaaaaaaaaaaddddddddddddddddddddddddd')
        items = response.meta['items']
        distribution_history=response.xpath('//tr[@class="tableView"]//td//text()').extract()
        print(distribution_history)
        #file = open("jsonnuveen.txt", "w")
        #file.write(response.text)
        #file.close()
        file = open("eaton.txt", "w")
        file.write(response.text)
        file.close()
        # print("reso.....................................",response_json)
        # historical_data = response_json['Distributions']
        # try:
        # items = items[0]
        # except:
        #   print("done")
        
        capital_gains_list = []
        dividend_history = []
        data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                          "record_date": "", "per_share": "", "reinvestment_price": ""}
        for dis in range(0,len(distribution_history),3):
            data_dict1['ex_date'] = distribution_history[dis]
            data_dict1['reinvestment_price'] = distribution_history[dis+2]
            data_dict1['ordinary_income'] = distribution_history[dis+1]
            dividend_history.append(data_dict1)
        #items['capital_gains'] = capital_gains_list
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
