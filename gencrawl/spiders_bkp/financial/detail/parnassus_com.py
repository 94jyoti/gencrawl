from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.util.statics import Statics
import json
import scrapy
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from datetime import datetime
import datetime
import urllib.parse
from gencrawl.util.statics import Statics


class parnassusDetail(FinancialDetailSpider):
    name = 'parnassus_com'
    def get_items_or_req(self, response, default_item={}):
        items = self.prepare_items(response, default_item)

        #open('parnassus.html','w').write(response.text)

        #print(items)
        
        #item=items[0]

        #print(item)

        #print("yyy:",response.text)

        count=0

        capital_gain_list=[]
        dividends_list=[]


        #year=response.xpath("//b[contains(text(),'Calendar Year End Data')]//ancestor::tr//following-sibling::tr//td//b[contains(text(),'Year')]//parent::td//following-sibling::td//strong//text()").extract()
        for block in response.xpath("(//table[@class='ui table table--complex'])[1]/tbody/tr"):
            count = count+1
        #print("capital_gains:",capital_gains)

            heading = block.xpath("td[1]/span/span/text()").get()

            
            if "Long-Term" in heading:
                print("here")
                cg_record_date =block.xpath("td[2]/span/span/text()").get()
                cg_ex_date =block.xpath("td[3]/span/span/text()").get()
                cg_pay_date =block.xpath("td[3]/span/span/text()").get()
                long_term_per_share =block.xpath("td[4]/span/span/text()").get()
                

                print("xxx:",heading,cg_record_date,cg_pay_date,long_term_per_share)
                data_dict1={"cg_ex_date": cg_ex_date, "cg_record_date": cg_record_date, "cg_pay_date": cg_pay_date, "short_term_per_share": "","long_term_per_share": long_term_per_share, "total_per_share": "", "cg_reinvestment_price": ""}

                capital_gain_list.append(data_dict1)
            else:
                print("1111")
                record_date =block.xpath("td[2]/span/span/text()").get()
                ex_date =block.xpath("td[3]/span/span/text()").get()
                pay_date =block.xpath("td[3]/span/span/text()").get()
                per_share =block.xpath("td[4]/span/span/text()").get()
                data_dict2={"ex_date": ex_date, "pay_date": pay_date, "ordinary_income": "", "qualified_income": "", "record_date": record_date,"per_share": per_share, "reinvestment_price": ""}

                dividends_list.append(data_dict2)

                #print("xxx:",heading,cg_record_date,cg_pay_date,long_term_per_share)



        
        
        items[0]['capital_gains']=capital_gain_list
        items[0]['dividends']=dividends_list


        #fundDistribution = [{"id":"274","fund":"PRILX","dividendType":"Income Dividend","recordDate":"2021-06-29T00:00:00.000Z","payableDate":"2021-06-30T00:00:00.000Z","reinvestDate":"2021-06-30T00:00:00.000Z","reinvestPrice":61.728930,"pricePerShare":0.0903000000},{"id":"270","fund":"PRILX","dividendType":"Income Dividend","recordDate":"2021-03-30T00:00:00.000Z","payableDate":"2021-03-31T00:00:00.000Z","reinvestDate":"2021-03-31T00:00:00.000Z","reinvestPrice":57.538530,"pricePerShare":0.0703000000},{"id":"264","fund":"PRILX","dividendType":"Income Dividend","recordDate":"2020-12-16T00:00:00.000Z","payableDate":"2020-12-17T00:00:00.000Z","reinvestDate":"2020-12-17T00:00:00.000Z","reinvestPrice":53.321520,"pricePerShare":0.1112000000},{"id":"260","fund":"PRILX","dividendType":"Long-Term Capital Gain","recordDate":"2020-11-18T00:00:00.000Z","payableDate":"2020-11-19T00:00:00.000Z","reinvestDate":"2020-11-19T00:00:00.000Z","reinvestPrice":51.552300,"pricePerShare":2.8417000000},{"id":"256","fund":"PRILX","dividendType":"Income Dividend","recordDate":"2020-09-29T00:00:00.000Z","payableDate":"2020-09-30T00:00:00.000Z","reinvestDate":"2020-09-30T00:00:00.000Z","reinvestPrice":51.142900,"pricePerShare":0.0767000000}]

        for i in items:
            print(i)
            yield self.generate_item(i, FinancialDetailItem)