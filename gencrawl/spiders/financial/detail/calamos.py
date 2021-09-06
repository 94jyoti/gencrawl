from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re


class CalamosfundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_calamos_com'
    custom_settings = {
        "RETRY_TIMES": 5,
        "CRAWLERA_ENABLED": True
    }
    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        file=open("brroke_test.html","w")
        file.write(response.text)
        file.close()
        for item in items:
            temp_url=item['fund_url'].rsplit("-",1)
            temp_url.remove(temp_url[len(temp_url)-1])
            item['fund_url']="".join(temp_url)+"-"+item['nasdaq_ticker'].lower()+"/"
        return items

