from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider

from datetime import datetime
import datetime
import urllib.parse
import re


class HardingComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_harding_com'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        #items = self.prepare_mapped_items(response, default_item)
        file=open("hard.html","w")
        file.write(response.text)
        file.close()
        print(response.text)
        return items
