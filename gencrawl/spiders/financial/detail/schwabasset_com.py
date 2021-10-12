from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
from tssplit import tssplit

from datetime import datetime
import datetime
import re
from gencrawl.util.statics import Statics
import itertools
import traceback
from copy import deepcopy

class SchwabassetComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_schwabasset_com'
    #allowed_domains = ['js.hs-banner.com']
    '''
    custom_settings = {
        "HTTPCACHE_ENABLED": False,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 4,
        "COOKIES_ENABLED": True,
        "COOKIES_DEBUG": True,
        "CRAWLERA_ENABLED":True
    }
    '''
    def get_items_or_req(self, response, default_item={}):
        items = super().get_items_or_req(response, default_item)
        # items = self.prepare_mapped_items(response, default_item)
        #url="https://js.hs-banner.com/cookie-banner/activity/click"
        #headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Accept-Encoding": "gzip, deflate, br","Accept-Language": "en-GB,en;q=0.9","Connection": "keep-alive","Cookie": 'csrftoken=eneIh9kDRI3LWet7SM29FRwEGkWljvBWHBiYLoZMYNP6PbPgfDK5qps6tzincw6Z; sessionid=amy0hswkwjrieyoj7n4ohggbjsvpzzeo; _gid=GA1.2.1412402084.1632728464; __hstc=136834799.b074e7c798f993551eb8103711f3696d.1632728470282.1632728470282.1632728470282.1; hubspotutk=b074e7c798f993551eb8103711f3696d; __hssrc=1; __hs_opt_out=no; __hs_initial_opt_in=true; srpperm="UT=A&JR=US&timestamp=2021-09-27T07%3A41%3A35.775088%2B00%3A00"; _ga_26HLM6RH2Z=GS1.1.1632728462.1.1.1632728500.0; _ga_86NWGFJN3V=GS1.1.1632728462.1.1.1632728500.0; _ga=GA1.2.1747902728.1632728462; __hssc=136834799.2.1632728470282',"Host": "www.cullenfunds.com","sec-ch-ua": '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',"Upgrade-Insecure-Requests": "1","User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

        meta = response.meta
        meta['items'] = items
        #print(items)
        try:
            test=response.xpath("//a[contains(text(),'Export Data')]//@href").extract()[0]
            print(test)
            url="https://www.schwabassetmanagement.com"+response.xpath("//a[contains(text(),'Export Data')]//@href").extract()[0]

            yield self.make_request(url,meta=meta,callback=self.parse_dividends, dont_filter=True)
        except:
            yield self.generate_item(items[0], FinancialDetailItem)
    def parse_dividends(self, response):
        items = response.meta['items']
        item=items[0]
        file=open("schwab.html","w")
        file.write(response.text)
        file.close()
        #print(response.text)
        data=response.text.split("\n")
        data = [i.replace("\r", "").strip() for i in data]
        while '' in data:
            data.remove('')
        data.remove(data[0])
        data.remove(data[-1])
        print(data)

        capital_gain_list=[]
        dividend_list=[]


        for row in data:
            print(row)
            row_list=row.split(",")
            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                          "record_date": "", "per_share": "", "reinvestment_price": ""}
            data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                          'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
            data_dict1['ex_date']=row_list[0]
            data_dict1['record_date']=row_list[1]
            data_dict1['pay_date']=row_list[2]
            data_dict1['ordinary_income']=row_list[3]
            data_dict2['short_term_per_share']=row_list[4]
            data_dict2['long_term_per_share']=row_list[5]
            data_dict1['per_share']=row_list[7]
            capital_gain_list.append(data_dict2)
            dividend_list.append(data_dict1)
        item['capital_gains']=capital_gain_list
        item['dividends']=dividend_list
        yield self.generate_item(item, FinancialDetailItem)



        '''
        item=items[0]
        temp_items=[]
        #print("yuyuyuyuyuyuyuyyuyuyuyuuyuyuui",response.text)
        share_class=response.xpath("(//span[contains(text(),'Share class')]//following::ul)[1]//li//text()").extract()
        for i in share_class:
            item['share_class']=i.split("(")[0]
            item['nasdaq_ticker']=re.findall(r'\(.*?\)',i)
            temp_items.append(deepcopy(item))
        file = open(share_class[0]+"_cullen.html", "w")
        file.write(response.text)
        file.close()
        temp_data = re.findall("<script>.*?('dividends-data')(.*?)</script>",response.text.replace("\n", "").replace("\r", "").replace("\t", ""))[0]
        temp_data_headers=re.findall("\).publish\((.*?)\);",temp_data[1])[0]
        finding_rows=(re.findall("{.*?rows:(.*?)], uuid.*?}", temp_data_headers)[0]).split("], [")
        capital_gain_list=[]
        dividends_list=[]

        for row in finding_rows:
            final_data=tssplit(row, delimiter=',')
            #for data in final_data:
            #print(data)
            data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "","record_date": "", "per_share": "", "reinvestment_price": ""}
            data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
            data_dict1['ex_date']=final_data[1].strip()
            data_dict1['record_date']=final_data[0].replace("[",'').strip()
            data_dict1['ordinary_income']=final_data[2].strip()
            data_dict2['short_term_per_share']=final_data[3].strip()
            data_dict2['long_term_per_share']=final_data[4].replace("]","").strip()
            data_dict1['reinvestment_price']=final_data[5].replace("]","").strip()
            capital_gain_list.append(data_dict2)
            dividends_list.append(data_dict1)

        for i in temp_items:
            i['capital_gains']=capital_gain_list
            i['dividends']=dividends_list
            yield self.generate_item(i, FinancialDetailItem)
    '''







