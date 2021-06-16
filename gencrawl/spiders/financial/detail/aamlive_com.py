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


class AamliveDetail(FinancialDetailSpider):
    name = 'financial_detail_aamlive_com'

    def get_items_or_req(self, response, default_item={}):

        parsed_items = []
        items = self.prepare_items(response, default_item)

        file = open('response.html', 'w')
        file.write(response.text)
        file.close()
        url_1 = "https://www.aamlive.com/" + response.xpath("//a[contains(text(),'Fees & Expenses')]/@href").extract()[0]
        print("urllllllll", url_1)
        meta = response.meta
        meta['items'] = items
        return self.make_request(url_1, callback=self.feesandexpenses, meta=meta, dont_filter=True)

    def feesandexpenses(self, response):
        items = response.meta['items']
        # print(items)
        file = open('response1.html', 'w')
        file.write(response.text)
        file.close()
        share_holder_temp = response.xpath('//strong[contains(text(),"Shareholder Fees")]/following::table[1]').extract()[0]
        shareholder_table = pd.read_html(share_holder_temp)
        final_shareholder = shareholder_table[0].set_index('Unnamed: 0').to_dict('dict')
        t = response.xpath('//strong[contains(text(),"Annual Fund Operating Expense")]/following::table[1]').extract()[0]
        expenses = pd.read_html(t)
        print(final_shareholder)

        final_expenses = expenses[0].set_index('Unnamed: 0').to_dict('dict')
        print(final_expenses)
        for item in items:
            print(item['share_class'].strip())
            for key in final_expenses:
                print("cndncdcn", key.replace('Share', ''))
                # print("dcdcdkn",item['share_class'].strip().replace('\xa0','')==key.replace('Share','').strip() )
                if (item['share_class'].strip().replace('\xa0', '') == key.replace('Share', '').strip()):
                    item['annual_fund_operating_expenses_after_fee_waiver'] = final_expenses[key][
                        'Total annual fund operating expenses after fee waiver and/or expense reimbursements']
                    item['fees_total_12b_1'] = final_expenses[key]['Distribution (Rule 12b-1) Fee']
                    item['other_expenses'] = final_expenses[key]['Other Expenses']
                    item['management_fee'] = final_expenses[key]['Management Fees']
                    item['shareholder_service_fees'] = final_expenses[key]['Shareholder Service Fees']
                    break
            for key in final_shareholder:
                if (item['share_class'].strip().replace('\xa0', '') == key.replace('Share', '').strip()):
                    item['deferred_sales_charge'] = final_shareholder[key]['Maximum deferred sales charge (load)  1']
                    item['redemption_fee'] = final_shareholder[key][
                        'Redemption fee (as a percentage of amount redeemed)  2']
                    item['maximum_sales_charge_full_load'] = final_shareholder[key][
                        'Maximum sales charge (load) imposed on purchases']

            url_2 = "https://www.aamlive.com/" +response.xpath("//a[contains(text(),'Distributions')]/@href").extract()[0]
            meta = response.meta
            meta['items'] = items

            yield self.make_request(url_2, callback=self.distributions, meta=meta, dont_filter=True)

        def distributions(self, response):
            items = response.meta['items']
            file = open('response2.html', 'w')
            file.write(response.text)
            file.close()
            
        '''
        share_holder_temp = \
        response.xpath('//strong[contains(text(),"Shareholder Fees")]/following::table[1]').extract()[0]
        shareholder_table = pd.read_html(share_holder_temp)
        final_shareholder = shareholder_table[0].set_index('Unnamed: 0').to_dict('dict')
        t = response.xpath('//strong[contains(text(),"Annual Fund Operating Expense")]/following::table[1]').extract()[
            0]
        expenses = pd.read_html(t)
        print(final_shareholder)

        final_expenses = expenses[0].set_index('Unnamed: 0').to_dict('dict')
        print(final_expenses)
        for item in items:
            print(item['share_class'].strip())
            for key in final_expenses:
                print("cndncdcn", key.replace('Share', ''))
                # print("dcdcdkn",item['share_class'].strip().replace('\xa0','')==key.replace('Share','').strip() )
                if(item['share_class'].strip().replace('\xa0', '') == key.replace('Share', '').strip()):
                    item['annual_fund_operating_expenses_after_fee_waiver'] = final_expenses[key][
                        'Total annual fund operating expenses after fee waiver and/or expense reimbursements']
                    item['fees_total_12b_1'] = final_expenses[key]['Distribution (Rule 12b-1) Fee']
                    item['other_expenses'] = final_expenses[key]['Other Expenses']
                    item['management_fee'] = final_expenses[key]['Management Fees']
                    item['shareholder_service_fees'] = final_expenses[key]['Shareholder Service Fees']
                    break
            for key in final_shareholder:
                if(item['share_class'].strip().replace('\xa0', '') == key.replace('Share', '').strip()):
                    item['deferred_sales_charge'] = final_shareholder[key]['Maximum deferred sales charge (load)  1']
                    item['redemption_fee'] = final_shareholder[key]['Redemption fee (as a percentage of amount redeemed)  2']
                    item['maximum_sales_charge_full_load'] = final_shareholder[key]['Maximum sales charge (load) imposed on purchases']


            url_2="https://www.aamlive.com/" + response.xpath("//a[contains(text(),'Distributions')]/@href").extract()[
            0]
            meta = response.meta
            meta['items'] = items

            yield self.generate_item(item, FinancialDetailItem)
           ''' 
