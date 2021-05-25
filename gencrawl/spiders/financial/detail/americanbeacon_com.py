from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd

class AmericanbeaconDetail(FinancialDetailSpider):
    name = 'financial_detail_americanbeacon_com'
    #allowed_domains = ['api.nuveen.com','www.nuveen.com']
    
    def get_items_or_req(self, response, default_item={}):
        
        # request = []
        items = self.prepare_items(response, default_item)
        #return_data=item['temp_class_returns'][0]
        #print("itemdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",items)
        for i in items:
            temp_data_returns=i['class_returns']
            temp_expense_ratio=i['class_expense_ratios']
            temp_class_benchmark=i['class_benchmarks']
            temp_sec_30=i['sec_30']
            #print(temp_data_returns)
            count=1
            for data in temp_data_returns:
                for j in data:
                    if(i['share_class']== data['share_class_1'].split(" ")[0].strip()):
                        i['share_inception_date']=data['inception_date']
                        break
                for expense in temp_expense_ratio:
                    for ex in expense:
                        if(i['share_class']==expense['expense_ratios_share_class']):
                            i['total_expense_gross']=expense['expense_ratios_gross']
                            i['total_expense_net']=expense['expense_ratios_net']
                bench_mark=[]
                for benchmark in temp_class_benchmark:
                    bench_mark.append(benchmark['benchmarks'])
                i['benchmarks']=bench_mark
                for sec in temp_sec_30:
                    for s in sec:
                        if(i['share_class']==sec['sec_30_share_class']):
                            i['sec_yield_30_day']=sec['sec_30_actual']
                            i['sec_yield_without_waivers_30_day']=sec['sec_30_unsubsized']

                #del i['sec_30']
                #del i['class_expense_ratios']
                #del i['class_benchmarks']
                #del i['class_returns']
#        print("doooookdnwdwdnwdwkdwkdkdnwdwdkndkwnwdnwkkn",items[0])
        yield self.generate_item(items[0], FinancialDetailItem)

        #data=[]
        '''
        soup = BeautifulSoup(return_data)
        table = soup.find('table', attrs={'id':'grdPerformance'})
        headers=[ele.text.strip() for ele in table.find_all('th')]
        table_body = table.find('tbody')
        rows = table.find_all('tr')
        data.append(headers)
        for row in rows:
            #for col in row.find_all('td'):
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
            data = [ele for ele in data if ele]
        #print(data)

        df_return_data=pd.DataFrame(return_data[1:],columns=return_data[0])
        print(df_return_data)
        '''
        #soup = BeautifulSoup(return_data, 'html.parser')
        #table = soup.find('table', attrs={'id':'grdPerformance'})
        #keys =[ele.text.strip() for ele in soup.find_all('th')]
        #rows = table.find_all('tr')
        
        #vals = [i.text for i in soup.find('tr', {'class': None}).find_all('td')]
        #for row in rows:
            #for col in row.find_all('td'):
         #   cols = row.find_all('td')
          #  cols = [ele.text.strip() for ele in cols]
           # data.append([ele for ele in cols if ele])
            #data = [ele for ele in data if ele]
        #vals=data
        #my_dict = dict(zip(keys, vals))
        #print (my_dict)