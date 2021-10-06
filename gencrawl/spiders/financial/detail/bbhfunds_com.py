from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import requests
from lxml import html


class BbhfundsfundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_bbhfunds_com'
    # custom_settings = {
    #     "RETRY_TIMES": 5,
    #     "CRAWLERA_ENABLED": True
    # }
    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        container_id = response.xpath("//div[contains(@id,'distribution_copy')]/@id"\
                        ).extract()[0].split('container_')[1].split('distribution')[0]
        years_list = response.xpath("//label[contains(text(),'Date as of')]/following-sibling::select[@name='AsOfDate']/option/@value").extract()
        check_ex_date = response.xpath("//li[div[contains(text(),'Dividend')]]/div[1]/text()")
        if check_ex_date:
            for i in range(len(items)):
                dividends = []
                capital_gains = []
                
                for year in years_list:
                    share_class = items[i]['share_class']
                    distribution_url = response.url+"/jcr:content/root/container/container/container_"+\
                                        str(container_id)+"/distribution_copy.html?hideFilter=true&ShareClass="+share_class+\
                                        '&AsOfDate='+str(year)
                    resp = requests.get(distribution_url)
                    
                    tree = html.fromstring(resp.text)
                    
                    ex_date = tree.xpath("//li[div[contains(text(),'Dividend')]]/div[1]/text()")[0].replace('\n','').strip()
                    record_date = tree.xpath("//li[div[contains(text(),'Record Date')]]/div[1]/text()")[0].replace('\n','').strip()
                    pay_date = tree.xpath("//li[div[contains(text(),'Payable')]]/div[1]/text()")[0].replace('\n','').strip()
                    cg_pay_date = pay_date
                    cg_ex_date = ex_date
                    cg_record_date = record_date

                    total_td_len = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td")
                    if len(total_td_len) == 7:
                        per_share = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td[6]/text()")[0].replace('\n','').strip()
                        reinvestment_price = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td[7]/text()")[0].replace('\n','').strip()
                        cg_reinvestment_price = reinvestment_price
                        total_per_share = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td[5]/text()")[0].replace('\n','').strip()
                        cg_long_term_per_share = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td[4]/text()")[0].replace('\n','').strip()
                        cg_short_term_per_share = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td[3]/text()")[0].replace('\n','').strip()
                    else:
                        check_reinv = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td[8]/text()")[0].replace('\n','').strip()
                        if check_reinv:
                            per_share = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td[7]/text()")[0].replace('\n','').strip()
                            reinvestment_price = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td[8]/text()")[0].replace('\n','').strip()
                            cg_reinvestment_price = reinvestment_price
                            total_per_share = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td[6]/text()")[0].replace('\n','').strip()
                            cg_long_term_per_share = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td[5]/text()")[0].replace('\n','').strip()
                            cg_short_term_per_share = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td[3]/text()")[0].replace('\n','').strip()
                        else:
                            per_share = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td[6]/text()")[0].replace('\n','').strip()
                            reinvestment_price = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td[7]/text()")[0].replace('\n','').strip()
                            cg_reinvestment_price = reinvestment_price
                            total_per_share = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td[5]/text()")[0].replace('\n','').strip()
                            cg_long_term_per_share = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td[4]/text()")[0].replace('\n','').strip()
                            cg_short_term_per_share = tree.xpath("//thead[tr[th[contains(text(),'Share Class/ Ticker')]]]/following-sibling::tbody/tr[1]/td[3]/text()")[0].replace('\n','').strip()

                    divident_dict = {'ex_date':ex_date, 'pay_date':pay_date,\
                                            'per_share':per_share,
                                            'reinvestment_price':reinvestment_price,\
                                            'record_date':record_date}

                    capital_gains_dict = {'cg_ex_date':cg_ex_date, 'cg_pay_date':cg_pay_date,\
                                        'short_term_per_share':cg_short_term_per_share,\
                                        'long_term_per_share':cg_long_term_per_share,\
                                        'total_per_share':total_per_share,\
                                        'cg_reinvestment_price':cg_reinvestment_price,\
                                        'cg_record_date':cg_record_date}
                    
                    dividends.append(divident_dict)
                    capital_gains.append(capital_gains_dict)
                    items[i]['dividends'] = dividends
                    items[i]['capital_gains'] = capital_gains
        return items
        