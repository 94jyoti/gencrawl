from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics


class AshmoreComDetail(FinancialDetailSpider):
    name = 'financial_detail_ashmore_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        print(len(items))
        print(items)
        file=open("ashmore.html","w")
        file.write(response.text)
        file.close()