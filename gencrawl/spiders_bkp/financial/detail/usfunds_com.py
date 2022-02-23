from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
import pandas as pd

class UsfundsComDetail(FinancialDetailSpider):
    name = 'financial_detail_usfunds_com'

    def get_items_or_req(self, response, default_item={}):
        file=open("usfunds.html","w")
        file.write(response.text)
        file.close()
        items = super().get_items_or_req(response, default_item)
        gross_url = "https://www.usfunds.com"+response.xpath("//a[text()='Performance']//@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        print(gross_url)
        yield self.make_request(gross_url, callback=self.performance, meta=meta)

    def performance(self, response):
        items = response.meta['items']
        gross_expense_table=response.xpath("//table[@class='returnsTable']//caption[contains(text(),'Quarter')]//parent::table").extract()[0]
        gross = pd.read_html(gross_expense_table)
        final_gross = gross[0].to_dict('dict')
        items[0]['total_expense_gross']=final_gross['Gross Expense Ratio'][0]
        meta = response.meta
        meta['items'] = items
        url="https://www.usfunds.com/our-funds/fund-performance/dividends-distributions/"
        yield self.make_request(url, callback=self.parse_dividends, meta=meta,dont_filter=True)

    def parse_dividends(self,response):
        items = response.meta['items']
        print(items[0])
        print("inside dividends")
        print(len(items))
        file = open("usfunddedddds.html", "w")
        file.write(response.text)
        file.close()
        try:
            #table_data = response.xpath("//h1[contains(text(),'Dividends & Distributions')]//following::table[2]//tbody//tr[position()>1]")
            #print(response.xpath("//h1[contains(text(),'Dividends & Distributions')]//following::table[2]//tbody//tr[position()>1]//td[2]//text()").extract())


            for item in items:
                table_data=response.xpath("//table[@class='returnsTable'][2]/tr[position()>1]")
                #if (table_data == []):
                 #   print("cdsc")

                print(len(table_data))
                dividends_list=[]
                for row in table_data:
                    print(item['instrument_name'].lower().strip() in row.xpath(".//td[1]//text()").extract_first().lower().strip())
                    print(row.xpath(".//td[1]//text()").extract_first())
                    if(item['instrument_name'].lower().strip() in row.xpath(".//td[1]//text()").extract_first().lower().strip()):
                        data_dict1 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                                      "record_date": "", "per_share": "", "reinvestment_price": ""}
                        data_dict2 = {'long_term_per_share': "", 'cg_ex_date': "", 'cg_record_date': "", 'cg_pay_date': "",
                                      'short_term_per_share': "", 'total_per_share': "", 'cg_reinvestment_price': ""}
                        data_dict1['ex_date']=row.xpath(".//td[2]//text()").extract_first()
                        data_dict1['per_share']=row.xpath(".//td[3]//text()").extract_first()
                        data_dict1['reinvestment_price']=row.xpath(".//td[4]//text()").extract_first()
                        dividends_list.append(data_dict1)
                        print(dividends_list)
                item['dividends']=dividends_list
                yield self.generate_item(item, FinancialDetailItem)
        except:
            yield self.generate_item(items[0], FinancialDetailItem)