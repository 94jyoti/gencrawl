from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
from gencrawl.util.statics import Statics
import re
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem


class ThornburgfundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_thornburg_com'
    custom_settings = {
        "RETRY_TIMES": 5,
        "CRAWLERA_ENABLED":False
    }
    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        url=response.xpath("//a[contains(text(),'PERFORMANCE')]//@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        print(url)
        yield self.make_request(url, callback=self.performance, meta=meta, dont_filter=True, method=Statics.CRAWL_METHOD_SELENIUM)

    def performance(self,response):
        print("cdcw")
        items = response.meta['items']
        for item in items:
            for row in response.xpath("//h3[contains(text(),'Fund Operating Expenses')]"):
                #print(row.xpath(".//span//text()").extract_first().replace("Class","").replace("Shares","").replace("-","").strip())
                #print(item['share_class'] in row.xpath(".//span//text()").extract_first().replace("Class","").replace("Shares","").replace("-","").strip())
                if(item['share_class'] in row.xpath(".//span//text()").extract_first().replace("Class","").replace("Shares","").replace("-","").strip() ):

                    item['total_expense_gross']=row.xpath("(.//following::table//strong[contains(text(),'Gross Annual Operating Expenses')]/parent::td)[1]/following-sibling::td//text()").extract()[0]
                    item['total_expense_net']=row.xpath("(.//following::table//strong[contains(text(),'Net Annual Operating Expenses')]/parent::td)[1]/following-sibling::td//text()").extract_first()
            for row in response.xpath("//h3[contains(text(),'Yields')]"):
                print(item['share_class'] in row.xpath(".//span//time//following::text()[1]").extract_first().replace("Class", "").replace("Shares", "").replace("-", "").strip())
                print(row.xpath(".//span//time//following::text()[1]").extract_first().replace("Class", "").replace("Shares", "").replace("-", "").strip())
                print(item['share_class'])
                if (item['share_class'] in row.xpath(".//span//time//following::text()[1]").extract_first().replace("Class", "").replace("Shares", "").replace("-", "").strip()):
                    item['sec_yield_30_day']=row.xpath("(.//following::table//strong[contains(text(),'30-day SEC')]//parent::td)[1]//following-sibling::td//text()").extract_first()
                    print("cdcd",item['sec_yield_30_day'])
                    item['sec_yield_date_30_day']=row.xpath(".//span//time//text()").extract()[0]
        url=response.xpath("//a[contains(text(), 'PORTFOLIO')] / @ href").extract()[0]

        meta = response.meta
        meta['items'] = items
        print(url)
        yield self.make_request(url, callback=self.parse_portfolio, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)

    def parse_portfolio(self,response):
        items = response.meta['items']
        for item in items:
            try:
                item['effective_duration']=response.xpath("//td[contains(text(),'Effective Duration')]//following-sibling::td//text()").extract()[0]
            except:
                pass
            try:
                item['effective_duration_date']=response.xpath("//h3[contains(text(),'Key Portfolio Attributes')]//span//time//text()").extract()[0]
            except:
                pass
            try:
                item['portfolio_assets']=response.xpath("//td[contains(text(),'Fund Assets')]//following-sibling::td//text()").extract()[0]
            except:
                pass
            try:

                item['portfolio_assets_date']=response.xpath("//h3[contains(text(),'Key Portfolio Attributes')]//span//time//text()").extract()[0]
            except:
                pass
            try:
                item['average_weighted_maturity']=response.xpath("//td[contains(text(),'Average Effective Maturity')]//following-sibling::td//text()").extract()[0]
            except:
                pass
            try:
                item['average_weighted_maturity_as_of_date']=response.xpath("//h3[contains(text(),'Key Portfolio Attributes')]//span//time//text()").extract()[0]
            except:
                pass
            yield self.generate_item(item, FinancialDetailItem)
