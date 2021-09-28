from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics


class a3financialDetail(FinancialDetailSpider):
    name = 'a3_financial'
    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)

        #print(items)
        
        #item=items[0]

        #print(item)


        # year=response.xpath("//b[contains(text(),'Calendar Year End Data')]//ancestor::tr//following-sibling::tr//td//b[contains(text(),'Year')]//parent::td//following-sibling::td//strong//text()").extract()
        # capital_gains=response.xpath("//b[contains(text(),'Calendar Year End Data')]//ancestor::tr//following-sibling::tr//td//b[contains(text(),'Capital Gains')]/parent::td//following-sibling::td//text()").extract()
        # dividends=response.xpath("//b[contains(text(),'Calendar Year End Data')]//ancestor::tr//following-sibling::tr//td//b[contains(text(),'Dividends')]//parent::td//following-sibling::td//text()").extract()
        # capital_gain_list=[]
        # dividends_list=[]
        # for i in range(len(year)):
        #     data_dict1={"cg_ex_date": "", "cg_record_date": "", "cg_pay_date": "", "short_term_per_share": "","long_term_per_share": "", "total_per_share": "", "cg_reinvestment_price": ""}
        #     data_dict2={"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "", "record_date": "","per_share": "", "reinvestment_price": ""}
        #     data_dict2['ex_date']=year[i]
        #     data_dict1['total_per_share']=capital_gains[i]
        #     data_dict2['ordinary_income']=dividends[i]
        #     capital_gain_list.append(data_dict1)
        #     dividends_list.append(data_dict2)
        # item['capital_gains']=capital_gain_list
        # item['dividends']=dividends_list

        for i in items:
            print(i)
            yield self.generate_item(i, FinancialDetailItem)