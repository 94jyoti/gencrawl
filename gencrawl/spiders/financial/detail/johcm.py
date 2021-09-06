from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re


class JohcmfundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_johcm_com'
    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        file=open("johcm_test.html","w")
        file.write(response.text)
        file.close()


