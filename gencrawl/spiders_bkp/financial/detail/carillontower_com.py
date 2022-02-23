from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
import scrapy
import re
from gencrawl.util.statics import Statics
from copy import deepcopy
from gencrawl.util.statics import Statics
class CarillionComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_carillion_com'

    def get_items_or_req(self, response, default_item={}):
        temp_items = super().get_items_or_req(response, default_item)
        iframe_url = response.xpath("//div[@id='KeyFacts']//iframe//@src").extract()[0]
        meta = response.meta
        meta['temp_items'] = temp_items
        yield self.make_request(iframe_url, callback=self.fund_details, meta=meta,method=Statics.CRAWL_METHOD_SELENIUM)

    def fund_details(self, response):
        temp_items = response.meta['temp_items']
        share_class_table=response.xpath("//table[2]//tr[position()>1]//td[1]/p/text()").extract()
        items=[]
        for share_class in share_class_table:
        	items.append(deepcopy(temp_items[0]))
        counter=0
        for item in items:
        	item['share_class']=share_class_table[counter]
        	counter=counter+1
        counter=1
        headers=response.xpath("//table[2]//tr[1]//td//text()").extract()
        for item in items:
        		item['total_net_assets']=response.xpath("//td[contains(text(),'Total net assets')]/following-sibling::td/text()").extract()[0]
        		item['total_net_assets_date']=response.xpath("//small[contains(text(),'as of')]/text()[2]").extract()[0]
        		item['benchmarks']=response.xpath("//td[contains(text(),'Benchmark')]/following-sibling::td/text()").extract()
        		item['minimum_initial_investment']=response.xpath("//td[contains(text(),'minimum investment')]/following-sibling::td/text()").extract()[0]
        		for row in response.xpath("//table[2]//tr"):
        				print("matchhinfnffnfn",item['share_class'] == row.xpath("//td[1]//text()"))
        				if(item['share_class'] == row.xpath(".//td[1]//text()").extract_first()):
        					if("Symbol" in headers):
        						index_symbol=headers.index("Symbol")
        						item['nasdaq_ticker']=row.xpath(".//td["+str(index_symbol+1)+"]//text()").extract_first()
        					if("CUSIP" in headers):
        						index_cusip=headers.index("CUSIP")
        						item['cusip']=row.xpath(".//td["+str(index_cusip+1)+"]//text()").extract_first()
        					if("Inception" in headers):
        						index_inception=headers.index("Inception")
        						item['share_inception_date']=row.xpath(".//td["+str(index_inception+1)+"]//text()").extract_first()
        				counter=counter+1
        				
        return items


