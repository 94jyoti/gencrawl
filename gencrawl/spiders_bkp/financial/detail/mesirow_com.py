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


class mesirowDetail(FinancialDetailSpider):
    #logging.basicConfig(filename="hsbc.log", level=logging.INFO)
    #logging.info("InvestorFundsUSHSBCDetail")
    name = 'mesirow_com'

    
    def get_items_or_req(self, response, default_item={}):
        #logging.info("InvestorFundsUSHSBCDetail...get_items_or_req")
        #print("here....")
        
        items = super().get_items_or_req(response, default_item)
        #items = self.prepare_items(response, default_item)

        #print("gggg")
        #print("Items:",len(items))

        #open('a.html','w',encoding='utf-8').write(response.text)

        meta = response.meta
        
        meta['items'] = items



        
        #print(items)

        #print(response.text)

        selector = scrapy.Selector(text=response.text, type="html")

        connectinglink = selector.xpath("//iframe[@id='mf_mutualfunddata']/@src").get()

        #print("connectinglink:",connectinglink)

        fund_mgrs = selector.xpath("//article[contains(@about,'bio')]//h3/div/text() | //article[contains(@about,'bio')]//h3/text()").getall()

        print("fund_mgrs:",fund_mgrs)

        fund_managers_list = []

        Dict = {}
        for f in fund_mgrs:
            if len(f)>2:
                print("f:",f)
                Dict = dict([('fund_manager',f)])
                print("DICT:",Dict)


                fund_managers_list.append(Dict)


        meta['fund_managers_list'] = fund_managers_list








        yield scrapy.Request(connectinglink,method='GET',callback=self.getshareclassname,meta=meta,dont_filter=True)


    def getshareclassname(self,response):

        meta = response.meta

        #open('xx.html','w',encoding='utf-8').write(response.text)

        #bond_type = "Small Cap"

        json_data = re.search('\{\"bondType\"\:(.*)\"\}', response.text).group(0)

        loaded_json = json.loads(json_data)

        #print("yyy:",loaded_json['bondType'],loaded_json['bondType'].replace(' ','%20'))

        meta['fund_class_name'] = loaded_json['bondType']





        url = 'https://mesirowfinancial.secure.force.com/episerver/aura?r=0&other.GIMD_HY_.getBonds=1&other.GIMD_HY_.getDates=3&other.GIMD_HY_.getPerformance=1&other.GIMD_HY_.getShareClassDetails=1'

        headers = {
            "Connection": "keep-alive",
            "sec-ch-ua": "\"Google Chrome\";v=\"93\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"93\"",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
            "sec-ch-ua-platform": "\"Windows\"",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "Origin": "https://mesirowfinancial.secure.force.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://mesirowfinancial.secure.force.com/episerver/GIMD_SC_MobileReadyTables",
            "Accept-Language": "en-US,en;q=0.9,hi;q=0.8"
        }



        # we need to pass the Bond Type
        body = "message=%7B%22actions%22%3A%5B%7B%22id%22%3A%224%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FGIMD_HY_Controller%2FACTION%24getShareClassDetails%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AGIMD_MobileReady_ShareClassDetail%22%2C%22params%22%3A%7B%22bondType%22%3A%22"+loaded_json['bondType'].replace(' ','%20')+"%22%7D%2C%22version%22%3Anull%7D%2C%7B%22id%22%3A%225%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FGIMD_HY_Controller%2FACTION%24getDates%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AGIMD_MobileReady_ShareClassDetail%22%2C%22params%22%3A%7B%7D%2C%22version%22%3Anull%7D%2C%7B%22id%22%3A%2210%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FGIMD_HY_Controller%2FACTION%24getPerformance%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AGIMD_MobileReady_PerformanceTable%22%2C%22params%22%3A%7B%22bondType%22%3A%22"+loaded_json['bondType'].replace(' ','%20')+"%22%7D%2C%22version%22%3Anull%7D%2C%7B%22id%22%3A%2211%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FGIMD_HY_Controller%2FACTION%24getDates%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AGIMD_MobileReady_PerformanceTable%22%2C%22params%22%3A%7B%7D%2C%22version%22%3Anull%7D%2C%7B%22id%22%3A%2214%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FGIMD_HY_Controller%2FACTION%24getBonds%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AGIMD_MobileReady_HoldingCharacteristics%22%2C%22params%22%3A%7B%22bondType%22%3A%22"+loaded_json['bondType'].replace(' ','%20')+"%22%7D%2C%22version%22%3Anull%7D%2C%7B%22id%22%3A%2215%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FGIMD_HY_Controller%2FACTION%24getDates%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AGIMD_MobileReady_HoldingCharacteristics%22%2C%22params%22%3A%7B%7D%2C%22version%22%3Anull%7D%5D%7D&aura.context=%7B%22mode%22%3A%22PROD%22%2C%22fwuid%22%3A%22YeF9IbuOAuhiq8yQ65xJFA%22%2C%22app%22%3A%22c%3AGIMD_HY_MobileTablesApp%22%2C%22loaded%22%3A%7B%22APPLICATION%40markup%3A%2F%2Fc%3AGIMD_HY_MobileTablesApp%22%3A%22cMmVVs8dW5NqH1EGfWZOgg%22%7D%2C%22dn%22%3A%5B%5D%2C%22globals%22%3A%7B%7D%2C%22uad%22%3Atrue%7D&aura.pageURI=%2Fepiserver%2FGIMD_SC_MobileReadyTables&aura.token=undefined"

        #body = 'message=%7B%22actions%22%3A%5B%7B%22id%22%3A%224%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FGIMD_HY_Controller%2FACTION%24getShareClassDetails%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AGIMD_MobileReady_ShareClassDetail%22%2C%22params%22%3A%7B%22bondType%22%3A%22High%20Yield%22%7D%2C%22version%22%3Anull%7D%2C%7B%22id%22%3A%225%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FGIMD_HY_Controller%2FACTION%24getDates%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AGIMD_MobileReady_ShareClassDetail%22%2C%22params%22%3A%7B%7D%2C%22version%22%3Anull%7D%2C%7B%22id%22%3A%2210%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FGIMD_HY_Controller%2FACTION%24getPerformance%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AGIMD_MobileReady_PerformanceTable%22%2C%22params%22%3A%7B%22bondType%22%3A%22High%20Yield%22%7D%2C%22version%22%3Anull%7D%2C%7B%22id%22%3A%2211%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FGIMD_HY_Controller%2FACTION%24getDates%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AGIMD_MobileReady_PerformanceTable%22%2C%22params%22%3A%7B%7D%2C%22version%22%3Anull%7D%2C%7B%22id%22%3A%2214%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FGIMD_HY_Controller%2FACTION%24getBonds%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AGIMD_MobileReady_HoldingCharacteristics%22%2C%22params%22%3A%7B%22bondType%22%3A%22High%20Yield%22%7D%2C%22version%22%3Anull%7D%2C%7B%22id%22%3A%2215%3Ba%22%2C%22descriptor%22%3A%22apex%3A%2F%2FGIMD_HY_Controller%2FACTION%24getDates%22%2C%22callingDescriptor%22%3A%22markup%3A%2F%2Fc%3AGIMD_MobileReady_HoldingCharacteristics%22%2C%22params%22%3A%7B%7D%2C%22version%22%3Anull%7D%5D%7D&aura.context=%7B%22mode%22%3A%22PROD%22%2C%22fwuid%22%3A%22YeF9IbuOAuhiq8yQ65xJFA%22%2C%22app%22%3A%22c%3AGIMD_HY_MobileTablesApp%22%2C%22loaded%22%3A%7B%22APPLICATION%40markup%3A%2F%2Fc%3AGIMD_HY_MobileTablesApp%22%3A%22cMmVVs8dW5NqH1EGfWZOgg%22%7D%2C%22dn%22%3A%5B%5D%2C%22globals%22%3A%7B%7D%2C%22uad%22%3Atrue%7D&aura.pageURI=%2Fepiserver%2FGIMD_HY_MobileReadyTables&aura.token=undefined'
        request = scrapy.Request(
            url=url,
            method='POST',
            dont_filter=True,
            headers=headers,
            body=body,
            callback=self.distributions,
            meta=meta
        )
        
        # yield scrapy.Request('https://mesirowfinancial.secure.force.com/episerver/GIMD_SC_MobileReadyTables',method='GET',callback=self.distributions,meta=meta,dont_filter=True)

        yield request
      
     

    def distributions(self,response):


        

        meta = response.meta

        fund_class_name = meta['fund_class_name']

        #open(fund_class_name+'.html','w',encoding='utf-8').write(response.text)


        #print("ddddd")

        #items = meta['items']

        #print(items)

        loaded_json = json.loads(response.text)

        print("hello:",loaded_json['actions'][0]['returnValue'])

        for j in loaded_json['actions'][0]['returnValue']:
            #print(j['Share_Class_Type__c'])



            item = meta['items']
            print(item)

            item_copy = copy.deepcopy(item)

            item_copy[0]['share_class'] = j['Share_Class_Type__c']
            item_copy[0]['cusip'] = j['CUSIP__c']
            item_copy[0]['nasdaq_ticker'] = j['Symbol__c']
            item_copy[0]['management_fee'] = str(j['Management_Fee__c'])+str("%")
            item_copy[0]['total_expense_gross'] = str(j['Gross_Expenses__c'])+str("%")
            item_copy[0]['total_expense_net'] = str(j['Net_Expenses__c'])+str("%")
            item_copy[0]['minimum_initial_investment'] = str(j['Min_Inv__c'])
            item_copy[0]['fund_managers'] = meta['fund_managers_list']


            #print("xxxx:",item_copy['share_class'])



            

            yield self.generate_item(item_copy[0], FinancialDetailItem)










        


       






    