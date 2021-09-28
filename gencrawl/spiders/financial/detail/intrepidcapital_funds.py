import pandas as pd
import numpy as np
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import requests
import json
from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics
import datetime


class IntrepidcapitalComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_intrepidcapital_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)

        url=response.xpath("//a[contains(text(),'Distributions')]//@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        yield self.make_request(url, callback=self.parse_distributions, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_GET)


    def parse_distributions(self,response):
        items = response.meta['items']
        file = open("interpridcapital.html", "w")
        file.write(response.text)
        file.close()
        for item in items:
            capital_gain_list=[]
            dividends_list=[]
            temp_share_class=item['share_class']
            print(temp_share_class)
            table_date=response.xpath("(//small[contains(text(),'"+temp_share_class+"')]/following::table[@class='table--mutual-fund table--stats'])[1]//tbody//tr")
            for row in table_date:
                data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                              "record_date": "", "per_share": "", "reinvestment_price": ""}
                data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                              'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
                print(row.xpath(".//td[1]//text()").extract_first())
                if(row.xpath(".//td[1]//text()").extract_first()=="Ordinary Income"):
                    print("inside if")
                    data_dict1['ex_date']=row.xpath('.//th[1]//text()').extract_first()
                    data_dict1['ordinary_income']=row.xpath('.//td[2]//text()').extract_first()
                    print(data_dict1['ordinary_income'])
                    data_dict1['reinvestment_price']=row.xpath('.//td[3]//text()').extract_first()
                elif(row.xpath(".//td[1]//text()").extract_first() == "Long-Term Capital Gain"):
                    print("second if")
                    for i in capital_gain_list:
                        if(i['cg_ex_date']==row.xpath('.//th[1]//text()').extract_first()):
                    #data_dict2['cg_ex_date'] = row.xpath('.//th[1]//text()').extract_first()
                            i['long_term_per_share'] = row.xpath('.//td[2]//text()').extract_first()
                            i['cg_reinvestment_price'] = row.xpath('.//td[3]//text()').extract_first()
                            continue
                        else:
                            data_dict2['cg_ex_date'] = row.xpath('.//th[1]//text()').extract_first()
                            data_dict2['long_term_per_share'] = row.xpath('.//td[2]//text()').extract_first()

                            data_dict2['cg_reinvestment_price'] = row.xpath('.//td[3]//text()').extract_first()
                            #print(data_dict2['long_term_per_share'], data_dict2['cg_ex_date'],
                            #data_dict2['cg_reinvestment_price'])
                elif(row.xpath(".//td[1]//text()").extract_first() == "Short-Term Capital Gain"):
                    for i in capital_gain_list:
                        if(i['cg_ex_date']==row.xpath('.//th[1]//text()').extract_first()):
                            print("isnide 3 if")
                            #data_dict2['cg_ex_date'] = row.xpath('.//th[1]//text()').extract_first()
                            i['short_term_per_share'] = row.xpath('.//td[2]//text()').extract_first()
                            i['cg_reinvestment_price'] = row.xpath('.//td[3]//text()').extract_first()
                            continue
                           # print(data_dict2['short_term_per_share'], data_dict2['cg_ex_date'],
                            #data_dict2['cg_reinvestment_price'])
                        else:
                            data_dict2['cg_ex_date'] = row.xpath('.//th[1]//text()').extract_first()
                            data_dict2['short_term_per_share'] = row.xpath('.//td[2]//text()').extract_first()
                            data_dict2['cg_reinvestment_price'] = row.xpath('.//td[3]//text()').extract_first()

                capital_gain_list.append(data_dict2)
                #print(capital_gain_list)
                dividends_list.append(data_dict1)
            #break
            item['capital_gains'] = capital_gain_list
            #print(item['capital_gains'])
            #df = pd.DataFrame(item['capital_gains'])
            #df = df.groupby('cg_ex_date', as_index=False).agg(lambda x: [y for y in list(set(x)) if str(y) != ''])
            #print(df)

            #df1 = df.applymap(lambda x: x[0] if (len(x) > 0) else None)
            #df1 = df1.applymap(lambda x: None if (x == '') else x)
            #df1 = df1.dropna(how='all', axis=0)
            #df1['cg_ex_date'] = df['cg_ex_date']
            #file=open("test.txt","w")
            #file.write(str(df1.to_dict('records')))
            #file.close()
            #print(df1.to_dict('records'))
           # item['capital_gains'] = df1.to_dict('records')
            item['dividends']=dividends_list
            print(len(dividends_list))
            print(len(capital_gain_list))

            yield self.generate_item(item, FinancialDetailItem)
        #return items