from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy


class SaturnaComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_saturna_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        no_of_items=len(items)
        no_of_cg=len(items[0]['capital_gains'])
        divide_capital_gains=int(no_of_cg/no_of_items)
        for i in range(len(items)):
        	if(i==0):
        		items[i]['capital_gains']=items[i]['capital_gains'][0:divide_capital_gains]
        		items[i]['dividends']=items[i]['dividends'][0:divide_capital_gains]
        	elif(i>1 and i<len(items)):
        		capital_gains_increment=divide_capital_gains+divide_capital_gains
        		items[i]['capital_gains']=items[i]['capital_gains'][divide_capital_gains,capital_gains_increment]
        		items[i]['dividends']=items[i]['dividends'][divide_capital_gains,capital_gains_increment]
        	else:
        		capital_gains_increment=divide_capital_gains+divide_capital_gains
        		items[i]['capital_gains']=items[i]['capital_gains'][divide_capital_gains:]
        		items[i]['dividends']=items[i]['dividends'][divide_capital_gains:]
        return items
