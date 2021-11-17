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
import requests
from lxml import html
from scrapy.selector import Selector
import copy


class summitryfundsDetail(FinancialDetailFieldMapSpider):
    name = 'summitryfunds_com'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        meta = response.meta
        meta['items'] = items
        yield scrapy.Request("https://www.summitryfunds.com/golub-team/", callback=self.distributions,
                             dont_filter=True,meta=meta)

    def distributions(self,response):
        meta = response.meta
        selector = scrapy.Selector(text=response.text, type="html")
        fund_mgr_list = selector.xpath("//h3/text()").getall()
        fund_mgrs = fund_mgr_list[:len(fund_mgr_list)-1]
        fund_managers_list = []
        for f in fund_mgrs:
            print("f:",f.split('–')[0])
            m = dict([('fund_manager', f.split('–')[0])])
            fund_managers_list.append(m)

        for i in meta['items']:
            i['fund_managers'] = fund_managers_list
            yield self.generate_item(i, FinancialDetailItem)
