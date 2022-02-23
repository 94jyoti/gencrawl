from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider


class JohcmfundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_johcm_com'
    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        for item in items:
            temp_row=response.xpath("((//table[@class='fundcodes-table'])[1]//tbody//tr)[position()>1]")
            for row in temp_row:
                if(row.xpath(".//td[1]//text()").extract_first()==item['nasdaq_ticker']):
                    item['cusip']=row.xpath(".//td[4]//text()").extract_first(None)
            yield self.generate_item(item, FinancialDetailItem)




