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
    name = 'financial_detail_federatedinvestors_com'
    custom_settings = {
        "COOKIES_ENABLED": True,
        "COOKIES_DEBUG": True
    }

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        meta = response.meta
        meta['item'] = items[0]
        selector = scrapy.Selector(text=response.text, type="html")
        tokenw = selector.xpath("//input[@id='tokenW']/@value").get()
        shareclassid = selector.xpath("//input[@id='shareclassid']/@value").get()
        fundbasketid = selector.xpath("//input[@id='fundbasketid']/@value").get()
        characteristicDate = selector.xpath("//input[@id='characteristicDate']/@value").get()
        distributionsDate = selector.xpath("//select[@id='distributionsDate']/option/text()").getall()
        
        print("distributionsDate:",distributionsDate)
        meta['distributionsDate'] = distributionsDate
        parsed_tokenw = urllib.parse.urlencode({"tokenW":tokenw})
        headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        }
        cookies = {"JSESSIONID": "0000YAhqWvQJ-LLoWvAY3skBWvo:1doueinte"}
        temp_dict ={}
        temp_dict['shareclassid'] = shareclassid
        temp_dict['fundbasketid'] = fundbasketid
        temp_dict['characteristicDate'] = characteristicDate
        temp_dict['parsed_tokenw'] = parsed_tokenw
        temp_dict['headers'] = headers
        meta['temp_dict'] = temp_dict

        #for item in items:

        #    yield self.generate_item(item, FinancialDetailItem)


        # for Portfolio Profile data
        #body='characteristicDate='+characteristicDate+'&&distributionsDate=2021&fundbasketid='+fundbasketid+'&shareclassid='+shareclassid+'&managedaccountid=&compositeid=&section=section-characteristics-portfolio-profile&tab=&'+parsed_tokenw+'&bonyClient=false'
        #yield scrapy.Request("https://www.federatedinvestors.com/products/product.do",method='POST',body = body,headers=headers,callback=self.get_portfolio_profile,dont_filter=True,meta=meta)


        # for 30 day yield
        #body='performanceReturnsAnnualizedReturnType=BT&characteristicDate='+characteristicDate+'&dafType=-1&fundbasketid='+fundbasketid+'&shareclassid='+shareclassid+'&managedaccountid=&compositeid=&section=&tab=tab-panel-yields&'+parsed_tokenw+'&bonyClient=false'
        #print("body:",body)
        #yield scrapy.Request("https://www.federatedinvestors.com/products/product.do",method='POST',body = body,headers=headers,callback=self.day_yield_details,dont_filter=True,meta=meta)

        
        # for Portfolio asset and Net  asset
        #body = "characteristicDate="+characteristicDate+"&distributionsDate=2021&fundbasketid="+fundbasketid+"&shareclassid="+shareclassid+"&managedaccountid=&compositeid=&section=section-characteristics-assets&tab=&"+parsed_tokenw+"&bonyClient=false"

        #yield scrapy.Request("https://www.federatedinvestors.com/products/product.do",method='POST',body = body,headers=headers,callback=self.get_portfolio_net_asset,dont_filter=True,meta=meta)

        
        
        distribution_data = []
        capital_gain_list = []
        final_item = []
        meta['distribution_data'] = distribution_data
        meta['capital_gain_list'] = capital_gain_list
        meta['final_item'] = final_item


        for dist_year in distributionsDate:

            #for Distribution Data
            #body = "characteristicDate="+characteristicDate+"&distributionsDate="+dist_year+"&fundbasketid="+fundbasketid+"&shareclassid="+shareclassid+"&managedaccountid=&compositeid=&section=section-distributions-income-tax&tab=tab-panel-distributions&"+parsed_tokenw+"&bonyClient=false"
            #yield scrapy.Request("https://www.federatedinvestors.com/products/product.do",method='POST',body = body,headers=headers,callback=self.distribution_data,dont_filter=True,meta=meta)

           

            # for Capital gains Data
            #body = "characteristicDate="+characteristicDate+"&distributionsDate=2021&fundbasketid="+fundbasketid+"&shareclassid="+shareclassid+"&managedaccountid=&compositeid=&section=section-distributions-income-tax&tab=tab-panel-distributions&"+parsed_tokenw+"&bonyClient=false"
            body = "performanceReturnsAnnualizedFrom=06-30-2021&performanceReturnsAnnualizedTo=08-31-2021&performanceReturnsAnnualizedReturnType=BT&ec-input__time-period-radio=EarliestCommon&ec-input__radio-button-subsequent-investment=Invest&ec-input__investment-type=Monthly&ec-input__fees=Annually&ec-input__pay-fees=OutOfPocketEnding&ec-input__radio-button-front-load=Standard&ec-hypothetical-growth-hypo-reinvest-chosen-button-name=reinvestDividends&ec-hypothetical-growth-hypo-reinvest-chosen-button-name=reinvestCapitalGains&ec-input__radio-button-filing-status=NoTaxes&ec-input__radio-button-pay=OutOfPocket&ec-input__radio-button-frequency=Monthly&ec-hypothetical-growth-hypo-report-builder-report-contents-button-name=coverPage&ec-hypothetical-growth-hypo-report-builder-report-contents-button-name=historicalPerformance&ec-hypothetical-growth-hypo-report-builder-report-contents-button-name=disclosure&characteristicDate="+characteristicDate+"&dafType=-1&distributionsDate="+dist_year+"&fundbasketid="+fundbasketid+"&shareclassid="+shareclassid+"&managedaccountid=&compositeid=&section=&tab=tab-panel-capital-gains&"+parsed_tokenw+"&bonyClient=false"
            yield scrapy.Request("https://www.federatedinvestors.com/products/product.do",method='POST',body = body,headers=headers,callback=self.capital_gain_data,dont_filter=True,meta=meta)
            


    def day_yield_details(self,response):

        meta = response.meta
        item = meta['item']
        temp_dict = meta['temp_dict']

        nasdaq_ticker = item['nasdaq_ticker']
        data_block = []
        for block in response.xpath("//table[@id='performance-returns-yield-table']//tr"):
            td_block_list= []
            for td_block in block.xpath("th/span"):
                td_value = td_block.xpath("text()").get()
                td_block_list.append(td_value)
            for td_block in block.xpath("td"):
                td_value = td_block.xpath("text()").get()
                td_block_list.append(td_value)
            for td_block in block.xpath("td"):
                td_value = td_block.xpath("time/@datetime").get()
                td_block_list.append(td_value)
            data_block.append(td_block_list)

        sec_yield_30_day = response.xpath("//table[@id='performance-returns-yield-table']//tr[1]/td[3]/text()").get()
        sec_yield_date_30_day = response.xpath("//table[@id='performance-returns-yield-table']//tr[1]/td[1]/time/@datetime").get()
        sec_yield_without_waivers_30_day = response.xpath("//table[@id='performance-returns-yield-table']//tr[1]/td[5]/text()").get()
        sec_yield_without_waivers_date_30_day = response.xpath("//table[@id='performance-returns-yield-table']//tr[1]/td[1]/time/@datetime").get()

        if len(data_block)>0:
            if data_block[0][3].strip()=='30-DAY':
                item['sec_yield_30_day'] = sec_yield_30_day
                item['sec_yield_date_30_day'] = sec_yield_date_30_day
                item['sec_yield_without_waivers_30_day'] = sec_yield_without_waivers_30_day
                item['sec_yield_without_waivers_date_30_day'] = sec_yield_without_waivers_date_30_day

            if data_block[0][3].strip()=='7-DAY':
                item['sec_yield_7_day'] = sec_yield_30_day
                item['sec_yield_date_7_day'] = sec_yield_date_30_day
       
        yield self.generate_item(item, FinancialDetailItem)

        #body='haracteristicDate='+characteristicDate+'&distributionsDate=2021&fundbasketid='+fundbasketid+'&shareclassid='+shareclassid+'&managedaccountid=&compositeid=&sectiom=section-characteristics-assets&'+parsed_tokenw+'&bonyClient=false'
        #body='characteristicDate=09-22-2021&distributionsDate=2021&fundbasketid=223&shareclassid=16251&managedaccountid=&compositeid=&section=section-characteristics-assets&tab=&tokenW=MTYzMjQxNTczNTk0Nzo1ODU1ODc5NzM%3D&bonyClient=false'
        #yield scrapy.Request("https://www.federatedinvestors.com/products/product.do",method='POST',body = body,headers=headers,callback=self.final_distributions,dont_filter=True,meta=meta)

    def get_portfolio_net_asset(self,response):
        meta = response.meta
        item = meta['item']
        ticker = item['nasdaq_ticker']
        share_class = item['share_class']
        portfolio_assets = response.xpath("(//td[@headers='assets-monthly-header']/span)[2]/text()").get()
        portfolio_assets_date = response.xpath("//span[contains(text(),'MONTHLY')]/time/span/text()").get()
        item['portfolio_assets'] = portfolio_assets
        item['portfolio_assets_date'] = portfolio_assets_date
        total_net_assets = response.xpath("(//td[@headers='assets-monthly-header']/span)[4]/text()").get()
        total_net_assets_date = portfolio_assets_date
        item['total_net_assets'] = total_net_assets
        item['total_net_assets_date'] = total_net_assets_date
        yield self.generate_item(item, FinancialDetailItem)

    def distribution_data(self,response):
        meta = response.meta
        final_item = meta['final_item']
        item = meta['item']
        distribution_data = meta['distribution_data']
        ticker = item['nasdaq_ticker']
        
       

        for tr_block in response.xpath("//table/tbody/tr"):
            record_date =tr_block.xpath("td[2]/text()").get()
            ex_date =tr_block.xpath("td[3]/time/@datetime").get()
            pay_date =tr_block.xpath("td[4]/time/@datetime").get()
            per_share = tr_block.xpath("td[6]/text()").get()


           

            data_dict2={"ex_date": ex_date, "pay_date": pay_date, "ordinary_income": "", "qualified_income": "", "record_date": record_date,"per_share": per_share, "reinvestment_price": ""}
            distribution_data.append(data_dict2)

       

        item['dividends'] = distribution_data
        distributionsDate = meta['distributionsDate']
        final_item.append(item)

        print("xx:",len(final_item),len(distributionsDate))
        if len(final_item) == len(distributionsDate):
            if len(item['dividends'])==0:
                file1 = open("federated_missing_data_urls_dividends.txt","a")
                file1.write(item['fund_url']+"\n")
            else:
                yield self.generate_item(item, FinancialDetailItem)

    def capital_gain_data(self,response):
        meta = response.meta
        final_item = meta['final_item']
        item = meta['item']
        ticker = item['nasdaq_ticker']
        distributionsDate = meta['distributionsDate']
        capital_gain_list = meta['capital_gain_list']
        status=False

        for tr_block in response.xpath("//table/tbody/tr"):
            cg_record_date =tr_block.xpath("td[2]/time/@datetime").get()
            cg_ex_date =tr_block.xpath("td[3]/time/@datetime").get()
            cg_pay_date =tr_block.xpath("td[4]/time/@datetime").get()
            short_term_per_share = tr_block.xpath("td[6]/text()").get()
            long_term_per_share = tr_block.xpath("td[7]/text()").get()
            total_capital_gains = tr_block.xpath("td[8]/text()").get()
            
            

            data_dict1={"cg_ex_date": cg_ex_date, "cg_record_date": cg_record_date, "cg_pay_date": cg_pay_date, "short_term_per_share": short_term_per_share,"long_term_per_share": long_term_per_share, "total_per_share": total_capital_gains, "cg_reinvestment_price": ""}
            capital_gain_list.append(data_dict1)
        
      
               

        item['capital_gains'] = capital_gain_list
        final_item.append(item)

        print("yy:",len(final_item),len(distributionsDate))
        if len(final_item) == len(distributionsDate):
            if len(item['capital_gains'])==0:
                file1 = open("federated_missing_data_urls_CapitalGains.txt","a")
                file1.write(item['fund_url']+"\n")
                yield self.generate_item(item, FinancialDetailItem)
            else:

                yield self.generate_item(item, FinancialDetailItem)

    def get_portfolio_profile(self,response):

        meta = response.meta
        item = meta['item']
        ticker = item['nasdaq_ticker']
        share_class = item['share_class']
        
        weighted_average_duration = response.xpath("//td[contains(text(),'Weighted Average Effective Duration')]/following-sibling::td/span/text()").get()
        weighted_average_duration_as_of_date = response.xpath("//table[@id='portfolio-profile']/caption/time/span/text()").get()
        average_weighted_maturity = response.xpath("(//span[contains(text(),'Weighted Average Maturity')]/following::span[1])[1]/text()").get()
        average_weighted_maturity_as_of_date = response.xpath("//table[@id='portfolio-profile-monthly']/caption/time/span/text()").get()
        average_weighted_effective_maturity = response.xpath("//td[contains(text(),' Weighted Average Effective Maturity ')]/following-sibling::td/span/text()").get()
        average_weighted_effective_maturity_as_of_date = response.xpath("//table[@id='portfolio-profile']/caption/time/span/text()").get()

        item['weighted_average_duration'] = weighted_average_duration
        item['weighted_average_duration_as_of_date'] = weighted_average_duration_as_of_date
        item['average_weighted_maturity'] = average_weighted_maturity
        item['average_weighted_maturity_as_of_date'] = average_weighted_maturity_as_of_date
        item['average_weighted_effective_maturity'] = average_weighted_maturity
        item['average_weighted_effective_maturity_as_of_date'] = average_weighted_maturity_as_of_date

        yield self.generate_item(item, FinancialDetailItem)

        
        