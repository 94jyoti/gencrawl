from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics

class NewyorklifeDetail(FinancialDetailSpider):
    name = 'financial_detail_newtorklifeinvestment_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        #file=open("newyork.html","w")
        #file.write(response.text)
        #file.close()
        dividends_data={"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "", "record_date": "","per_share": "", "reinvestment_price": ""}
        dividends_data['ex_date']=str(response.xpath("(//span[contains(text(),'Dividends')]//following::span[contains(text(),'Payable')])[1]//parent::div//following-sibling::div//span//text()").extract_first())
        dividends_data['pay_date']=str(dividends_data['ex_date'])
        dividends_data['per_share']=str(response.xpath("(//span[contains(text(),'Dividends')]//following::span[contains(text(),'Per Share')])[1]//parent::div//following-sibling::div//span//text()").extract_first())
        #capital_gains
        #capital_gains_data={"cg_ex_date": "", "cg_record_date": "", "cg_pay_date": "", "short_term_per_share": "","long_term_per_share": "", "total_per_share": "", "cg_reinvestment_price": ""}
        #capital_gains_data['cg_pay_date']=str(response.xpath("(//span[contains(text(),'Capital')]//following::span[contains(text(),'Payable')])[1]//parent::div//following-sibling::div//span//text()").extract_first())
        #print("cbksbcksc",capital_gains_data['cg_record_date'])
       # if(capital_gains_data['cg_record_date'].strip()=="-"):
         #   capital_gains_data['cg_record_date']="temporary"
        #capital_gains_data['short_term_per_share']=str(response.xpath("(//span[contains(text(),'Capital')]//following::span[contains(text(),'Short Term')])[1]//parent::div//following-sibling::div//span//text()").extract_first())
        #if (capital_gains_data['short_term_per_share'].strip() == "-"):
          #  capital_gains_data['short_term_per_share'] = "temporary"
        #capital_gains_data['long_term_per_share'] = str(response.xpath("(//span[contains(text(),'Capital')]//following::span[contains(text(),'Long Term')])[1]//parent::div//following-sibling::div//span//text()").extract_first())
        #if (capital_gains_data['long_term_per_share'].strip() == "-"):
         #   capital_gains_data['long_term_per_share'] = "temporary"

        #capital_gains_data['total_per_share']=str(response.xpath("(//span[contains(text(),'Capital')]//following::span[contains(text(),'Per Share')])[1]//parent::div//following-sibling::div//span//text()").extract_first())
        for item in items:
            item['dividends']=[dividends_data]
            #item['capital_gains']=[capital_gains_data]
            yield self.generate_item(item, FinancialDetailItem)
        
