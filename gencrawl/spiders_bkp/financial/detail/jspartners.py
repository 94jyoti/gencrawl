from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
from gencrawl.util.statics import Statics
import re
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
import json

class JspartnerDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_jspartner_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        file = open("jspartners.html", "w")
        file.write(response.text)
        file.close()