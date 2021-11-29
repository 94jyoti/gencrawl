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


class NicholasFundsDetail(FinancialDetailFieldMapSpider):
    name = 'nicholasfunds_com'

    
    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        meta = response.meta
        meta['items'] = items

        fundname_class_expense_ratio_list = []

        selector = scrapy.Selector(text=response.text, type="html")

        fund_assets_currency = selector.xpath("//strong[contains(text(),'Fund Assets')]/text()").get()

        print("fund_assets_currency:",fund_assets_currency)

        currency_symbol = re.findall(r"\((.*)\)",fund_assets_currency)[0]

        print(currency_symbol)

        for s in selector.xpath("//td[contains(text(),'Expense Ratio')]"):
            ss = s.xpath("text()").get()
            tt = s.xpath("following-sibling::td/text()").get()
            #print("ss:",ss,tt)
            fundname_class_expense_ratio_list.append((ss,tt))

        temp_distribution_list = []
        for block in selector.xpath("//select[@id='F21_1_select']/option"):
            distribution_years = block.xpath("text()").get()
            distribution_classification = block.xpath("@value").get()
            temp_distribution_list.append([distribution_years,distribution_classification])

        share_count=0

        temp_dis_list = []
        dist_year = '2021'

        for block in selector.xpath("//h4[contains(text(),'Distribution History')]"):
            share_class_temp = block.xpath("text()").get().split('-')[-1].strip()
            print("share_class_temp:",share_class_temp)

            count=0
            share_count = share_count+1
            print("share_count:",share_count)

            for main_table in block.xpath("following::div[2]"):
                for main_table_row in main_table.xpath("table/tbody/tr"):
                    count=count+1

                    if count==1:
                        for td in main_table_row.xpath("td/strong"):
                        
                            td_value = td.xpath("text()").get()

                    if count>1 and share_count==1:

                        td_list=[]
                        for td in main_table_row.xpath("td"):
                        
                            td_value = td.xpath("span/text()|text()").get()
                            td_list.append(td_value)
                        temp_dis_list.append([share_class_temp,dist_year,td_list])

                    if count>1 and share_count>1:
                        td_list=[]

                        for td in main_table_row.xpath("td"):

                        
                            td_value = td.xpath("span/text()|text()").get()
                            td_list.append(td_value)
                        temp_dis_list.append([share_class_temp,dist_year,td_list])
        
        for c,i in enumerate(items):

            capital_gain_list=[]

            if 'share_class' in items[0].keys():

                #print("iiiii:",i)

                for s in temp_dis_list:
                    print("ssss:",s)
                    if s[0]==items[c]['share_class']:
                        print("hello:",s[0],items[c]['share_class'])

                        cg_record_date =""
                        cg_ex_date =""
                        cg_pay_date =s[2][0]
                        long_term_per_share =s[2][3]
                        short_term_per_share =s[2][2]
                        short_term_per_share =s[2][2]
                        total_per_share=s[2][4]

                        data_dict1={"cg_ex_date": cg_ex_date, "cg_record_date": cg_record_date, "cg_pay_date": cg_pay_date, "short_term_per_share": short_term_per_share,"long_term_per_share": long_term_per_share, "total_per_share": total_per_share, "cg_reinvestment_price": ""}
                        capital_gain_list.append(data_dict1)

                i['total_net_assets'] = i['total_net_assets'] + " "+ currency_symbol

                for j in fundname_class_expense_ratio_list:

                    #print("jjjjj",j[0])
                    if i['instrument_name'].split(",")[0].strip() in j[0] and i['share_class'] in j[0]:
                        #print("matched:",j)
                        i['total_expense_gross'] = j[1]
                        i['capital_gains']=capital_gain_list

                        #yield self.generate_item(i, FinancialDetailItem)
                meta['item'] = i
                capital_gains_no_of_years = len(temp_distribution_list[1:-1])
                meta['capital_gains_no_of_years'] = capital_gains_no_of_years
                print("temp_distribution_list_final:",temp_distribution_list[1:-1],capital_gains_no_of_years)
                for y in temp_distribution_list[1:-1]:
                    print(y,y[1])

                    docID = selector.xpath("//input[@id='F21_DocID']/@value").get()

                    #print("docID:",docID)

                    url = "https://www.nicholasfunds.com/display/components/Blocks/AggregationV2/Support/AggregationV2Ajax.asmx/GetFilterResults"

                    payload = {
                    "docID":docID,
                    "blockID":"21",
                    "args":{"pageNumber":"1","keyword":"","classifications":y[1]}
                    }

                    headers={
                        "Content-Type": "application/json; charset=UTF-8",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"

                    }

                    #print(payload)
                    yield scrapy.Request(url,method='POST',headers=headers,body=json.dumps(payload),callback=self.distributions,dont_filter=True,meta=meta)


            else:
                #print("iiiii:",i)
                #print("share_class: ",response.url,"",i['instrument_name'].split(",")[0])
                print("inside_else")


                for s in temp_dis_list:
                    print("ssss:",s)
                    
                    cg_record_date =""
                    cg_ex_date =""
                    cg_pay_date =s[2][0]
                    long_term_per_share =s[2][3]
                    short_term_per_share =s[2][2]
                    total_per_share=s[2][4]

                    
                    
                    data_dict1={"cg_ex_date": cg_ex_date, "cg_record_date": cg_record_date, "cg_pay_date": cg_pay_date, "short_term_per_share": short_term_per_share,"long_term_per_share": long_term_per_share, "total_per_share": total_per_share, "cg_reinvestment_price": ""}
                    #data_dict2={"ex_date": ex_date, "pay_date": pay_date, "ordinary_income": "", "qualified_income": "", "record_date": record_date,"per_share": per_share, "reinvestment_price": ""}
                    #data_dict2['ex_date']=year[i]
                    #data_dict1['total_per_share']=capital_gains[i]
                    #data_dict2['ordinary_income']=dividends[i]
                    capital_gain_list.append(data_dict1)
                    #dividends_list.append(data_dict2)
            
                    #items[0]['dividends']=dividends_list

                   


                i['total_net_assets'] = selector.xpath("//strong[contains(text(),'Fund Assets')]//parent::td//following-sibling::td//text()").get()
                i['total_net_assets'] = i['total_net_assets'] + " "+ currency_symbol
                i['minimum_initial_investment'] = selector.xpath("//strong[contains(text(),'Minimum Initial Investment')]//parent::td//following-sibling::td//text()").get()
                for j in fundname_class_expense_ratio_list:
                    if i['instrument_name'].split(",")[0].strip() in j[0]:
                        #print("matched:",j)
                        i['total_expense_gross'] = j[1]
                        i['capital_gains']=capital_gain_list
                        

                meta['item'] = i
                capital_gains_no_of_years = len(temp_distribution_list[1:-1])
                meta['capital_gains_no_of_years'] = capital_gains_no_of_years
                print("temp_distribution_list_final:",temp_distribution_list[1:-1],capital_gains_no_of_years)
                for y in temp_distribution_list[1:-1]:
                    print(y,y[1])

                    docID = selector.xpath("//input[@id='F21_DocID']/@value").get()

                    print("docID:",docID)

                    url = "https://www.nicholasfunds.com/display/components/Blocks/AggregationV2/Support/AggregationV2Ajax.asmx/GetFilterResults"

                    payload = {
                    "docID":docID,
                    "blockID":"21",
                    "args":{"pageNumber":"1","keyword":"","classifications":y[1]}
                    }

                    headers={
                        "Content-Type": "application/json; charset=UTF-8",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"

                    }

                    print(payload)
                    yield scrapy.Request(url,method='POST',headers=headers,body=json.dumps(payload),callback=self.distributions,dont_filter=True,meta=meta)

                        #yield self.generate_item(i, FinancialDetailItem)

    def distributions(self,response):




        meta = response.meta
        i = meta['item']

        meta['test'] = []

        print("inside here")
        print(i)
        #open('nicholas.html','w',encoding='utf-8').write(response.text)

        json_data = json.loads(response.text)

        print(json_data['d']['htmlData'])

        open('nicholas.html','w',encoding='utf-8').write(json_data['d']['htmlData'])

        share_count=0

        temp_dis_list = []
        dist_year = '2021'


        selector = scrapy.Selector(text=json_data['d']['htmlData'], type="html")

        for block in selector.xpath("//h4[contains(text(),'Distribution History')]"):
            share_class_temp = block.xpath("text()").get().split('-')[-1].strip()
            print("share_class_temp:",share_class_temp)

            count=0
            share_count = share_count+1
            print("share_count:",share_count)



            for main_table in block.xpath("parent::div"):

                
                
                for main_table_row in main_table.xpath("table/tbody/tr"):
                    count=count+1
                    
                    

                    if count==1:

                        print("main_table_row:",main_table_row, count)

                        for td in main_table_row.xpath("td/strong"):
                        
                            td_value = td.xpath("text()").get()

                            print("main_table_td:",td_value)
                            

                    if count>1 and share_count==1:

                        td_list=[]

                        print("main_table_row:",main_table_row, count)

                        for td in main_table_row.xpath("td"):
                        
                            td_value = td.xpath("strong/text()|text()").get()
                            td_list.append(td_value)

                            print("main_table_td:",td_value)
                        temp_dis_list.append([share_class_temp,"",td_list])
                        meta['test'].append(temp_dis_list)

                    if count>1 and share_count>1:
                        td_list=[]
                        print("main_table_row:",main_table_row, count)

                        for td in main_table_row.xpath("td"):

                        
                            td_value = td.xpath("strong/text()|text()").get()
                            td_list.append(td_value)

                            print("main_table_td:",td_value)
                        temp_dis_list.append([share_class_temp,"",td_list])
                        meta['test'].append(temp_dis_list)

        print("temp_dis_list222:",temp_dis_list,len(temp_dis_list))
        #print("tttttt:", meta['test'])


        for s in temp_dis_list:

            print("testing:",s)
            #if i['share']
            print(s[0],s[2])
            if 'share_class' in i.keys():
                if s[0]==i['share_class']:

                    cg_record_date =""
                    cg_ex_date =""
                    cg_pay_date =s[2][0]
                    long_term_per_share =s[2][3]
                    short_term_per_share =s[2][2]
                    total_per_share = s[2][4]

                    
                    
                    data_dict1={"cg_ex_date": cg_ex_date, "cg_record_date": cg_record_date, "cg_pay_date": cg_pay_date, "short_term_per_share": short_term_per_share,"long_term_per_share": long_term_per_share, "total_per_share": total_per_share, "cg_reinvestment_price": ""}
                    #data_dict2={"ex_date": ex_date, "pay_date": pay_date, "ordinary_income": "", "qualified_income": "", "record_date": record_date,"per_share": per_share, "reinvestment_price": ""}
                    #data_dict2['ex_date']=year[i]
                    #data_dict1['total_per_share']=capital_gains[i]
                    #data_dict2['ordinary_income']=dividends[i]
                    i['capital_gains'].append(data_dict1)
            else:
                print("insde_else_block:",s)
                cg_record_date =""
                cg_ex_date =""
                cg_pay_date =s[2][0]
                long_term_per_share =s[2][3]
                short_term_per_share =s[2][2]
                total_per_share = s[2][4]

                    
                    
                data_dict1={"cg_ex_date": cg_ex_date, "cg_record_date": cg_record_date, "cg_pay_date": cg_pay_date, "short_term_per_share": short_term_per_share,"long_term_per_share": long_term_per_share, "total_per_share": total_per_share, "cg_reinvestment_price": ""}
                #data_dict2={"ex_date": ex_date, "pay_date": pay_date, "ordinary_income": "", "qualified_income": "", "record_date": record_date,"per_share": per_share, "reinvestment_price": ""}
                #data_dict2['ex_date']=year[i]
                #data_dict1['total_per_share']=capital_gains[i]
                #data_dict2['ordinary_income']=dividends[i]
                i['capital_gains'].append(data_dict1)


        print("capital_gains_no_of_years:",meta['capital_gains_no_of_years'])
        #x= meta['capital_gains_no_of_years']

        #print(i['capital_gains'],len(i['capital_gains']))

        if len(i['capital_gains'])==meta['capital_gains_no_of_years']:

            yield self.generate_item(i, FinancialDetailItem)


                 










       






    