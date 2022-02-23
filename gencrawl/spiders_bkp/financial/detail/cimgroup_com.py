from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re

class CimgroupComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_cimgroup_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        no_of_items=len(items)
        maximum_sales=response.xpath("//p[contains(text(),'Returns')]//text()").extract()
        for i in range(len(items)):
            if(items[i]['share_class'].strip()=="Class A"):
                items[i]['maximum_sales_charge_full_load']=re.findall(r'\d+%',maximum_sales[0])
            if(items[i]['share_class'].strip()=="Class L"):
                items[i]['maximum_sales_charge_full_load']=re.findall(r'\d+%',maximum_sales[-1])
        return items
