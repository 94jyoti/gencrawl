from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import json
import pandas as pd
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem


class BaillieComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_baillie_com'
    custom_settings = {
        "RETRY_TIMES": 5,
        "CRAWLERA_ENABLED": True,
        "COOKIES_ENABLED": True,
        "COOKIES_DEBUG": True
    }

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        file = open("baillie_gifford.html", "w")
        file.write(response.text)
        file.close()
        table_data=response.xpath("(//table[@class='distributions-table distributions'])[1]//tbody//tr")

        for item in items:
            capital_gain_list=[]
            dividend_list=[]
            for row in table_data:

                if(item['nasdaq_ticker']==row.xpath(".//td[1]//text()").extract_first().strip()):
                        data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                                      "record_date": "", "per_share": "", "reinvestment_price": ""}
                        data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "",
                                      'cg_pay_date': "", 'short_term_per_share': "", 'total_per_share': "",
                                      'cg_reinvestment_price': ""}
                        data_dict2['short_term_per_share'] =row.xpath(".//td[3]//text()").extract_first().strip()
                        data_dict2['long_term_per_share'] =row.xpath(".//td[6]//text()").extract_first().strip()
                        data_dict1['per_share'] = row.xpath(".//td[7]//text()").extract_first().strip()
                        data_dict1['ordinary_income'] = row.xpath(".//td[2]//text()").extract_first().strip()
                        data_dict1['ex_date'] = row.xpath(".//td[8]//text()").extract_first().strip()
                        data_dict1['pay_date'] = row.xpath(".//td[9]//text()").extract_first().strip()
                        data_dict1['qualified_income'] = row.xpath(".//td[4]//text()").extract_first().strip()
                        capital_gain_list.append(data_dict2)
                        dividend_list.append(data_dict1)
            item['capital_gains']=capital_gain_list
            item['dividends']=dividend_list
            yield self.generate_item(item, FinancialDetailItem)
