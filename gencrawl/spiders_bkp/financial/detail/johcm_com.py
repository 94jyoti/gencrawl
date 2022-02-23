from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider


class JohcmfundsComDetail(FinancialDetailFieldMapSpider):
    name = 'johcm_com'
    def get_items_or_req(self, response, default_item=None):

        meta = response.meta

        items = super().get_items_or_req(response, default_item)

        tickers = response.xpath("//td[contains(.,'Gross Expense Ratio*')]//td[contains(.,'X')]/text()").getall()

        print("tickers:",tickers)

        for index,item in enumerate(items):

            items[index]['nasdaq_ticker'] = tickers[index]
            print("items[index]['nasdaq_ticker']:",items[index]['nasdaq_ticker'])

        print("items:",items)
        for index,item in enumerate(items):
            temp_row=response.xpath("((//table[@class='fundcodes-table'])[1]//tbody//tr)[position()>1]")
            for row in temp_row:
                if(row.xpath(".//td[1]//text()").extract_first()==item['nasdaq_ticker']):
                    item['cusip']=row.xpath(".//td[4]//text()").extract_first(None)
            print("uuuu:",item['nasdaq_ticker'])
            
            
        
            meta['item']=item

            url = "https://www.johcm.com/us/how-to-invest/231/distributions"

            yield scrapy.Request(url,method='GET',callback=self.distributions,meta=meta,dont_filter=True)

    def distributions(self,response):

        print("distributions....")

        meta = response.meta
        item = meta['item']

        selector = scrapy.Selector(text=response.text, type="html")

        record_date = response.xpath("//*[contains(text(),'Record Date')]/parent::td/following-sibling::td/text()").get()
        print("record_date:",record_date)

        ex_date_reinvestment_date = response.xpath("//*[contains(text(),'Ex-Dividend and Reinvestment Date')]/parent::td/following-sibling::td/text()").get()
        print("ex_date_reinvestment_date:",ex_date_reinvestment_date)

        payable_date = response.xpath("//*[contains(text(),'Payable Date')]/parent::td/following-sibling::td/text()").get()
        print("payable_date:",payable_date)

        meta['record_date'] = record_date
        meta['ex_date_reinvestment_date'] =ex_date_reinvestment_date
        meta['payable_date'] = payable_date

        for first_block in selector.xpath("(//div[@class='fund-performance']/table)[1]"):
            #print("first_block:",first_block)
            for row_tr in first_block.xpath("tbody/tr"):
                
                td_title = row_tr.xpath("td[1]/strong/text()").get()
                td_value = row_tr.xpath("td[2]/text()").get()
                #print("row_tr:",td_title,td_value)

        temp_main_block =[]
        #temp_tr_block =[]

        
        
        for second_block in selector.xpath("(//div[@class='fund-performance']/table)[2]/tbody/tr"):
            #print("second_block:",second_block)
            temp_tr_block = []

            for row_td in second_block.xpath("td"):
               
                temp_td_block=[]
                td_ticker_value1 = row_td.xpath("p/text()[following-sibling::br] | text()[following-sibling::br] | text()").get()
               
                if td_ticker_value1 is None:
                    td_ticker_value1=''
                #print("td_ticker_value1:",td_ticker_value1)

                #temp_td_block.append(td_ticker_value1)


                td_ticker_value2 = row_td.xpath("p/text()[preceding-sibling::br] | text()[preceding-sibling::br] | p/text()").getall()
                temp_td_block.append(td_ticker_value1.replace('\xa0','').strip())
                for t in td_ticker_value2:
                    #print("tt:",t)
                    if t is None:
                        t=''
                    #if len(t)>1:
                    t = t.replace('\xa0','').strip()
                    temp_td_block.append(t)
                #print("temp_td_block:",temp_td_block)
            
                temp_tr_block.append(temp_td_block)

            #print("temp_tr_block:",temp_tr_block)


            #print("td_ticker_value:",temp_tickerwise_block)

            temp_main_block.append(temp_tr_block)
        #print("temp_main_block:",temp_main_block,len(temp_main_block))


        for t in temp_main_block:
            print(t)
            del t[3][0]
            del t[4][0]
            del t[5][0]

        #print("temp_main_block:",temp_main_block,len(temp_main_block))

        



        capital_gain_list=[]
        dividends_list=[]
        
        


        print("item['nasdaq_ticker']:",item['nasdaq_ticker'])
        for dist_share_class in temp_main_block:
            print("dist_share_class:",dist_share_class)
            for c,s in enumerate(dist_share_class[2]):
                print("ss:",s,item['nasdaq_ticker'])
                if s==item['nasdaq_ticker']:
                    print("dddd:",s,c)

                    long_term_per_share = dist_share_class[4][c]
                    short_term_per_share = dist_share_class[5][c]
                    cg_ex_date=meta['ex_date_reinvestment_date']
                    cg_record_date= meta['record_date']
                    cg_pay_date=meta['payable_date']
                    if len(dist_share_class[3])>0:
                        ordinary_income = dist_share_class[3][c]
                    else:
                        ordinary_income=""
                    data_dict1={"cg_ex_date": cg_ex_date, "cg_record_date": cg_record_date, "cg_pay_date": cg_pay_date, "short_term_per_share": short_term_per_share,"long_term_per_share": long_term_per_share, "total_per_share": "", "cg_reinvestment_price": ""}
                    data_dict2={"ex_date": "", "pay_date": "", "ordinary_income": ordinary_income, "qualified_income": "", "record_date": "","per_share": "", "reinvestment_price": ""}
                    #data_dict2['ex_date']=year[i]
                    #data_dict1['total_per_share']=capital_gains[i]
                    #data_dict2['ordinary_income']=dividends[i]
                    capital_gain_list.append(data_dict1)
                    dividends_list.append(data_dict2)
        item['capital_gains'] = capital_gain_list
        item['dividends'] = dividends_list
                    
        yield self.generate_item(item, FinancialDetailItem)
