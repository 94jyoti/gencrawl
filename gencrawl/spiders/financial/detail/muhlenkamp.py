from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics

class MuhlenkampComDetail(FinancialDetailSpider):
    name = 'financial_detail_muhlenkamp_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        #item=items[0]
        file=open("muhlx.html","w")
        file.write(response.text)
        file.close()
        distribution_url=response.xpath("//a[contains(text(),'Distributions')]//@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        yield self.make_request(distribution_url, callback=self.dividends, meta=meta, dont_filter=True, method=Statics.CRAWL_METHOD_SELENIUM)

    def dividends(self,response):
        items = response.meta['items']
        dividend_data=response.xpath("//h3[contains(text(),'Capital Gains')]//following::table//tbody//tr")
        capital_gains_list=[]
        dividend_list=[]
        for row in dividend_data:
            data_dict1={"cg_ex_date": "", "cg_record_date": "", "cg_pay_date": "", "short_term_per_share": "","long_term_per_share": "", "total_per_share": "", "cg_reinvestment_price": ""}
            data_dict2={"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "", "record_date": "","per_share": "", "reinvestment_price": ""}
            data_dict2['record_date']=row.xpath(".//td[2]//text()").extract_first()
            data_dict1['total_per_share']=row.xpath(".//td[3]//text()").extract_first()
            data_dict2['ordinary_income']=row.xpath(".//td[4]//text()").extract_first()
            data_dict2['per_share']=row.xpath(".//td[6]//text()").extract_first()
            capital_gains_list.append(data_dict1)
            dividend_list.append(data_dict2)
        for item in items:
            item['capital_gains']=capital_gains_list
            item['dividends']=dividend_list
            yield self.generate_item(item, FinancialDetailItem)