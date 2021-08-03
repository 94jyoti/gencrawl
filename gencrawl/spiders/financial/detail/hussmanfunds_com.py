from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime

class HussmanfundsComDetail(FinancialDetailSpider):
    name = 'financial_detail_hussmanfunds_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        temp=items[0]['fund_managers'][0]['fund_manager']
        print("tempppp",items[0]['fund_managers'])
        fund_manager_list=[]
        #if("&" in temp):
        #	temp=temp.split("&")
        #	print("temppppppppp",temp)
        for i in temp:
        	data=i.replace("\n","").replace("&","")
        	
        	print(data)
        	data_dict={"fund_manager": ""}
        	data_dict['fund_manager']=data
        	empty={k: v for k, v in data_dict.items() if not  v}
        	print("emptytytyyt",empty)
        	for k in empty:
        		print(k)
        		del data_dict[k]
        	print("dcdcddc",data_dict)
        	
        	fund_manager_list.append(data_dict)
        items[0]['fund_managers']=fund_manager_list
        meta = response.meta
        
        
        meta['items'] = items
        main_url=response.xpath("//span[contains(text(),'Home')]//parent::a//@href").extract()[0]
        yield self.make_request(main_url, callback=self.home, meta=meta, dont_filter=True)
        
    def home(self, response):
        items = response.meta['items']
        tickers_temp=response.xpath("//ul[@class='fundList'][1]//li//a//text()").extract()
        print("ndkncdkckdnckncd",tickers_temp)
        for i in tickers_temp:
        	print('sn',items[0]['instrument_name'])
        	if(items[0]['instrument_name'] in i ):
        		items[0]['nasdaq_ticker']=i.split("-")[-1].strip()
        		print(items[0]['nasdaq_ticker'])
        yield self.generate_item(items[0], FinancialDetailItem)	