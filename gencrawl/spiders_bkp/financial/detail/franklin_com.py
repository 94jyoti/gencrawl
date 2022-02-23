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
from lxml import etree
# import platform
import re
# print(platform.python_version())
from bs4 import BeautifulSoup


class FranklinliveDetail(FinancialDetailSpider):
    name = 'financial_detail_franklin_com'

    def get_items_or_req(self, response, default_item={}):
        parsed_items = []
        items = self.prepare_items(response, default_item)
        url_1 = "https://www.franklintempleton.com" + \
                response.xpath("//a[contains(text(),'Portfolio')]/@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        return self.make_request(url_1, callback=self.portfolio, meta=meta, dont_filter=True)

    def portfolio(self, response):
        items = response.meta['items']
        item = items[0]
        strategy = []
        for i in range(2,len(item['temp_investment_strategyyy'])):
            strategy.append(item['temp_investment_strategyyy'][i]	.replace("\n","").replace("<li>","").replace("</li>","").replace("<b>","").replace("</b>",""))
        item['investment_strategy'] = " ".join(strategy)
        try:
            item['average_duration'] = \
                response.xpath('//th[contains(text(),"Average Duration")]//following-sibling::td//b//text()').extract()[
                    0]

            item['average_duration_as_of_date'] = \
                ("".join(response.xpath('//th[contains(text(),"Average Duration")]//small//text()').extract())).split(
                    "(")[
                    0].strip()
        except:
            print("inside except")
        try:
            item['average_weighted_maturity'] = response.xpath(
                '//th[contains(text(),"Average Weighted Maturity")]//following-sibling::td//b//text()').extract()[0]
            item['average_weighted_maturity_as_of_date'] = \
                ("".join(response.xpath(
                    "//th[contains(text(),'Average Weighted Maturity')]//small//text()").extract())).split("(")[
                    0].strip()
        except:
            print("inside except")
        item['portfolio_assets'] = "".join(
            response.xpath("//th[contains(text(),'Total Fund Assets')]//following-sibling::td//b//text()").extract())
        item['portfolio_assets_date'] = \
            ("".join(response.xpath("//th[contains(text(),'Total Fund Assets')]//small//text()").extract())).split("(")[
                0].strip()
        item['total_net_assets'] = "".join(
            response.xpath("//th[contains(text(),'Net Assets')]//following-sibling::td//b//text()").extract())
        item['total_net_assets_date'] = \
            ("".join(response.xpath("//th[contains(text(),'Net Assets')]//small//text()").extract())).split("(")[
                0].strip()
        url_2 = "https://www.franklintempleton.com" + \
                response.xpath("//a[contains(text(),'Performance')]/@href").extract()[0]
        meta = response.meta
        meta['items'] = item
        yield self.make_request(url_2, callback=self.performance, meta=meta, dont_filter=True)

    def performance(self, response):
        items = response.meta['items']
        items['benchmarks'] = response.xpath(
            "//h3[contains(text(),'Benchmarks')]/following-sibling::ul//li//benchmarkname//text()").extract()
        url_3 = "https://www.franklintempleton.com" + \
                response.xpath("//a[contains(text(),'Distributions')]/@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        return self.make_request(url_3, callback=self.distributions, meta=meta, dont_filter=True)
        '''
    
        url_3 = "https://www.franklintempleton.com" + \
                response.xpath("//a[contains(text(),'Tax Info')]/@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        # print(urls)
        items['url_3'] = url_3
        # yield self.generate_item(items, FinancialDetailItem)
        # print(items)
        # yield self.generate_item(items, FinancialDetailItem)
        return self.make_request(url_3, callback=self.tax_info, meta=meta, dont_filter=True)
        '''
    def distributions(self, response):
        items = response.meta['items']
        file = open('response3.html', 'w')
        file.write(response.text)
        file.close()
        items['dividend_frequency'] = response.xpath(
            '//th[contains(text(),"Dividend Distributions")]//following-sibling::td//b//text()').extract_first()
        try:
            print("inside tryryyyy")
            temp_year = response.xpath(
                '//h3[contains(text(),"Year-to-Date Distributions Per Share")]//small//datetodayus//text()').extract()[
                0]
            year = temp_year.split("/")[-1]
            distributions_data = response.xpath("//table[@class='table table-grouped distributions-ytd-table']").extract()[0]
            dividend_history_list = []
            distributions_table = pd.read_html(distributions_data)
            for index, row in distributions_table[0].iterrows():
                data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                              "record_date": "", "per_share": "", "reinvestment_price": ""}
                index1 = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61, 64, 67, 70,73,76, 79, 82]
                if (index in index1):
                    data_dict1['ex_date'] = row['Ex-Date']+ " "+str(year)
                    print("clnclcncnclkkc", row['Ex-Date'])
                    data_dict1['record_date'] = row['Record Date']+" "+str(year)
                    data_dict1['pay_date'] = row['Payable Date']+" "+str(year)
                    data_dict1['per_share'] = row['Amount ($)']
                    data_dict1['reinvestment_price'] = row['Reinvestment Price ($)']

                    dividend_history_list.append(data_dict1)
                else:
                    continue
                for i in dividend_history_list:
                    if(i['per_share']=="0.0000-0.0000"):
                    	del dividend_history_list[-1]
                    	break
                    if(i['reinvestment_price']=="TBD"):
                    	del dividend_history_list[-1]
                    	break
            items['dividends'] = dividend_history_list
        except:
            print("inside except")
        url_3 = "https://www.franklintempleton.com" + \
                response.xpath("//a[contains(text(),'Tax Info')]/@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        items['url_3'] = url_3
        yield self.generate_item(items, FinancialDetailItem)

    def tax_info(self, response):
        print("444444444444444")
        items = response.meta['items']
        years = response.xpath("//select[@id='tax-year']//option//text()").extract()
        url_list = []
        for i in years:
            url_list.append(items['url_3'] + "?taxYear=" + str(i))
        meta = response.meta
        url_1 = url_list[0]
        url_list.pop(0)
        final_year = str(url_1).split("=")[-1]
        items['urls'] = url_list
        items['final_year'] = final_year
        items['flag'] = 1
        meta['items'] = items
        return self.make_request(url_1, callback=self.distribution_history, meta=meta, dont_filter=True)

    def distribution_history(self, response):
        items = response.meta['items']
        distributions_data = \
            response.xpath('//strong[contains(text(),"DISTRIBUTIONS (PER SHARE)")]/following::div[1]//table').extract()[
                0]
        count = 0
        if (items['flag'] == 1):
            items['capital_gains'] = []
            items['dividends'] = []
            items['flag'] = 0
        capital_gain_table = pd.read_html(distributions_data)
        capital_gain_final = capital_gain_table[0].to_dict('dict')
        for index, row in capital_gain_table[0].iterrows():
            data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                          'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                          "record_date": "", "per_share": "", "reinvestment_price": ""}
            try:
                data_dict2['cg_record_date'] = row['Record Date']+ " " + items['final_year']
                data_dict1['record_date'] = row['Record Date']+ " " + items['final_year']
            except:
                print("2")
            try:
                data_dict2['cg_pay_date'] = row['Pay Date'] + " " + items['final_year']
                data_dict1['pay_date'] = row['Pay Date'] + " " + items['final_year']
            except:
                print("3")
            try:
                data_dict2['total_per_share'] = row['Total Distributions ($)']
                
                data_dict1['per_share'] = row['Total Distributions ($)']
            except:
                print("4")
            try:
            	data_dict1['ordinary_income'] = row['Ordinary Dividends ($) [further-information]  Close  Ordinary Dividends represent dividends paid by a fund that are derived from interest, dividends, net short-term capital gains and other types of ordinary income earned by the fund. For a fund that elects to pass through its foreign taxes paid (a non-cash item), a shareholder\'s allotted share of foreign taxes has been added to the Ordinary Dividend cash distributions received by the shareholder. This information is reported on the box labeled Ordinary Dividends on Form 1099-DIV.']
            	print('ordinalry income',data_dict1['ordinary_income'])
            except:
            	print("5")
            try:
            	data_dict1['qualified_income'] =row['Qualified Dividend Income ($) [further-information]  Close  This amount reflects the portion of a fund\'s distribution of Ordinary Dividends that may be eligible for a reduced capital gain tax rate. To be eligible for the lower tax rates, certain holding periods apply, and shareholders should consult their tax advisor to determine the amount eligible for the reduced rate. This amount represents both cash distributions and non-cash amounts, such as foreign taxes paid, that have been allocated to shareholders. This information is reported on the Form 1099-DIV in the box labeled Qualified Dividends.']
            except:
            	print("6")
            try:
                data_dict2['long_term_per_share'] = row['Long-Term Cap Gains ($)']
            except:
                print("7")
            items['capital_gains'].append(data_dict2)
            items['dividends'].append(data_dict1)
        try:
            del items['capital_gains'][-1]
            del items['dividends'][-1]
        except:
            print("inside except")
        if (len(items['urls']) == 0):
            yield self.generate_item(items, FinancialDetailItem)

        else:
            url_1 = items['urls'][0]
            final_year = str(url_1).split("=")[-1]
            items['urls'].pop(0)
            items['final_year'] = final_year
            meta = response.meta
            meta['items'] = items
            yield self.make_request(url_1, callback=self.distribution_history, meta=meta, dont_filter=True)

