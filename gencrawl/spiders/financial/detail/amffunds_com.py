from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics


class AmffundsComDetail(FinancialDetailSpider):
    name = 'financial_detail_amffunds_com'

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        meta = response.meta
        meta['items'] = items
        file = open("amf.html", "w")
        file.write(response.text)
        file.close()
        url="https://www.amffunds.com/html/div-"+items[0]['fund_url'].split("-")[-1].replace(".php","").lower()+".html"
        yield self.make_request(url, callback=self.parse_dividends, meta=meta,dont_filter=True)


    def parse_dividends(self,response):
        items = response.meta['items']
        print("here")
        file=open("amffunds.html","w")
        file.write(response.text)
        file.close()
        counter=1
        flag=1
        final_data_list=[]
        while flag:

            #print("//table//b[contains(text(),'Record Date')]/following::table[1]//tr//td[contains(@align,'center')]//span[1]//text()["+str(counter)+"] | //table//b[contains(text(),'Record Date')]/following::table[1]//tr//td[contains(@align,'center')]//p//text()["+str(counter)+"]")
            table_data = response.xpath(
                "//table//b[contains(text(),'Record Date')]/following::table[1]//tr//td[contains(@align,'center') or contains(@align,'right')]//span[1]//text()[" + str(
                    counter) + "] | //table//b[contains(text(),'Record Date')]/following::table[1]//tr//td[contains(@align,'center')]//p//text()[" + str(
                    counter) + "]").extract()

            #table_data=response.xpath("//table//b[contains(text(),'Record Date')]/following::table[1]//tr//td[contains(@align,'center')]//span[1]//text()["+str(counter)+"] | //table//b[contains(text(),'Record Date')]/following::table[1]//tr//td[contains(@align,'center')]//p//text()["+str(counter)+"]").extract()
            if (table_data == []):
                flag = 0
                break
            table_data=[data.replace("\n","").replace("\t","").strip() for data in table_data]
            counter = counter + 1
            final_data_list.append(table_data)

        #print(final_data_list)
        distribution_list = []
        count=1
        for data in final_data_list:
            print(data)
            print(count)
            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                          "record_date": "", "per_share": "", "reinvestment_price": ""}
            data_dict1['record_date'] = data[0]
            data_dict1['pay_date'] = data[1]
            try:
                temp_per_share = data[2].split(" ")
                data_dict1['reinvestment_price'] = data[3]
                print("yahan tk a gya")
                while('' in temp_per_share):
                    temp_per_share.remove('')
                print("yahan bhi aa gye")
                print(len(temp_per_share))
                count=count+1
                print("yahan bhi aa gye")
                if(len(temp_per_share)==2):
                    print(data)
                    print(count)
                    break
                else:
                    data_dict1['per_share'] = data[2]
            except:
                print("data",data)
                data_dict1['per_share'] = data[2]

            distribution_list.append(data_dict1)
            #print(distribution_list)
        data_list_divide=final_data_list[count-2:]
        print("diviide----------------",data_list_divide)
        flag=0
        for data in data_list_divide:
            print(data)
            if(flag==1):
                temp_per_share.append(data[2])
            if(len(data[2].split(" "))==2):
                temp_per_share = data[2].split(" ")
            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                          "record_date": "", "per_share": "", "reinvestment_price": ""}
            print(temp_per_share)
            while ('' in temp_per_share):
                temp_per_share.remove('')
            if(len(temp_per_share)==2):
                print("inside temp if")
                data_dict1['per_share']=temp_per_share[0]
                print(temp_per_share[0])
                temp_per_share.remove(temp_per_share[0])
                flag=1
            else:
                data_dict1['per_share'] = temp_per_share[0]



            data_dict1['record_date'] = data[0]
            data_dict1['pay_date'] = data[1]
            if(len(data)==4):
                data_dict1['reinvestment_price'] = data[2]
            print(data_dict1)


            distribution_list.append(data_dict1)





            '''
            for row in row_data:
                print("inside second for")
                print("row:::::",row)
                data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                              "record_date": "", "per_share": "", "reinvestment_price": ""}
                data_dict1['record_date']=row[0]
                data_dict1['pay_date']=row[1]
                data_dict1['per_share']=row[2]
                data_dict1['reinvestment_price']=row[3]
                distribution_list.append(data_dict1)
                print(distribution_list)
                break
            break'''
        items[0]['dividends']=distribution_list
        yield self.generate_item(items[0], FinancialDetailItem)