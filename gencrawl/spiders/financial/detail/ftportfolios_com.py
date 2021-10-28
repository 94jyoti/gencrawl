from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import requests
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
import json
import urllib.parse
from copy import deepcopy


class FtportfoliosComDetail(FinancialDetailSpider):
    name = 'financial_detail_ftportfolios_com'
    custom_settings = {
        "HTTPCACHE_ENABLED": True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 4,
        "COOKIES_ENABLED": True,
        "CRAWLERA_ENABLED": False
    }

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        for i in items:
            nasdaq_ticker = i['nasdaq_ticker']
            url = "https://www.ftportfolios.com/Retail/MF/MFDividHistory.aspx?Ticker=" + nasdaq_ticker
            meta = response.meta
            meta['item'] = i
           
            
            resp = self.make_request(url, callback=self.parse_distribution, meta=meta)
            return resp

    def parse_distribution(self, response):
        meta = response.meta
        item = meta['item']
        years_list = response.xpath("//select[@id='ContentPlaceHolder1_DistributionHistory_ddlDistributionHistoryYearSelection']/option/@value").getall()
        meta['years_list'] = years_list

        distribution_data_final = []
        meta['distribution_data_final'] = distribution_data_final
        distribution_data = []
        meta['distribution_data'] = distribution_data
        
        for year in years_list:
            tmeta = deepcopy(meta)
            meta['year'] = year
            
            view_state_param = response.xpath("//input[@id='__VIEWSTATE']/@value").get()
            event_validation = response.xpath("//input[@id='__EVENTVALIDATION']/@value").get()
            prev_page = response.xpath("//input[@id='__PREVIOUSPAGE']/@value").get()
            view_stat_gen = response.xpath("//input[@id='__VIEWSTATEGENERATOR']/@value").get()
            body = {'ctl00$ScriptManager1': 'ctl00$ContentPlaceHolder1$DistributionHistory$upDistributionHistory|ctl00$ContentPlaceHolder1$DistributionHistory$btnSubmit',
                    'ScriptManager1_HiddenField':'',
                    'ctl00$SearchControl$txtProductSearch':'',
                    'hidProductSearchControlID': 'ctl00$SearchControl$txtProductSearch',
                    'ctl00$ContentPlaceHolder1$DistributionHistory$ddlDistributionHistoryYearSelection': year,
                    '__EVENTTARGET': '',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': view_state_param,
                    '__VIEWSTATEGENERATOR': view_stat_gen,
                    '__PREVIOUSPAGE': prev_page,
                    '__EVENTVALIDATION': event_validation,
                    'ctl00$ContentPlaceHolder1$DistributionHistory$btnSubmit': 'List Distribution History',
                    '__ASYNCPOST': True,
                    'ctl00$SearchControl$txtProductSearch': '',
                    'ctl00$ContentPlaceHolder1$DistributionHistory$txtMinDate': '',
                    'ctl00$ContentPlaceHolder1$DistributionHistory$txtMaxDate': '',
                    '__VIEWSTATEENCRYPTED':''
                }
            yield scrapy.Request(response.url,
                                 headers={'X-MicrosoftAjax':'Delta=true', 'X-Requested-With': 'XMLHttpRequest',
                                          'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                                          'X-MicrosoftAjax': 'Delta=true', "Referer": response.url, "Accept": "*/*"},
                                 body=urllib.parse.urlencode(body), method='POST', dont_filter=True,
                                 callback=self.parse_dividends, meta=meta)

    def parse_dividends(self, response):
        meta = response.meta
        item = meta['item']
        year = meta['year']


       
        distribution_data = meta['distribution_data']
        distribution_data_final = meta['distribution_data_final']
        years_list = meta['years_list']
        item = meta['item']
       
        

        for tr_block in response.xpath("//table[@class='fundSilverGrid']//tr[position()>1]"):
            cg_record_date =tr_block.xpath("td[3]/text()").get().strip()
            cg_ex_date =tr_block.xpath("td[2]/text()").get().strip()
            cg_pay_date =tr_block.xpath("td[4]/text()").get().strip()
            per_share = tr_block.xpath("td[5]/text()").get().strip()

            #print("xx:",year,cg_record_date)


            #data_dict1={"cg_ex_date": "", "cg_record_date": "", "cg_pay_date": "", "short_term_per_share": "","long_term_per_share": "", "total_per_share": "", "cg_reinvestment_price": ""}
            data_dict2={"ex_date": cg_ex_date, "pay_date": cg_pay_date, "ordinary_income": "", "qualified_income": "", "record_date": cg_record_date,"per_share": per_share, "reinvestment_price": ""}
            #capital_gains.append(data_dict1)
            
            distribution_data.append(data_dict2)
            #print("xx:",len(distribution_data))
        #distribution_data.append(temp_dist_list)

        distribution_data_final.append(distribution_data)
        #print("yy:",len(distribution_data_final))
        

             
        #item['capital_gains'] = capital_gains
        
        #final_item.append(item)
        print("xx:",len(distribution_data_final),len(years_list))
        if len(distribution_data_final)==len(years_list):
            item['dividends'] = distribution_data_final[-1]
            yield self.generate_item(item, FinancialDetailItem)

