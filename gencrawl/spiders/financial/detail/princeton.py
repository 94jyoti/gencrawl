from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
from gencrawl.util.statics import Statics
import re
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem


class PrincetonComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_princeton_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        url="https://www.princetontreasuryfund.com/"+response.xpath("//a[contains(text(),'MANAGEMENT')]//@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        print(url)
        yield self.make_request(url, callback=self.parse_manager, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)

    def parse_manager(self, response):
        print("cdcw")

        items = response.meta['items']
        for item in items:
            temp_manager_list=[]
            manager_temp=response.xpath("//h2[contains(text(),'Portfolio Managers')]//following::div[contains(@class,'rTable')]//h2//text()").extract()
            for i in manager_temp:
                data_dict={"fund_manager":""}
                data_dict['fund_manager']=i
                temp_manager_list.append(data_dict)
            item['fund_managers']=temp_manager_list
            yield self.generate_item(item, FinancialDetailItem)

