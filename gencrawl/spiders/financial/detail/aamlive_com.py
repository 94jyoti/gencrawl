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
        items = self.prepare_items(response, default_item)
        url_1 = "https://www.aamlive.com/" + response.xpath("//a[contains(text(),'Fees & Expenses')]/@href").extract()[
            0]
        counter = 0
        for item in items:
            item['total_expense_net'] = item['temp_expense_net'][counter].replace('net', '').strip()
            item['total_expense_gross'] = item['temp_expense_gross'][counter].replace('gross', '').strip()
            counter = counter + 1
        meta = response.meta
        meta['items'] = items
        return self.make_request(url_1, callback=self.feesandexpenses, meta=meta, dont_filter=True)

    def feesandexpenses(self, response):
        items = response.meta['items']
        share_holder_temp = \
            response.xpath('//strong[contains(text(),"Shareholder Fees")]/following::table[1]').extract()[0]
        shareholder_table = pd.read_html(share_holder_temp)
        final_shareholder = shareholder_table[0].set_index('Unnamed: 0').to_dict('dict')
        t = response.xpath('//strong[contains(text(),"Annual Fund Operating Expense")]/following::table[1]').extract()[
            0]
        expenses = pd.read_html(t)
        final_expenses = expenses[0].set_index('Unnamed: 0').to_dict('dict')
        for item in items:
            for key in final_expenses:
                if (item['share_class'].strip().replace('\xa0', '') == key.replace('Share', '').strip()):
                    item['annual_fund_operating_expenses_after_fee_waiver'] = final_expenses[key][
                        'Total annual fund operating expenses after fee waiver and/or expense reimbursements']
                    item['fees_total_12b_1'] = final_expenses[key]['Distribution (Rule 12b-1) Fee']
                    item['other_expenses'] = final_expenses[key]['Other Expenses']
                    item['management_fee'] = final_expenses[key]['Management Fees']
                    try:
                        item['acquired_fund_fees_and_expenses'] = final_expenses[key]['Acquired Fund Fees and Expenses']
                    except:
                        pass
                    try:
                        item['expense_waivers'] = final_expenses[key]['Fee waiver and/or Expense Reimbursements3']
                    except:
                        try:
                            item['expense_waivers'] = final_expenses[key]['Fee waiver and/or expense reimbursements3']
                        except:
                            pass
                    try:
                        item['shareholder_service_fees'] = final_expenses[key]['Shareholder Service Fees']
                    except:
                        item['shareholder_service_fees'] = final_expenses[key]['Shareholder Services Fee']
                    break
            for key in final_shareholder:
                if (item['share_class'].strip().replace('\xa0', '') == key.replace('Share', '').strip()):
                    item['deferred_sales_charge'] = final_shareholder[key]['Maximum deferred sales charge (load)  1']
                    item['redemption_fee'] = final_shareholder[key][
                        'Redemption fee (as a percentage of amount redeemed)  2']
                    item['maximum_sales_charge_full_load'] = final_shareholder[key][
                        'Maximum sales charge (load) imposed on purchases']

            url_2 = "https://www.aamlive.com/" + \
                    response.xpath("//a[contains(text(),'Distributions')]/@href").extract()[0]
            meta = response.meta
            meta['item'] = item
            yield self.make_request(url_2, callback=self.distributions, meta=meta, dont_filter=True)

    def distributions(self, response):
        item = response.meta['item']
        recent_distributions = response.xpath(
            "//strong[contains(text(),'Most Recent Dividend Distribution')]/following::div[1]//tbody//tr")

        for tr in recent_distributions:
            share_class = tr.xpath("./td[1]/text()").extract_first().split("(")[0].replace("Class", "").strip()
            distributions_list = []
            if (item['share_class'].strip().replace('/xa0', '') == share_class):
                data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                              "record_date": "", "per_share": "", "reinvestment_price": ""}
                data_dict1['ex_date'] = tr.xpath("./td[2]/text()").extract_first()
                data_dict1['per_share'] = tr.xpath("./td[3]/text()").extract_first()
                data_dict1['reinvestment_price'] = tr.xpath("./td[4]/text()").extract_first()
                distributions_list.append(data_dict1)
                item['dividends'] = distributions_list

        table_data = response.xpath(
            "//*[contains(text(), 'Distributions')]/ancestor::div[contains(@class,'sfContentBlock')]/following-sibling::div//table/ancestor::details/parent::div")
        for data in table_data:
            share_class_item = data.xpath(".//strong//text()").extract_first().replace("Class", "").split("(")[
                0].strip()
            table_header = data.xpath(".//table//thead//th//text()").extract()

            dividend_list = []
            capital_gain_list = []
            if (share_class_item == item['share_class'].strip().replace('/xa0', '')):
                data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                              "record_date": "", "per_share": "", "reinvestment_price": ""}
                data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                              'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
                if ('Capital Gains Per Share ($)' in table_header):
                    for i in data.xpath(".//tbody//tr"):
                        data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "",
                                      'cg_pay_date': "", 'short_term_per_share': "", 'total_per_share': "",
                                      'cg_reinvestment_price': ""}
                        data_dict2['cg_ex_date'] = i.xpath(".//td[1]//text()").extract_first()
                        data_dict2['total_per_share'] = i.xpath(".//td[2]//text()").extract_first()
                        data_dict2['cg_reinvestment_price'] = i.xpath(".//td[3]//text()").extract_first()
                        capital_gain_list.append(data_dict2)
                else:
                    for i in data.xpath(".//tbody//tr"):
                        data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                                      "record_date": "", "per_share": "", "reinvestment_price": ""}
                        data_dict1['ex_date'] = i.xpath(".//td[1]//text()").extract_first()
                        data_dict1['per_share'] = i.xpath(".//td[2]//text()").extract_first()
                        data_dict1['reinvestment_price'] = i.xpath(".//td[3]//text()").extract_first()
                        dividend_list.append(data_dict1)
                for i in dividend_list:
                    item['dividends'].append(i)
                item['capital_gains'] = capital_gain_list

        yield self.generate_item(item, FinancialDetailItem)
