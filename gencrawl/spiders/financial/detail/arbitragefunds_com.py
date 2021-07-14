from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re


class ArbitragefundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_arbitragefunds_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        for item in items:
            inception_date = item.pop("share_inception_date", None)
            if inception_date:
                inception_date = inception_date.split(".")[0].replace("Inception dates: ", "").split(";")
                ticker = item['nasdaq_ticker']
                for i in inception_date:
                    if ticker in i:
                        inception = re.search(r'(\d{1,2}/\d{1,2}/\d{1,2})', i)
                        if inception:
                            item['share_inception_date'] = inception.group(1)
        return items
