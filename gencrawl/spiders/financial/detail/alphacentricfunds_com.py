from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
from datetime import datetime
import datetime
import urllib.parse
import re
from gencrawl.util.statics import Statics
# import urllib
import itertools
import logging


class AlphacentricDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_alphacentricfunds_com'

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        meta = response.meta
        meta['items'] = items
        items2 = []
        strategy_list =[]
        objective_list=[]
        min_initial_investment_list=[]
        min_additional_investment_list=[]
        content = re.findall(r'<div class="title-mobile">(.*?)<span class="mk-button--text">Download Fact Sheet</span>', response.text,re.DOTALL)
        for x in content:    
            selector = scrapy.Selector(text=x, type="html")
            strategy_list_items = selector.xpath("//p[contains(text(),'Strategy')]/text()").getall()
            strategy_list.append(' '.join(strategy_list_items))

            objective_list_items = selector.xpath("//p[contains(text(),'Objective')]/text()").getall()
            objective_list.append(' '.join(objective_list_items))

            objective_list_items = selector.xpath("//p[contains(text(),'Objective')]/text()").getall()
            objective_list.append(' '.join(objective_list_items))


            min_initial_investment = selector.xpath("//p[contains(text(),'Minimum Investment')]/text()").get()
            min_initial_investment_list.append(min_initial_investment)

            min_additional_investment = selector.xpath("//p[contains(text(),'Minimum Investment')]/text()").get()
            min_additional_investment_list.append(min_additional_investment)

        count = 0
        count1=0
        for i in items:
            if "Share" in i['share_class']:
                count1 = count1+1
                for j in i['share_class'].split(','):
                    count = count+1
                    items2.append(i)
                    items2[count-1]['share_class'] = j.split(':')[0]
                    items2[count-1]['nasdaq_ticker'] = j.split(':')[-1]
                    items2[count-1]['investment_strategy'] =  strategy_list[count1-1]
                    items2[count-1]['investment_objective'] =  objective_list[count1-1]
                    items2[count-1]['minimum_initial_investment'] =  min_initial_investment_list[count1-1]
                    items2[count-1]['minimum_additional_investment'] =  min_additional_investment_list[count1-1]
                    yield self.generate_item(items2[count-1], FinancialDetailItem)
                    
            else:
                count1 = count1+1
                xx = re.findall(r'\((.*)\)', i['share_class'])
                jj = xx[0].split('|')
                for j in jj:
                    items2.append(i)
                    count = count+1
                    items2[count-1]['share_class'] = ""
                    items2[count-1]['nasdaq_ticker'] = j
                    items2[count-1]['investment_strategy'] =  strategy_list[count1-1]
                    items2[count-1]['investment_objective'] =  objective_list[count1-1]
                    items2[count-1]['minimum_initial_investment'] =  min_initial_investment_list[count1-1]
                    items2[count-1]['minimum_additional_investment'] =  min_additional_investment_list[count1-1]
                    yield self.generate_item(items2[count-1], FinancialDetailItem)