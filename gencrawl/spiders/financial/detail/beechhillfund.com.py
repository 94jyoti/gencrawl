from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics


class BeechhillfundComDetail(FinancialDetailSpider):
    name = 'financial_detail_beechhillfund_com'
    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        file=open("beechhil.html","w")
        file.write(response.text)
        file.close()
        #yield self.generate_item(items[0], FinancialDetailItem)


