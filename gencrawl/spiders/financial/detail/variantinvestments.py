from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics
from copy import deepcopy

class VariantComDetail(FinancialDetailSpider):
    name = 'financial_detail_variant_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        meta = response.meta
        meta['items'] = items
        file = open("amf.html", "w")
        file.write(response.text)
        file.close()
        url="https://funds.variantinvestments.com/distribution-history/"
        yield self.make_request(url, callback=self.parse_dividends, meta=meta,dont_filter=True)


    def parse_dividends(self,response):
        items = response.meta['items']
        final_items=[]
        file=open("varient.html","w")
        file.write(response.text)
        file.close()
        for i in range(len(items)+1):
            final_items.append(deepcopy(items[0]))

        final_items[1]['nasdaq_ticker']="UNIQX"
        final_items[1]['instrument_name']="Variant Alternative Income Fund (UNIQX)"
        print(final_items)
        dividend_list=[]
        capital_gain_list=[]
        table_data=response.xpath("//table[@id='tablepress-19']//tbody//tr")
        for row in table_data:
            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "", "record_date": "", "per_share": "", "reinvestment_price": ""}
            data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
            data_dict2['cg_ex_date']=row.xpath(".//td[1]//text()").extract_first()
            data_dict2['total_per_share']=row.xpath(".//td[3]//text()").extract_first()
            capital_gain_list.append((data_dict2))
        final_items[0]['capital_gains']=capital_gain_list

        table_data = response.xpath("//table[@id='tablepress-20']//tbody//tr")
        capital_gain_list = []
        for row in table_data:
            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                          "record_date": "", "per_share": "", "reinvestment_price": ""}
            data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                          'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
            data_dict2['cg_ex_date'] = row.xpath(".//td[1]//text()").extract_first()
            data_dict2['total_per_share'] = row.xpath(".//td[3]//text()").extract_first()
            capital_gain_list.append((data_dict2))
        final_items[1]['capital_gains'] = capital_gain_list




        for items in final_items:
            yield self.generate_item(items, FinancialDetailItem)