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
        meta = response.meta
        meta['items'] = items
        #url="https://www.guggenheiminvestments.com/"+response.xpath("(//a[contains(text(),'Distributions')])[2]//@href").extract()[0]
        url=items[0]['fund_url']+"/distributions"
        yield self.make_request(url, callback=self.dividends, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)

    def dividends(self, response):
        items = response.meta['items']
        file=open("guggen.html","w")
        file.write(response.text)
        file.close()
        excel_url="https://www.guggenheiminvestments.com"+response.xpath("//a[contains(text(),'Export to Excel')]//@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        '''
        with open('websites.csv', 'rbU') as csv_file:
            data = csv.reader(csv_file)
            scrapurls = []
            for row in data:
                scrapurls.append(row)
            return scrapurls
        '''

        yield self.make_request(excel_url, callback=self.parse_distributions, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)

    def parse_distributions(self,response):
        items = response.meta['items']
        print(items)
        file = open("guggen1.html", "w")
        file.write(response.text)
        file.close()

        #yield self.generate_item(items[0], FinancialDetailItem)