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
import requests
from lxml import html
from scrapy.selector import Selector
import copy


class yorktownfundsDetail(FinancialDetailFieldMapSpider):
    name = 'yorktownfunds_com'

    custom_settings = {
        "HTTPCACHE_ENABLED": False,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 4,
        "COOKIES_ENABLED": True,
        "COOKIES_DEBUG": True,
        "CRAWLERA_ENABLED":True
    }

    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
       
        meta = response.meta
        
        #print("fff:",items)

        temp_ticker_list = ['YOVAX','YOVLX','YOVIX']
        temp_class_list = ['A','L','I']

        if items[0]['fund_url']=="https://yorktownfunds.com/funds-performance/small-cap-fund-2/":
                item_copy = copy.deepcopy(items[0])
                item_copy['nasdaq_ticker']='YOVIX'
                items.append(item_copy)
                items[0]['share_class']='A'
                items[1]['share_class']='L'
                items[2]['share_class']='I'
                
                
        meta['items'] = items  

        #open('yorktownfunds.html','w',encoding='utf-8').write(response.text)

        url ="https://yorktownfunds.com/funds-performance/distributions/"

        yield scrapy.Request(url,method='GET',callback=self.distributions,meta=meta,dont_filter=True)

    def distributions(self,response):
        meta = response.meta

        items = meta['items']

        
        

        #open('yorktownfunds.html','w',encoding='utf-8').write(response.text)

        final_data =[]

        for dist_years_block in response.xpath("//div[@class='tb-heading' and contains(text(),'Monthly')]"):
            main_data_block=[]
            #dist_year = dist_years_block.xpath("@id").get()
            #print("dist_year:",dist_year.split('-')[0])
            #print(dist_years_block)
            heading = dist_years_block.xpath("text()").get()
            #print("heading:",heading)

            for block in dist_years_block.xpath("parent::div/table/*"):
                #print(block)
                #heading = table_data.xpath("parent::table/parent::div/div/text()").get()
                #print("table_data:",table_data)
                for h in block.xpath("tr"):
                    td_block=[]
                    td_block.append(heading)
                    #td_block.append(dist_year.split('-')[0])
                    for t in h.xpath("*"):
                        #print("sss:",t.xpath("text()").get())
                        td_value =t.xpath("text()").get()

                        if td_value=='\n':
                            #print("inside...")
                            td_value =t.xpath("p/text()").get()

                        

                        
                        #print("td_value:",heading,td_value)
                        
                        td_block.append(td_value)


                        for t1 in t.xpath("table/*/tr/*"):
                            #print(t1.xpath("text()").get())

                            td_block.append(t1.xpath("text()").getall())

                    main_data_block.append(td_block) 

            final_data.append(main_data_block)
        
        print("final_data:",final_data)

        

        for i in items:
            #print(i)

                
            capital_gain_list=[]
            dividends_list=[]
            #print("fff:",'CLASS '+i['share_class'],i['nasdaq_ticker'],i['instrument_name'])
            #print(i['dividends'])

            for d in final_data:

                #print("dddd",d)

                if len(d)>0:
                    #print(d[0][0])
                    #if d[0][0]=='2013 Quarterly Capital Income Fund Distributions':
                    #    break
                    if 'Capital Gains' in d[0][0] and i['instrument_name'] in d[0][0]:
                        print("yipee")
                        #print(d[0])
                        for class_loc,t in enumerate(d[0]):
                            
                            #print(d,type(d))
                            #if isinstance(t,list):
                            
                            #    print(t,type(t),len(t))

                                #print(t[0],t[1])
                                #if len(t)==2:
                                    #if 'CLASS '+i['share_class']==t[0] and i['nasdaq_ticker'] in t[1]:
                            
                            temp = i['share_class']
                            if temp=='I':
                                temp='INST.'
                            else:
                                temp = 'CLASS '+temp

                            if temp==t:
                                #print("hurray !!!")
                                #print(d,class_loc,len(d))

                                #print("Class_loc:",class_loc)

                                for record_date_loc,t in enumerate(d[0]):
                                    if 'RECORD'==t:
                                        print("Record_date:",record_date_loc)
                                for ex_date_loc,t in enumerate(d[0]):
                                    if 'EX-DIV/'==t:
                                        print("ExDate:",ex_date_loc)
                                for payable_date_loc,t in enumerate(d[0]):
                                    if 'PAYABLE'==t:
                                        print("Payable_date:",payable_date_loc)




                                for c in range(1,len(d)):
                                    #print(c,d[c][7],d[c][8],d[c][9])

                                    cg_record_date = d[c][record_date_loc]
                                    cg_pay_date = d[c][payable_date_loc]
                                    cg_ex_date=""
                                    cg_reinvestment_price=""

                                    #print(d[c][1])
                                    if d[c][1]=='Short Term':
                                        #print("here1")
                                        short_term_per_share=d[c][class_loc].strip()
                                        #print("short_term_per_share:",short_term_per_share)
                                    if d[c][1]=='Long Term':
                                        #print("here2")
                                        long_term_per_share=d[c][class_loc].strip()
                                        #print("long_term_per_share:",long_term_per_share)


                                data_dict1={"cg_ex_date": cg_ex_date, "cg_record_date": cg_record_date, "cg_pay_date": cg_pay_date, "short_term_per_share": short_term_per_share,"long_term_per_share": long_term_per_share, "total_per_share": "", "cg_reinvestment_price": cg_reinvestment_price}
                                    #data_dict2={"ex_date": ex_date, "pay_date": pay_date, "ordinary_income": "", "qualified_income": "", "record_date": record_date,"per_share": per_share, "reinvestment_price": ""}
                                #print(data_dict1)
                                capital_gain_list.append(data_dict1)
                    else:
                        for counter,t in enumerate(d[0]):
                            #print(d,type(d))

                            if isinstance(t,list):
                            
                                #print("Hurray",t,type(t),len(t))

                                #print(t[0],t[1])
                                if len(t)==2:
                                    #if 'CLASS '+i['share_class']==t[0] and i['nasdaq_ticker'] in t[1]:
                                    #print("ttt:",t,d[0][0])

                                    temp = i['share_class']
                                    if temp=='I':
                                        temp='INST.'
                                    else:
                                        temp = 'CLASS '+temp

                                    if temp==t[0] and i['nasdaq_ticker'] in t[1]:
                                        print("hurray !!!",counter)
                                        print(d)
                                        #print("vinod:",d,len(d),counter)

                                        if '2013 Quarterly Capital Income Fund Distributions' in d[0][0]:
                                            print("escaped")

                                            
                                        elif '2014 Quarterly Capital Income Fund Distributions' in d[0][0]:
                                            print("escaped")

                                        else:

                                            for c2,t in enumerate(d[0]):
                                                if 'RECORD'==t:
                                                    record_date_loc=c2
                                                    print("Record_date:",record_date_loc)
                                            for c2,t in enumerate(d[0]):
                                                if 'EX-DIVIDEND/'==t:
                                                    ex_date_loc=c2
                                                    print("ExDate:",ex_date_loc)
                                            for c2,t in enumerate(d[0]):
                                                if 'PAYABLE'==t:
                                                    payable_date_loc=c2
                                                    print("Payable_date:",payable_date_loc)
                                            for c2,t in enumerate(d[0]):
                                                if 'EX-DATE'==t:
                                                    ex_date_date_loc=c2
                                                    print("ex_date:",ex_date_date_loc)


                                           

                                            for c in range(1,len(d)):
                                                #print(c,d[c][7],d[c][8],d[c][9])
                                                #print(d[c])

                                                record_date = d[c][record_date_loc-1]
                                                pay_date = d[c][payable_date_loc-1]
                                                ex_date=d[c][ex_date_date_loc-1]
                                                #reinvestment_price=d[c][8]
                                                #print("d[c][counter]:", d[c][counter-1][0])
                                                per_share = d[c][counter-1][0]
                                                ordinary_income = d[c][counter-1][0]

            #                                   data_dict1={"cg_ex_date": cg_ex_date, "cg_record_date": cg_record_date, "cg_pay_date": cg_pay_date, "short_term_per_share": "","long_term_per_share": "", "total_per_share": "", "cg_reinvestment_price": cg_reinvestment_price}
                                            
                                    
                                    
                                                data_dict2={"ex_date": ex_date, "pay_date": pay_date, "ordinary_income": ordinary_income, "qualified_income": "", "record_date": record_date,"per_share": per_share, "reinvestment_price": ""}
                                                #print(data_dict2)

            # #print(data_dict1)
                                                dividends_list.append(data_dict2)
            i['capital_gains']=capital_gain_list
            i['dividends']=dividends_list

            yield self.generate_item(i, FinancialDetailItem)
        