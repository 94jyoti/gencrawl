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


class FederatedInvestorsDetail(FinancialDetailSpider):
    logging.basicConfig(filename="hsbc.log", level=logging.INFO)
    logging.info("InvestorFundsUSHSBCDetail")
    name = 'financial_detail_federatedinvestors_com'

    custom_settings = {
        
        "COOKIES_ENABLED": True,
        "COOKIES_DEBUG": True
    }

    

    def get_items_or_req(self, response, default_item={}):
        logging.info("InvestorFundsUSHSBCDetail...get_items_or_req")
        items = super().get_items_or_req(response, default_item)
        #print("Items:",len(items))

        meta = response.meta

        meta['item'] = items[0]

        selector = scrapy.Selector(text=response.text, type="html")
        tokenw = selector.xpath("//input[@id='tokenW']/@value").get()

        shareclassid = selector.xpath("//input[@id='shareclassid']/@value").get()

        fundbasketid = selector.xpath("//input[@id='fundbasketid']/@value").get()

        characteristicDate = selector.xpath("//input[@id='characteristicDate']/@value").get()

        parsed_tokenw = urllib.parse.urlencode({"tokenW":tokenw})

        
        h = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"


        
        }
        cookies = {
            "JSESSIONID": "0000YAhqWvQJ-LLoWvAY3skBWvo:1doueinte"
            
            
        }
        
        body='performanceReturnsAnnualizedReturnType=BT&characteristicDate='+characteristicDate+'&dafType=-1&fundbasketid='+fundbasketid+'&shareclassid='+shareclassid+'&managedaccountid=&compositeid=&section=&tab=tab-panel-yields&'+parsed_tokenw+'&bonyClient=false'



        r = scrapy.Request("https://www.federatedinvestors.com/products/product.do",method='POST',body = body,headers=h,callback=self.distributions,dont_filter=True,meta=meta)

        yield(r)



    def distributions(self,response):

        meta = response.meta

        item = meta['item']

        nasdaq_ticker = item['nasdaq_ticker']

        open(nasdaq_ticker+'.html','w',encoding='utf-8').write(response.text)

        data_block = []
        for block in response.xpath("//table[@id='performance-returns-yield-table']//tr"):
            print("block:",block)
            td_block_list= []
            for td_block in block.xpath("th/span"):
                td_value = td_block.xpath("text()").get()
                print("td_value:",td_value)
                td_block_list.append(td_value)
            for td_block in block.xpath("td"):
                td_value = td_block.xpath("text()").get()
                print("td_value:",td_value)
                td_block_list.append(td_value)
            for td_block in block.xpath("td"):
                td_value = td_block.xpath("time/@datetime").get()
                print("td_value:",td_value)
                td_block_list.append(td_value)
            data_block.append(td_block_list)

        sec_yield_30_day = response.xpath("//table[@id='performance-returns-yield-table']//tr[1]/td[3]/text()").get()
    
        sec_yield_date_30_day = response.xpath("//table[@id='performance-returns-yield-table']//tr[1]/td[1]/time/@datetime").get()
        sec_yield_without_waivers_30_day = response.xpath("//table[@id='performance-returns-yield-table']//tr[1]/td[5]/text()").get()
        sec_yield_without_waivers_date_30_day = response.xpath("//table[@id='performance-returns-yield-table']//tr[1]/td[1]/time/@datetime").get()
        if data_block[0][4].strip()=='30-DAY':

            item['sec_yield_30_day'] = sec_yield_30_day
            item['sec_yield_date_30_day'] = sec_yield_date_30_day
            item['sec_yield_without_waivers_30_day'] = sec_yield_without_waivers_30_day
            item['sec_yield_without_waivers_date_30_day'] = sec_yield_without_waivers_date_30_day

        if data_block[0][4].strip()=='7-DAY':

            item['sec_yield_7_day'] = sec_yield_30_day
            item['sec_yield_date_7_day'] = sec_yield_date_30_day


        yield self.generate_item(item, FinancialDetailItem)
