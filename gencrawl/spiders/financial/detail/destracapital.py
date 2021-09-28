from gencrawl.spiders.financial.financial_detail_spider import FinancialDetailSpider
from gencrawl.spiders.financial.financial_detail_field_mapping import FinancialDetailFieldMapSpider
import scrapy
import re
from gencrawl.util.statics import Statics
import re
from gencrawl.items.financial.financial_detail_item import FinancialDetailItem
import requests
from scrapy.selector import Selector

class DestracapitalfundsComDetail(FinancialDetailFieldMapSpider):
    name = 'financial_detail_destracapital_com'

    def get_items_or_req(self, response, default_item=None):
        items = super().get_items_or_req(response, default_item)
        file=open("destra.html","w")
        file.write(response.text)
        file.close()

        distribution_data=response.xpath("//h2[contains(text(),'Current Distribution')]//following::table[@class='fund-performance-table']//tr[position()>1]")
        for item in items:
            print("inside firts for")
            dividends_list = []
            for row in distribution_data:
                #capital_gain_list = []
                print("inside seicond loop")

                #print(row.xpath(".//td[1]//text()").extract_first())
                #print((row.xpath(".//td[1]//text()").extract_first()).replace("\n","").strip()==item['nasdaq_ticker'].strip())
                print(item['nasdaq_ticker'])
                temp_ticker=row.xpath(".//td[1]//text()").extract_first()
                print("ticker----",temp_ticker)
                if(temp_ticker==None):
                    continue
                if(temp_ticker.replace("\n","").strip()==item['nasdaq_ticker'].strip()):
                    print("isnide if")
                    #data_dict1 = {"cg_ex_date": "", "cg_record_date": "", "cg_pay_date": "", "short_term_per_share": "","long_term_per_share": "", "total_per_share": "", "cg_reinvestment_price": ""}
                    data_dict2 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "","record_date": "", "per_share": "", "reinvestment_price": ""}
                    data_dict2['per_share']=row.xpath(".//td[2]//text()").extract_first()
                    data_dict2['record_date']=row.xpath(".//td[3]//text()").extract_first()
                    data_dict2['ex_date']=row.xpath(".//td[4]//text()").extract_first()
                    data_dict2['pay_date']=row.xpath(".//td[5]//text()").extract_first()
                    print(data_dict2)
                    dividends_list.append(data_dict2)
            item['dividends']=dividends_list
        try:
            #(response.xpath("//p[contains(text(),'historical distributions')]/a//text()").extract()[0]=="Click Here"):
            api_url="https://www.destracapital.com/"+response.xpath("//p[contains(text(),'historical distributions')]/a//@href").extract_first()
            rsp_share_waise = requests.get(api_url)
            resp =rsp_share_waise.text
            file=open("response.html","w")
            file.write(resp)
            file.close()
            selector = Selector(text=resp)
            print("here")
            table_row=selector.xpath("//table//tbody//tr")
            headers=selector.xpath("//table//thead//tr//th//text()").extract()
            headers = [i.replace("Distribution Amount", "").strip() for i in headers]
            print(headers)


            for item in items:
                capital_gain_list=[]
                dividends_list=[]
                #print("inside for")
                #print(item['share_class'])
                #print(item['share_class'].replace("Shares","Share") in headers)
                if(item['share_class'].replace("Shares","Share") in headers):
                    index_num=headers.index(item['share_class'].replace("Shares","Share"))+1
                    print("index num",index_num)
                    for row in table_row:
                        data_dict2 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "",
                                      "record_date": "", "per_share": "", "reinvestment_price": ""}
                        data_dict2['per_share'] = row.xpath(".//td["+str(index_num)+"]//text()").extract_first()
                        print(data_dict2['per_share'])

                        data_dict2['record_date'] = row.xpath(".//td[1]//text()").extract_first()
                        data_dict2['ex_date'] = row.xpath(".//td[2]//text()").extract_first()
                        data_dict2['pay_date'] = row.xpath(".//td[3]//text()").extract_first()
                        #print(data_dict2)
                        item['dividends'].append(data_dict2)
                yield self.generate_item(item, FinancialDetailItem)
        except:
            for item in items:
                yield self.generate_item(item, FinancialDetailItem)





