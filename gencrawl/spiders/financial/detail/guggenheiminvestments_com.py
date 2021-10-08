from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics

class GuggenheimComDetail(FinancialDetailSpider):
    name = 'financial_detail_guggenheim_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        for row in response.xpath("//h3[contains(text(),'Symbols & CUSIPs')]//following::table[1]//tbody//tr"):
            temp_class=row.xpath(".//td[1]//text()").extract()[0].strip()
            if(items[0]['share_class'].lower().replace("class","").strip() in temp_class):
                items[0]['cusip']=row.xpath(".//td[3]//text()").extract()[0]
                items[0]['share_inception_date']=row.xpath(".//td[4]//text()").extract()[0]
        distribution_url = items[0]['fund_url'] + '/distributions'
        print(distribution_url)
        meta = response.meta
        meta['items'] = items
        url=response.xpath("//a[contains(text(),'Export')]//@href").extract()
        yield self.make_request(distribution_url, callback=self.parse_distribution, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_GET)
        #yield self.generate_item(items[0], FinancialDetailItem)

    def parse_distribution(self, response):
        items = response.meta['items']
        ticker = items[0]['nasdaq_ticker']
        file=open("guggenheim.html","w")
        file.write(response.text)
        file.close()

        #current_ticker = response.xpath("//h1[contains(@class, 'fund-ticker')]/text()").extract()[0]
        dividends = []
        capital_gains = []
        
        distributions = response.xpath("//table[contains(@id, 'distributionsTable')]/tbody/tr")
        # if ticker == 'Server Error':
        #     items[0]['nasdaq_ticker'] = current_ticker
        for row in distributions:
            pay_ex_date = row.xpath('./td[1]/text()').extract()[0]
            record_date = row.xpath('./td[2]/text()').extract()[0]
            reinvestment_price = row.xpath('./td[3]/text()').extract()[0]
            per_share = row.xpath('./td[4]/text()').extract()[0]
            per_share_small_cap_gains = row.xpath('./td[5]/text()').extract()[0]
            per_share_large_cap_gains = row.xpath('./td[6]/text()').extract()[0]
            total_per_share = row.xpath('./td[7]/text()').extract()[0]

            divident_dict = {'ex_date':pay_ex_date, 'pay_date':pay_ex_date,
                            'per_share':per_share,
                            'record_date':record_date,
                            'reinvestment_price': reinvestment_price}

            dividends.append(divident_dict)
            
            capital_gains_dict = {'cg_ex_date':pay_ex_date, 'cg_pay_date':pay_ex_date,\
                                    'short_term_per_share':per_share_small_cap_gains,\
                                    'long_term_per_share':per_share_large_cap_gains,\
                                    'total_per_share':total_per_share,
                                    'cg_record_date':record_date,
                                    'cg_reinvestment_price': reinvestment_price}

            capital_gains.append(capital_gains_dict)

        items[0]['dividends'] = dividends
        items[0]['capital_gains'] = capital_gains
        yield self.generate_item(items[0], FinancialDetailItem)
