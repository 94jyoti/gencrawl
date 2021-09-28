from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics
import re
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider


class partnerselectfundsDetail(FinancialDetailFieldMapSpider):
    name = 'partnerselectfunds_com'
    def get_items_or_req(self, response, default_item={}):
        meta = response.meta

        items = self.prepare_items(response, default_item)

        
        meta['items']=items


        tickers = response.xpath("//th[contains(text(),'Expense Ratios')]/following-sibling::th/text()[not(contains(.,'Ratio'))]").getall()

       
        count=0
        for i in items:

            if i['nasdaq_ticker']=="":


                ticker_value = response.xpath("//td[contains(text(),'Symbol')]/following-sibling::td/text()").get()
       

            print("ticker_value:",i['nasdaq_ticker'])


            #count = count+1
            #print("count:",count)

            
            #print("hello:",i['nasdaq_ticker'])

            meta['items'] = items

                

            url = "https://partnerselectfunds.com/distributions/"

            headers = {
                "authority": "partnerselectfunds.com",
                "cache-control": "max-age=0",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\\",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "sec-fetch-site": "none",
                "sec-fetch-mode": "navigate",
                "sec-fetch-user": "?1",
                "sec-fetch-dest": "document",
                "accept-language": "en-US,en;q=0.9,hi;q=0.8"
            }

            yield scrapy.Request(url,method="GET",callback=self.distributions,headers=headers,dont_filter=True,meta=meta)

        
    def distributions(self,response):

        #open('partnerselectfunds.html','w',encoding='utf-8').write(response.text)

        meta = response.meta

        items = meta['items']

        nasdaq_ticker = items[0]['nasdaq_ticker']



        #print("items:",items[0])

        temp_distribution_data_all = re.findall('var visualizer = (.*);', response.text)

        #print("temp_distribution_data_all:",temp_distribution_data_all)

        count=0
        dist_data_final=[]
        for d in temp_distribution_data_all:
            count=count+1

            #print("dd:",d)



            json_data = json.loads(d)['charts']

            #print("count...",count,"....json_data:",json_data['charts'])

            #open('partnerselectfunds11.txt','w',encoding='utf-8').write(json.dumps(json_data))


            #json_data = json.loads(temp_distribution_data_all[0])['charts']
            #print("json_data:",json_data)
            

           
            dist_data_final.append(json_data) 

        xx = dist_data_final[-1]
        #print("dist_data_final:",xx,type(xx))

        #print(list(xx.keys()))

       
        final_data = []
        for x in list(xx.keys()):
            series_list = []
            fund_block_data = []
            series_data = xx[x]['series']
            #print("series_data:",x,series_data)
            block_data = xx[x]['data']
            #print("block_data:",x,block_data)
            for label in series_data:
                #print("label:",label)
                #print(label['label'])
                series_list.append(label['label'])

            #print("series_list:",series_list)

            final_data.append([series_list,block_data])
            #print("fund_block_data:",fund_block_data)

        #final_data.append(fund_block_data)
        print("final_data:",final_data)

        


        #for data in dist_data_final[-1]:

            #print("Keys:",data.keys())
            #keys_value = data.keys()
            #print(keys_value)

        #for k in keys_value:
        #    print(k)

            #for j in dist_data_final:

                #print("jjj:",j[k])






       
        
        #print("Items:",items)

        for i in items:



            capital_gain_list=[]
            dividends_list=[]
            
            
            
            for d in final_data:
           
                # For Capital Gains
                if 'Gain' in ' | '.join(d[0]):
                    print("Here...",d[0],len(d[0]))
                    record_date_loc=""
                    ST_gain_loc=""
                    LT_gain_loc=""
                    ticker_loc=""
                    Net_Investment_Income_loc=""
                    Total_Distribution_loc=""
                    Ex_Div_Date_loc=""
                    Reinvestment_Price_loc=""

                    for index,col_name in enumerate(d[0]):
                        if 'Record' in col_name:
                            print(index,col_name)
                            record_date_loc = index
                        if 'Short-Term Capital Gain' in col_name or 'ST Cap Gains' in col_name:
                            print(index,col_name)
                            ST_gain_loc = index
                        if 'Long-Term Capital Gain' in col_name:
                            print(index,col_name)
                            LT_gain_loc = index
                        if 'Ticker' in col_name:
                            print(index,col_name)
                            ticker_loc = index
                        if 'Net Investment Income' in col_name:
                            print(index,col_name)
                            Net_Investment_Income_loc = index
                        if 'Total Distribution' in col_name:
                            print(index,col_name)
                            Total_Distribution_loc = index
                        if 'Ex-Div Date' in col_name:
                            print(index,col_name)
                            Ex_Div_Date_loc = index
                        if 'Reinvestment Price' in col_name:
                            print(index,col_name)
                            Reinvestment_Price_loc = index


                    for all_row in range(1,len(d)):
                       print("hhh:",d[all_row])
                       for row in d[all_row]:
                        print("row:",row)


                        dist_ticker = row[1].strip()
                        if i['nasdaq_ticker']==dist_ticker:
                            #print("here...",dist_ticker)
                            
                            cg_record_date =row[record_date_loc]
                            cg_ex_date =row[Ex_Div_Date_loc]
                            cg_pay_date =""
                            if LT_gain_loc=="":
                                long_term_per_share =""

                            else:
                                long_term_per_share =row[LT_gain_loc]

                            if ST_gain_loc=="":
                                short_term_per_share=""
                            else:
                                short_term_per_share=row[ST_gain_loc]

                            reinvestment_price =row[Reinvestment_Price_loc]

                            total_per_share = row[Total_Distribution_loc]


                            data_dict1={"cg_ex_date": cg_ex_date, "cg_record_date": cg_record_date, "cg_pay_date": cg_pay_date, "short_term_per_share": short_term_per_share,"long_term_per_share": long_term_per_share, "total_per_share": total_per_share, "cg_reinvestment_price": reinvestment_price}
                            #data_dict2={"ex_date": ex_date, "pay_date": pay_date, "ordinary_income": "", "qualified_income": "", "record_date": record_date,"per_share": per_share, "reinvestment_price": ""}
                            #data_dict2['ex_date']=year[i]
                            #data_dict1['total_per_share']=capital_gains[i]
                            #data_dict2['ordinary_income']=dividends[i]
                            capital_gain_list.append(data_dict1)
                            #dividends_list.append(data_dict2)
                else:
                    print("No_gains")
                    print("else Here...",d[0],len(d[0]))
                    record_date_loc=""
                    ST_gain_loc=""
                    LT_gain_loc=""
                    ticker_loc=""
                    Net_Investment_Income_loc=""
                    Total_Distribution_loc=""
                    Ex_Div_Date_loc=""
                    Reinvestment_Price_loc=""

                    for index,col_name in enumerate(d[0]):
                        if 'Record' in col_name:
                            print(index,col_name)
                            record_date_loc = index
                        if 'Short-Term Capital Gain' in col_name or 'ST Cap Gains' in col_name:
                            print(index,col_name)
                            ST_gain_loc = index
                        if 'Long-Term Capital Gain' in col_name:
                            print(index,col_name)
                            LT_gain_loc = index
                        if 'Ticker' in col_name:
                            print(index,col_name)
                            ticker_loc = index
                        if 'Net Investment Income' in col_name:
                            print(index,col_name)
                            Net_Investment_Income_loc = index
                        if 'Total Distribution' in col_name:
                            print(index,col_name)
                            Total_Distribution_loc = index
                        if 'Ex-Div Date' in col_name:
                            print(index,col_name)
                            Ex_Div_Date_loc = index
                        if 'Reinvestment Price' in col_name:
                            print(index,col_name)
                            Reinvestment_Price_loc = index

                    for all_row in range(1,len(d)):
                       print("hhh:",d[all_row])
                       for row in d[all_row]:
                        print("row:",row)


                        dist_ticker = row[1].strip()
                        if i['nasdaq_ticker']==dist_ticker:
                            #print("here...",dist_ticker)
                            
                            record_date =row[record_date_loc]
                            ex_date =row[Ex_Div_Date_loc]
                            pay_date =""
                            

                            reinvestment_price =row[Reinvestment_Price_loc]

                            total_per_share = row[Total_Distribution_loc]

                            ordinary_income = row[Net_Investment_Income_loc]

                            per_share = row[Net_Investment_Income_loc]




                            #data_dict1={"cg_ex_date": cg_ex_date, "cg_record_date": cg_record_date, "cg_pay_date": cg_pay_date, "short_term_per_share": short_term_per_share,"long_term_per_share": long_term_per_share, "total_per_share": total_per_share, "cg_reinvestment_price": reinvestment_price}
                            data_dict2={"ex_date": ex_date, "pay_date": pay_date, "ordinary_income": ordinary_income, "qualified_income": "", "record_date": record_date,"per_share": per_share, "reinvestment_price": reinvestment_price}
                            #data_dict2['ex_date']=year[i]
                            #data_dict1['total_per_share']=capital_gains[i]
                            #data_dict2['ordinary_income']=dividends[i]
                            #capital_gain_list.append(data_dict1)
                            dividends_list.append(data_dict2)


                    
            i['capital_gains']=capital_gain_list
            i['dividends']=dividends_list
            yield self.generate_item(i, FinancialDetailItem)