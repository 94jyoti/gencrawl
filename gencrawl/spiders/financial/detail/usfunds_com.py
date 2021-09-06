from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
import pandas as pd

class UsfundsComDetail(FinancialDetailSpider):
    name = 'financial_detail_usfunds_com'

    def get_items_or_req(self, response, default_item={}):
        file=open("usfunds.html","w")
        file.write(response.text)
        file.close()
        items = super().get_items_or_req(response, default_item)
        gross_url = "https://www.usfunds.com"+response.xpath("//a[text()='Performance']//@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        print(gross_url)
        yield self.make_request(gross_url, callback=self.performance, meta=meta)

    def performance(self, response):
        items = response.meta['items']
        gross_expense_table=response.xpath("//table[@class='returnsTable']//caption[contains(text(),'Quarter')]//parent::table").extract()[0]
        gross = pd.read_html(gross_expense_table)
        final_gross = gross[0].to_dict('dict')
        items[0]['total_expense_gross']=final_gross['Gross Expense Ratio'][0]  
        yield self.generate_item(items[0], FinancialDetailItem)