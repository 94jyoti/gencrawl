from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
import scrapy
import re
from gencrawl.util.statics import Statics
class SchrodersComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_schroders_com'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        iframe_url = response.xpath("//h2[contains(text(),'Fund Details')]/following::iframe[1]//@src").extract()[0]
        meta = response.meta
        meta['items'] = items
        yield self.make_request(iframe_url, callback=self.fund_details, meta=meta,method=Statics.CRAWL_METHOD_SELENIUM)

    def fund_details(self, response):
        items = response.meta['items']
        share_class_table=response.xpath("//thead//tr/th[position()>1]//text()").extract()
        for item in items:
        	if(item['share_class'] in share_class_table):
        		item['total_net_assets_date']=response.xpath("//p[contains(text(),'As of')]//span//text()").extract()[0]
        		index_share_class=share_class_table.index(item['share_class'])
        		counter=0
        		for row in response.xpath("//tbody//tr"):
        				title=row.xpath("./td[1]//text()").extract_first()
        				if("ticker" in  title.lower()):
        					item['nasdaq_ticker']=row.xpath(".//td["+str(index_share_class+2)+"]//text()").extract_first()
        				if("cusip" in title.lower()):
        					item['cusip']=row.xpath(".//td["+str(index_share_class+2)+"]//text()").extract_first()
        				if("inception date" in title.lower()):
        					item['share_inception_date']=row.xpath(".//td["+str(index_share_class+2)+"]//text()").extract_first()
        				if("benchmark" in title.lower()):
        					item['benchmarks']=row.xpath(".//td["+str(index_share_class+2)+"]//text()").extract_first()
        				if("fund assets *" in title.lower()):
        					item['total_net_assets']=" ".join(row.xpath(".//td["+str(index_share_class+2)+"]//span//text()").extract())
        				if("minimum investment" in title.lower()):
        					item['minimum_initial_investment']=row.xpath(".//td["+str(index_share_class+2)+"]//text()").extract_first()
        				if("min. subsequent inv." in title.lower()):
        					item['minimum_additional_investment']=row.xpath(".//td["+str(index_share_class+2)+"]//text()").extract_first()
        				counter=counter+1
        				
        return items


