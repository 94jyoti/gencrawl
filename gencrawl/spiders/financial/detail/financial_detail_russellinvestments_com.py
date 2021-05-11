from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json


class RussellComDetail(FinancialDetailSpider):
    name = 'financial_detail_russellinvestments_com'
    
    def get_items_or_req(self, response, default_item={}):
        
        items=self.prepare_items(response, default_item)
        item=items[0]
        info_json=item['temp_info_json_data'][0]
        
        cusip_data=info_json['KeyFacts']['Grid']
        #print(cusip_data)
        for i in cusip_data:
            if(i['Title'].lower()=="cusip"):
                item['cusip_data_value']=i['Value']
            if("totalnetassets" in str(i['Title']).lower().replace(" ","")):
                item['portfolio_assets']=i['Value']
                item['date']=i['AsOfDate']
            if(("expensesgross") in i['Name'].lower().replace(" ","")):
                item['total_expense_gross']=i['Value']
            if(("expensesnet") in i['Name'].lower().replace(" ","")):
                item['total_expense_net']=i['Value']
        return [item]
        #print(items)
        #file=open("abc.json","w")
        #file.write(json.dumps(item[0]['temp_info_json_data'][0]))
        #file.close()
        
        # return self.make_request(performance_api, callback=self.parse_performance_response, meta=meta)



