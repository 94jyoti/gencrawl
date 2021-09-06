from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re


class BbhfundsfundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_bbhfunds_com'
    custom_settings = {
        "RETRY_TIMES": 5,
        "CRAWLERA_ENABLED": True
    }
    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        file=open("bbh.html","w")
        file.write(response.text)
        file.close()

