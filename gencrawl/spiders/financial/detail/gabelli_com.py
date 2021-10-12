from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics
import requests

class GabelliComDetail(FinancialDetailSpider):
    name = 'financial_detail_gabelli_com'
    allowed_domains = ['gabdotcom-api.com']
    custom_settings = {
        "RETRY_TIMES": 5,
        "COOKIES_ENABLED": True,
        "COOKIES_DEBUG": True,
        "CRAWLERA_ENABLED": True,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 4,
    }

    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)
        file=open("gabeill.html","w")
        file.write(response.text)
        file.close()
        api_url="https://gabdotcom-api.com/api/v1/tax_info/"+items[0]['fund_url'].rsplit("/")[-1]
        print(api_url)
        resp = requests.get(api_url)
        print("heree")
        json_resp = json.loads(resp.text)
        print(json_resp)
        year_list=[]
        item=items[0]
        capital_gain_list=[]
        dividends_list=[]
        for row in json_resp:
            for j in json_resp[row]:
                data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "","record_date": "", "per_share": "", "reinvestment_price": ""}
                data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                              'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
                data_dict1['ex_date']=j['ex_date'].split("T")[0]
                data_dict1['pay_date']=j['pay_date'].split("T")[0]
                data_dict2['long_term_per_share']=j['lt_gains']
                data_dict2['short_term_per_share']=j['st_gains']
                data_dict1['per_share']=j['total_dist']
                data_dict1['ordinary_income']=j['inv_income']
                capital_gain_list.append(data_dict2)
                dividends_list.append(data_dict1)
        item['capital_gains']=capital_gain_list
        item['dividends']=dividends_list
        yield self.generate_item(item, FinancialDetailItem)


