from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics

class MundovalComDetail(FinancialDetailSpider):
    name = 'financial_detail_mundoval_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        temp_data=response.xpath("(//a[@title='Mundoval Fund'])[2]//text()").extract()
        print(temp_data)
        data_dict1={"per_share":"","ex_date":""}
        data_dict1['per_share']=temp_data[0].split(":")[-1]
        data_dict1["ex_date"]=response.xpath("(//a[@title='Mundoval Fund'])[1]//text()").extract()[0].split("as of")[-1].strip()
        data_dict2={"short_term_per_share":"","long_term_per_share":""}
        data_dict2["short_term_per_share"]=temp_data[1].split(":")[-1]
        data_dict2['long_term_per_share']=temp_data[2].split(":")[-1]
        for item in items:
            item['capital_gains']=[data_dict2]
            item['dividends']=[data_dict1]

            yield self.generate_item(item, FinancialDetailItem)