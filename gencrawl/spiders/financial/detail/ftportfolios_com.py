from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import requests


class FtportfoliosComDetail(FinancialDetailSpider):
    name = 'financial_detail_ftportfolios_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        # import pdb;pdb.set_trace()
        url = 'https://www.ftportfolios.com'+response.xpath('//a[contains(text(),"Distribution History")]/@href').extract()[0]
        meta = response.meta
        meta['items'] = items
        resp = self.make_request(url, callback=self.parse_distribution, meta=meta)
        return resp


    def parse_distribution(self, response):
        # Extracting ticker and cusip from home page
        # import pdb;pdb.set_trace()
        years_list = response.xpath("//select[@id='ContentPlaceHolder1_DistributionHistory_ddlDistributionHistoryYearSelection']/option/@value").extract()
        url  =  response.url
        # url = 'https://www.ftportfolios.com/Retail/MF/MFDividHistory.aspx?Ticker=FPEAX'
        view_state_param = response.xpath("/input[@id='__VIEWSTATE']/@value").extract()[0]
        event_validation = response.xpath("/input[@id='__EVENTVALIDATION']/@value").extract()[0]
        prev_page = response.xpath("/input[@id='__PREVIOUSPAGE']/@value").extract()[0]
        view_stat_gen = response.xpath("/input[@id='__VIEWSTATEGENERATOR']/@value").extract()[0]
        hid_prod_search_id = response.xpath("/input[@id='hidProductSearchControlID']/@value").extract()[0]
        resp = requests.post(url,\
                            headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
                            'X-MicrosoftAjax':'Delta=true',\
                            'X-Requested-With':'XMLHttpRequest',\
                            'Content-Type':'application/json',
                            'Cookie':'__utmz=86768719.1629201177.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ASP.NET_SessionId=1hdbscvp00epx4vvbgi5q1gg; __utmc=86768719; __utma=86768719.1519675452.1629201177.1629275010.1629288303.4; __utmt=1; __utmt_b=1; __utmb=86768719.2.10.1629288303'}, \
                            
                            data={'ctl00$ScriptManager1': 'ctl00$ContentPlaceHolder1$DistributionHistory$upDistributionHistory|ctl00$ContentPlaceHolder1$DistributionHistory$btnSubmit', \
                            'hidProductSearchControlID': hid_prod_search_id, \
                            'ctl00$ContentPlaceHolder1$DistributionHistory$ddlDistributionHistoryYearSelection': 2017,\
                            # '__VIEWSTATE':view_state_param,
                            '__VIEWSTATEGENERATOR':view_stat_gen,
                            # '__PREVIOUSPAGE':prev_page,
                            '__EVENTVALIDATION':event_validation,
                            'ctl00$ContentPlaceHolder1$DistributionHistory$btnSubmit':'List Distribution History',
                            '__ASYNCPOST':True,
                            'ctl00$SearchControl$txtProductSearch':'',
                            'ctl00$ContentPlaceHolder1$DistributionHistory$txtMinDate':'',
                            'ctl00$ContentPlaceHolder1$DistributionHistory$txtMaxDate':'',
                            '__VIEWSTATEENCRYPTED':''
                            })
        print(resp.status_code, resp.reason)
        # import pdb;pdb.set_trace()
        # dist_table = resp.xpath('//table[@class = "fundSilverGrid"]//tr').extract()
        # items = response.meta['items']
        