from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
import scrapy
import re
from gencrawl.util.statics import Statics

class VlfundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_vlfunds_com'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        for item in range(len(items)):
        	if(items[item]['share_class']==[]):
        		share_class_temp=response.xpath("//h1/parent::div/div/div/div/following-sibling::div/div[1]//text()").extract()[item]
        		items[item]['share_class']=share_class_temp.split(" ")[-1].replace("(","").replace(")","")
        		if(items[item]['share_class']=="Inv"):
        			items[item]['share_class']="Investor Class"
        meta = response.meta
        meta['items'] = items
        benchmark_url=response.xpath("//a[contains(text(),'Performance')]//@href").extract()[0]
        yield self.make_request(benchmark_url, callback=self.performance, meta=meta,method=Statics.CRAWL_METHOD_SELENIUM)

    def performance(self, response):
        items = response.meta['items']
        for i in items:
        	benchmark=[i.replace("\t","").replace("\n","") for i in list(set(response.xpath("//table[@id='aartable']//tr//td[2]//a//parent::td/text()").extract()))]
        	while("" in benchmark) :
        		benchmark.remove("")
        	i['benchmarks']=benchmark	
        return items


