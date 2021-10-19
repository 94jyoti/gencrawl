from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import json
import pandas as pd
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from copy import deepcopy


class FeimComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_feim_com'
    custom_settings = {
        "RETRY_TIMES": 5,
        "CRAWLERA_ENABLED": True,
        "COOKIES_ENABLED": True,
        "COOKIES_DEBUG": True
    }

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        file = open("fiemtetstsststt"
                    ".html", "w")
        file.write(response.text)
        file.close()
        temp_items = []
        data = re.findall('Drupal\.settings,(.*?)></script>', response.text.replace("\n", ""))[0].replace(
            ");//--><!]]", "")
        json_data = json.loads(data)
        print(data)

        '''

        for item in items:
            if (item['minimum_initial_investment'] == []):
                temp_investment = response.xpath('//td[contains(text(),"Minimum Investment")]/text()').extract()
                temp_investment = [i.replace("Minimum Investment - Class", '').strip() for i in temp_investment]
                counter = -1

                for item_invest in temp_investment:
                    counter = counter + 1
                    print(item_invest)
                    print(item['share_class'])
                    if (item['share_class'] in item_invest):
                        item['minimum_initial_investment'] = response.xpath(
                            '//td[contains(text(),"Minimum Investment")]/following-sibling::td//text()').extract()[
                            counter]
            # minimum addition investment
            if (item['minimum_additional_investment'] == []):
                temp_min_investment = response.xpath('//td[contains(text(),"Subsequent Investment")]/text()').extract()
                temp_min_investment = [i.replace("Subsequent Investment - Class", '').strip() for i in
                                       temp_min_investment]
                counter = -1
                for item_invest in temp_min_investment:
                    counter = counter + 1
                    if (item['share_class'] in item_invest):
                        item['minimum_additional_investment'] = response.xpath(
                            '//td[contains(text(),"Subsequent Investment")]/following-sibling::td//text()').extract()[
                            counter]

        '''

        print("lebthgghghgghgh", len(items))

        node_value = list(json_data['charts'])[-1]
        print("here i am ")
        distribution_data = json_data['charts'][node_value]
        ticker_list = []
        for ticker in distribution_data['data_info']['legends'].keys():
            ticker_list.append(ticker)

        try:
            for ticker in ticker_list:
                ticker_value=distribution_data['data_info']['legends'][ticker]['legend']
                items[0]['nasdaq_ticker'] = ticker_value
                print(ticker_value)

                temp_items.append(deepcopy(items[0]))
        except:
            for i in items:
                yield self.generate_item(i, FinancialDetailItem)

        #print(ti  cker_list)
        for item in range(len(temp_items)):
            print("isnide first for loop")
            dict_key = ticker_list[item]
            print(dict_key)
            capital_gain_list = []

            dividend_list = []
            cg_data = distribution_data['data_info']['data'][dict_key]
            if ("Dividend" in json_data['charts'][node_value]['data_info']['chart_title']):
                for data in cg_data.values():
                    for k in data.values():
                        data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                                      "record_date": "", "per_share": "", "reinvestment_price": ""}
                        data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "",
                                      'cg_pay_date': "", 'short_term_per_share': "", 'total_per_share': "",
                                      'cg_reinvestment_price': ""}
                        data_dict1['record_date'] = k['column_0']
                        data_dict1['ex_date'] = k['column_2']
                        data_dict1['pay_date'] = k['column_4']
                        # cg_reinvestmentprice-ordinary income
                        data_dict1['per_share'] = k['column_5']
                        data_dict1['reinvestment_price'] = k['column_6']
                        #capital_gain_list.append(data_dict2)

                        dividend_list.append(data_dict1)
            if ("Capital" in json_data['charts'][node_value]['data_info']['chart_title']):
                # print("isnide capital")
                for i in cg_data.values():
                    for j in i.values():
                        print("kcsdkcndkcskncsdkcds",j)
                        data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                                      "record_date": "", "per_share": "", "reinvestment_price": ""}
                        data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "",
                                      'cg_pay_date': "", 'short_term_per_share': "", 'total_per_share': "",
                                      'cg_reinvestment_price': ""}
                        data_dict2['cg_record_date'] = j['column_0']
                        data_dict2['cg_ex_date'] = j['column_1']
                        data_dict2['cg_pay_date'] = j['column_2']
                        # cg_reinvestmentprice-ordinary income
                        #map to income
                        data_dict2['cg_reinvestment_price'] = j['column_3']
                        data_dict2['short_term_per_share'] = j['column_4']
                        data_dict2['long_term_per_share'] = j['column_5']
                        try:

                            data_dict2['total_per_share'] = j['column_7']
                        except:
                            pass
                        # print(capital_gain_list)
                        capital_gain_list.append(data_dict2)
                        #dividend_list.append(data_dict1)
            temp_items[item]['capital_gains'] = capital_gain_list
            temp_items[item]['dividends'] = dividend_list

        try:
            node_value1 = list(json_data['charts'])[-2]
            distribution_data1 = json_data['charts'][node_value1]
            ticker_list = []
            for ticker in distribution_data1['data_info']['legends'].keys():
                ticker_list.append(ticker)
            print("for secind node", ticker_list)
            for item in range(len(temp_items)):
                dict_key = ticker_list[item]
                print(dict_key)
                capital_gain_list = []
                dividend_list = []
                cg_data = distribution_data1['data_info']['data'][dict_key]
                # print(cg_data)
                if ("Dividend" in json_data['charts'][node_value1]['data_info']['chart_title']):
                    for data in cg_data.values():
                        # print("second node inside first for")
                        for k in data.values():
                            # print("inside seconf for second node")
                            # print(k)
                            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                                          "record_date": "", "per_share": "", "reinvestment_price": ""}
                            data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "",
                                          'cg_pay_date': "", 'short_term_per_share': "", 'total_per_share': "",
                                          'cg_reinvestment_price': ""}
                            data_dict1['record_date'] = k['column_0']
                            data_dict1['ex_date'] = k['column_2']
                            data_dict1['pay_date'] = k['column_4']
                            # cg_reinvestmentprice-ordinary income
                            data_dict1['per_share'] = k['column_5']
                            data_dict1['reinvestment_price'] = k['column_6']
                            #print("divideendndn",)

                            #temp_items[item]['capital_gains'].append(data_dict2)
                            temp_items[item]['dividends'].append(data_dict1)

        except Exception as e:
            print(e)


       #
        for item in temp_items:
            yield self.generate_item(item, FinancialDetailItem)
