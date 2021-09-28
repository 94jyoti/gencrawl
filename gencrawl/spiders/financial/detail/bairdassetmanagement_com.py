import pandas as pd
import numpy as np

from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import requests
import json
import datetime


class BairdassetmanagementComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_bairdassetmanagement_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        share_class_val = response.xpath("//div[@id='Overview']//select[@class='ddlShareClass']/option/@value").extract()
        total_items = []
        for i in range(len(share_class_val)):
            capital_gain_list=[]
            dividends_list=[]
            fund_manager_list=[]
            api_url = "https://www.bairdassetmanagement.com/api/GetShareClassData?shareClassId="+share_class_val[i]+"&isQuarterEnd=false&isCurrentYear=true"
            rsp_share_waise = requests.get(api_url)
            json_resp = json.loads(rsp_share_waise.text)
            items[i]['nasdaq_ticker'] = json_resp['ShareClass']['Ticker']
            items[i]['cusip'] = json_resp['ShareClass']['CUSIP']
            items[i]['portfolio_assets'] = json_resp['Performance']['FormattedTotalFundAUM']
            
            temp_date = json_resp['ShareClass']['InceptionDate'].replace('T00:00:00','').strip()
            datetime_object = datetime.datetime.strptime(temp_date, "%Y-%m-%d")
            share_inception_date = datetime_object.strftime("%m/%d/%Y")
            items[i]['share_inception_date'] = share_inception_date
            
            items[i]['total_expense_gross'] = json_resp['ShareClass']['GrossExpenseRatio']
            items[i]['total_expense_net'] = json_resp['ShareClass']['NetExpenseRatio']
            items[i]['portfolio_assets_date'] = json_resp['Morningstar']['FormattedDateLabel'\
                                                                ].replace('Data as of ','').strip()
            items[i]['asset_class'] = json_resp['ShareClass']['Style']
            try:
                items[i]['benchmarks'] = json_resp['Benchmarks'][0]['Name']
            except:
                items[i]['benchmarks'] = 'NA'

            json_data=json_resp['Distributions']
            for row in json_data:
                data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "","record_date": "", "per_share": "", "reinvestment_price": ""}
                data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
                data_dict1['ex_date']=row['FormattedExDate']
                data_dict1['pay_date']=row['FormattedPayDate']
                data_dict1['record_date']=row['FormattedRecordDate']
                data_dict1['reinvestment_price']=row['FormattedReinvestmentPrice']
                if(row['DistributionType']=='Income'):
                    data_dict1['per_share']=row['Dividend']
                elif(row['DistributionType']=='Short Term Capital Gain' or row['DistributionType']=='Long Term Capital Gain'):
                    data_dict2['total_per_share']=row['Dividend']
                capital_gain_list.append(data_dict2)
                dividends_list.append(data_dict1)

            api_url1 = "https://www.bairdassetmanagement.com/api/GetShareClassData?shareClassId=" + share_class_val[i] + "&isQuarterEnd=false&isCurrentYear=false"
            rsp_share_waise1 = requests.get(api_url1)
            json_resp1 = json.loads(rsp_share_waise1.text)
            json_data1 = json_resp1['Distributions']
            for row in json_data1:
                data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                              "record_date": "", "per_share": "", "reinvestment_price": ""}
                data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                              'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}


                if (row['DistributionType'] == 'Income'):
                    data_dict1['per_share'] = row['Dividend']

                    data_dict1['ex_date'] = row['FormattedExDate']
                    data_dict1['pay_date'] = row['FormattedPayDate']
                    data_dict1['record_date'] = row['FormattedRecordDate']
                    data_dict1['reinvestment_price'] = row['FormattedReinvestmentPrice']
                elif (row['DistributionType'] == 'Short Term Capital Gain'):
                    data_dict2['short_term_per_share'] = row['Dividend']
                    data_dict2['cg_reinvestment_price']=row['FormattedReinvestmentPrice']
                    data_dict2['cg_ex_date']=row['FormattedExDate']
                    data_dict2['cg_pay_date']=row['FormattedPayDate']
                    data_dict2['cg_record_date']=row['FormattedRecordDate']
                elif(row['DistributionType'] == 'Long Term Capital Gain'):
                    data_dict2['cg_reinvestment_price'] = row['FormattedReinvestmentPrice']
                    data_dict2['cg_ex_date'] = row['FormattedExDate']
                    data_dict2['cg_pay_date'] = row['FormattedPayDate']
                    data_dict2['cg_record_date'] = row['FormattedRecordDate']
                    data_dict2['long_term_per_share'] = row['Dividend']
                capital_gain_list.append(data_dict2)
                dividends_list.append(data_dict1)

            items[i]['capital_gains']=capital_gain_list
            print(items[i]['capital_gains'])
            df=pd.DataFrame(items[i]['capital_gains'])
            df=df.groupby('cg_record_date',as_index=False).agg(lambda x: [y for y in list(set(x)) if str(y) != ''])

            df1=df.applymap(lambda x : x[0] if(len(x)>0) else None)
            df1=df1.applymap(lambda x : None if(x=='') else x)
            df1=df1.dropna(how='all', axis=0)
            df1['cg_record_date']=df['cg_record_date']
            items[i]['capital_gains']=df1.to_dict('records')
            items[i]['dividends']=dividends_list
            print(items[i]['capital_gains'])


        return items
        