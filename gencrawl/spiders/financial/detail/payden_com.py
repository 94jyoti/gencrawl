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
        #import ipdb;ipdb.set_trace()
        logging.info("InvestorFundsUSHSBCDetail...get_items_or_req")
        print("*** TEsting 1 ***")
        items = super().get_items_or_req(response, default_item)
        distribution_url = "https://www.payden.com/dividends.aspx"
        selector = scrapy.Selector(text=response.text, type="html")
        tickers = selector.xpath("//select[@id='drpClass']/option/@value").getall()
        meta = response.meta
        meta['items'] = items
        if len(tickers)>1:
            #yield self.generate_item(items[0], FinancialDetailItem)
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
            
            yield self.make_request(distribution_url, callback=self.parse_distribution, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)
            


    def distributions(self,response):
        distribution_url = "https://www.payden.com/dividends.aspx"        
        meta = response.meta
        ticker = meta['ticker']
        #yield self.make_request(distribution_url, callback=self.parse_distribution, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)
        selector = scrapy.Selector(text=response.text, type="html")
        cusip = selector.xpath("//td[contains(text(),'CUSIP')]/following-sibling::td/text()").get()
        share_class = selector.xpath("//select[contains(@name,'Class')]/option[@selected]/text()").get()
        portfolio_assets = selector.xpath("//td[contains(text(),'Fund Total Net Assets')]/following-sibling::td/text()").get()
        maximum_sales_charge_full_load = selector.xpath("//td[contains(text(),'Sales Charge')]/following-sibling::td/text()").get()
        share_inception_date = selector.xpath("(//td[contains(text(),'Share Class Inception Date')]/following-sibling::td)[1]/text()").get()
        item = meta['items']
        item_copy = copy.deepcopy(item)
        item_copy[0]['nasdaq_ticker']=ticker
        item_copy[0]['cusip']=cusip
        item_copy[0]['share_class']=share_class
        item_copy[0]['portfolio_assets']=portfolio_assets
        item_copy[0]['share_inception_date']=share_inception_date
        meta['items'] = item_copy
        
        yield self.make_request(distribution_url, callback=self.parse_distribution, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)

    def parse_distribution(self, response):
        
        cap_gain_url = "https://www.payden.com/capitalGains.aspx"
        meta = response.meta
        items = meta['items']

        dividends = []
        current_ticker = items[0]['nasdaq_ticker']
        ticker_list = response.xpath("//tr[th]/following-sibling::tr/td[4]/text()").extract()
        per_share_list = response.xpath("//tr[th]/following-sibling::tr/td[3]/text()").extract()
        reinv_list = response.xpath("//tr[th]/following-sibling::tr/td[2]/text()").extract()
        ticker_index = ticker_list.index(current_ticker)

        # Logic for Income Distribution
        divident_dict = {"per_share": per_share_list[ticker_index],
                        "reinvestment_price": reinv_list[ticker_index]}
        dividends.append(divident_dict)

        items[0]['dividends'] = dividends
        meta['items'] = items

        yield self.make_request(cap_gain_url, callback=self.parse_cap_gains, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)

    def parse_cap_gains(self, response):
        meta = response.meta
        items = meta['items']

        capital_gains = []
        current_ticker = items[0]['nasdaq_ticker']
        ticker_list = response.xpath("//tr[th]/following-sibling::tr/td[8]/text()").extract()
        short_term_list = response.xpath("//tr[th]/following-sibling::tr/td[3]/text()").extract()
        reinv_list = response.xpath("//tr[th]/following-sibling::tr/td[2]/text()").extract()
        long_term_list = response.xpath("//tr[th]/following-sibling::tr/td[4]/text()").extract()
        record_date = response.xpath("//tr[th]/following-sibling::tr/td[5]/text()").extract()
        ex_date = response.xpath("//tr[th]/following-sibling::tr/td[6]/text()").extract()
        payable_date = response.xpath("//tr[th]/following-sibling::tr/td[7]/text()").extract()
        ticker_index = ticker_list.index(current_ticker)

        capital_gains_dict = {'cg_ex_date':ex_date[ticker_index], 'cg_pay_date':payable_date[ticker_index],
                        'short_term_per_share':short_term_list[ticker_index],
                        'long_term_per_share':long_term_list[ticker_index],
                        'cg_record_date':record_date[ticker_index],
                        'cg_reinvestment_price': reinv_list[ticker_index]}

        capital_gains.append(capital_gains_dict)

        items[0]['capital_gains'] = capital_gains

        meta['items'] = items

        yield self.generate_item(items[0], FinancialDetailItem)
