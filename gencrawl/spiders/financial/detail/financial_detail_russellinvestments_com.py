from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
class RussellComDetail(FinancialDetailSpider):
    name = 'financial_detail_russellinvestments_com'
    
    def parse_main_class(self,response):
        response_json = json.loads(response.text)
        cusip_data=response_json['KeyFacts']['Grid']
        #print(cusip_data)
        item_id=response_json['FundDetail']['Id'].replace("{","").replace("}","")
         
        #share_class=response_json['ShareClass']
        item={}
        item['instrument_name']=response_json['Fund']['FundName']
        item['nasdaq_ticker']=response_json['FundDetail']['Identifier']
        item['share_class']=response_json['ShareClass']
        item['fund_url']="https://russellinvestments.com"+response_json['FundDetail']['Url']
        item['share_inception_date']=(response_json['FundDetail']['InceptionDate']).split("T")[0]
        for i in cusip_data:
            if(i['Title'].lower()=="cusip"):
                item['cusip']=i['Value']
            if("totalnetassets" in str(i['Title']).lower().replace(" ","")):
                item['portfolio_assets']=i['Value']
                item['date']=i['AsOfDate']
            if(("expensesgross") in i['Name'].lower().replace(" ","")):
                item['total_expense_gross']=i['Value']
            if(("expensesnet") in i['Name'].lower().replace(" ","")):
                item['total_expense_net']=i['Value']
                
        stats_data=response_json['KeyFacts']['Statistics']
        for stats in stats_data:
            if("weightedaverageduration" in str(stats['Title']).lower().replace(" ","")):
                item['duration']=stats['Value']
                item['duration_as_of_date']=stats['AsOfDate']
            if("weightedaveragematurity" in str(stats['Title']).lower().replace(" ","")):
                item['average_weighted_maturity']=stats['Value']
                item['average_weighted_maturity_as_of_date']=stats['AsOfDate']
            if("12-monthdistributionyield" in str(stats['Title']).lower().replace(" ","")):
                item['distribution_yield_12_month']=stats['Value']
        
        end_date=datetime.datetime.today().strftime('%m/%d/%Y')
        #start_date="05%2F12%2F2020"
        #endDate=startDate - datetime.timedelta(days=365)
        start_date=datetime.datetime.now()-datetime.timedelta(days=365)
        start_date=start_date.strftime('%m/%d/%Y')
        #endDate="05%2F12%2F2021"
        api_url="https://russellinvestments.com/api/FundV2/GetDistributions?startDate="+urllib.parse.quote(start_date,safe='')+"&endDate="+urllib.parse.quote(end_date,safe='')+"&shareClass="+item['share_class']+"&itemId="+item_id
        #print("apppppppppppp",api_url)
        meta = response.meta
        meta['items'] = item
        r=self.make_request(api_url, callback=self.parse_performance_response,meta=meta)
        return r
        
        
    def get_items_or_req(self, response, default_item={}):
        request=[]
        items=self.prepare_items(response, default_item)
        html_data=response.text
        item=items[0]
        info_json=item['temp_info_json_data'][0]
        # file=open("abc.json","w")
        # file.write(json.dumps(items[0]['temp_info_json_data'][0]))
        # file.close()
        file=open("response.html","w")
        file.write(response.text)
        file.close()
        #find out share classes name
        item_id=info_json['FundDetail']['Id'].replace("{","").replace("}","")
        first_share_class=item['share_class']
        share_classes=[]
        for share in info_json['FundDetail']['ShareClasses']: 
            share_classes.append(share['Name'])
            
        #print(share_classes)
        for share_class in share_classes:
            if(share_class!=first_share_class):
                
                url="https://russellinvestments.com/api/FundV2/GetFund?itemId="+item_id+"&shareClass="+share_class
                r=self.make_request(url,callback=self.parse_main_class,meta=response.meta,dont_filter=True)
                request.append(r)
                
        item['share_inception_date']=(info_json['FundDetail']['InceptionDate']).split("T")[0]
        
        #print("shareclass--------------",share_class)
        #item_id to call an api for fetching historical details
        #html_data=response.text
        #start_date=response.xpath('//input[@id="startDate"]/@value/text()').extract()
        # print(start_date)
        
        #item_id=info_json['FundDetail']['Id'].replace("{","").replace("}","")
        start_date="05%2F12%2F2020"
        endDate="05%2F12%2F2021"
        api_url="https://russellinvestments.com/api/FundV2/GetDistributions?startDate="+start_date+"&endDate="+endDate+"&shareClass="+share_class+"&itemId="+item_id
        meta = response.meta
        meta['items'] = items
        #print("api_url",api_url)
        
        #print("itemid------------------------",item_id)
        #print("dateteeeeeeeeeeeeeeeeeeee",(info_json['FundDetail']['InceptionDate']).split("T")[0])
        cusip_data=info_json['KeyFacts']['Grid']
        #print(cusip_data)
        for i in cusip_data:
            if(i['Title'].lower()=="cusip"):
                item['cusip']=i['Value']
            if("totalnetassets" in str(i['Title']).lower().replace(" ","")):
                item['portfolio_assets']=i['Value']
                item['date']=i['AsOfDate']
            if(("expensesgross") in i['Name'].lower().replace(" ","")):
                item['total_expense_gross']=i['Value']
            if(("expensesnet") in i['Name'].lower().replace(" ","")):
                item['total_expense_net']=i['Value']
                
        stats_data=info_json['KeyFacts']['Statistics']
        for stats in stats_data:
            if("weightedaverageduration" in str(stats['Title']).lower().replace(" ","")):
                item['duration']=stats['Value']
                item['duration_as_of_date']=stats['AsOfDate']
            if("weightedaveragematurity" in str(stats['Title']).lower().replace(" ","")):
                item['average_weighted_maturity']=stats['Value']
                item['average_weighted_maturity_as_of_date']=stats['AsOfDate']
            if("12-monthdistributionyield" in str(stats['Title']).lower().replace(" ","")):
                item['distribution_yield_12_month']=stats['Value']
                
        #return [item]
        #print(items)
        
        #return self.make_request(performance_api, callback=self.parse_performance_response, meta=meta)
        #return self.make_request(api_url, callback=self.parse_performance_response,meta=meta)
        r=self.make_request(api_url, callback=self.parse_performance_response,meta=meta)
        request.append(r)
        return request
         #print(historical_data)
        #self.make_request(performance_api, callback=self.parse_performance_response, meta=meta)
    def parse_performance_response(self, response):
        #print("11111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
        items = response.text
        items = response.meta['items']
        response_json = json.loads(response.text)
        #print(response_json)
        historical_data=response_json['Distributions']
        #count_LtCapGainRate=0
        try:
            items=items[0]
        except:
            print("done")
        capital_gains_list=[]
        #print(historical_data)
        for i in historical_data:
            #data_dict={}
            data_dict={'long_term_per_share':"",'ex_date':"",'record_date':"",'pay_date':"",'short_term_per_share':"",'total_per_share':"",'reinvestment_price':""}
            
            #print(i)
            #print("checkkkkkkkkkkkkkkkkk",i["LtCapGainRate"])
            #count_LtCapGainRate=count_LtCapGainRate+1
            # data_dict['ex_date']=i['ExDate'].split("T")[0]
            # data_dict['record_date']= None
            # data_dict['pay_date']= None
            # data_dict['short_term_per_share']= i['StCapGainRate']
            # data_dict['long_term_per_share']=i['LtCapGainRate']
            # data_dict['total_per_share']=None
            # data_dict['reinvestment_price']=None
            # capital_gains_list.append(data_dict)
        #print("dataaaaaaaa",data_dict)
        #items['capital_gains']=capital_gains_list
            #if(i["LtCapGainRate"]!=None):  
            if(i["LtCapGainRate"]!=None):  
                data_dict['long_term_per_share']=i['LtCapGainRate']
                data_dict['ex_date']=i['ExDate'].split("T")[0]
                data_dict['record_date']=None
                data_dict['pay_date']= None
                data_dict['short_term_per_share']= i['StCapGainRate']
                data_dict['total_per_share']=None
                data_dict['reinvestment_price']=None
                capital_gains_list.append(data_dict)
        #print("data_dict",data_dict)
        items['capital_gains']=capital_gains_list
        print("before yieldddddddddddddddddddddddddddddddddddddddddddddddd",items['capital_gains'])
        #print("1cdwocnocncneddddddccmmmmmmmmmmmmm111111111111111111111111111111111",items)
        yield  self.generate_item(items, FinancialDetailItem)


