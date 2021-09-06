from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics

import re


class NorthernComDetail(FinancialDetailSpider):
    name = 'financial_detail_northern_com'
    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        print("dcnsncklsdnccnksl")
        file = open("northern.html", "w")
        file.write(response.text)
        file.close()
        data = response.xpath("//script[contains(text(),'window.__PRELOADED_STATE_')]//text()").extract()[0]
        # temp=re.findall("window.__PRELOADED_STATE__ =(.*?);window.__GLOBAL",data)
        # print(temp)
        # json_data=json.loads(temp[]0)
        # print(json_data)
        # json_data1=json.loads(json_data)
        # print(json_data1['content']['body']['components']['props']['title'])
        # yield self.generate_item(items[0], FinancialDetailItem)