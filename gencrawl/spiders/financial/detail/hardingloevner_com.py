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


class HardingloevnerDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_hardingloevner_com'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        meta = response.meta
        meta['items'] = items
        
        nonceword = response.text.find("nonce")
        admin_url = response.text.find("admin_url")
        nonce_value = response.text[nonceword+8:admin_url-3]
       
        meta['nonce'] = nonce_value

        id_value = response.xpath("//article/@id").get().replace('post-','')
        meta['id_value'] = id_value

        no_of_classes = response.xpath("//ul/li/a[contains(@class,'hlmetadata_link')]")
        if len(no_of_classes)>0:

            for c in response.xpath("//ul/li/a[contains(@class,'hlmetadata_link')]"):
                instrument_class_name = c.xpath("text()").get()
                instrument_class_url = c.xpath("@data-id").get()
                
                meta['instrument_class_name'] = instrument_class_name

                meta['instrument_class_url'] = instrument_class_url

                page_url = "https://www.hardingloevner.com/ways-to-invest/us-mutual-funds/global-equity-portfolio/#" + instrument_class_url

                logging.info(page_url)
                instrument_class_url_1 =  response.url.split('/')[-2]
                meta['instrument_class_url_1'] = instrument_class_url_1
                nonce_value = meta['nonce']

                string_to_find_start = response.text.find("\""+instrument_class_url_1+"\":{\"id\":")

                length1 = len("\""+instrument_class_url+"\":{\"id\":")

                string_to_find_end = response.text.find("\",\"footer_perfomance",string_to_find_start)

                id2_value = response.text[string_to_find_start+length1+1:string_to_find_end]
                meta['id2_value'] = id2_value


                yield scrapy.Request("https://www.hardingloevner.com/wp-json/hlmetadata/v1/us-mutual-funds/fund_facts/"+instrument_class_url_1+"/"+id_value, method='POST',callback=self.test, headers={'content-length': '0', 'x-wp-nonce': nonce_value,'accept': 'application/json, text/javascript, */*; q=0.01', 'x-requested-with': 'XMLHttpRequest' },dont_filter=True,meta=meta)

                yield scrapy.Request("https://www.hardingloevner.com/wp-json/hlmetadata/v1/us-mutual-funds/fund_facts/"+instrument_class_url+"/"+id_value, method='POST',callback=self.dividends, headers={'content-length': '0', 'x-wp-nonce': nonce_value,'accept': 'application/json, text/javascript, */*; q=0.01', 'x-requested-with': 'XMLHttpRequest' },dont_filter=True,meta=meta)

        else:
            instrument_class_url =  response.url.split('/')[-2]
            meta['instrument_class_url'] = instrument_class_url
            nonce_value = meta['nonce']

            string_to_find_start = response.text.find("\""+instrument_class_url+"\":{\"id\":")
            length1 = len("\""+instrument_class_url+"\":{\"id\":")

            string_to_find_end = response.text.find("\",\"footer_perfomance",string_to_find_start)
            id2_value = response.text[string_to_find_start+length1+1:string_to_find_end]
            meta['id2_value'] = id2_value
            
            yield scrapy.Request("https://www.hardingloevner.com/wp-json/hlmetadata/v1/us-mutual-funds/asof_date/"+id2_value, method='POST',callback=self.getclassname, headers={'content-length': '0', 'x-wp-nonce': nonce_value,'accept': 'application/json, text/javascript, */*; q=0.01', 'x-requested-with': 'XMLHttpRequest' },dont_filter=True,meta=meta)

    def getclassname(self,response):
        meta = response.meta
        nonce_value = meta['nonce']
        data = json.loads(response.text)

        instrument_class_url = meta["instrument_class_url"]
        id_value = meta["id_value"]
        share_class = data["class"]["class_name"]
        meta['instrument_class_name'] = share_class
        meta['items'][0]['share_class'] = share_class
        

        url = "https://www.hardingloevner.com/wp-json/hlmetadata/v1/us-mutual-funds/performance/"+meta['id2_value']+"/2021-06-30?month_end=false"


        yield scrapy.Request(url, method='POST',callback=self.dividends2, headers={'content-length': '0', 'x-wp-nonce': meta['nonce'],'accept': 'application/json, text/javascript, */*; q=0.01', 'x-requested-with': 'XMLHttpRequest' },dont_filter=True,meta=meta)

        yield scrapy.Request("https://www.hardingloevner.com/wp-json/hlmetadata/v1/us-mutual-funds/fund_facts/"+instrument_class_url+"/"+id_value, method='POST',callback=self.dividends, headers={'content-length': '0', 'x-wp-nonce': nonce_value,'accept': 'application/json, text/javascript, */*; q=0.01', 'x-requested-with': 'XMLHttpRequest' },dont_filter=True,meta=meta)


    def test(self,response):

        
        meta = response.meta

        url = "https://www.hardingloevner.com/wp-json/hlmetadata/v1/us-mutual-funds/performance/"+meta['id2_value']+"/2021-06-30?month_end=false"


        yield scrapy.Request(url, method='POST',callback=self.dividends2, headers={'content-length': '0', 'x-wp-nonce': meta['nonce'],'accept': 'application/json, text/javascript, */*; q=0.01', 'x-requested-with': 'XMLHttpRequest' },dont_filter=True,meta=meta)


    def dividends(self, response):

        
        meta = response.meta
        data = json.loads(response.body)

        #print(data['data'][0])
        selector = scrapy.Selector(text=data['data'][0], type="html")
        nasdaq_ticker = selector.xpath("//div[contains(text(),'Ticker')]/preceding-sibling::div/text()").get()
        inception_date = selector.xpath("//div[contains(text(),'Inception Date')]/preceding-sibling::div/text()").get()
        cusip = selector.xpath("//div[contains(text(),'CUSIP')]/preceding-sibling::div/text()").get()
        total_fund_assets = selector.xpath("//div[contains(text(),'Total Fund Assets')]/preceding-sibling::div/text()").get()
        min_investment = selector.xpath("//div[contains(text(),'Minimum Investment')]/preceding-sibling::div/text()").get()
        portfolio_assets = selector.xpath("//div[contains(text(),'Total Fund Assets')]//preceding-sibling::div/text()").get()
        portfolio_assets_date = selector.xpath("//p[@class='asof_date_facts']/text()").get()

        maximum_sales_charge_full_load = selector.xpath("//div[contains(text(),'Sales Charge')]//preceding-sibling::div/text()").get()

        minimum_initial_investment = selector.xpath("//div[contains(text(),'Minimum Investment')]//preceding-sibling::div/text()").get()

        total_expense_gross = selector.xpath("//div[text()='Expense Ratio' or text()='Gross Expense Ratio']//preceding-sibling::div/text()").get()
        turnover_rate = selector.xpath("//div[contains(text(),'Turnover')]//preceding-sibling::div/text()").get()
        turnover_rate_date = selector.xpath("//p[@class='asof_date_facts']/text()").get()
        dividend_frequency = selector.xpath("//div[contains(text(),'Dividend Policy')]//preceding-sibling::div/text()").get()
        #benchmarks = selector.xpath("(//table[@id='table-us-mutual-funds-month']//following::td[contains(text(),'Index')])[1]/text()").get()

        #meta['cusip'] = cusip

        meta['items'][0]['share_class'] = meta['instrument_class_name']
        #print(meta['items'][0]['cusip'])
        meta['items'][0]['cusip'] = cusip
        meta['items'][0]['share_inception_date'] = inception_date
        meta['items'][0]['nasdaq_ticker'] = nasdaq_ticker
        meta['items'][0]['portfolio_assets'] = portfolio_assets
        meta['items'][0]['portfolio_assets_date'] = portfolio_assets_date
        meta['items'][0]['maximum_sales_charge_full_load'] = maximum_sales_charge_full_load
        meta['items'][0]['total_expense_gross'] = total_expense_gross
        meta['items'][0]['minimum_initial_investment'] = minimum_initial_investment
        meta['items'][0]['turnover_rate'] = turnover_rate
        meta['items'][0]['turnover_rate_date'] = turnover_rate_date
        meta['items'][0]['dividend_frequency'] = dividend_frequency
       
        for i in meta['items']:
            yield self.generate_item(i, FinancialDetailItem)

        

    def dividends2(self,response):
        meta = response.meta
        jsonresponse = json.loads(response.text)
        meta['items'][0]['benchmarks'] = jsonresponse["data"][1][0]









        
    

    

   
        
      
   
    
