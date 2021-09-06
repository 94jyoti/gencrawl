from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics

class GuggenheimComDetail(FinancialDetailSpider):
    name = 'financial_detail_guggenheim_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        for row in response.xpath("//h3[contains(text(),'Symbols & CUSIPs')]//following::table[1]//tbody//tr"):
            temp_class=row.xpath(".//td[1]//text()").extract()[0].strip()
            if(items[0]['share_class'].lower().replace("class","").strip() in temp_class):
                items[0]['cusip']=row.xpath(".//td[3]//text()").extract()[0]
                items[0]['share_inception_date']=row.xpath(".//td[4]//text()").extract()[0]
        yield self.generate_item(items[0], FinancialDetailItem)