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
import traceback

from copy import deepcopy

class CohenandsteersComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_cohenandsteers_com'



    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        for item in items:
            try:
                if(item['share_class'] in response.xpath("(//h6[contains(text(),'Gross Expense')])[1]//text()  | (//h6[contains(text(),'Expense')])[1]//text() ").extract()[0].split("(")[-1].replace("Class","").strip()):
                    item['total_expense_gross']=response.xpath("(//h6[contains(text(),'Gross Expense')])[1]//following::h3[1]//text() | (//h6[contains(text(),'Expense')])[1]//following::h3[1]//text()").extract()[0]
            except:
                pass
            try:
                if(item['share_class'] in response.xpath("(//h6[contains(text(),'Net Expense')])[1]//text()").extract()[0].split("(")[-1].replace("Class","").strip()):
                    item['total_expense_net'] = response.xpath("(//h6[contains(text(),'Net Expense')])[1]//following::h3[1]//text()").extract()[0]
            except:
                pass
            yield self.generate_item(item, FinancialDetailItem)