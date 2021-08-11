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


class CavanalComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_cavanal_com'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        # items = self.prepare_mapped_items(response, default_item)

        performance_url = "https://cavanalhillfunds.com/" + \
                          response.xpath("//a[@class='tab--performance']//@href").extract()[0]
        print(performance_url)
        try:
            meta = response.meta
            meta['items'] = items
            print("insisde try")
            yield self.make_request(performance_url, callback=self.parse_performance, meta=meta,
                                    method=Statics.CRAWL_METHOD_SELENIUM,dont_filter=True)
        except:

            for i in items:
                print("inside except")
                yield self.generate_item(i, FinancialDetailItem)

    def parse_performance(self, response):
        items = response.meta['items']
        file = open("testttt.html", "w")
        file.write(response.text)
        file.close
        print(items)
        print("yahaa n huhcndskcdsnks")
        try:
            table_column = response.xpath(
                "//h2[contains(text(),'Current Yield')]//following::table[1]//thead//tr[1]//th//text()").extract()
            print("table colejewvsvnsk")
            data=response.xpath("//h2[contains(text(),'Current Yield')]//following::table[1]//tbody//tr")
            print("datatatatatatt",data)
            if(data!=[]):
                for row in data:
                    for item in items:
                        #print(items)
                        print("isndieiedededed")
                        print(item['nasdaq_ticker'])
                        print(row.xpath("./td[1]/text()").extract_first())
                        #print("111112211111111aaaaa11111111")
                        if (item['nasdaq_ticker'] in row.xpath("./td[1]/text()").extract_first()):
                            print("isnide ifff main")
                            item['sec_yield_30_day'] = row.xpath('.//td[4]/text()').extract_first()
                            item['sec_yield_7_day'] = row.xpath('.//td[2]/text()').extract_first()
                            item['sec_yield_date_30_day'] = \
                            	response.xpath("//h2[contains(text(),'Current Yield')]//span//text()").extract()[0].replace(
                                "as of", "").strip()
                            item['sec_yield_date_7_day'] = \
                            	response.xpath("//h2[contains(text(),'Current Yield')]//span//text()").extract()[0].replace(
                                "as of", "").strip()
                            #print("111112211111111aaaaa11111111")
                            print(item)
                            yield self.generate_item(item, FinancialDetailItem)
            else:
                for i in items:
                    yield self.generate_item(i, FinancialDetailItem)
        except:
            for i in items:
                yield self.generate_item(i, FinancialDetailItem)