from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import requests
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
import json
import urllib.parse


class FtportfoliosComDetail(FinancialDetailSpider):
    name = 'financial_detail_ftportfolios_com'
    custom_settings = {
        "HTTPCACHE_ENABLED": False,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 4,
        "COOKIES_ENABLED": True,
        "COOKIES_DEBUG": True
    }

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)


        #print("items:",items)

        for i in items:
            #print(i)
            nasdaq_ticker = i['nasdaq_ticker']
            print("nasdaq_ticker:",nasdaq_ticker)
            url = "https://www.ftportfolios.com/Retail/MF/MFDividHistory.aspx?Ticker="+nasdaq_ticker
            meta = response.meta
            meta['item'] = i
            resp = self.make_request(url, callback=self.parse_distribution, meta=meta)
            return resp


    def parse_distribution(self, response):
        meta = response.meta
        item = meta['item']
        open('ftport.html', 'w').write(response.text)
        print("inside parse_distribution")
        # Extracting ticker and cusip from home page
        # import pdb;pdb.set_trace()
        years_list = response.xpath("//select[@id='ContentPlaceHolder1_DistributionHistory_ddlDistributionHistoryYearSelection']/option/@value").getall()
        print("years_list:",years_list)
        url  =  response.url
        print(url)

        capital_gain_list=[]
        dividends_list=[]

        years_list=['2011']

        for year in years_list:
            print(year)

            # url = 'https://www.ftportfolios.com/Retail/MF/MFDividHistory.aspx?Ticker=FPEAX'
            view_state_param = response.xpath("//input[@id='__VIEWSTATE']/@value").get()
            #print(view_state_param)
            event_validation = response.xpath("//input[@id='__EVENTVALIDATION']/@value").get()
            #print(event_validation)
            prev_page = response.xpath("//input[@id='__PREVIOUSPAGE']/@value").get()
            #print(prev_page)
            view_stat_gen = response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").get()
            #print(view_stat_gen)
            #hid_prod_search_id = response.xpath("/input[@id='hidProductSearchControlID']/@value").get()
            yield scrapy.Request(url,\
                                headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
                                'X-MicrosoftAjax':'Delta=true',\
                                'X-Requested-With':'XMLHttpRequest',\
                                'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                                'X-MicrosoftAjax': 'Delta=true',"Referer":"https://www.ftportfolios.com/Retail/MF/MFDividHistory.aspx?Ticker=FPEAX","Origin":"https://www.ftportfolios.com","Host": "www.ftportfolios.com",'Connection': 'keep-alive','Accept-Encoding':'gzip, deflate, br',"Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8","Cache-Control": "no-cache","Accept": "*/*"

                                },
                                
                                body=urllib.parse.urlencode({'ctl00$ScriptManager1': 'ctl00$ContentPlaceHolder1$DistributionHistory$upDistributionHistory|ctl00$ContentPlaceHolder1$DistributionHistory$btnSubmit',

                                'ScriptManager1_HiddenField':'',
                                'ctl00$SearchControl$txtProductSearch':'',
                                'hidProductSearchControlID': 'ctl00$SearchControl$txtProductSearch',
                                'ctl00$ContentPlaceHolder1$DistributionHistory$ddlDistributionHistoryYearSelection': year,
                                '__EVENTTARGET':'',
                                '__EVENTARGUMENT':'',
                                '__VIEWSTATE':view_state_param,
                                '__VIEWSTATEGENERATOR':view_stat_gen,
                                '__PREVIOUSPAGE':prev_page,
                                '__EVENTVALIDATION':event_validation,
                                'ctl00$ContentPlaceHolder1$DistributionHistory$btnSubmit':'List Distribution History',
                                '__ASYNCPOST':'True',
                                'ctl00$SearchControl$txtProductSearch':'',
                                'ctl00$ContentPlaceHolder1$DistributionHistory$txtMinDate':'',
                                'ctl00$ContentPlaceHolder1$DistributionHistory$txtMaxDate':'',
                                '__VIEWSTATEENCRYPTED':''
                                }),method='POST',dont_filter=True,callback=self.dividends)




    def dividends(self,response):
        open('testing.html', 'w').write(response.text)