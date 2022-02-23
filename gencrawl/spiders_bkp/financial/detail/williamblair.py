from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics


class WilliamblairfundsComDetail(FinancialDetailSpider):
    name = 'financial_detail_williamblair_com'
    custom_settings = {
        "RETRY_TIMES": 5,
        "CRAWLERA_ENABLED": True,
        "DOWNLOAD_DELAY": 4
    }

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        meta = response.meta
        meta['items'] = items
        url = "https://www.williamblairfunds.com"+response.xpath("//a[contains(text(),'Fund Facts')]/@href").extract()[0]
        print(url)
        yield self.make_request(url, callback=self.funds_fact, meta=meta,method=Statics.CRAWL_METHOD_SELENIUM)
    def funds_fact(self,response):
        items = response.meta['items']
        print("here")
        items[0]['share_inception_date']=response.xpath("//td[contains(text(),'Inception Date')]//following-sibling::td//text()").extract_first()
        items[0]['total_expense_gross']=response.xpath("//td[contains(text(),'Gross')]//following-sibling::td//text()").extract_first()
        items[0]['total_expense_net']=response.xpath("//td[contains(text(),'Expense Ratio (Net)')]//following-sibling::td//text()").extract_first()
        items[0]['nasdaq_ticker']=response.xpath("//td[contains(text(),'Ticker')]//following-sibling::td//text()").extract_first()
        items[0]['cusip']=response.xpath("//td[contains(text(),'CUSIP')]//following-sibling::td//text()").extract_first()
        items[0]['portfolio_assets']=response.xpath("//td[contains(text(),'Total Net Assets')]//following-sibling::td//text()").extract_first()+" "+response.xpath("//td[contains(text(),'Total Net Assets')]//span//text()").extract_first().replace("(","").replace(")","").strip()
        items[0]['portfolio_assets_date']=response.xpath("//h3[@class='fund-name']//following::text()[contains(.,'As of')]").extract_first().replace("As of","").strip()
        items[0]['turnover_rate']=response.xpath("//td[contains(text(),'Turnover')]//following-sibling::td//text()").extract_first()
        items[0]['turnover_rate_date']=response.xpath("//h3[@class='fund-name']//following::text()[contains(.,'As of')]").extract_first().replace("As of","").strip()
        print(items)
        meta = response.meta
        meta['items'] = items
        print(response.xpath("//a[text()='Performance']/@href").extract())
        url = "https://www.williamblairfunds.com/" +response.xpath("//a[text()='Performance']/@href").extract()[0]
        print(url)
        file=open("williamblair.html","w")
        file.write(response.text)
        file.close()
        yield self.make_request(url, callback=self.performance, meta=meta, method=Statics.CRAWL_METHOD_SELENIUM)

    def performance(self,response):
        items = response.meta['items']
        print("here")
        items[0]['benchmarks']=response.xpath("//h2[contains(text(),'Calendar Year Total Returns')]//following::table//tbody//td[1][contains(text(),'Index')]//text()").extract()
        if(len(items[0]['benchmarks'])==0):
            items[0]['benchmarks']=response.xpath("//h2[contains(text(),'Standardized Returns')]//following::table//tbody//td[1][contains(text(),'Index')]").extract()
        meta = response.meta
        print(items[0]['benchmarks'])
        meta['items'] = items
        print(response.xpath("//a[contains(text(),'Management')]/@href").extract())
        url = "https://www.williamblairfunds.com/" +response.xpath("//a[contains(text(),'Management')]/@href").extract()[0]
        print(url)
        yield self.make_request(url, callback=self.parse_portfolio_managers, meta=meta, method=Statics.CRAWL_METHOD_SELENIUM)
    def parse_portfolio_managers(self,response):
        items = response.meta['items']
        print("there")
        fund_manager_list=[]
        managers_temp=response.xpath("//h3[contains(@class,'fund-name')]//parent::div//h2"
                                     "//text()").extract()
        print(managers_temp)
        if(len(managers_temp)==0):
            managers_temp=response.xpath("//h3[contains(@class,'fund-name')]//parent::div//h2//text()").extract()
        print("second",managers_temp)
        #experience_years=response.xpath("//strong[contains(text(),'Tenure with William Blair:')]//following::text()[contains(.,'Since')]").extract()
        for i in range(len(managers_temp)):
            data_dict={"fund_manager": "", "fund_manager_years_of_experience_in_industry":""}
            data_dict['fund_manager']=managers_temp[i]
            #data_dict['fund_manager_years_of_experience_in_industry']=experience_years[i]
            fund_manager_list.append(data_dict)
        items[0]['fund_managers']=fund_manager_list
        yield self.generate_item(items[0], FinancialDetailItem)


