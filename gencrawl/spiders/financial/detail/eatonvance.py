from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
import re


class EatonvanceComDetail(FinancialDetailSpider):
    name = 'financial_detail_eatonvance_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        item = items[0]
        # item['share_class'] = item['fund_url'].split("=")[-1]
        #file=open("eatonjson.html","w")
        #file.write(response.text)
        #file.close()
        fund_managers_list = []
        fund_managers_temp = item['temp_fund_managers']
        data_dict = {"fund_manager": "", "fund_manager_years_of_experience_in_industry": "", "fund_manager_firm": "",
                     "fund_manager_years_of_experience_with_fund": ""}
        # print("dddddddd",item['benchmarks'])
        # item['benchmarks']=list(item['benchmarks'].split("@"))
        print("benchmarks-------------------------------------",item['temp_benchmark'])
        benchmarks=[]
        benchmark_temp=item['temp_benchmark']
        for i in benchmark_temp:
        	data=re.findall('<td style=.*?>(.*?)<span .*?>(.*?)<sup.*?</td>',i)
        	print(data)
        
        portfolio=item['temp_assets']
        if(len(portfolio)==2):
        	item['total_net_assets']=portfolio[0]
        	item['portfolio_assets']=portfolio[1]
        elif(len(portfolio)==1):
        	item['total_net_assets']=portfolio[0]
        else:
        	item['portfolio_assets']=response.xpath("//td[contains(text(),'Total Net ')]//following-sibling::td//text()").extract()[0]
        for i in range(len(fund_managers_temp)):
            if (i % 2 == 0):
                data_dict['fund_manager'] = fund_managers_temp[i].strip()
            else:
                data_dict['fund_manager_years_of_experience_with_fund'] = fund_managers_temp[i]
                fund_managers_list.append(data_dict)
        item['fund_managers'] = fund_managers_list
        capital_gain_temp_list = []
        capital_gain_list = []
        capital_gain_temp = item['temp_capital_gain']
        print("fsdfs;lfmsfsf", capital_gain_temp)
        capital_data_dict = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                             'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
        for i in capital_gain_temp:
            capital_gain_temp_list.append(re.findall('<td style=.*?>(.*?)</td>', i)[0])
        print("capitaklllll", capital_gain_temp_list)
        for capital in range(0, len(capital_gain_temp), 4):
            capital_data_dict['cg_ex_date'] = capital_gain_temp[capital]
            capital_data_dict['short_term_per_share'] = capital_gain_temp[capital + 1]
            capital_data_dict['long_term_per_share'] = capital_gain_temp[capital + 2]
            capital_data_dict['cg_reinvestment_price'] = capital_gain_temp[capital + 3]
            capital_gain_list.append(capital_data_dict)
            print("capitaaaaaaaall.......................", capital)
        # print(capital_gain_list)
        print("fund_urllllllll", item['fund_url'])
        if (len(capital_gain_list) != 0):
            item['capital_gains'] = capital_gain_list
        meta = response.meta
        meta['items'] = item
        try:
            # api_url ='https://funds.eatonvance.com/'+response.xpath('//table[@name="DIVIDENDHISTORY"]//tfoot//*[contains(text(),"View All")]//@href').extract()[0]
            api_url = "https://funds.eatonvance.com/includes/view-all.php?symbol=" + item['nasdaq_ticker'] + "&code=10"
            print("cnldnckldncklnnnnlll")
            item['api_url'] = api_url
            # https://funds.eatonvance.com/includes/view-all.php?symbol=EIGIX&code=10
            print(api_url)
            return self.make_request(api_url, callback=self.parse_performance_response, meta=meta)
        # request.append(r)
        # return r
        except:
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            return self.generate_item(item, FinancialDetailItem)
        # return response

    def parse_performance_response(self, response):
        print('wdwaaaaaaaaaaaddddddddddddddddddddddddd')
        items = response.meta['items']
        distribution_history = response.xpath('//tr[@class="tableView"]//td//text()').extract()
        print(distribution_history)
        # file = open("jsonnuveen.txt", "w")
        # file.write(response.text)
        # file.close()
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
        for dis in range(0, len(distribution_history), 3):
            data_dict1['ex_date'] = distribution_history[dis]
            data_dict1['reinvestment_price'] = distribution_history[dis + 2]
            data_dict1['ordinary_income'] = distribution_history[dis + 1]
            dividend_history.append(data_dict1)
        # items['capital_gains'] = capital_gains_list
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
