from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import json
import codecs
import csv
from io import BytesIO
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem


class AngeloakcapitalComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_angleoakcapital_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)

        try:
            distributions_url_temp = response.xpath("//h2[contains(text(),'Distributions')]/following::div[position()=1]//div[contains(@class,'table')][position()=1]/@data-table").extract()[0]
            distributions_url = json.loads(distributions_url_temp)['csvURL']
            meta = response.meta
            meta['items'] = items
            yield self.make_request(distributions_url, callback=self.distributions, meta=meta)
        except:
            yield self.generate_item(items[0], FinancialDetailItem)

    def distributions(self, response):
        items = response.meta['items']
        item = items[0]
        data_csv = response.text
        buffer = BytesIO(response.body)
        decoder = codecs.getreader('utf-8')
        data = list(csv.DictReader(decoder(buffer, errors='strict')))
        capital_gains_list = []
        dividend_history = []
        for d in data:
            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                          "record_date": "", "per_share": "", "reinvestment_price": ""}
            data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                          'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
            if (d['Record Date']):
                data_dict1['record_date'] = d['Record Date']
                data_dict2['cg_record_date'] = d['Record Date']
            if (d['Payable Date']):
                data_dict1['pay_date'] = d['Payable Date']
                data_dict2['cg_pay_date'] = d['Payable Date']
            try:

                data_dict1['reinvestment_price'] = d['Reinvestment Price ($/share)']
                data_dict2['cg_reinvestment_price'] = d['Reinvestment Price ($/share)']
            except:
                pass
            try:
                data_dict1['ordinary_income'] = d['Ordinary Income ($/share)']
            except:
                pass
            try:

                data_dict2['long_term_per_share'] = d['LT Cap Gains ($/share)']
            except:
                pass
            try:
                data_dict2['short_term_per_share'] = d['ST Cap Gains ($/share)']
            except:
                pass
            dividend_history.append(data_dict1)
            capital_gains_list.append(data_dict2)
        item['capital_gains'] = capital_gains_list
        item['dividends'] = dividend_history
        yield self.generate_item(item, FinancialDetailItem)
        
        
        
