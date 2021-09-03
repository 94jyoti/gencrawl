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
            
        return items
        