'''

        url=response.xpath("//a[contains(text(),'PERFORMANCE')]//@href").extract()[0]
        meta = response.meta
        meta['items'] = items
        print(url)
        yield self.make_request(url, callback=self.performance, meta=meta, dont_filter=True, method=Statics.CRAWL_METHOD_GET)

    def performance(self,response):
        print("cdcw")
        file=open("performance thiodnd.html","w")
        file.write(response.text)
        file.close()
        items = response.meta['items']
        for item in items:
            print("inside for")
            for row in response.xpath("//h3[contains(text(),'Fund Operating Expenses')]"):
                #print(row.xpath(".//span//text()").extract_first().replace("Class","").replace("Shares","").replace("-","").strip())
                #print(item['share_class'] in row.xpath(".//span//text()").extract_first().replace("Class","").replace("Shares","").replace("-","").strip())
                if(item['share_class'] in row.xpath(".//span//text()").extract_first().replace("Class","").replace("Shares","").replace("-","").strip() ):
                    item['total_expense_gross']=row.xpath("(.//following::table//strong[contains(text(),'Gross Annual Operating Expenses')]/parent::td)[1]/following-sibling::td//text()").extract()[0]
                    item['total_expense_net']=row.xpath("(.//following::table//strong[contains(text(),'Net Annual Operating Expenses')]/parent::td)[1]/following-sibling::td//text()").extract_first()
            for row in response.xpath("//h3[contains(text(),'Yields')]"):
                print(item['share_class'] in row.xpath(".//span//time//following::text()[1]").extract_first().replace("Class", "").replace("Shares", "").replace("-", "").strip())
                print(row.xpath(".//span//time//following::text()[1]").extract_first().replace("Class", "").replace("Shares", "").replace("-", "").strip())
                print(item['share_class'])
                if (item['share_class'] in row.xpath(".//span//time//following::text()[1]").extract_first().replace("Class", "").replace("Shares", "").replace("-", "").strip()):
                    item['sec_yield_30_day']=row.xpath("(.//following::table//strong[contains(text(),'30-day SEC')]//parent::td)[1]//following-sibling::td//text()").extract_first()
                    print("cdcd",item['sec_yield_30_day'])
                    item['sec_yield_date_30_day']=row.xpath(".//span//time//text()").extract()[0]
            #diviends
            print("herrererr")
            capital_gain_list=[]
            dividends_list=[]
            count=0
            for row in response.xpath("//section[@class='block tables tables__performance-dividends-and-capital-gains']"):
                #print(row.xpath(".//following-sibling::table//tbody//tr[1]//td[2]//text()").extract())
                #print(item['share_class'] in row.xpath(".//span//text()").extract_first().replace("Class", "").replace("Shares", "").replace("-", "").strip())
                #print(row.xpath(".//span//text()").extract_first().replace("Class", "").replace("Shares", "").replace("-", "").strip())
                #print(item['share_class'])
                if (item['share_class'] in row.xpath(".//span//text()").extract_first().replace("Class", "").replace("Shares", "").replace("-", "").strip()):
                    data_dict1 = {"cg_ex_date": "", "cg_record_date": "", "cg_pay_date": "", "short_term_per_share": "","long_term_per_share": "", "total_per_share": "", "cg_reinvestment_price": ""}
                    data_dict2 = {"ex_date": "", "pay_date": "", "ordinary_income": "", "qualified_income": "","record_date": "", "per_share": "", "reinvestment_price": ""}
                    data_dict1['cg_record_date']=row.xpath("(.//following::table//tr//td//strong[contains(text(),'Capital Gains')])[1]//text()").extract_first().split("paid")[-1].strip()
                    print(data_dict1['cg_record_date'])
                    if("capital" in data_dict1['cg_record_date'] or "Capital" in data_dict1['cg_record_date'] ):
                        data_dict1['cg_record_date']=data_dict1['cg_record_date'].split("(")[-1].replace(")","")
                    data_dict1['short_term_per_share']=row.xpath("(.//following::table[1]//tr//td//strong[contains(text(),'Short')])[1]//following::td[1]//text()").extract_first()
                    data_dict1['long_term_per_share']=row.xpath("(.//following::table[1]//tr//td//strong[contains(text(),'Long')])[1]//following::td[1]//text()").extract_first()
                    data_dict1['total_per_share']=row.xpath("(.//parent::header/following-sibling::div//table)//strong[contains(text(),'Total (per share)')]//parent::td//following-sibling::td//text()").extract_first()
                    print("captststsststststt",data_dict1['total_per_share'])
                    if(data_dict1['total_per_share']==None):
                        print("indsiiddeedede dnoowwnd---------")
                        data_dict1['total_per_share'] = row.xpath("(.//parent::header/following-sibling::div//table)//strong[contains(text(),'Capital Gain')]//parent::td//following-sibling::td//text()").extract_first()

                    data_dict2['record_date']=row.xpath("(.//following::table[1]//tr//td//strong[contains(text(),'Dividend')])[1]//text()").extract_first().split("paid")[-1].replace(")","").replace("(","").strip()
                    if ("Dividend" in data_dict2['record_date']):
                        data_dict2['record_date'] = data_dict2['record_date'].replace("Dividend", "")

                    data_dict2['ordinary_income']=row.xpath("(.//parent::header/following-sibling::div//table)//strong[contains(text(),'Dividend')]//parent::td//following-sibling::td//text()").extract_first()
                    #print(data_dict2['ordinary_income'])
                    capital_gain_list.append(data_dict1)
                    dividends_list.append(data_dict2)
                    count=count+1
                    #print(capital_gain_list)
            item['capital_gains']=capital_gain_list
            item['dividends']=dividends_list
        url=response.xpath("//a[contains(text(), 'PORTFOLIO')] / @ href").extract()[0]
        meta = response.meta
        meta['items'] = items
        #print(url)
        yield self.make_request(url, callback=self.parse_portfolio, meta=meta, dont_filter=True,method=Statics.CRAWL_METHOD_SELENIUM)

    def parse_portfolio(self,response):
        items = response.meta['items']
        for item in items:
            try:
                item['effective_duration']=response.xpath("//td[contains(text(),'Effective Duration')]//following-sibling::td//text()").extract()[0]
            except:
                pass
            try:
                item['effective_duration_date']=response.xpath("//h3[contains(text(),'Key Portfolio Attributes')]//span//time//text()").extract()[0]
            except:
                pass
            try:
                item['portfolio_assets']=response.xpath("//td[contains(text(),'Fund Assets')]//following-sibling::td//text()").extract()[0]
            except:
                pass
            try:
                item['portfolio_assets_date']=response.xpath("//h3[contains(text(),'Key Portfolio Attributes')]//span//time//text()").extract()[0]
            except:
                pass
            try:
                item['average_weighted_maturity']=response.xpath("//td[contains(text(),'Average Effective Maturity')]//following-sibling::td//text()").extract()[0]
            except:
                pass
            try:
                item['average_weighted_maturity_as_of_date']=response.xpath("//h3[contains(text(),'Key Portfolio Attributes')]//span//time//text()").extract()[0]
            except:
                pass
            yield self.generate_item(item, FinancialDetailItem)
'''