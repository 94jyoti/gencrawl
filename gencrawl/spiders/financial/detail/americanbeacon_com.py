from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd


class AmericanbeaconDetail(FinancialDetailSpider):
    name = 'financial_detail_americanbeacon_com'

    # allowed_domains = ['api.nuveen.com','www.nuveen.com']

    def get_items_or_req(self, response, default_item={}):

        parsed_items = []
        items = self.prepare_items(response, default_item)
        headers = response.xpath("//h3[contains(text(), 'TOTAL RETURNS')]/parent::div//tr[1]/th/text()").extract()
        cusip_index = str(headers.index('CUSIP'))
        #try:
        #	distribution=response.xpath("//strong[contains(text(), 'Distribution')]//parent::td//following-sibling::td//span//text()").extract()[0]
        #except:
        #	print("distribuyionnnnnnnnn not foiund")
        # return_data=item['temp_class_returns'][0]
        # print("itemdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",items)
        for i in items:
            i['average_weighted_maturity_as_of_date'] = i['effective_duration_date']
            i['sec_yield_without_waivers_date_30_day'] = i['effective_duration_date']
            i['sec_yield_date_30_day'] = i['effective_duration_date']
            temp_data_returns = i['class_returns']
            # print(temp_data_returns)
            temp_expense_ratio = i['class_expense_ratios']
            # temp_class_benchmark = i['class_benchmarks']
            temp_sec_30 = i['sec_30']
            temp_fund_manager_list = i['temp_fund_managers']
            # print(temp_sec_30)
            count = 1
            #response_1=response.replace(body=response.body.replace(b'<br>', b' ').replace(b'\n',b' ').replace(b'"',b''))
            fund_manager = response.xpath("//strong[contains(text(), 'Portfolio  Manager')]//parent::p//following-sibling::ul[position()=1]//li").extract()
            print(fund_manager)
            fund_managers_list = []
            for fund in fund_manager:
                fund=fund.replace('<li>','').replace('<br>','').replace('</li>','')
                print("fundddd", fund)
                dict = {"fund_manager": "", "fund_manager_years_of_experience_in_industry": "", "fund_manager_firm": "",
                        "fund_manager_years_of_experience_with_fund": ""}
                dict['fund_manager'] = str(fund.split(";")[0]).split(",")[0]
                dict['fund_manager_years_of_experience_in_industry'] = "since " + str(fund.split(" ")[-1])
                fund_managers_list.append(dict)
            print(fund_managers_list)
            i['fund_managers'] = fund_managers_list
            for data in temp_data_returns:
                for j in data:
                    if (i['share_class'] == data['share_class_1'].split(" ")[0].strip()):
                        i['share_inception_date'] = data['inception_date']
                        if (cusip_index == "2"):
                            i['cusip'] = str(data['cusip'])
                        elif (cusip_index == "3"):
                            i['cusip'] = str(data['cusip_1'])
                        # print('cusipsppspspspspspspspspspspspsspspsppsppsppspsp',i['cusip'])
                for expense in temp_expense_ratio:
                    for ex in expense:
                        if (i['share_class'] == expense['expense_ratios_share_class']):
                            i['total_expense_gross'] = expense['expense_ratios_gross']
                            i['total_expense_net'] = expense['expense_ratios_net']

                # print("mqinqmqiqiqiiqiqiqqiiqiqiqqiqiqiqiiqiqiqi",i['investment_strategy'])
                # for invest in i['investment_strategy']:
                # investment=" ".join(i['investment_strategy'])
                # print("inecsudtmentntttntntntnntntntnt",investment)
                # i['investment_strategy']=investment
                '''
                bench_mark = []

                for benchmark in temp_class_benchmark:
                    bench_mark.append(benchmark['benchmarks'])
                i['benchmarks'] = bench_mark
                '''
                # print("secccccccccccfeferferfefef",i[temp_sec_30])
                for sec in temp_sec_30:
                    for s in sec:
                        print("sec;;;;;;;;;;;[[[[[[[[[[[[]]]]]]]]]]]]", sec)
                        if (i['share_class'] == sec['sec_30_share_class']):
                            i['sec_yield_30_day'] = sec['sec_30_actual']
                            i['sec_yield_without_waivers_30_day'] = sec['sec_30_unsubsized']
                        # print()
                        if ("Distribution" in sec['sec_30_share_class']):
                            print(type(sec['sec_30_actual']))
                            print("insideeeeeeeeeeeeeeeeeee")
                            if (len(sec['sec_30_actual']) != 0):
                                i['distribution_frequency'] = sec['sec_30_actual']
                                print(i['distribution_frequency'])
                            elif(len(sec['sec_30_unsubsized']) != 0):
                                i['distribution_frequency'] = sec['sec_30_unsubsized']
                                print(i['distribution_frequency'])
                        else:
                            try:
                                i['distribution_frequency'] =response.xpath("//strong[contains(text(), 'Distribution')]//parent::td//following-sibling::td//span//text()").extract()[0]
                                print("after second if    ")
                            except:
                                i['distribution_frequency']=""
            parsed_items.append(self.generate_item(i, FinancialDetailItem))
        return parsed_items