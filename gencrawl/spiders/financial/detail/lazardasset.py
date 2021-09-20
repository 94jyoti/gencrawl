from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics

class LazardComDetail(FinancialDetailSpider):
    name = 'financial_detail_lazard_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        file=open("lazard.html","w")
        file.write(response.text)
        file.close()
        yield self.generate_item(items[0], FinancialDetailItem)