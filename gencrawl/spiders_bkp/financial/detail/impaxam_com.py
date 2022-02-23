from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics
import re
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider


class impaxamDetail(FinancialDetailFieldMapSpider):
    name = 'impaxam_com'
    custom_settings = {
        "HTTPCACHE_ENABLED": False
        
    }

    def get_items_or_req(self, response, default_item={}):
        meta = response.meta

        items = self.prepare_items(response, default_item)

        
        for item in items:

            meta['item']=item

            url = item['fund_url']

            print("URL:",url)


            headers = {
                "authority": "impaxam.com",
                "cache-control": "max-age=0",
                "sec-ch-ua": "\\",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\\",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "sec-fetch-site": "none",
                "sec-fetch-mode": "navigate",
                "sec-fetch-user": "?1",
                "sec-fetch-dest": "document",
                "accept-language": "en-US,en;q=0.9,hi;q=0.8"
            }

            cookies = {
                "_gcl_au": "1.1.1932262537.1634703598",
                "_mkto_trk": "id:488-YOI-759&token:_mch-impaxam.com-1634703598121-97342",
                "_ga": "GA1.2.1489582936.1634703598",
                "_gid": "GA1.2.631527979.1634703598",
                "investor_country": "united-states",
                "investor_type": "institutional-investor",
                "investor_label": "Institutional%20Investor",
                "share_class": "sterling-a-accumulation"
            }

            yield scrapy.Request(url,headers=headers,cookies=cookies,callback=self.parse_distribution,dont_filter=True,meta=meta)

    def parse_distribution(self,response):
        meta = response.meta
        item = meta['item']
       

        share_classes = response.xpath("//select[@name='ClassSelect']/option/text()").getall()
        tickers = response.xpath("//div[contains(text(),'Symbol')]/following-sibling::div/text()").getall()
        print("share_classes:",share_classes,tickers)
        for c,ticker in enumerate(tickers):

            meta['ticker'] = ticker
            meta['share_class'] = share_classes[c]
            url = "https://impaxam.com/customer-service/distributions/"

            headers = {
                "authority": "impaxam.com",
                "cache-control": "max-age=0",
                "sec-ch-ua": "\\",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\\",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "sec-fetch-site": "none",
                "sec-fetch-mode": "navigate",
                "sec-fetch-user": "?1",
                "sec-fetch-dest": "document",
                "accept-language": "en-US,en;q=0.9,hi;q=0.8"
            }

            cookies = {
                "_gcl_au": "1.1.1932262537.1634703598",
                "_mkto_trk": "id:488-YOI-759&token:_mch-impaxam.com-1634703598121-97342",
                "_ga": "GA1.2.1489582936.1634703598",
                "_gid": "GA1.2.631527979.1634703598",
                "investor_country": "united-states",
                "investor_type": "institutional-investor",
                "investor_label": "Institutional%20Investor",
                "share_class": "sterling-a-accumulation"
            }

            yield scrapy.Request(url,headers=headers,cookies=cookies,callback=self.parse_distribution_2,dont_filter=True,meta=meta)

    def parse_distribution_2(self,response):
        meta = response.meta
        item= meta['item']

        ticker = meta['ticker']
        share_class = meta['share_class']

        item['nasdaq_ticker'] = ticker
        item['share_class']=share_class

        open('impaxam.html','w',encoding='utf-8').write(response.text)

        years = response.xpath("//div[@class='tab-label' or @class='tab-label active']/text()").getall()

        capital_gain_list = []
        dividends_list = []
        for data in response.xpath("//div[@class='tab-content--html']"):
            for heading in data.xpath("h2"):
                headingtext = heading.xpath("text()").get()
                print("heading:",headingtext)

                for table_data in heading.xpath("following-sibling::table[1]"):
                    print(table_data)
                    for tr_block in table_data.xpath("tbody/tr"):
                        #print(tr_block)
                        if tr_block.xpath("td[2]/text()").get() is not None:
                            ticker = tr_block.xpath("td[2]/text()").get().strip()
                        ordinary_income = tr_block.xpath("td[3]/text()").get()
                        short_term_per_share = tr_block.xpath("td[4]/text()").get()
                        long_term_per_share = tr_block.xpath("td[5]/text()").get()
                        total_capital_gain_rate = tr_block.xpath("td[6]/text()").get()

                        print([ticker,ordinary_income,short_term_per_share,long_term_per_share,total_capital_gain_rate])
                        #if ticker==item['nasdaq_ticker']:
                        if ticker==item['nasdaq_ticker']:
                            print("xx:",ticker,item['nasdaq_ticker'])
                            data_dict1={"cg_ex_date": headingtext, "cg_record_date": "", "cg_pay_date": "", "short_term_per_share": short_term_per_share,"long_term_per_share": long_term_per_share, "total_per_share": total_capital_gain_rate, "cg_reinvestment_price": ""}
                            data_dict2={"ex_date": headingtext, "pay_date": "", "ordinary_income": ordinary_income, "qualified_income": "", "record_date": "","per_share": "", "reinvestment_price": ""}
                                    
                            capital_gain_list.append(data_dict1)
                            dividends_list.append(data_dict2)
                            print(data_dict1)
                            print(data_dict2)

        item['capital_gains']=capital_gain_list
        item['dividends']=dividends_list
        yield self.generate_item(item, FinancialDetailItem)

