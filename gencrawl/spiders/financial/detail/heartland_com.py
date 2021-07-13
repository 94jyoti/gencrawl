from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re

class SaturnaComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_heartland_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        print(items)
        file=open("heartland.html","w")
        file.write(response.text)
        file.close()
        return items
