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
from gencrawl.util.statics import Statics
# import urllib
import itertools


class IntrepidCapitalDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_intrepidcapitalfunds_com'
    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        meta = response.meta
        meta['items'] = items
        yield scrapy.Request("https://intrepidcapitalfunds.com/strategies/mutual-funds/income/performance/", method='GET',callback=self.dividends,dont_filter=True,meta=meta)

    def dividends(self,response):
        benchmarks = response.selector.xpath("//table[contains(@class,'mutual-fund')]//tbody/tr[not(contains(.,'Fund'))]/th[not(contains(.,'2')) and not(contains(.,'Morningstar'))]/text()").getall()
        meta = response.meta
        items = meta['items']
        for i in items:
            i['benchmarks'] = benchmarks
            yield self.generate_item(i, FinancialDetailItem)