from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
import datetime
import urllib.parse
from gencrawl.util.statics import Statics
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem

class CalamosfundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_calamos_com'
    custom_settings = {
        "RETRY_TIMES": 5,
        "CRAWLERA_ENABLED": True
    }
    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        for item in items:
            temp_url=item['fund_url'].rsplit("-",1)
            temp_url.remove(temp_url[len(temp_url)-1])
            item['fund_url']="".join(temp_url)+"-"+item['nasdaq_ticker'].lower()+"/"
        meta = response.meta
        meta['items'] = items
        distribution_url=items[0]['fund_url']+response.xpath("(//a[contains(text(),'Distribution')]//@href)[1]").extract()[0]
        print("cddcdccdcdc")
        yield self.make_request(distribution_url, callback=self.parse_distributions, meta=meta, method=Statics.CRAWL_METHOD_GET,dont_filter=True)
    def parse_distributions(self,response):
        items = response.meta['items']
        file=open("calalmos.html","w")
        file.write(response.text)
        file.close()
        capital_temp=response.xpath("//h2[contains(text(),'Total Capital')]//following::table[1]//tbody//tr")
        capital_gain_list=[]
        dividends_list=[]
        dividends_temp=response.xpath("//h2[contains(text(),'Distributions')]//following::table[1]//tbody//tr")

        for row in dividends_temp:
            #print(row)
            #print(row)
            data_dict1={"ex_date": "", "ordinary_income": "", "reinvestment_price": ""}
            print("tetsststst",row.xpath(".//td[1]//text()").extract_first())
            
            try:
                data_dict1['ex_date']=row.xpath(".//td[1]//text()").extract_first()
                data_dict1['ordinary_income']=row.xpath(".//td[2]//text()").extract_first()
                data_dict1['reinvestment_price']=row.xpath(".//td[3]//text()").extract_first()
                dividends_list.append(data_dict1)
            except:
                data_dict1['ex_date'] = row.xpath(".//td[1]//span//text()").extract_first()
                data_dict1['ordinary_income'] = row.xpath(".//td[2]//span//text()").extract_first()
                data_dict1['reinvestment_price'] = row.xpath(".//td[3]//span//text()").extract_first()
                dividends_list.append(data_dict1)
            #print(data_dict1)

        '''
        for row in capital_temp:
            data_dict={"cg_ex_date": "", "total_per_share": ""}
            try:
                data_dict['cg_ex_date']=row.xpath(".//td[1]//text()").extract_first()
                data_dict['total_per_share']=row.xpath(".//td[2]//text()").extract_first()
                capital_gain_list.append(data_dict)
            except:
                data_dict['cg_ex_date'] = row.xpath(".//td[1]//span//text()").extract_first()
                data_dict['total_per_share'] = row.xpath(".//td[2]//span//text()").extract_first()
                capital_gain_list.append(data_dict)
            print(data_dict)

        for item in items:

            item['capital_gains']=capital_gain_list
            yield self.generate_item(item, FinancialDetailItem)'''
        for item in items:
            #item.pop('capital_gains')
            item['dividends'] =dividends_list


            yield self.generate_item(item, FinancialDetailItem)






