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


class summitryfundsDetail(FinancialDetailFieldMapSpider):
    logging.basicConfig(filename="hsbc.log", level=logging.INFO)
    logging.info("InvestorFundsUSHSBCDetail")
    name = 'summitryfunds_com'

    
    def get_items_or_req(self, response, default_item={}):
        logging.info("InvestorFundsUSHSBCDetail...get_items_or_req")
        items = super().get_items_or_req(response, default_item)
        #print("Items:",len(items))

        #open('a.html','w',encoding='utf-8').write(response.text)

        meta = response.meta
        
        meta['items'] = items



        yield scrapy.Request("https://www.summitryfunds.com/golub-team/",callback=self.distributions,dont_filter=True,meta=meta)

    def distributions(self,response):
        meta = response.meta

        open('summitryfunds.html','w',encoding='utf-8').write(response.text)

        selector = scrapy.Selector(text=response.text, type="html")

        fund_mgr_list = selector.xpath("//h3/text()").getall()

        print("fund_mgr_list:",fund_mgr_list,len(fund_mgr_list),fund_mgr_list[:len(fund_mgr_list)-1])

        fund_mgrs = fund_mgr_list[:len(fund_mgr_list)-1]

        fund_managers_list = []

        Dict = {}
        for f in fund_mgrs:
            print("f:",f.split('–')[0])
            Dict = dict([('fund_manager',f.split('–')[0])])
            print("DICT:",Dict)


            fund_managers_list.append(Dict)


        for i in meta['items']:

            i['fund_managers'] =  fund_managers_list

            yield self.generate_item(i, FinancialDetailItem)



       






    