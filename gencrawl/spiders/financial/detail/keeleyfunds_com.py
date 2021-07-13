from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
import re


class KeeleyComDetail(FinancialDetailSpider):
    name = 'financial_detail_keeley_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        # print("first length of itemmsmssmsmsms", len(items))
        item = items[0]
        ticker = item['fund_url'].split("/")[-2]
        market_data = response.xpath("//a[contains(text(),'Market Data')]/@href").extract()[0]
        # print(temp_url)
        market_url = "https://keeleyfunds.com/funds/" + ticker + "/" + market_data
        # print(market_url)
        # print("inside try")
        try:
            meta = response.meta
            meta['items'] = items
            # print("inside one try")
            yield self.make_request(market_url, callback=self.market_data, meta=meta)
        except:

            for i in items:
                # print("isnide except")
                yield self.generate_item(i, FinancialDetailItem)

    # for i in items:
    #	yield self.generate_item(i, FinancialDetailItem)

    def market_data(self, response):
        # print('wdwaaaaaaaaaaaddddddddddddddddddddddddd')
        items = response.meta['items']

        # print("second lenth of items", len(items))
        # print(items)
        file = open("testttt.html", "w")
        file.write(response.text)
        file.close
        # https://keeleyfunds.com/funds/kmdvx/market.php
        benchmarks = response.xpath(
            "//span[contains(text(),'Quarterly')]/following::table//tr[position()>1]/td[1][contains(text(),'Index')]//text()").extract()
        # print(benchmarks)
        for i in items:
            i['benchmarks'] = benchmarks
            # print(i['benchmarks'])
        item = items[0]

        # print(item)
        ticker = item['fund_url'].split("/")[-2]

        fund_data = response.xpath("//a[contains(text(),'Fund Characteristics')]/@href").extract()[0]
        # print(temp_url)
        fund_url = "https://keeleyfunds.com/funds/" + ticker + "/" + fund_data
        # print(fund_url)
        meta = response.meta
        meta['items'] = items
        yield self.make_request(fund_url, callback=self.fund_characterstics, meta=meta)

    def fund_characterstics(self, response):
        # print("cdnklcndslkcndcndscdnscskl")
        items = response.meta['items']
        # print("thierd lenth of items", len(items))
        # sec_yield_30_day=response.xpath("//td[contains(text(),'30 day SEC YIELD (subsidized) ')]/following-sibling::td[1]/text()").extract()[0]
        # sec_yield_date_30_day=response.xpath("//div[@id='share-info']/following::span[1]//text()").extract()[0]
        # sec_yield_without_waivers_30_day=response.xpath("//td[contains(text(),'30 day SEC YIELD (unsubsidized) ')]/following-sibling::td[1]/text()").extract()[0]
        # sec_yield_without_waivers_date_30_day=response.xpath("//div[@id='share-info']/following::span[1]//text()").extract()[0]
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

