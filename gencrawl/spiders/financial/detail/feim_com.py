from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import pandas as pd
class FeimComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_feim_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        for item in items:
            if(item['minimum_initial_investment']==[]):
                temp_investment=response.xpath('//td[contains(text(),"Minimum Investment")]/text()').extract()
                temp_investment=[i.replace("Minimum Investment - Class",'').strip() for i in temp_investment]
                counter=-1
                for item_invest in temp_investment:
                    counter=counter+1
                    if(item['share_class'] in item_invest):
                        item['minimum_initial_investment']=response.xpath('//td[contains(text(),"Minimum Investment")]/following-sibling::td//text()').extract()[counter]
            #minimum addition investment
            if(item['minimum_additional_investment']==[]):
                temp_min_investment=response.xpath('//td[contains(text(),"Subsequent Investment")]/text()').extract()
                temp_min_investment=[i.replace("Subsequent Investment - Class",'').strip() for i in temp_min_investment]
                counter=-1
                for item_invest in temp_min_investment:
                    counter=counter+1
                    if(item['share_class'] in item_invest):
                        item['minimum_additional_investment']=response.xpath('//td[contains(text(),"Subsequent Investment")]/following-sibling::td//text()').extract()[counter]

            
        return items