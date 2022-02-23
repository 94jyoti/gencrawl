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


class KeeleyComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_keeley_com'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        #items = self.prepare_mapped_items(response, default_item)
        item = items[0]
        print("frdvvdfvdfvdfvdfvdfv",items)
        ticker = item['fund_url'].split("/")[-2]
        market_data = response.xpath("//a[contains(text(),'Market Data')]/@href").extract()[0]
        market_url = "https://keeleyfunds.com/funds/" + ticker + "/" + market_data
        try:
            meta = response.meta
            meta['items'] = items
            yield self.make_request(market_url, callback=self.market_data, meta=meta)
        except:

            for i in items:
                yield self.generate_item(i, FinancialDetailItem)
    def market_data(self, response):
        items = response.meta['items']
        file = open("testttt.html", "w")
        file.write(response.text)
        file.close
        benchmarks = response.xpath(
            "//span[contains(text(),'Quarterly')]/following::table//tr[position()>1]/td[1][contains(text(),'Index')]//text()").extract()
        share_inception_date=(response.xpath("//*[contains(text(),'S.I.')]/text()").extract()[0]).replace("S.I.","").strip()
        for i in items:
            i['benchmarks'] = benchmarks
            i['share_inception_date']=share_inception_date
        item = items[0]
        ticker = item['fund_url'].split("/")[-2]

        fund_data = response.xpath("//a[contains(text(),'Fund Characteristics')]/@href").extract()[0]
        fund_url = "https://keeleyfunds.com/funds/" + ticker + "/" + fund_data
        meta = response.meta
        meta['items'] = items
        yield self.make_request(fund_url, callback=self.fund_characterstics, meta=meta)

    def fund_characterstics(self, response):
        items = response.meta['items']
        try:
            for i in items:
                print("=============================================================================================",
                      items)
                try:
                    i['sec_yield_30_day'] = response.xpath(
                    "//td[contains(text(),'30 day SEC YIELD (subsidized)')]/following-sibling::td[1]/text()").extract()[
                    0]
                except:
                    i['sec_yield_30_day'] = response.xpath(
                        " //td[contains(text(),'30 day SEC Yield (subsidized)')]/following-sibling::td[1]/text()").extract()[
                        0]
    
                i['sec_yield_date_30_day'] = response.xpath("//div[@id='share-info']/following::span[1]//text()").extract()[
                    0]
                try:
                    i['sec_yield_without_waivers_30_day'] = response.xpath(
                        "//td[contains(text(),'30 day SEC YIELD (unsubsidized) ')]/following-sibling::td[1]/text()").extract()[
                        0]
                except:
                    i['sec_yield_without_waivers_30_day'] = response.xpath(
                        "//td[contains(text(),'30 day SEC Yield (unsubsidized)')]/following-sibling::td[1]/text()").extract()[
                        0]
                i['sec_yield_without_waivers_date_30_day'] = \
                response.xpath("//div[@id='share-info']/following::span[1]//text()").extract()[0]
                yield self.generate_item(i, FinancialDetailItem)
        except:
            for i in items:
                yield self.generate_item(i, FinancialDetailItem)

