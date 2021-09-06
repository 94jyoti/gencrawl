from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics

class TortoiseComDetail(FinancialDetailSpider):
    name = 'financial_detail_tortoise_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        main_url=items[0]['fund_url'].split("#")[0]+response.xpath("//a[@id='performance-tab']/@href").extract()[0]
        #main_url = "https://www.commercefunds.com/fund-information/mutual-funds"
        print(main_url)
        meta = response.meta
        meta['items'] = items
        yield self.make_request(main_url, callback=self.parse_gross, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)

    def parse_gross(self, response):
        items = response.meta['items']
        headers=response.xpath("(//table[contains(@id,'DataTables_Table')])[1]//tbody//tr//td[1]//text()").extract()
        for row in response.xpath("(//table[contains(@id,'DataTables_Table')])[1]//tbody//tr"):
            temp_ticker=row.xpath(".//td[1]//text()").extract()[0]
            print(temp_ticker)
            print("ldlcdncld",items[0]['nasdaq_ticker'])
            print(items[0]['nasdaq_ticker'].strip() in temp_ticker.strip())
            if(response.xpath("(//table[contains(@id,'DataTables_Table')])[1]//thead//th[contains(text(),'Net')]").extract()==[]):
                if(items[0]['nasdaq_ticker'].strip() in temp_ticker.strip()):
                    print("isnide if")
                    items[0]['total_expense_gross']=row.xpath(".//td[position()=last()]").extract()[0]
            elif(response.xpath("(//table[contains(@id,'DataTables_Table')])[1]//thead//th[contains(text(),'Net')]").extract()[0]):
                if (items[0]['nasdaq_ticker'].strip() in temp_ticker.strip()):
                    print("isnide if")
                    items[0]['total_expense_gross'] = row.xpath(".//td[position()=last()-1]").extract()[0]
                    items[0]['total_expense_net'] = row.xpath(".//td[position()=last()]").extract()[0]
        yield self.generate_item(items[0], FinancialDetailItem)