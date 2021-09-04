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
import logging
import requests
from lxml import html
from scrapy.selector import Selector
import copy


class PaydenDetail(FinancialDetailSpider):
    logging.basicConfig(filename="hsbc.log", level=logging.INFO)
    logging.info("InvestorFundsUSHSBCDetail")
    name = 'financial_detail_payden_com'

    
    def get_items_or_req(self, response, default_item={}):
        logging.info("InvestorFundsUSHSBCDetail...get_items_or_req")
        items = super().get_items_or_req(response, default_item)
        #print("Items:",len(items))

        meta = response.meta
        
        meta['items'] = items

        #print("meta['items']:",meta['items'])
        print("hello")

        selector = scrapy.Selector(text=response.text, type="html")
        tickers = selector.xpath("//select[@id='drpClass']/option/@value").getall()

        print("tickers:",len(tickers))

        if len(tickers)>1:
            for ticker in tickers[1:]:
                meta['ticker'] = ticker



                form = {
                       
                        "__VIEWSTATE":selector.xpath("//input[@id='__VIEWSTATE']/@value").get(),

                        "__VIEWSTATEGENERATOR":selector.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").get(),

                        "__EVENTVALIDATION": selector.xpath("//input[@id='__EVENTVALIDATION']/@value").get(),

                        "drpClass":ticker

                        }


                h = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
                }

                r = scrapy.Request(response.url,method='POST',body = urllib.parse.urlencode(form),headers=h,callback=self.distributions,dont_filter=True,meta=meta)

                yield(r)
        else:
            for i in items:
                yield self.generate_item(i, FinancialDetailItem)


           


    def distributions(self,response):
        print("here")
        meta = response.meta
        ticker = meta['ticker']

        #print(response.text)
        #open(ticker+'.html','w',encoding='utf-8').write(response.text)
        selector = scrapy.Selector(text=response.text, type="html")
        #tickers = selector.xpath("//select[@id='drpClass']/option/@value").getall()

        item = meta['items']

        item_copy = copy.deepcopy(item)

        
        item_copy[0]['nasdaq_ticker']=ticker

        print("item_copy:",item_copy)




        #yield self.generate_item(item_copy, FinancialDetailItem)





    