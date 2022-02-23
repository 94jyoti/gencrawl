from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
from gencrawl.util.statics import Statics
import re
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem


class MuzinichusfundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_muzinicus_com'
    custom_settings = {
        "RETRY_TIMES": 5,
        "CRAWLERA_ENABLED": True,

    }
    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        #file=open("munizini_test.html","w")
        #file.write(response.text)
        #file.close()
        #for item in items:
        try:
            inception_date_temp=response.xpath("//p[contains(text(),'Inception Date')]//text()").extract()[0]
            print(inception_date_temp)
            date=re.findall(r'\d*/\d*/\d+',inception_date_temp)
            print(date)
            for item in range(len(items)):
                items[item]['share_inception_date']=date[item]
        except:
            pass
        print("jbjbjbj",items[0]['share_class'])
        print(response.xpath("//table[@class='fund_table']/tbody/tr/td[1]//text()").extract())
        for item in range(len(items)):
            if(items[item]['share_class']==[]):
                items[item]['share_class'] =response.xpath("//table[@class='fund_table']/tbody/tr/td[1]//text()").extract()[item].split("–")[-1]
            items[item]['share_class']=items[item]['share_class'].split("-")[-1].strip()
        print("//div[@class='menu-main-container']//a[contains(text(),'"+items[0]['instrument_name']+"')]//parent::li//a[(text()='Fund Holdings & Portfolio Characteristics')]//@href")
        url=response.xpath("//div[@class='menu-main-container']//a[contains(text(),'"+items[0]['instrument_name'].strip()+"')]//parent::li//a[(text()='Fund Holdings & Portfolio Characteristics')]//@href").extract()[0]
        print(url)

        meta = response.meta
        meta['items'] = items
        yield self.make_request(url, callback=self.parse_sec_data, meta=meta, dont_filter=True, method=Statics.CRAWL_METHOD_SELENIUM)
    def parse_sec_data(self,response):
        print("done")
        items = response.meta['items']
        share_class_temp=response.xpath("//table[@class='fund_table']/tbody/tr/td[1]//span//text()").extract()
        for item in items:
            item['effective_duration']=response.xpath("//td[contains(text(),'Average Duration (yrs)')]/following-sibling::td/text()").extract()[0]
            item['effective_duration_date']=response.xpath("//th[contains(text(),'Portfolio Characteristics')]//text()").extract()[0].split("as of")[-1].strip()
            item['sec_yield_30_day']=response.xpath("//td[contains(text(),'30-Day SEC Yield with waiver')]/following-sibling::td/text()").extract()[0]
            item['sec_yield_date_30_day']=response.xpath("//th[contains(text(),'Portfolio Characteristics')]//text()").extract()[0].split("as of")[-1].strip()
            item['sec_yield_without_waivers_30_day']=response.xpath("//td[contains(text(),'30-Day SEC Yield w/o waiver')]/following-sibling::td/text()").extract()[0]
            item['sec_yield_without_waivers_date_30_day']=response.xpath("//th[contains(text(),'Portfolio Characteristics')]//text()").extract()[0].split("as of")[-1].strip()
            yield self.generate_item(item, FinancialDetailItem)